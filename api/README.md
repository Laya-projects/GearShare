# GearShare Mini API

From the repository root, start the API with:

```text
python -m uvicorn api.main:app --reload
```

The API reads `TODAY` from the environment and otherwise uses the real date.
