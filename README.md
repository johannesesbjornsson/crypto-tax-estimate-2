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