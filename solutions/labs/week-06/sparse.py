from forgeagent.retrieval import BM25


def rank(query,chunks,k=5,k1=1.2,b=.75):
    return BM25(chunks,k1=k1,b=b).search(query,k)
