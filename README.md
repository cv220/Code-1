# Linear System Tools

This project provides both a console workflow and a modern PyQt-based graphical interface for entering and solving square linear systems using NumPy.

## Requirements

- Python 3.11+
- NumPy
- PyQt5 (`pip install PyQt5`)

## Console Usage

Run the console helper to enter the system manually:

```bash
python hello_spyder.py
```

1. Enter the size `n` of the square matrix.
2. Provide each coefficient when prompted (the program identifies the row/column).
3. Provide each right-hand-side entry.
4. Review the displayed solution and optionally save it to a text file.

## GUI Usage

Launch the PyQt application for a paper-style entry grid:

```bash
python ui_app.py
```

- Set the desired system size with the spin box and click **Generate Grid** (or press Enter) to refresh the table.
- Type coefficients and RHS entries directly in the grid, then click **Solve** to compute the solution.
- Use **Load Coefficients…** or **Load RHS…** to import whitespace-separated values from text files.
- Choose **Save Solution…** to export the most recent solution vector to a file.
- Click **Clear** to reset all inputs and results.

Both interfaces rely on the shared `linear_solver.solve_linear_system` helper, ensuring consistent results between the console and GUI experiences.
