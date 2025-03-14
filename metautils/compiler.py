import os
import subprocess
from typing import Optional, Tuple

class Generator:
    static_var = 1

    @classmethod
    def generate(cls) -> int:
        tmp = cls.static_var
        cls.static_var += 1
        return tmp

    @classmethod
    def clear(cls) -> None:
        cls.static_var = 1


def compile_latex(latex_code: str, temp_dir: str) -> Tuple[Optional[str], str, str, subprocess.CompletedProcess]:
    tex_file = os.path.join(temp_dir, f"test_mtx_{Generator.generate()}.tex")
    pdf_file = tex_file.replace(".tex", ".pdf")

    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(latex_code)

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", temp_dir, tex_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    stderr_output = result.stderr.decode()
    stdout_output = result.stdout.decode()

    if os.path.exists(pdf_file):
        return pdf_file, stdout_output, stderr_output, result
    else:
        return None, stdout_output, stderr_output, result
