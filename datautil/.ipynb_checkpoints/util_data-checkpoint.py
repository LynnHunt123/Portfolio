import pandas as pd
import numpy as np

def scale(series, method = "standard"):
    if method == "standard":
        return (series - np.mean(series)) / np.std(series)
    elif method == "minmax":
        return (series - np.max(series)) / (np.max(series) - np.min(series))