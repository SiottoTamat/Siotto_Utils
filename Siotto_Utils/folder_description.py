import os
from pathlib import Path

from openpyxl import Workbook


def write_folder_tree(root_dir: Path, output_txt: Path):
    with output_txt.open("w", encoding="utf-8") as f:
        for path, dirs, _ in os.walk(root_dir):
            rel_path = Path(path).relative_to(root_dir)
            indent = "    " * len(rel_path.parts)
            f.write(
                f"{indent}"
                f"{rel_path.name if rel_path.name else root_dir.name}\n"
            )


def write_file_excel(
    root_dir: Path,
    output_xlsx: Path,
    allowed_extensions: list[str],
    title: str = "Filtered Files",
):
    wb = Workbook()
    ws = wb.active
    ws.title = title
    ws.append(["Relative Path", "Description", "Author"])

    for path in root_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in allowed_extensions:
            rel_path = str(path.relative_to(root_dir))
            ws.append([rel_path, "", ""])

    wb.save(output_xlsx)


def generate_reports(
    folder_path: str,
    file_types: list[str],
    output_txt: str = "folder_tree.txt",
    output_xlsx: str = "filtered_files.xlsx",
    worksheet_title: str = "Filtered Files",
):
    folder = Path(folder_path).resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"{folder} is not a valid directory.")

    output_txt_path = folder / output_txt
    output_xlsx_path = folder / output_xlsx

    allowed_extensions = [
        ext.lower() if ext.startswith(".") else f".{ext.lower()}"
        for ext in file_types
    ]

    write_folder_tree(folder, output_txt_path)
    write_file_excel(
        folder, output_xlsx_path, allowed_extensions, title=worksheet_title
    )

    print(f"Generated:\n- {output_txt_path}\n- {output_xlsx_path}")


# Example usage
# if __name__ == "__main__":
#     generate_reports(
#         r"path...\@@Deliverables_202505",
#         ["png", "jpg", "xlsx", "csv", "docx", "pdf", "aprx", "kml"],
#         "ASRfolder_tree.txt",
#         "ASR_selected_files.xlsx",
#         "ASRP_Project_Files",
#     )
