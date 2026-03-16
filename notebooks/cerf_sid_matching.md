---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
  kernelspec:
    display_name: ds-ibtracs-matching
    language: python
    name: ds-ibtracs-matching
---

# CERF matching

```python
%load_ext jupyter_black
%load_ext autoreload
%autoreload 2
```

```python
import json
from io import BytesIO

import ocha_stratus as stratus
import pandas as pd

from src.datasources import cerf
```

## Load data

### CERF

```python
df_cerf = cerf.load_cerf_applications()
```

```python
CERF_URL = "https://cerf.un.org/what-we-do/allocation/all/summary/{cerf_id}"
```

```python
df_cerf.columns
```

```python
df_cerf_storms = df_cerf[
    (df_cerf["EmergencyTypeName"] == "Storm")
    & (df_cerf["WindowFullName"] == "Rapid Response")
]
```

```python
df_cerf_storms["url"] = df_cerf_storms["ApplicationCode"].apply(
    lambda x: CERF_URL.format(cerf_id=x)
)
```

```python
df_cerf_storms
```

### IBTrACS storms

```python
query = """
SELECT *
FROM storms.ibtracs_storms
"""
with stratus.get_engine(stage="prod").connect() as con:
    df_storms = pd.read_sql(query, con)
```

```python
df_storms_recent = df_storms[df_storms["season"] >= 2006]
```

```python
IBTRACS_URL = "https://ncics.org/ibtracs/index.php?name=v04r01-{sid}"
```

```python
df_storms_recent["url"] = df_storms_recent["sid"].apply(
    lambda x: IBTRACS_URL.format(sid=x)
)
```

## Merge

Go through each CERF allocation and see if the description fits a TC. If so, grab the TC `sid` and put it in the `new_cerfcode2sid` dict. If it doesn't match, put in `None`.

Storms can be looked up by basin and year here: https://ncics.org/ibtracs/index.php?name=browse-year-basin

```python
new_cerfcode2sid = {
    "07-RR-SDN-13738": None,
    "07-RR-DOM-13362": "2007345N18298",
}
```

```python
df_cerf_storms["sid"] = df_cerf_storms["ApplicationCode"].apply(
    lambda x: new_cerfcode2sid.get(x, "")
)
```

```python
cols = ["ApplicationCode", "CN_Summary"]
```

```python
for _, row in df_cerf_storms[df_cerf_storms["sid"] == ""].iterrows():
    print(row["ApplicationCode"])
    print(row["CN_Summary"])
    print(row["url"])
    print()
```

```python

```

```python

```
