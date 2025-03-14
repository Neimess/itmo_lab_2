import os
import subprocess
from typing import Any, Optional, Tuple

from latex_generator_neimess_itmo.latex_utils import image_latex, mtx

from metautils import compile_latex


def matrix_tex_generator(matrix: list[list[Any]]) -> Tuple[Optional[str], str, str, subprocess.CompletedProcess]:
    latex_code = mtx(matrix)
    return compile_latex(latex_code, "artifacts/task_1")


def image_tex_generator(image_path: str) -> Tuple[Optional[str], str, str, subprocess.CompletedProcess]:
    if not os.path.isfile(image_path):
        raise FileNotFoundError
    latex_code = image_latex(image_path)
    return compile_latex(latex_code, "artifacts/task_2")


def main() -> None:
    matrix = [[r"\gamma", r"\kappa", r"\alpha", r"\psi"], [r"\epsilon", r"\iota", r"\Phi", r"\Psi"]]
    mat = matrix_tex_generator(matrix)
    if mat[0]:
        print(f"PDF was generated at {mat[0]}")
    else:
        print(f"error while compile file stderr: {mat[2]}")
    image_path = os.path.join("artifacts", "task_2", "python_meme.png")
    image = image_tex_generator(image_path)
    if image[0]:
        print(f"PDF was generated at {image[0]}")
    else:
        print(f"error while compile file stderr: {image[2]}")


if __name__ == "__main__":
    main()
