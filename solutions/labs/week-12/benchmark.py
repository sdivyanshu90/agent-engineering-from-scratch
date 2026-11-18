def summarize(cases,split):
    if split not in {"dev","heldout"}: raise ValueError("unknown split")
    rows=[row for row in cases if row.get("split")==split]
    if not rows: raise ValueError("split must have fixed nonempty cases")
    ids=[r.get("id") for r in rows]
    if any(not isinstance(i,str) or not i for i in ids) or len(set(ids))!=len(ids):
        raise ValueError("case IDs must be unique")
    solved=sum(row.get("solved") is True for row in rows)
    return {"split":split,"denominator":len(rows),"solved":solved,
            "rate":solved/len(rows),"cases":[{"id":r["id"],"solved":r.get("solved") is True,
                "status":r.get("status","unknown")} for r in rows]}
