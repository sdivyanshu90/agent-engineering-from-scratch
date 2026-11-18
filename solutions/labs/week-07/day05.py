def reconcile(used,reported,limit):
    if any(type(n) is not int or n<0 for n in (used,reported,limit)) or limit<1: raise ValueError('invalid budget')
    total=used+reported
    return {'used':total,'overshot':total>limit,'may_continue':total<limit}
