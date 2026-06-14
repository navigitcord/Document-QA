import faiss
import numpy as np


class FAISSVectorStore:

    def __init__(self):

        self.index = None

        self.chunks = []

    def create_index(self, embedded_chunks):

        self.chunks = embedded_chunks

        vectors = np.array(
            [chunk["embedding"] for chunk in embedded_chunks],
            dtype=np.float32
        )

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(vectors)

        print(
            f"Indexed {len(embedded_chunks)} chunks"
        )

    def search(self, query_embedding, top_k=5):

        query_vector = np.array(
            [query_embedding],
            dtype=np.float32
        )

        distances, indices = self.index.search(
            query_vector,
            top_k
        )

        results = []

        for idx, distance in zip(
            indices[0],
            distances[0]
        ):

            if idx != -1:

                chunk = self.chunks[idx].copy()

                chunk["score"] = float(distance)

                results.append(chunk)

        return results