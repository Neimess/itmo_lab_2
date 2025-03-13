import glob
import os

import pytest

# from src import image_latex
# Заменен на Pypi
from latex_generator_neimess_itmo.latex_utils import image_latex

from .metautils import Generator, compile_latex

RESOURCE_FOLDER_PATH = os.path.join("artifacts", "task_2")


@pytest.fixture(scope="module", autouse=True)
def clear_generator():
    Generator.clear()


@pytest.fixture(scope="function", autouse=True)
def clean_latex_dir():
    yield
    if os.path.exists(RESOURCE_FOLDER_PATH):
        for ext in ["log", "aux"]:
            files = glob.glob(os.path.join(RESOURCE_FOLDER_PATH, f"*.{ext}"))
            for file in files:
                os.remove(file)

    tex_files = glob.glob(os.path.join(RESOURCE_FOLDER_PATH, "*.tex"))
    if tex_files:
        tex_files.sort(key=os.path.getmtime, reverse=True)
        for file in tex_files[1:]:
            os.remove(file)

    pdf_files = glob.glob(os.path.join(RESOURCE_FOLDER_PATH, "*.pdf"))
    if pdf_files:
        pdf_files.sort(key=os.path.getmtime, reverse=True)
        for file in pdf_files[1:]:
            os.remove(file)


@pytest.fixture(scope="function")
def image_path():
    return os.path.join(RESOURCE_FOLDER_PATH, "python_meme.png")


@pytest.fixture(scope="function")
def output_dir():
    return RESOURCE_FOLDER_PATH


@pytest.mark.parametrize(
    "arguments",
    [
        {},
        {"centering": True, "position": "h", "caption": "Example Image 1", "label": "fig:img1", "width": r"\textwidth"},
        {
            "centering": False,
            "position": "!",
            "caption": "Centered Image",
            "label": "fig:img2",
            "width": "0.8\\textwidth",
        },
        {
            "centering": True,
            "position": "t",
            "caption": "Top Positioned Image",
            "label": "fig:img3",
            "width": "0.5\\textwidth",
        },
        {"centering": False, "position": "b", "caption": "Bottom Image", "label": "fig:img4", "width": "7cm"},
        {"centering": False, "position": "b", "caption": "Wide Image", "label": "fig:img10", "width": "20cm"},
        {"centering": True, "position": "p", "caption": "Page Image", "label": "fig:img5", "width": "10cm"},
        {"centering": True, "position": "h", "caption": "Scaled Image", "label": "fig:img6", "width": "0.3\\textwidth"},
        {"centering": False, "position": "!", "caption": "Large Image", "label": "fig:img7", "width": "15cm"},
        {"centering": True, "position": "h", "caption": "With Default Width", "label": "fig:img8"},
        {"centering": True, "position": "t", "caption": "Narrow Image", "label": "fig:img9", "width": "5cm"},
    ],
)
def test_image_kwargs(image_path, arguments, output_dir):
    latex_code = image_latex(image_path, **arguments)
    assert isinstance(latex_code, str)
    pdf_file, _, stderr_output, result = compile_latex(latex_code, str(output_dir), graphicx=True)
    assert pdf_file is not None, f"Compilation failed: {stderr_output}"
    assert os.path.exists(pdf_file)
    assert result.returncode == 0


def test_no_image():
    with pytest.raises(FileNotFoundError) as excinfo:
        image_latex("no_exists.png")
    assert "no_exists.png" in str(excinfo.value), "Error must contains name of unexisted file"
