from typing import List


def mtx(matrix: List[List[object]], hlines: bool = True, vlines: bool = True) -> str:
    """
    Convert a matrix into a valid LaTex-formatted table string
    Args:
        matrix (List[List[object]]): The matrix to convert, containing elements convertible to str.
        hlines (bool): Whether to include horizontal lines. Defaults to True.
        vlines (bool): Whether to include vertical lines. Defaults to True.

    Returns:
        str: A string containing LaTeX-formatted table code.
    """

    if not matrix or not matrix[0]:
        return ""

    cols = len(matrix[0])
    table_format = ("|" if vlines else "") + ("c|" if vlines else "c") * cols
    header = f"\\begin{{tabular}}{{{table_format}}}\n" + ("\\hline\n" if hlines else "")
    footer = "\\end{tabular}"
    body = "\n".join((" & ".join(map(str, row)) + " \\\\ " + ("\\hline" if hlines else "")) for row in matrix)
    return header + body + "\n" + footer


mtx([[1, 233, 3], [32, 324, 1]], True, False)
