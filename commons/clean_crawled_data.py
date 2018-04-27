import os
import shutil


def clean_up_data():
    """Clean up data folder for writing new crawled data"""
    if os.path.exists("data"):
        shutil.rmtree("data")