import json
from os import path

def load_stats_data(stats_path):
    with open(stats_path, 'r') as f:
        stats_data = json.load(f)
    return stats_data
