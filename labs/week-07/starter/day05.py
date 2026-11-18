"""Lab 5: reconcile completed usage against a bounded token budget."""
def reconcile(used, reported, limit):
    if any(type(n) is not int or n<0 for n in (used,reported,limit)):
        raise ValueError('nonnegative integer counts required')
    # TODO: charge completed usage and prevent another action after overshoot.
    total=used+reported
    return {'used':total,'may_continue':total < limit}
