import re

def clean_text(text):

    text = text.lower()

    text = re.sub(r'\n', ' ', text)

    text = re.sub(r'\s+', ' ', text)

    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    return text.strip()


def preprocess_documents(documents):

    cleaned_docs = []

    for doc in documents:
        cleaned_docs.append(clean_text(doc))

    return cleaned_docs
