"""Deterministic toy BPE over Unicode characters; not provider token counting."""
from collections import Counter


def merge_pair(symbols, pair):
    output=[]
    i=0
    while i < len(symbols):
        if i+1 < len(symbols) and (symbols[i],symbols[i+1]) == pair:
            output.append(symbols[i]+symbols[i+1])
            i+=2
        else:
            output.append(symbols[i])
            i+=1
    return output


def learn_merges(text, steps=2):
    if type(steps) is not int or steps < 0:
        raise ValueError("nonnegative integer steps required")
    symbols,merges=list(text),[]
    for _ in range(steps):
        counts=Counter(zip(symbols,symbols[1:]))
        if not counts: break
        pair=min(counts,key=lambda pair:(-counts[pair],pair))
        symbols=merge_pair(symbols,pair)
        merges.append(pair)
    return merges


def encode(text, merges):
    symbols=list(text)
    for pair in merges:
        symbols=merge_pair(symbols,pair)
    return symbols


def decode(symbols):
    return "".join(symbols)
