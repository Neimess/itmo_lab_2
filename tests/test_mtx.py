import glob
import os

import pytest

# from src import mtx
from latex_generator_neimess_itmo.latex_utils import mtx

from metautils import Generator, compile_latex

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
    assert result.returncode == 0, f"Something went wrong: {stderr_output}"


@pytest.mark.parametrize(
    "input_matrix, kwargs",
    [
        ([[r"$\alpha$", r"$\beta$", r"$\gamma$"], [r"$\delta$", r"$\epsilon$", r"$\zeta$"]], {}),
        # Без аргументов
        (
            [[r"$\eta$", r"$\theta$", r"$\iota$"], [r"$\kappa$", r"$\lambda$", r"$\mu$"]],
            {"hlines": True},
        ),
        # Горизонтальные линии
        (
            [[r"$\nu$", r"$\xi$", r"$\O$"], [r"$\pi$", r"$\rho$", r"$\sigma$"]],
            {"vlines": True},
        ),
        # Вертикальные линии
        (
            [[r"$\tau$", r"$\upsilon$", r"$\varphi$"], [r"$\chi$", r"$\psi$", r"$\omega$"]],
            {"col_align": "lcr"},
        ),
        # Разное выравнивание столбцов
        (
            [[r"$\alpha$", r"$\beta$"], [r"$\gamma$", r"$\delta$"]],
            {"table_env": True, "caption": "Greek Letters", "label": "tab:greek"},
        ),
        # Табличная среда с подписью
        ([[r"$\epsilon$", r"$\zeta$"], [r"$\eta$", r"$\theta$"]], {"pos": "H"}),
        # Позиционирование
        (
            [[r"$\Gamma$", r"$\Delta$", r"$\Theta$"], [r"$\Lambda$", r"$\Xi$", r"$\Pi$"]],
            {"hlines": True, "vlines": True},
        ),
        # Горизонтальные + вертикальные линии
        (
            [[r"$\Sigma$", r"$\Upsilon$", r"$\Phi$"], [r"$\Psi$", r"$\Omega$", r"$\alpha$"]],
            {"col_align": "rrl"},
        ),
        # Разное выравнивание
        (
            [[r"$\beta$", r"$\gamma$", r"$\delta$"], [r"$\epsilon$", r"$\zeta$", r"$\eta$"]],
            {"table_env": True, "pos": "t", "caption": "Test Table", "label": "tab:test"},
        ),
        # Сложная комбинация аргументов
    ],
)
def test_mtx_greek_cases(input_matrix, kwargs, output_dir):
    latex_code = mtx(input_matrix, **kwargs)
    assert isinstance(latex_code, str)
    assert r"\begin{tabular}" in latex_code

    pdf_file, stdout_output, stderr_output, result = compile_latex(latex_code, str(output_dir))
    assert pdf_file is not None, f"Compilation failed: {stdout_output}"
    assert os.path.exists(pdf_file)
    assert result.returncode == 0, f"Something went wrong: {stdout_output}"


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
