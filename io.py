from pathlib import Path


def is_xlsx(filename: str) -> bool:
    return extension(filename) == "xlsx"


def is_csv(filename: str) -> bool:
    return extension(filename) == "csv"


def extension(filename: str) -> str:
    return Path(filename).suffix[1:]
