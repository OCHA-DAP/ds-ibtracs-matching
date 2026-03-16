import xml.etree.ElementTree as ET

import pandas as pd
import requests

CERF_API_BASE_URL = "https://cerfgms-webapi.unocha.org/"


def load_cerf_applications() -> pd.DataFrame:
    """Load all CERF applications from the API into a DataFrame."""
    url = f"{CERF_API_BASE_URL}v1/application/All.xml"
    response = requests.get(url)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    records = [
        {
            child.tag: (
                None
                if child.get("{http://www.w3.org/2001/XMLSchema-instance}nil") == "true"
                else child.text
            )
            for child in app
        }
        for app in root
    ]
    return pd.DataFrame(records)
