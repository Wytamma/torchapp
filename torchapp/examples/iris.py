#!/usr/bin/env python3

from pathlib import Path
import numpy as np
from torch.utils.data import random_split, DataLoader, Dataset
from sklearn.datasets import load_iris
from torch import nn
import torchapp as ta
import torch
from torchmetrics import Metric, Accuracy
import lightning as L

class IrisDataset(Dataset):
    def __init__(self, df):
        self.df = df

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        x = torch.tensor(row[['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']].values, dtype=torch.float32)
        y = torch.tensor(row['target'], dtype=int)
        return x, y
    

class IrisApp(ta.TorchApp):
    """
    A classification app to predict the type of iris from sepal and petal lengths and widths.

    A classic dataset publised in:
        Fisher, R.A. “The Use of Multiple Measurements in Taxonomic Problems” Annals of Eugenics, 7, Part II, 179–188 (1936).
    For more information about the dataset, see:
        https://scikit-learn.org/stable/datasets/toy_dataset.html#iris-plants-dataset
    """
    @ta.method
    def data(self, validation_fraction: float = 0.2, batch_size: int = 32):
        iris_data = load_iris(as_frame=True)
        df = iris_data['frame']
        validation_df = df.sample(frac=validation_fraction)
        train_df = df.drop(validation_df.index)
        train_dataset = IrisDataset(train_df)
        val_dataset = IrisDataset(validation_df)
        data_module = L.LightningDataModule()
        data_module.train_dataloader = lambda: DataLoader(train_dataset, batch_size=batch_size)
        data_module.val_dataloader = lambda: DataLoader(val_dataset, batch_size=batch_size)
        return data_module

    # @ta.method
    # def metrics(self) -> list[Metric]:
    #     return [Accuracy()]

    @ta.method
    def model(self):
        return nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 3),
        )

    @ta.method
    def loss_function(self):
        return nn.CrossEntropyLoss()

    @ta.method
    def get_bibtex_files(self):
        files = super().get_bibtex_files()
        files.append(Path(__file__).parent / "iris.bib")
        return files


if __name__ == "__main__":
    IrisApp.tools()
