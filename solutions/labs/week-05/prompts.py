from forgeagent.llm_app import build_request as prompt


def fingerprint(request):
    return request.fingerprint()
