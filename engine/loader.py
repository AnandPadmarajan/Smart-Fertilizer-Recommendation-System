import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load_crop_requirements():
    path = os.path.join(DATA_DIR, "crop_requirements.csv")
    return pd.read_csv(path)

def load_soil_thresholds():
    path = os.path.join(DATA_DIR, "soil_thresholds.csv")
    return pd.read_csv(path)

def load_fertilizer_content():
    path = os.path.join(DATA_DIR, "fertilizer_content.csv")
    return pd.read_csv(path)