"""Tkinter UI shell for entering linear systems."""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from linear_solver import solve_linear_system
from numpy.linalg import LinAlgError


class LinearSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Linear System Entry")

        self._size_var = tk.StringVar(value="2")
        self.coeff_entries = []
        self.rhs_entries = []
        self.solution_var = tk.StringVar(value="")
        self._latest_solution = []

        self._configure_style()
        self._build_controls()

    def _configure_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        base_font = ("Segoe UI", 10)
        heading_font = ("Segoe UI Semibold", 10)

        background = style.lookup("TFrame", "background")
        if not background:
            background = "#f4f4f7"
            style.configure(".", background=background)
        self.configure(background=background)

        style.configure("TLabel", font=base_font, padding=(4, 2))
        style.configure("TButton", font=base_font, padding=(6, 4))
        style.configure("TEntry", font=base_font)
        style.configure("TLabelframe", padding=(8, 6))
        style.configure("TLabelframe.Label", font=heading_font)

    def _build_controls(self):
        control_frame = ttk.Frame(self)
        control_frame.grid(column=0, row=0, padx=12, pady=12, sticky="w")

        ttk.Label(control_frame, text="System size (n):").grid(column=0, row=0, sticky="w")
        size_entry = ttk.Entry(control_frame, width=5, textvariable=self._size_var)
        size_entry.grid(column=1, row=0, padx=(4, 12))
        size_entry.bind("<Return>", self._on_generate_grid_event)
        size_entry.bind("<KP_Enter>", self._on_generate_grid_event)

        generate_button = ttk.Button(control_frame, text="Generate Grid", command=self.generate_grid)
        generate_button.grid(column=2, row=0)

        button_frame = ttk.Frame(self)
        button_frame.grid(column=0, row=2, padx=12, pady=(6, 4), sticky="w")

        solve_button = ttk.Button(button_frame, text="Solve", command=self._on_solve)
        solve_button.grid(column=0, row=0, padx=(0, 6))

        clear_button = ttk.Button(button_frame, text="Clear", command=self._on_clear)
        clear_button.grid(column=1, row=0, padx=(0, 6))

        load_coeff_button = ttk.Button(button_frame, text="Load Coefficients", command=self._on_load_coefficients)
        load_coeff_button.grid(column=2, row=0, padx=(0, 6))

        load_rhs_button = ttk.Button(button_frame, text="Load RHS", command=self._on_load_rhs)
        load_rhs_button.grid(column=3, row=0, padx=(0, 6))

        save_solution_button = ttk.Button(button_frame, text="Save Solution", command=self._on_save_solution)
        save_solution_button.grid(column=4, row=0)

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.grid(column=0, row=1, padx=12, pady=12)

        solution_frame = ttk.Frame(self)
        solution_frame.grid(column=0, row=3, padx=12, pady=(4, 12), sticky="we")
        solution_frame.columnconfigure(0, weight=1)
        ttk.Label(solution_frame, text="Solution:").grid(column=0, row=0, sticky="w")
        ttk.Label(solution_frame, textvariable=self.solution_var, justify="left").grid(column=0, row=1, sticky="w")

        self.generate_grid()

    def _clear_grid_widgets(self):
        for child in self.grid_frame.winfo_children():
            child.destroy()
        self.coeff_entries.clear()
        self.rhs_entries.clear()

    def generate_grid(self):
        self._clear_grid_widgets()

        try:
            size = int(self._size_var.get())
        except ValueError:
            size = 0

        if size <= 0:
            ttk.Label(self.grid_frame, text="Enter a positive integer for n.").grid(column=0, row=0)
            return

        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = ttk.Entry(self.grid_frame, width=8, justify="center")
                entry.grid(column=j, row=i, padx=2, pady=2)
                self._bind_entry_navigation(entry, i, j, is_rhs=False)
                row_entries.append(entry)
            self.coeff_entries.append(row_entries)

            separator = ttk.Label(self.grid_frame, text="|")
            separator.grid(column=size, row=i, padx=(8, 4))

            rhs_entry = ttk.Entry(self.grid_frame, width=8, justify="center")
            rhs_entry.grid(column=size + 1, row=i, padx=2, pady=2)
            self._bind_entry_navigation(rhs_entry, i, size, is_rhs=True)
            self.rhs_entries.append(rhs_entry)

        if self.coeff_entries:
            self.coeff_entries[0][0].focus_set()

    def _on_solve(self):
        coefficients = []
        rhs = []

        try:
            for row_entries in self.coeff_entries:
                row = [float(entry.get()) for entry in row_entries]
                coefficients.append(row)
            rhs = [float(entry.get()) for entry in self.rhs_entries]
        except ValueError:
            messagebox.showerror("Invalid Input", "Please ensure every matrix and vector entry contains a numeric value.")
            return

        try:
            solution = solve_linear_system(coefficients, rhs)
        except LinAlgError as err:
            messagebox.showerror("Solve Error", f"Unable to solve the system: {err}")
            return

        formatted = ", ".join(f"x{i + 1} = {value:.6g}" for i, value in enumerate(solution))
        self.solution_var.set(formatted)
        self._latest_solution = solution

    def _on_clear(self):
        for row in self.coeff_entries:
            for entry in row:
                entry.delete(0, tk.END)
        for entry in self.rhs_entries:
            entry.delete(0, tk.END)
        self.solution_var.set("")
        self._latest_solution = []

    def _on_generate_grid_event(self, event):
        self.generate_grid()
        return "break"

    def _bind_entry_navigation(self, entry, row, col, *, is_rhs: bool):
        entry.bind("<Up>", lambda event, r=row, c=col, rhs=is_rhs: self._move_focus(r, c, rhs, "Up"))
        entry.bind("<Down>", lambda event, r=row, c=col, rhs=is_rhs: self._move_focus(r, c, rhs, "Down"))
        entry.bind("<Left>", lambda event, r=row, c=col, rhs=is_rhs: self._move_focus(r, c, rhs, "Left"))
        entry.bind("<Right>", lambda event, r=row, c=col, rhs=is_rhs: self._move_focus(r, c, rhs, "Right"))

    def _move_focus(self, row: int, col: int, is_rhs: bool, direction: str):
        size = len(self.coeff_entries)
        if size == 0:
            return "break"

        new_row = row
        new_col = col
        new_is_rhs = is_rhs

        if direction == "Up":
            if row > 0:
                new_row = row - 1
        elif direction == "Down":
            if row < size - 1:
                new_row = row + 1
        elif direction == "Left":
            if is_rhs:
                new_is_rhs = False
                new_col = size - 1
            elif col > 0:
                new_col = col - 1
            elif row > 0:
                new_row = row - 1
                new_is_rhs = True
                new_col = size
            else:
                return "break"
        elif direction == "Right":
            if not is_rhs:
                if col < size - 1:
                    new_col = col + 1
                else:
                    new_is_rhs = True
                    new_col = size
            else:
                if row < size - 1:
                    new_row = row + 1
                    new_is_rhs = False
                    new_col = 0
                else:
                    return "break"

        self._focus_cell(new_row, new_col, new_is_rhs)
        return "break"

    def _focus_cell(self, row: int, col: int, is_rhs: bool):
        if is_rhs:
            target = self.rhs_entries[row]
        else:
            target = self.coeff_entries[row][col]
        target.focus_set()
        target.icursor(tk.END)

    def _on_load_coefficients(self):
        path = filedialog.askopenfilename(title="Select coefficient matrix file", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not path:
            return

        try:
            matrix = self._read_matrix_file(path)
        except ValueError as err:
            messagebox.showerror("Load Error", str(err))
            return

        size = len(matrix)
        self._size_var.set(str(size))
        self.generate_grid()

        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                self.coeff_entries[i][j].delete(0, tk.END)
                self.coeff_entries[i][j].insert(0, str(value))

    def _on_load_rhs(self):
        if not self.coeff_entries:
            messagebox.showinfo("Load RHS", "Generate the coefficient grid before loading the RHS vector.")
            return

        expected_size = len(self.coeff_entries)
        path = filedialog.askopenfilename(title="Select RHS vector file", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not path:
            return

        try:
            vector = self._read_vector_file(path, expected_size)
        except ValueError as err:
            messagebox.showerror("Load Error", str(err))
            return

        for i, value in enumerate(vector):
            self.rhs_entries[i].delete(0, tk.END)
            self.rhs_entries[i].insert(0, str(value))

    def _on_save_solution(self):
        if not self._latest_solution:
            messagebox.showinfo("Save Solution", "Solve the system before saving the solution.")
            return

        path = filedialog.asksaveasfilename(title="Save solution", defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as output_file:
                for value in self._latest_solution:
                    output_file.write(f"{value}\n")
        except OSError as err:
            messagebox.showerror("Save Error", f"Could not save solution: {err}")

    def _read_matrix_file(self, path: str):
        rows = []
        with open(path, "r", encoding="utf-8") as matrix_file:
            for line in matrix_file:
                stripped = line.strip()
                if not stripped:
                    continue
                parts = stripped.split()
                try:
                    row = [float(part) for part in parts]
                except ValueError as err:
                    raise ValueError(f"Non-numeric value found in matrix file: {err}") from err
                rows.append(row)

        if not rows:
            raise ValueError("Matrix file is empty.")

        size = len(rows)
        if any(len(row) != size for row in rows):
            raise ValueError("Matrix file must describe a square matrix (same number of rows and columns).")

        return rows

    def _read_vector_file(self, path: str, expected_size: int):
        values = []
        with open(path, "r", encoding="utf-8") as vector_file:
            for line in vector_file:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    values.append(float(stripped))
                except ValueError as err:
                    raise ValueError(f"Non-numeric value found in RHS file: {err}") from err

        if len(values) != expected_size:
            raise ValueError("The RHS vector length must match the coefficient matrix size.")

        return values


if __name__ == "__main__":
    app = LinearSystemApp()
    app.mainloop()
