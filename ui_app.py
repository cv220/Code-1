"""PyQt-based UI for entering and solving linear systems."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from PyQt5 import QtCore, QtGui, QtWidgets

from linear_solver import solve_linear_system


@dataclass
class AugmentedMatrix:
    coefficients: List[List[float]]
    rhs: List[float]


class LinearSystemWindow(QtWidgets.QMainWindow):
    """Main window that mimics pencil-and-paper matrix entry."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Linear System Workspace")
        self.resize(960, 640)

        self._solution_labels: List[QtWidgets.QLabel] = []

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        self._layout = QtWidgets.QVBoxLayout(central)
        self._layout.setContentsMargins(24, 24, 24, 24)
        self._layout.setSpacing(18)

        self._build_setup_panel()
        self._build_matrix_table()
        self._build_actions_panel()
        self._build_solution_panel()

        self._generate_grid()

    # ------------------------------------------------------------------
    # UI construction helpers
    def _build_setup_panel(self) -> None:
        setup_box = QtWidgets.QGroupBox("Setup")
        self._layout.addWidget(setup_box)

        layout = QtWidgets.QHBoxLayout(setup_box)
        layout.setSpacing(12)

        layout.addWidget(QtWidgets.QLabel("System size (n):"))

        self._size_spin = QtWidgets.QSpinBox()
        self._size_spin.setRange(1, 12)
        self._size_spin.setValue(3)
        self._size_spin.setAccelerated(True)
        self._size_spin.setFixedWidth(90)
        self._size_spin.editingFinished.connect(self._generate_grid)
        layout.addWidget(self._size_spin)

        self._generate_button = QtWidgets.QPushButton("Generate Grid")
        self._generate_button.clicked.connect(self._generate_grid)
        layout.addWidget(self._generate_button)

        layout.addStretch(1)

    def _build_matrix_table(self) -> None:
        self._matrix_table = QtWidgets.QTableWidget()
        self._matrix_table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self._matrix_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self._matrix_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self._matrix_table.setAlternatingRowColors(True)
        self._matrix_table.setStyleSheet(
            "QTableWidget {"
            "  background-color: #ffffff;"
            "  gridline-color: #d0d0d0;"
            "  font-size: 14px;"
            "}"
            "QHeaderView::section {"
            "  background-color: #f3f4f9;"
            "  font-weight: 600;"
            "  border: none;"
            "  padding: 6px;"
            "}"
        )
        self._layout.addWidget(self._matrix_table, stretch=1)

    def _build_actions_panel(self) -> None:
        actions_box = QtWidgets.QGroupBox("Actions")
        self._layout.addWidget(actions_box)

        layout = QtWidgets.QHBoxLayout(actions_box)
        layout.setSpacing(12)

        self._solve_button = QtWidgets.QPushButton("Solve")
        self._solve_button.clicked.connect(self._on_solve)
        layout.addWidget(self._solve_button)

        self._clear_button = QtWidgets.QPushButton("Clear")
        self._clear_button.clicked.connect(self._clear_matrix)
        layout.addWidget(self._clear_button)

        self._load_coeff_button = QtWidgets.QPushButton("Load Coefficients…")
        self._load_coeff_button.clicked.connect(self._on_load_coefficients)
        layout.addWidget(self._load_coeff_button)

        self._load_rhs_button = QtWidgets.QPushButton("Load RHS…")
        self._load_rhs_button.clicked.connect(self._on_load_rhs)
        layout.addWidget(self._load_rhs_button)

        self._save_button = QtWidgets.QPushButton("Save Solution…")
        self._save_button.clicked.connect(self._on_save_solution)
        layout.addWidget(self._save_button)

        layout.addStretch(1)

    def _build_solution_panel(self) -> None:
        self._solution_box = QtWidgets.QGroupBox("Solution")
        self._layout.addWidget(self._solution_box)

        self._solution_layout = QtWidgets.QGridLayout(self._solution_box)
        self._solution_layout.setContentsMargins(12, 12, 12, 12)
        self._solution_layout.setHorizontalSpacing(18)
        self._solution_layout.setVerticalSpacing(6)

    # ------------------------------------------------------------------
    # Grid management
    def _generate_grid(self) -> None:
        size = self._size_spin.value()
        self._matrix_table.clear()
        self._matrix_table.setRowCount(size)
        self._matrix_table.setColumnCount(size + 1)

        horiz_headers = [f"c{i + 1}" for i in range(size)] + ["rhs"]
        self._matrix_table.setHorizontalHeaderLabels(horiz_headers)
        vert_headers = [f"r{i + 1}" for i in range(size)]
        self._matrix_table.setVerticalHeaderLabels(vert_headers)

        for row in range(size):
            for col in range(size + 1):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self._matrix_table.setItem(row, col, item)

        self._matrix_table.viewport().update()
        self._matrix_table.setCurrentCell(0, 0)
        self._clear_solution()

    def _clear_matrix(self) -> None:
        for row in range(self._matrix_table.rowCount()):
            for col in range(self._matrix_table.columnCount()):
                item = self._matrix_table.item(row, col)
                if item is not None:
                    item.setText("")
                    item.setBackground(QtGui.QColor("white"))
        self._clear_solution()

    # ------------------------------------------------------------------
    # File helpers
    def _on_load_coefficients(self) -> None:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select coefficient matrix",
            "",
            "Text Files (*.txt);;All Files (*)",
        )
        if not path:
            return

        try:
            matrix = self._read_matrix(Path(path))
        except ValueError as exc:
            QtWidgets.QMessageBox.critical(self, "Load Error", str(exc))
            return

        size = len(matrix)
        self._size_spin.setValue(size)
        self._generate_grid()

        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                self._matrix_table.item(i, j).setText(str(value))

    def _on_load_rhs(self) -> None:
        if self._matrix_table.rowCount() == 0:
            QtWidgets.QMessageBox.information(self, "Load RHS", "Generate the grid first.")
            return

        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select RHS vector",
            "",
            "Text Files (*.txt);;All Files (*)",
        )
        if not path:
            return

        try:
            rhs = self._read_vector(Path(path), self._matrix_table.rowCount())
        except ValueError as exc:
            QtWidgets.QMessageBox.critical(self, "Load Error", str(exc))
            return

        for i, value in enumerate(rhs):
            self._matrix_table.item(i, self._matrix_table.columnCount() - 1).setText(str(value))

    def _on_save_solution(self) -> None:
        if not self._solution_labels:
            QtWidgets.QMessageBox.information(self, "Save Solution", "Solve the system first.")
            return

        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save solution",
            "solution.txt",
            "Text Files (*.txt);;All Files (*)",
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as handle:
                for label in self._solution_labels:
                    handle.write(f"{label.property('value')}\n")
        except OSError as exc:
            QtWidgets.QMessageBox.critical(self, "Save Error", f"Could not save solution: {exc}")

    # ------------------------------------------------------------------
    # Solve logic
    def _on_solve(self) -> None:
        matrix = self._collect_matrix()
        if matrix is None:
            return

        try:
            solution = solve_linear_system(matrix.coefficients, matrix.rhs)
        except Exception as exc:  # pylint: disable=broad-except
            QtWidgets.QMessageBox.critical(self, "Solve Error", str(exc))
            return

        self._render_solution(solution)

    def _collect_matrix(self) -> AugmentedMatrix | None:
        coeffs: List[List[float]] = []
        rhs: List[float] = []
        size = self._matrix_table.rowCount()
        errors = []

        for row in range(size):
            coeff_row: List[float] = []
            for col in range(self._matrix_table.columnCount()):
                item = self._matrix_table.item(row, col)
                if item is None:
                    continue
                text = item.text().strip()
                if not text:
                    errors.append((row, col))
                    continue
                try:
                    value = float(text)
                except ValueError:
                    errors.append((row, col))
                    continue

                if col == self._matrix_table.columnCount() - 1:
                    rhs.append(value)
                else:
                    coeff_row.append(value)

            if len(coeff_row) != size:
                errors.append((row, -1))
            coeffs.append(coeff_row)

        if len(rhs) != size or errors:
            self._highlight_errors(errors)
            QtWidgets.QMessageBox.warning(
                self,
                "Invalid Input",
                "Ensure every entry contains a numeric value and the RHS column is filled.",
            )
            return None

        self._clear_error_highlights()
        return AugmentedMatrix(coefficients=coeffs, rhs=rhs)

    def _highlight_errors(self, locations: List[tuple[int, int]]) -> None:
        self._clear_error_highlights()
        for row, col in locations:
            if col == -1:
                continue
            item = self._matrix_table.item(row, col)
            if item is not None:
                item.setBackground(QtGui.QColor("#ffcccc"))

    def _clear_error_highlights(self) -> None:
        for row in range(self._matrix_table.rowCount()):
            for col in range(self._matrix_table.columnCount()):
                item = self._matrix_table.item(row, col)
                if item is not None:
                    item.setBackground(QtGui.QColor("white"))

    def _render_solution(self, solution: List[float]) -> None:
        self._clear_solution()
        for index, value in enumerate(solution):
            label = QtWidgets.QLabel(f"x{index + 1}")
            value_label = QtWidgets.QLabel(f"{value:.6g}")
            value_label.setProperty("value", value)
            label.setStyleSheet("font-weight: 600;")
            self._solution_layout.addWidget(label, index, 0)
            self._solution_layout.addWidget(value_label, index, 1)
            self._solution_labels.append(value_label)

    def _clear_solution(self) -> None:
        while self._solution_layout.count():
            item = self._solution_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self._solution_labels.clear()

    # ------------------------------------------------------------------
    # File readers
    @staticmethod
    def _read_matrix(path: Path) -> List[List[float]]:
        rows: List[List[float]] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    row = [float(part) for part in stripped.split()]
                except ValueError as exc:
                    raise ValueError("Matrix file contains non-numeric values.") from exc
                rows.append(row)

        if not rows:
            raise ValueError("Matrix file is empty.")

        size = len(rows)
        if any(len(row) != size for row in rows):
            raise ValueError("Matrix must be square (same number of rows and columns).")

        return rows

    @staticmethod
    def _read_vector(path: Path, expected: int) -> List[float]:
        values: List[float] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    values.append(float(stripped))
                except ValueError as exc:
                    raise ValueError("RHS file contains non-numeric values.") from exc

        if len(values) != expected:
            raise ValueError("RHS vector length must match the matrix size.")

        return values


def apply_modern_palette(app: QtWidgets.QApplication) -> None:
    """Apply a gently contrasted Fusion palette for a modern appearance."""

    app.setStyle("Fusion")
    palette = QtGui.QPalette()

    base = QtGui.QColor(248, 249, 252)
    highlight = QtGui.QColor(87, 109, 219)
    text = QtGui.QColor(33, 37, 41)

    palette.setColor(QtGui.QPalette.Window, base)
    palette.setColor(QtGui.QPalette.WindowText, text)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(241, 243, 248))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(255, 255, 220))
    palette.setColor(QtGui.QPalette.ToolTipText, text)
    palette.setColor(QtGui.QPalette.Text, text)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(236, 239, 245))
    palette.setColor(QtGui.QPalette.ButtonText, text)
    palette.setColor(QtGui.QPalette.Highlight, highlight)
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(255, 255, 255))

    app.setPalette(palette)

    font = QtGui.QFont("Segoe UI", 10)
    app.setFont(font)


def main() -> None:
    app = QtWidgets.QApplication([])
    apply_modern_palette(app)
    window = LinearSystemWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
