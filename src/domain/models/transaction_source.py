from dataclasses import dataclass

@dataclass
class TransactionSource:
    venue: str
    source_file: str | None