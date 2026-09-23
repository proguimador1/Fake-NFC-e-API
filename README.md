## Fake NFC-e Generator

This is an API that generates XML files for fake **NFC-e (Brazilian electronic consumer invoices)**.

To run the API, first install the dependencies:

```bash
uv sync
```

Then, start the FastAPI server:

```bash
uv run fastapi run nfce_generator.py
```

The API provides the following endpoint to generate a fake xml:

```http
POST /api/gerar-compra
```

If you want to generate a database containing fake NFC-e XML files, run:

```bash
python xml_database_generator.py
```
