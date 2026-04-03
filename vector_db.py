from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

class QdrantStorage: 
    def __init__(self, url="http://localhost:6333", collection="docs", dim="3072"): 
        self.client=QdrantClient(url=url, timeout=30)
        self.collection=collection
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

# dimensions is essentially numebr of values we have inside of a vector and we are turnign text docs into a vector and compare them using this distance formyla and vectors that are closer to each other in this vector space have similarity, so essentially we are going to find relevant data by similarity and then send that to out llm

# upsert: insert+update
# payload is human readable data that we have vectorised
# we convert all three things into a pointStruct which is required by qdrant and insert that pointstruct into vector database

    def upsert(self, ids, vectors, payloads):
        points = [PointStruct(ids=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(id))]
        self.client.upsert(self.collection, points=points)

    def search(self, query_vector, top_k: int = 5):

        # search database on the basis of query vector and store results 
        results = self.client.search(
            collection_name = self.collection,
            query_vector=query_vector,
            with_payload=True,

            limit=top_k,
            # just means, give me top 5 resutls
        )
        contexts = []

        # if we wan we can make sources an array too, so we dont lose info about which context is associated with which source, but here we prefer not having duplicate sources so we make it a set.
        sources = set() 
        # because we dont want to keep adding same source again and again

        # destructure results and add to contexts and sources that will be returned 
        for r in results:
            payload = getattr(r, "payload", None) or {}
            text = payload.get("text", "")
            source = payload.get("source", "")

            if (text):
                contexts.append(text)
                sources.add(source)

        return { "contexts": contexts, "sources": list(sources)}