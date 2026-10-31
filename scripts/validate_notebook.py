from pathlib import Path

import nbformat


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "lazada_sentiment_analysis.ipynb"


def main() -> None:
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    nbformat.validate(notebook)

    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    errors = [
        output
        for cell in code_cells
        for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]
    unexecuted = [
        index
        for index, cell in enumerate(notebook.cells)
        if cell.cell_type == "code" and cell.get("execution_count") is None
    ]

    print(f"Notebook: {NOTEBOOK_PATH}")
    print(f"Cells: {len(notebook.cells)} ({len(code_cells)} code)")
    print(f"Execution errors: {len(errors)}")
    print(f"Unexecuted code cells: {unexecuted}")

    if errors or unexecuted:
        raise SystemExit(1)


if __name__ == "__main__":
    main()


