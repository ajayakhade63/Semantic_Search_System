import numpy as np
import skfuzzy as fuzz


class FuzzyCluster:

    def __init__(self, n_clusters=20):

        self.n_clusters = n_clusters
        self.centers = None
        self.membership = None

    def fit(self, embeddings):

        data = np.array(embeddings).T

        centers, membership, _, _, _, _, _ = fuzz.cluster.cmeans(
            data,
            self.n_clusters,
            m=2,
            error=0.005,
            maxiter=1000
        )

        self.centers = centers
        self.membership = membership

        return centers, membership

    def get_document_distribution(self, doc_index):

        return self.membership[:, doc_index]