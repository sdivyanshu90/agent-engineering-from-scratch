from forgeagent.retrieval import chunk_text


def split_document(path,text,lines=8,overlap=1):
    return chunk_text(path,text,lines=lines,overlap=overlap)
