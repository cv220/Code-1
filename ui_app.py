"""PyQt5 UI for entering and solving linear systems."""
from __future__ import annotations

from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from linear_solver import solve_linear_system


class LinearSystemWindow(QMainWindow):
    """Main window providing a modern PyQt-based matrix input experience."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Linear System Solver")
        self.resize(900, 640)

        self._size_spin: QSpinBox | None = None
        self._grid_layout: QGridLayout | None = None
        self._solution_layout: QVBoxLayout | None = None

        self._coeff_fields: List[List[QLineEdit]] = []
        self._rhs_fields: List[QLineEdit] = []
        self._solution_labels: List[QLabel] = []
        self._latest_solution: List[float] = []

        self._apply_palette()
        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction helpers
    def _apply_palette(self) -> None:
        """Switch to the Fusion style and soften the palette for a modern feel."""

        QApplication.setStyle("Fusion")
        palette = QPalette()
        background = QColor(245, 247, 250)
        accent = QColor(66, 133, 244)
        text_color = QColor(45, 52, 63)

        palette.setColor(QPalette.Window, background)
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(236, 240, 243))
        palette.setColor(QPalette.Button, QColor(252, 253, 255))
        palette.setColor(QPalette.ButtonText, text_color)
        palette.setColor(QPalette.WindowText, text_color)
        palette.setColor(QPalette.Text, text_color)
        palette.setColor(QPalette.Highlight, accent)
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

        QApplication.setPalette(palette)

        base_font = QFont("Segoe UI", 10)
        QApplication.setFont(base_font)

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 20, 24, 24)
        main_layout.setSpacing(18)

        main_layout.addWidget(self._build_setup_panel())
        main_layout.addWidget(self._build_action_panel())
        main_layout.addWidget(self._build_grid_panel())
        main_layout.addWidget(self._build_solution_panel())

        self._regenerate_grid()

    def _build_setup_panel(self) -> QGroupBox:
        setup_box = QGroupBox("Setup")
        setup_layout = QHBoxLayout(setup_box)
        setup_layout.setContentsMargins(16, 12, 16, 12)
        setup_layout.setSpacing(12)

        size_label = QLabel("System size (n):")
        size_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        size_spin = QSpinBox()
        size_spin.setRange(1, 12)
        size_spin.setValue(3)
        size_spin.setAccelerated(True)
        size_spin.editingFinished.connect(self._regenerate_grid)
        size_spin.setFixedWidth(80)
        self._size_spin = size_spin

        generate_button = QPushButton("Generate Grid")
        generate_button.clicked.connect(self._regenerate_grid)
        generate_button.setDefault(True)

        setup_layout.addWidget(size_label)
        setup_layout.addWidget(size_spin)
        setup_layout.addWidget(generate_button)
        setup_layout.addStretch()

        return setup_box

    def _build_action_panel(self) -> QGroupBox:
        actions_box = QGroupBox("Actions")
        actions_layout = QHBoxLayout(actions_box)
        actions_layout.setContentsMargins(16, 12, 16, 12)
        actions_layout.setSpacing(10)

        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self._on_solve)
        solve_button.setShortcut("Ctrl+Return")

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self._on_clear)
        clear_button.setShortcut("Ctrl+Backspace")

        load_coeff_button = QPushButton("Load Coefficients")
        load_coeff_button.clicked.connect(self._on_load_coefficients)

        load_rhs_button = QPushButton("Load RHS")
        load_rhs_button.clicked.connect(self._on_load_rhs)

        save_solution_button = QPushButton("Save Solution")
        save_solution_button.clicked.connect(self._on_save_solution)

        for button in (
            solve_button,
            clear_button,
            load_coeff_button,
            load_rhs_button,
            save_solution_button,
        ):
            button.setMinimumWidth(140)

        actions_layout.addWidget(solve_button)
        actions_layout.addWidget(clear_button)
        actions_layout.addWidget(load_coeff_button)
        actions_layout.addWidget(load_rhs_button)
        actions_layout.addWidget(save_solution_button)
        actions_layout.addStretch()

        return actions_box

    def _build_grid_panel(self) -> QGroupBox:
        container_box = QGroupBox("Augmented Matrix")
        container_layout = QVBoxLayout(container_box)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(12)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setHorizontalSpacing(12)
        grid_layout.setVerticalSpacing(10)

        scroll_area.setWidget(grid_widget)

        container_layout.addWidget(scroll_area)

        self._grid_layout = grid_layout

        return container_box

    def _build_solution_panel(self) -> QGroupBox:
        solution_box = QGroupBox("Solution")
        layout = QVBoxLayout(solution_box)
        layout.setContentsMargins(16, 12, 16, 16)
        layout.setSpacing(8)

        caption = QLabel("Solve the system to see variable assignments.")
        caption.setObjectName("solutionCaption")
        layout.addWidget(caption)

        self._solution_layout = layout

        return solution_box

    # ------------------------------------------------------------------
    # Grid management
    def _clear_grid(self) -> None:
        if not self._grid_layout:
            return

        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self._coeff_fields.clear()
        self._rhs_fields.clear()

    def _regenerate_grid(self) -> None:
        if self._grid_layout is None or self._size_spin is None:
            return

        size = self._size_spin.value()
        self._clear_grid()

        header_font = QFont(QApplication.font())
        header_font.setPointSize(header_font.pointSize() + 1)
        header_font.setBold(True)

        # Column headers
        header = QLabel()
        header.setMinimumWidth(24)
        self._grid_layout.addWidget(header, 0, 0, alignment=Qt.AlignCenter)
        for col in range(size):
            label = QLabel(f"c{col + 1}")
            label.setFont(header_font)
            label.setAlignment(Qt.AlignCenter)
            self._grid_layout.addWidget(label, 0, col + 1)

        rhs_header = QLabel("b")
        rhs_header.setFont(header_font)
        rhs_header.setAlignment(Qt.AlignCenter)
        self._grid_layout.addWidget(rhs_header, 0, size + 2)

        # Divider line spans all rows
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setStyleSheet("color: #d0d5dd;")
        self._grid_layout.addWidget(divider, 0, size + 1, size + 1, 1)

        for row in range(size):
            row_label = QLabel(f"r{row + 1}")
            row_label.setFont(header_font)
            row_label.setAlignment(Qt.AlignCenter)
            self._grid_layout.addWidget(row_label, row + 1, 0)

            row_fields: List[QLineEdit] = []
            for col in range(size):
                field = self._create_matrix_field()
                self._grid_layout.addWidget(field, row + 1, col + 1)
                row_fields.append(field)
            self._coeff_fields.append(row_fields)

            rhs_field = self._create_matrix_field()
            self._grid_layout.addWidget(rhs_field, row + 1, size + 2)
            self._rhs_fields.append(rhs_field)

        if self._coeff_fields:
            self._coeff_fields[0][0].setFocus()

        self._clear_solution_labels()

    def _create_matrix_field(self) -> QLineEdit:
        field = QLineEdit()
        field.setAlignment(Qt.AlignCenter)
        field.setMaximumWidth(96)
        field.setPlaceholderText("0")
        field.setClearButtonEnabled(True)
        return field

    # ------------------------------------------------------------------
    # Solution handling
    def _clear_solution_labels(self) -> None:
        if not self._solution_layout:
            return

        for label in self._solution_labels:
            self._solution_layout.removeWidget(label)
            label.deleteLater()
        self._solution_labels.clear()

        if self._solution_layout.count():
            # Keep the caption (index 0) only
            while self._solution_layout.count() > 1:
                item = self._solution_layout.takeAt(1)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def _display_solution(self, solution: List[float]) -> None:
        if self._solution_layout is None:
            return

        self._clear_solution_labels()

        caption = self._solution_layout.itemAt(0).widget()
        if isinstance(caption, QLabel):
            caption.setText("Solution vector:")

        solution_font = QFont(QApplication.font())
        solution_font.setPointSize(solution_font.pointSize() + 1)

        for index, value in enumerate(solution, start=1):
            label = QLabel(f"x{index} = {value:.6g}")
            label.setFont(solution_font)
            label.setAlignment(Qt.AlignLeft)
            self._solution_layout.addWidget(label)
            self._solution_labels.append(label)

    # ------------------------------------------------------------------
    # Actions
    def _on_solve(self) -> None:
        try:
            coefficients = self._collect_coefficients()
            rhs = self._collect_rhs()
        except ValueError as exc:
            self._show_error("Invalid Input", str(exc))
            return

        try:
            solution = solve_linear_system(coefficients, rhs)
        except Exception as exc:  # noqa: BLE001 - surface solver issues to the user
            self._show_error("Solve Error", f"Unable to solve the system: {exc}")
            return

        self._latest_solution = solution
        self._display_solution(solution)

    def _on_clear(self) -> None:
        for row in self._coeff_fields:
            for field in row:
                field.clear()
        for field in self._rhs_fields:
            field.clear()
        self._latest_solution = []
        self._clear_solution_labels()
        if self._solution_layout:
            caption = self._solution_layout.itemAt(0).widget()
            if isinstance(caption, QLabel):
                caption.setText("Solve the system to see variable assignments.")

    def _on_load_coefficients(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select coefficient matrix file", "", "Text Files (*.txt);;All Files (*)")
        if not path:
            return

        try:
            matrix = self._read_matrix_file(path)
        except ValueError as exc:
            self._show_error("Load Error", str(exc))
            return

        size = len(matrix)
        if self._size_spin:
            self._size_spin.setValue(size)
        self._regenerate_grid()

        for row_index, row in enumerate(matrix):
            for col_index, value in enumerate(row):
                self._coeff_fields[row_index][col_index].setText(str(value))

    def _on_load_rhs(self) -> None:
        if not self._coeff_fields:
            self._show_info("Load RHS", "Generate the coefficient grid before loading the RHS vector.")
            return

        expected_size = len(self._coeff_fields)
        path, _ = QFileDialog.getOpenFileName(self, "Select RHS vector file", "", "Text Files (*.txt);;All Files (*)")
        if not path:
            return

        try:
            vector = self._read_vector_file(path, expected_size)
        except ValueError as exc:
            self._show_error("Load Error", str(exc))
            return

        for index, value in enumerate(vector):
            self._rhs_fields[index].setText(str(value))

    def _on_save_solution(self) -> None:
        if not self._latest_solution:
            self._show_info("Save Solution", "Solve the system before saving the solution.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save solution", "solution.txt", "Text Files (*.txt);;All Files (*)")
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as handle:
                for value in self._latest_solution:
                    handle.write(f"{value}\n")
        except OSError as exc:
            self._show_error("Save Error", f"Could not save solution: {exc}")

    # ------------------------------------------------------------------
    # Data helpers
    def _collect_coefficients(self) -> List[List[float]]:
        if not self._coeff_fields:
            raise ValueError("Generate the coefficient grid first.")

        matrix: List[List[float]] = []
        for row_index, row in enumerate(self._coeff_fields):
            matrix_row: List[float] = []
            for col_index, field in enumerate(row):
                text = field.text().strip()
                if not text:
                    raise ValueError(f"Coefficient at row {row_index + 1}, column {col_index + 1} is empty.")
                matrix_row.append(float(text))
            matrix.append(matrix_row)
        return matrix

    def _collect_rhs(self) -> List[float]:
        if not self._rhs_fields:
            raise ValueError("Generate the coefficient grid first.")

        values: List[float] = []
        for index, field in enumerate(self._rhs_fields):
            text = field.text().strip()
            if not text:
                raise ValueError(f"Right-hand-side value at row {index + 1} is empty.")
            values.append(float(text))
        return values

    def _read_matrix_file(self, path: str) -> List[List[float]]:
        rows: List[List[float]] = []
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if not stripped:
                    continue
                parts = stripped.split()
                try:
                    row = [float(part) for part in parts]
                except ValueError as exc:
                    raise ValueError(f"Non-numeric value found in matrix file: {exc}") from exc
                rows.append(row)

        if not rows:
            raise ValueError("Matrix file is empty.")

        size = len(rows)
        if any(len(row) != size for row in rows):
            raise ValueError("Matrix file must describe a square matrix.")

        return rows

    def _read_vector_file(self, path: str, expected_size: int) -> List[float]:
        values: List[float] = []
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    values.append(float(stripped))
                except ValueError as exc:
                    raise ValueError(f"Non-numeric value found in RHS file: {exc}") from exc

        if len(values) != expected_size:
            raise ValueError("The RHS vector length must match the coefficient matrix size.")

        return values

    # ------------------------------------------------------------------
    # Messaging helpers
    def _show_error(self, title: str, message: str) -> None:
        QMessageBox.critical(self, title, message)

    def _show_info(self, title: str, message: str) -> None:
        QMessageBox.information(self, title, message)


def run_app() -> None:
    """Entry point used by the module and external callers."""

    import sys

    app = QApplication.instance()
    should_cleanup = False
    if app is None:
        should_cleanup = True
        app = QApplication(sys.argv)

    window = LinearSystemWindow()
    window.show()

    if should_cleanup:
        sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
