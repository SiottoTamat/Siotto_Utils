import json
from pathlib import Path


def merge_jsons(location_json_folder, key: str = "filename") -> dict:
    """
    Merge multiple JSON files from a folder into a single dictionary.

    Args:
        location_json_folder (Path): Path to the folder containing JSON files.
        key (str): Key to use for indexing each loaded JSON.
                   If 'filename', the filename (without extension) is used.
                   Otherwise, tries to use the value inside the JSON corresponding to the specified key.
                   If the key is missing, falls back to using the filename.

    Returns:
        dict: A dictionary where each key is either the filename or a specified value from each JSON,
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
