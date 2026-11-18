def route(task, confidence):
    if not isinstance(task,str) or type(confidence) not in (int,float) or not 0<=confidence<=1: raise ValueError('invalid task or confidence')
    if confidence < .6: return {'mode':'review','state':'REVIEW'}
    if task.startswith('fixed:'): return {'mode':'workflow','state':'PARSE'}
    return {'mode':'agent','state':'DECIDE'}
