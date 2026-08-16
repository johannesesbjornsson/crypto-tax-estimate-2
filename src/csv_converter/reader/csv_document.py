from dataclasses import dataclass


@dataclass
class CSVDocument:
    headers: list[str]
    rows: list[dict[str, str]]