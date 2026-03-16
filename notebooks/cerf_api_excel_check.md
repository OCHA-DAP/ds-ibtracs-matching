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

# CERF check

Verifying that the CERF API matches the Excel export

```python
%load_ext jupyter_black
%load_ext autoreload
%autoreload 2
```

```python
from io import BytesIO

import ocha_stratus as stratus
import pandas as pd

from src.datasources import cerf
```

```python
blob_name = "cerf/AllocationsByYear.xlsx"
```

```python
df_cerf_excel = pd.read_excel(
    BytesIO(stratus.load_blob_data(blob_name, container_name="global"))
)
```

```python
test_country_name = "Afghanistan"
```

```python
df_cerf_excel.dtypes
```

```python
df_cerf_excel_test = df_cerf_excel[
    df_cerf_excel["Country"] == test_country_name
].sort_values("Allocation date", ascending=False)
```

```python
df_cerf_api = cerf.load_cerf_applications()
```

```python
df_cerf_api.dtypes
```

```python
df_cerf_api["CN_ERC_EndorsementDate"] = pd.to_datetime(
    df_cerf_api["CN_ERC_EndorsementDate"]
)
```

```python
df_cerf_api[["TotalAmountApproved", "CN_AmountRequested"]] = (
    df_cerf_api[["TotalAmountApproved", "CN_AmountRequested"]].astype(float).astype(int)
)
```

```python
cols = ["CN_ERC_EndorsementDate", "TotalAmountApproved"]
df_cerf_api_test = df_cerf_api[
    df_cerf_api["CountryName"] == test_country_name
].sort_values("CN_ERC_EndorsementDate", ascending=False)
```

```python
len(df_cerf_excel)
```

```python
len(df_cerf_api)
```

```python
df_merge = df_cerf_excel.merge(
    df_cerf_api,
    left_on=["Country", "Amount in US$", "Allocation date"],
    right_on=["CountryName", "TotalAmountApproved", "CN_ERC_EndorsementDate"],
    how="outer",
)
```

```python
column_mapping = {
    old: new
    for old, new in zip(
        ["CountryName", "TotalAmountApproved", "CN_ERC_EndorsementDate"],
        ["Country", "Amount in US$", "Allocation date"],
        strict=True,
    )
}
```

```python
column_mapping
```

```python

```
