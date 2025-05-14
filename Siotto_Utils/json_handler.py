import inspect
import json
import re
from pathlib import Path

import pandas as pd

from Siotto_Utils.logger_utils import setup_logger


def merge_jsons(location_json_folder, key: str = "filename") -> dict:
    """
    Merge multiple JSON files from a folder into a single dictionary.

    Args:
        location_json_folder (Path): Path to the folder containing JSON files.
        key (str): Key to use for indexing each loaded JSON.
                   If 'filename', the filename (without extension) is used.
                   Otherwise, tries to use the value inside the JSON
                   corresponding to the specified key.
                   If the key is missing, falls back to using the filename.

    Returns:
        dict: A dictionary where each key is either the filename
            or a specified value from each JSON,
            and the value is the parsed JSON content.
    """
    merged_dicts = {}
    name_jsons = [f.name for f in location_json_folder.glob("*.json")]
    for name in name_jsons:
        with open(location_json_folder / f"{name}", "r", encoding="utf-8") as f:
            data = json.load(f)
        if key == "filename":
            dict_key = Path(name).stem
        else:
            dict_key = data.get(
                key, Path(name).stem
            )  # fallback to filename if key missing
            print(f"No such key '{key}' in the JSON file '{name}': {data}\n")

        merged_dicts[dict_key] = data
    return merged_dicts


def excel_to_json(filename: Path) -> None:
    """
    Converts each worksheet in an Excel file into separate JSON files.
    Each JSON is named <filename>_<sheet_name>.json and saved
    in the same directory.
    Logs each conversion using a function-specific logger.
    """
    func_name = inspect.currentframe().f_code.co_name
    logger = setup_logger(f"{__name__}.{func_name}")

    filename = Path(filename)
    stem = filename.stem

    try:
        sheets = pd.read_excel(filename, sheet_name=None)
    except Exception as e:
        logger.error(f"Failed to read Excel file: {filename} — {e}")
        return

    for sheet_name, df in sheets.items():
        safe_sheet_name = re.sub(r"[^\w\d_-]", "_", sheet_name.strip())
        json_filename = filename.parent / f"{stem}_{safe_sheet_name}.json"
        try:
            df.to_json(json_filename, orient="records", force_ascii=False, indent=2)
            logger.info(f"Saved {json_filename} as a JSON file.")
        except Exception as e:
            logger.error(f"Failed to write JSON for sheet '{sheet_name}': {e}")
