# Code-1

## TI-84 Plus CE Linear Interpolation Programs

This repository contains both TI-Basic and TI-Python programs that quickly solve linear interpolation problems on a TI-84 Plus CE calculator. The formula used is:

```
Y = Y₁ + (X - X₁) * ((Y₂ - Y₁) / (X₂ - X₁))
```

### Shared features
- Clears the home screen and displays the interpolation formula.
- Prompts for each required value (`X₁`, `Y₁`, `X₂`, `Y₂`, `X`).
- Checks for `X₁ = X₂` before performing the division so the calculator never raises "Check all arguments entered.".
- Computes the interpolated `Y` value and displays the result.

### TI-Basic version
1. Create a new program on the TI-84 Plus CE and name it (for example) `LININT`.
2. Enter the listing from [`LINEAR_INTERP_TI84.txt`](LINEAR_INTERP_TI84.txt) exactly. Use the `Sto>` key (located above the `ON` key) to type the `→` token, and use the multiplication key so that the calculator inserts `*` rather than a `×` symbol.
3. Run the program and supply the requested inputs to obtain the interpolated `Y` value.

### TI-Python version
1. Open the Python app on the TI-84 Plus CE and create a new program (for example, `lin_interp`).
2. Type or import the code from [`LINEAR_INTERP_TI84.py`](LINEAR_INTERP_TI84.py). The script uses `ti_system.cls()` to clear the screen before displaying the formula and re-prompts until a valid numeric value is entered for each input.
3. Run the script. If `X₁` equals `X₂`, the program displays an error message; otherwise it prints the interpolated `Y` value and waits for you to press `Enter` before closing.

Both code files are formatted so they can be typed directly into the calculator or imported with TI Connect CE.
