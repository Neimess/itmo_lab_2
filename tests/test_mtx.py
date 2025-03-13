import glob
import os

import pytest

# from src import mtx
from latex_generator_neimess_itmo.latex_utils import mtx

from .metautils import Generator, compile_latex

RESOURCE_FOLDER_PATH = os.path.join("artifacts", "task_1")


@pytest.fixture(scope="module", autouse=True)
def clear_generator():
    Generator.clear()


@pytest.fixture(scope="function", autouse=True)
def clean_latex_dir():
    yield
    if os.path.exists(RESOURCE_FOLDER_PATH):
        for ext in ["log", "aux", "pdf"]:
            for file in glob.glob(os.path.join(RESOURCE_FOLDER_PATH, f"*.{ext}")):
                os.remove(file)


@pytest.fixture(scope="function")
def output_dir():
    return RESOURCE_FOLDER_PATH


@pytest.mark.parametrize(
    "input_matrix",
    [
        [[1]],
        [[1, 2], [3, 4]],
        [["A", "B", "C"], ["D", "E", "F"]],
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [list(range(1, 20)) for _ in range(20)],
    ],
)
def test_mtx_various_cases(input_matrix, output_dir):
    latex_code = mtx(input_matrix)
    assert isinstance(latex_code, str)
    assert r"\begin{tabular}" in latex_code

    pdf_file, _, stderr_output, result = compile_latex(latex_code, str(output_dir))

    assert pdf_file is not None, f"Compilation failed: {stderr_output}"
    assert os.path.exists(pdf_file)
    assert result.returncode == 0


def test_mtx_basic():
    matrix = [[]]
    latex_code = mtx(matrix)
    expected_code = ""
    assert latex_code.strip() == expected_code.strip()


def test_mtx_no_hlines():
    matrix = [[1, 2], [3, 4]]
    latex_code = mtx(matrix, hlines=False)
    assert r"\hline" not in latex_code


def test_mtx_no_vlines():
    matrix = [[1, 2], [3, 4]]
    latex_code = mtx(matrix, vlines=False)
    assert "|" not in latex_code.split("\\begin{tabular}")[1]


def test_mtx_empty():
    assert mtx([]) == ""


def test_mtx_compile(tmp_path):
    matrix = [["A", "B"], ["C", "D"]]
    latex_code = mtx(matrix)

    temp_dir = tmp_path / "latex_test"
    temp_dir.mkdir()

    pdf_file, _, stderr_output, result = compile_latex(latex_code, str(temp_dir))

    assert pdf_file is not None, f"Compilation failed: {stderr_output}"
    assert os.path.exists(pdf_file)
    assert result.returncode == 0


if __name__ == "__main__":
    pytest.main()
