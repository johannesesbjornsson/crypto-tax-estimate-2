import sys
from pathlib import Path
import zipfile

sys.path.insert(0, str(Path(__file__).parent / "src"))

from csv_converter.reader.csv_reader import CSVReader
from csv_converter.detection.detector import CSVFormatDetector

from database.session import get_session
from database.repositories.exchange_rate_repository import ExchangeRateRepository
import re

def main():

    marketdata_path = Path("downloaded_files/marketdata")

    zip_files = sorted(
        marketdata_path.rglob("*.zip")
    )

    reader = CSVReader()

    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, "r") as archive:
            csv_name = archive.namelist()[0]

            m = re.search('(^[A-Z]+)(USDT)', csv_name)

            if m:
                asset = m.group(1)
                quote_currency = m.group(2)
            else:
                raise(f"Unable to match pair from {csv_name}")


            with archive.open(csv_name) as csv_file:
                content = csv_file.read().decode("utf-8")

                document = reader.read_content(
                    content=content, 
                    document_name=csv_name,
                    custom_headers=["open time", "open", "high", "low", "close", "volume", "close time", "quote asset volume", "number of trades", "taker buy base asset volume", "taker buy quote asset volume", "ignore"]
                )
                detector = CSVFormatDetector()
                parser = detector.detect(document)
                marketdata = parser.parse(document, asset=asset, quote_currency=quote_currency)



if __name__ == "__main__":
    main()