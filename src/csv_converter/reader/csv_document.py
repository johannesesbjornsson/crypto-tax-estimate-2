from dataclasses import dataclass


@dataclass
class CSVDocument:
    headers: list[str]
    document_name: str
    rows: list[dict[str, str]]