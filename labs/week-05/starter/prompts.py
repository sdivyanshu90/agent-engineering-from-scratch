from forgeagent.models import Message,Request


def prompt(source,model,version='v1'):
    return Request(model,(Message('user',source),),256,version)


def fingerprint(request):
    return 'baseline'
