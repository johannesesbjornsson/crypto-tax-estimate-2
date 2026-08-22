from datetime import datetime
from decimal import Decimal
import re

from csv_converter.reader.csv_document import CSVDocument
from csv_converter.parsers.kraken.models import (
    KrakenTransaction,
    KrakenTrade,
    KrakenDeposit,
    KrakenStaking,
    KrakenWithdrawl,
)
from .normaliser import Krakennormaliser


class KrakenTransactionParser:
    REQUIRED_COLUMNS = {
        "txid",
        "refid",
        "time",
        "type",
        "subtype",
        "aclass",
        "asset",
        "wallet",
        "amount",
        "fee",
        "balance"
    }

    def can_parse(self, document: CSVDocument) -> bool:
        return self.REQUIRED_COLUMNS.issubset(
            set(document.headers)
        )

    def create_trade_transaction(self, sell_currenct: dict, buy_currency: dict, document_name: str) -> KrakenTrade:
        
        trade = KrakenTrade(
            tx_id=sell_currenct['txid'],
            ref_id=sell_currenct['refid'],
            timestamp=datetime.strptime(
                sell_currenct["time"],
                "%Y-%m-%d %H:%M:%S",
            ),
            price=Decimal(abs(Decimal(sell_currenct["amount"]))/Decimal(buy_currency['amount'])),
            from_asset=sell_currenct['asset'],
            from_asset_amount=abs(Decimal(sell_currenct['amount'])),
            to_asset=buy_currency['asset'],
            to_asset_amount=Decimal(buy_currency['amount']),
            fee=Decimal(sell_currenct['fee']),
            fee_asset=sell_currenct['asset'],
            source=document_name,
        )
        return trade


    def santize_asset_name(self, asset_name) -> str:
        m = re.search('([A-Z]+)', asset_name)
        if m:
            return m.group(1)
        else:
            raise ValueError(f"Unable to find assetname in {asset_name}")

    def parse(self, document: CSVDocument) -> list[KrakenTransaction]:
        transactions = []
        pening_insert = {}
        normaliser = Krakennormaliser() 
        for row in document.rows:
            transaction = None

            if row['type'] == "trade":                        
                if pening_insert:
                    if row['refid'] in pening_insert:
                        transaction = self.create_trade_transaction(pening_insert[row['refid']], row, document.document_name)
                        pening_insert.pop(row['refid'])
                        
                    else:
                        raise ValueError(f"Pending insert is not empty: {pening_insert}")
                else:
                    pening_insert[row['refid']] = row
            elif row['type'] == "staking" or row['type'] == "earn":
                transaction = KrakenStaking(
                    tx_id=row['txid'],
                    ref_id=row['refid'],
                    timestamp=datetime.strptime(
                        row["time"],
                        "%Y-%m-%d %H:%M:%S",
                    ),
                    asset=self.santize_asset_name(row['asset']),
                    amount=Decimal(row['amount']),
                    source=document.document_name
                )
                
            elif row['type'] == "deposit":
                transaction = KrakenDeposit(
                    tx_id=row['txid'],
                    ref_id=row['refid'],
                    timestamp=datetime.strptime(
                        row["time"],
                        "%Y-%m-%d %H:%M:%S",
                    ),
                    asset=self.santize_asset_name(row['asset']),
                    amount=Decimal(row['amount']),
                    source=document.document_name
                )
            elif row['type'] == "withdrawal":
                transaction = KrakenWithdrawl(
                    tx_id=row['txid'],
                    ref_id=row['refid'],
                    timestamp=datetime.strptime(
                        row["time"],
                        "%Y-%m-%d %H:%M:%S",
                    ),
                    asset=self.santize_asset_name(row['asset']),
                    amount=Decimal(row['amount']),
                    source=document.document_name
                )
            
            elif row['type'] == "transfer":
                pass
            else:
                raise ValueError(f"unknown transaction type {row['type']}")

            if transaction:
                transactions.append(normaliser.normalize(transaction))
            

        return transactions

