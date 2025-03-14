# 📄 latex-generator-neimess-itmo

**latex-generator-neimess-itmo** — это Python-библиотека для удобного создания кода **LaTeX** с таблицами и изображениями. Для форматирования таблиц (`mtx`) и вставки изображений (`image_latex`) в `.tex`-файлы.

# 📌 Ссылка на PyPI

📦 PyPI: https://pypi.org/project/latex-generator-neimess-itmo/

# Дополнительно для проверяющего

1. 📌 src/latex_converter.py не используется – это исходный код, который был отправлен на PyPI.  
2. 📌 Основная программа работающая с зависимостью.
    ```python
    uv run src/main.py
    ```
3. 📌 tests запускает установленный пакет latex_generator_neimess_itmo, а не файлы из src.
    ```python
    uv run pytest tests -vv -s
    ```
4. 📌 Тесты для src закомментированы.



##  Установка

Установить библиотеку можно через **PyPI**:

```bash
pip install latex-generator-neimess-itmo
```

---

##  Использование

### **Генерация таблицы в LaTeX**
```python
from latex-generator-neimess-itmo.latex_utils import mtx

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

table_code = mtx(matrix, caption="Пример таблицы", label="tab:example", table_env=True)
print(table_code)
```
📌 **Вывод**:
```latex
\documentclass{article}

\begin{document}
\begin{table}[h]
\begin{tabular}{|c|c|c|}
\hline
1 & 2 & 3 \\\hline
4 & 5 & 6 \\\hline
7 & 8 & 9 \\\hline
\end{tabular}
\caption{Пример таблицы}
\label{tab:example}
\end{table}
\end{document}
```

---

### 🔹 **Добавление изображения в LaTeX**
```python
from latex-generator-neimess-itmo.latex_utils import image_latex

image_code = image_latex("example.png", caption="Пример изображения", label="fig:example")
print(image_code)
```
📌 **Вывод**:
```latex
\documentclass{article}
\usepackage{graphicx}
\begin{document}
\begin{figure}[h]
\centering
\includegraphics[width=\textwidth]{example.png}
\caption{Пример изображения}
\label{fig:example}
\end{figure}
\end{document}
```

---

## 📄 **Генерация PDF-файла**
Можно объединить таблицу и изображение и скомпилировать `.tex` в **PDF**:

```python
from latex-generator-neimess-itmo.latex_utils import mtx, image_latex
import subprocess

# Данные
matrix = [[1, 2], [3, 4]]

# Генерация LaTeX-кода
table_code = mtx(matrix, caption="Таблица", label="tab:my_table", table_env=True)
image_code = image_latex("example.png", caption="Изображение", label="fig:my_image")

# Создание документа
latex_doc = f"""
\documentclass{article}
\usepackage{graphicx}
\begin{document}

{table_code}

{image_code}

\end{document}
"""

# Сохранение в файл
with open("document.tex", "w") as f:
    f.write(latex_doc)

# Компиляция в PDF (требуется установленный TeX Live / MiKTeX)
subprocess.run(["pdflatex", "document.tex"])
```

📌 **После выполнения появится файл `document.pdf` с таблицей и изображением.**

---

## 🛠 **Параметры функций**

### 📌 `mtx(matrix, **kwargs)`
| Параметр    | Тип   | Описание |
|-------------|-------|-----------|
| `matrix`    | `List[List[object]]` | Двумерный список с данными таблицы |
| `hlines`    | `bool` | Включить горизонтальные линии (по умолчанию `True`) |
| `vlines`    | `bool` | Включить вертикальные линии (по умолчанию `True`) |
| `col_align` | `str`  | Выравнивание столбцов (`"c"`, `"l"`, `"r"`) |
| `table_env` | `bool` | Заворачивать в `table`-окружение (по умолчанию `False`) |
| `pos`       | `str`  | Позиция таблицы (`"h"`, `"H"`, `"t"`, `"b"`, `"p"`) |
| `caption`   | `str`  | Описание таблицы |
| `label`     | `str`  | Метка для ссылки на таблицу |

---

### 📌 `image_latex(image_path, **kwargs)`
| Параметр    | Тип   | Описание |
|-------------|-------|-----------|
| `image_path` | `str`  | Путь к изображению |
| `centering`  | `bool` | Центрирование (по умолчанию `True`) |
| `position`   | `str`  | Позиция (`"h"`, `"t"`, `"b"`, `"p"`, `"!"`) |
| `caption`    | `str`  | Описание изображения |
| `label`      | `str`  | Метка для ссылки на изображение |
| `width`      | `str`  | Ширина изображения (по умолчанию `\textwidth`) |
