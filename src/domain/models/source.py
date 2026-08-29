from dataclasses import dataclass
import datetime

@dataclass
class Source:
    venue: str
    source_file: str | None