"""Utility helpers for solving linear systems."""
from typing import List

import numpy as np


def solve_linear_system(coefficients: List[List[float]], rhs: List[float]) -> List[float]:
    """Solve Ax = b using numpy and return the solution as a Python list."""
    a_np = np.array(coefficients, dtype=float)
    b_np = np.array(rhs, dtype=float)
    solution = np.linalg.solve(a_np, b_np)
    return solution.tolist()
