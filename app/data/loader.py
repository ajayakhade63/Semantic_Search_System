import os

def load_dataset(data_dir="dataset/20_newsgroups"):

    documents = []
    labels = []

    categories = os.listdir(data_dir)

    for category in categories:

        category_path = os.path.join(data_dir, category)

        if not os.path.isdir(category_path):
            continue

        for file in os.listdir(category_path):

            file_path = os.path.join(category_path, file)

            try:
                with open(file_path, "r", encoding="latin1") as f:
                    text = f.read()
                    documents.append(text)
                    labels.append(category)
            except:
                continue

    return documents, labels
