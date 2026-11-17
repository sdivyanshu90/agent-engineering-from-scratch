from forgeagent.retrieval import DenseIndex


def nearest(vectors,query,k=5,approximate=False):
    return DenseIndex(vectors).search(query,k,approximate=approximate)
