from forgeagent.learning import affine


def project(embedding,position,wq,wk,wv):
    if not embedding or len(embedding)!=len(position) or len(wq)!=len(wk):
        raise ValueError("content/position widths and query/key widths must match")
    hidden=[a+b for a,b in zip(embedding,position)]
    return tuple(affine(hidden,weights,[0]*len(weights)) for weights in (wq,wk,wv))
