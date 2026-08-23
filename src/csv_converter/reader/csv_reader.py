import csv
from pathlib import Path

from .csv_document import CSVDocument


class CSVReader:

    def read(self, file_path: Path) -> CSVDocument:
        with file_path.open(
            mode="r",
            encoding="utf-8-sig",
            newline="",
        ) as file:

            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError("CSV file has no headers")

            headers = list(reader.fieldnames)
            rows = list(reader)

        return CSVDocument(
            headers=headers,
            document_name=file_path.name,
            rows=rows,
            number_data_rows=len(rows)
        )