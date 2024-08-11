import json
from typing import List, Dict

import pandas as pd
import requests


class DataLoader:
    def __init__(self, url: str):
        self.url = url

    def load_data(self) -> List[Dict]:
        """
        Fetches the JSONL data from the provided URL and loads it into a list of dictionaries.
        """
        response = requests.get(self.url)
        data = [json.loads(line) for line in response.text.strip().split('\n')]
        return data

    def get_dataframe(self) -> pd.DataFrame:
        """
        Converts the loaded data into a Pandas DataFrame.
        """
        data = self.load_data()
        df = pd.json_normalize(data)
        return df
