"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from typing import List, Dict, Any
import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_average_latency(latencies: List[float]) -> float:
    """Calculate average latency using NumPy."""
    return float(np.mean(np.array(latencies)))


def load_telemetry_csv(csv_file: str) -> pd.DataFrame:
    """Load telemetry data from CSV using Pandas."""
    return pd.read_csv(csv_file)


def aggregate_metrics_by_device(df: pd.DataFrame, device_col: str, metric_col: str):
    """Aggregate metrics by device using Pandas groupby."""
    return df.groupby(device_col)[metric_col].mean()


if __name__ == "__main__":
    print("09_data_analysis – answer key (run exercises.py to practice)")
