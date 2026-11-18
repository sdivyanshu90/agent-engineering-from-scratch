def repair_is_verified(events):
    if not isinstance(events,list): return False
    kinds=[e.get("event") for e in events if isinstance(e,dict)]
    try:
        pi=kinds.index("patch_proposed")
        ai=kinds.index("patch_approved",pi+1)
        wi=kinds.index("patch_applied",ai+1)
        ti=kinds.index("tests_end",wi+1)
    except ValueError: return False
    try: proposal,approval,write,test=(events[i] for i in (pi,ai,wi,ti))
    except (IndexError,TypeError): return False
    pid=proposal.get("proposal_id")
    return (bool(pid) and approval.get("approved") is True
        and approval.get("proposal_id")==pid==write.get("proposal_id")
        and proposal.get("review_sha256")==approval.get("review_sha256")
        and proposal.get("after_sha256")==write.get("revision")==test.get("revision")
        and test.get("status")=="passed")
