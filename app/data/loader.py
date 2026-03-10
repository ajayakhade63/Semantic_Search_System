from sklearn.datasets import fetch_20newsgroups
import pandas as pd

def load_dataset():

    newsgroups = fetch_20newsgroups(
        subset="all",
        remove=("headers", "footers", "quotes")
    )

    texts = newsgroups.data
    labels = newsgroups.target
    categories = newsgroups.target_names

    df = pd.DataFrame({
        "text": texts,
        "label": labels
    })

    return df, categories
