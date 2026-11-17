from forgeagent.retrieval import fuse


def combine(rankings,constant=60,k=5):
    return fuse(rankings,constant=constant,k=k)
