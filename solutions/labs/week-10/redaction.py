SAFE={'event','status','seconds','step'}
def redact(event):return {key:value for key,value in event.items() if key in SAFE}
