from typing import Tuple
import pandas as pd
import csv
from tkinter import filedialog, messagebox
import codecs


__author__ = "Andrea Siotto."
__copyright__ = "Open Source"
__credits__ = ["Andrea Siotto"]
__license__ = "Undecided"
__version__ = "1.0"
__maintainer__ = "Andrea Siotto"
__email__ = "siotto.public@gmail.com"
__status__ = "Development"


def check_UTF_8(file) -> bool:
    """
    Check that the file is utf-8 compliant
    """
    try:
        with codecs.open(file, encoding="utf-8-sig", errors="strict") as f:
            for _ in f:
                pass
        return True
    except UnicodeDecodeError:
        return False


def read_excel(filename: str, sheet=0, to_dict=True) -> list[dict] | list[list]:
    """
    Takes the path of the file and returns a list of dictionaries or a list of lists.
    Optionally takes a specific name of the sheet. If the argument to_dict is False,
    returns a list of lists.
    Default sheet name is "Data"
    """
    try:
        df = pd.read_excel(filename, sheet_name=sheet, dtype=str)
    except Exception as e:
        raise ValueError(f"Failed to read Excel file {filename}: {e}")

    if to_dict:
        return df.fillna("").to_dict("records")
    else:
        headers = df.columns.values.tolist()
        df = df.fillna("")
        data = df.values.tolist()
        data.insert(0, headers)
        return data


def read_csv(filename: str, to_dict=True) -> list[dict] | list[list]:
    """
    Takes the path of the csv file and returns a list of dictionaries.
    """
    locations = []
    try:
        with open(filename, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            headers = next(reader)
            if to_dict:
                for row in reader:
                    locations.append({key: value for key, value in zip(headers, row)})
            else:
                locations.append(headers)
                locations.extend(reader)
        return locations
    except Exception as e:
        raise ValueError(f"Failed to read CSV file {filename}: {e}")


def file_to_list(
    defaultDir: str, filename: str = "", to_dict=True
) -> Tuple[list[dict] | list[list], str]:
    """
    The main function to open a csv or excel file and produce a list of dictionaries.
    It opens an openfiledialog and then from the chosen file returns the list. Each row is an
    element of the list as a dictionary with the key as the name of the column and the value as the value
    of the cell.
    """
    allowed_files = [
        ("Excel files", "*.xls *.xlsx *.xlsm *.xlsb *.odf *.ods *.odt"),
        ("CSV files", "*.csv"),
    ]

    if not filename:
        filename = filedialog.askopenfilename(
            filetypes=allowed_files, initialdir=defaultDir
        )
    if not filename:
        return [], ""

    try:
        ext = filename.rsplit(".", 1)[-1].lower()
        if ext == "csv":
            return read_csv(filename, to_dict), filename
        elif ext in ["xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt"]:
            return read_excel(filename, to_dict=to_dict), filename
        else:
            messagebox.showerror(
                title="Unsupported File",
                message="This program only supports CSV and Excel files.",
            )
            return [], ""
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error reading file: {e}")
        return [], ""


def list_to_file(list_data: list, defaultDir: str) -> None:
    """
    The main handler for transforming a list of dictionaries into a file.
    open an openfiledialog, asking for a filename and then save it either as
    a csv or as an excel file.
    """

    allowed_files = [
        ("Excel files", "*.xls *.xlsx *.xlsm *.xlsb *.odf *.ods *.odt"),
        ("CSV files", "*.csv"),
    ]

    filename = filedialog.asksaveasfilename(
        filetypes=allowed_files, initialdir=defaultDir, defaultextension=".xlsx"
    )
    if not filename or not list_data:
        return

    try:
        ext = filename.rsplit(".", 1)[-1].lower()

        if isinstance(list_data[0], dict):
            df = pd.DataFrame(list_data)
        elif isinstance(list_data[0], list):
            # First element is header, the rest are rows
            df = pd.DataFrame(list_data[1:], columns=list_data[0])
        else:
            raise ValueError("Unsupported data format for export.")

        if ext == "csv":
            df.to_csv(filename, index=False, encoding="utf-8-sig")
        else:
            df.to_excel(filename, index=False)

        messagebox.showinfo(title="Success", message="File saved successfully.")
    except Exception as e:
        messagebox.showerror(title="Save Error", message=f"Failed to save file: {e}")
