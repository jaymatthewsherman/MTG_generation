import torch
import pandas as pd
from io import StringIO


class CardDataset(torch.utils.data.Dataset):
    def __init__(self, content, tokenizer):
        self.cards = []
        if isinstance(content, str):
            with open(content, "r", encoding="utf-8") as file:
                self.cards = list([line.strip() for line in file.readlines()])
                file.close()
        elif isinstance(content, pd.DataFrame):
            self.cards = self.convert_df_to_strs(content)
        else:
            assert False, "content is not a str or pd.DataFrame"
        self.tokenizer = tokenizer

    def convert_df_to_strs(self, df):
        if 'name' in df.columns:
            df = df.drop('name', axis=0)
        buffer = StringIO()
        df.to_csv(buffer, index=False, header=False, sep=" ")
        buffer.seek(0)
        return [line.strip() for line in buffer.readlines()]

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, idx):
        return torch.tensor(self.tokenizer.encode(self.cards[idx]).ids)