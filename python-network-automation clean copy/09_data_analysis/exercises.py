"""
Python Network Automation - Data Analysis Exercises
"""

from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In production: import numpy as np, pandas as pd, matplotlib.pyplot as plt


def calculate_average_latency(latencies: List[float]) -> float:
    """Calculate average latency using NumPy."""
    # TODO: Use np.array() and np.mean()
    # return np.mean(np.array(latencies))
    pass


def load_telemetry_csv(csv_file: str):
    """Load telemetry data from CSV using Pandas."""
    # TODO: Use pd.read_csv()
    # return pd.read_csv(csv_file)
    pass


def aggregate_metrics_by_device(df, device_col: str, metric_col: str):
    """Aggregate metrics by device using Pandas groupby."""
    # TODO: Use df.groupby(device_col)[metric_col].mean()
    pass


if __name__ == "__main__":
    print("Data Analysis Exercises")
