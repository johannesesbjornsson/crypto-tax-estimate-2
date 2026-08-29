# crypto-tax-estimate-2

For fun



```
docker compose -f docker-compose.yml up -d
```

```
flyway -environment=local migrate
```

```
flyway -environment=local  clean  -cleanDisabled=false
```


```
psql "postgresql://postgres:password@localhost:5432/crypto_tax"
```


```
pytest tests/csv_converter/
```


Download USD/EUR data from here: 
https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/eurofxref-graph-usd.en.html ```

Download USD/GBP data from here
https://www.bankofengland.co.uk/boeapps/database/Rates.asp?Travel=NIxIRx&into=GBP


Download Binance marketdata from here
https://github.com/binance/binance-public-data/tree/master 


```
git clone https://github.com/binance/binance-public-data.git
cd binance-public-data
pip install -r python/requirements.txt
python3 python/download-kline.py \
    -t spot \
    -s BTCUSDT ETHUSDT SOLUSDT \
    -i 1h \
    -startDate 2022-01-01 \
    -endDate 2026-05-01 \
    -folder /Users/johannesesbjornsson/Documents/workspace/crypto-tax-estimate-2/downloaded_files/marketdata/
```