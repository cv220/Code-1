from ti_system import cls


def get_value(prompt):
    """Prompt for a floating-point value until the user enters a valid number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def main():
    cls()
    print("LINEAR INTERP")
    print("Y=Y1+(X-X1)")
    print("*((Y2-Y1)/(X2-X1))")

    x1 = get_value("X1? ")
    y1 = get_value("Y1? ")
    x2 = get_value("X2? ")
    y2 = get_value("Y2? ")
    x = get_value("X? ")

    denominator = x2 - x1
    if denominator == 0:
        print("ERROR: X1 = X2")
        input("Press Enter to exit.")
        return

    slope = (y2 - y1) / denominator
    y = y1 + (x - x1) * slope

    print("Y =", y)
    input("Press Enter to exit.")


if __name__ == "__main__":
    main()
