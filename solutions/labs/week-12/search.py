import re

def search_sources(sources, query, limit=5):
    if not isinstance(sources,dict) or type(limit) is not int or not 1<=limit<=20:
        raise ValueError("bounded mapping and positive limit required")
    terms=set(re.findall(r"[a-z0-9_]+",query.casefold()))
    if not terms: raise ValueError("searchable query required")
    results=[]
    for path,text in sources.items():
        if not isinstance(path,str) or not isinstance(text,str): raise ValueError("text mapping required")
        rows=text.splitlines()
        matched=[]
        for number,row in enumerate(rows,1):
            tokens=set(re.findall(r"[a-z0-9_]+",row.casefold()))
            score=len(terms & tokens)
            if score: matched.append((number,score,row[:240]))
        if matched:
            results.append({"path":path,"score":sum(x[1] for x in matched),"line":matched[0][0],"snippet":matched[0][2]})
    return sorted(results,key=lambda x:(-x["score"],x["path"]))[:limit]
