"""Week 6 transparent retrieval mechanisms; no model or vector service required."""
from collections import Counter,defaultdict
from dataclasses import dataclass
import hashlib
import math
from .documents import tokenize


@dataclass(frozen=True)
class Chunk:
    identifier: str
    path: str
    revision: str
    start_line: int
    end_line: int
    text: str


@dataclass(frozen=True)
class Scored:
    identifier: str
    score: float


def chunk_text(path,text,*,lines=8,overlap=1):
    if type(lines) is not int or lines<1 or type(overlap) is not int or not 0<=overlap<lines:
        raise ValueError('require positive window and 0<=overlap<window')
    revision=hashlib.sha256(text.encode()).hexdigest()
    rows=text.splitlines(keepends=True)
    output=[]
    for start in range(0,len(rows),lines-overlap):
        stop=min(start+lines,len(rows))
        key=hashlib.sha256(f'{path}\0{revision}\0{start+1}:{stop}'.encode()).hexdigest()
        output.append(Chunk(key,path,revision,start+1,stop,''.join(rows[start:stop])))
        if stop==len(rows):break
    return output


def _limit(k):
    if type(k) is not int or k<0:raise ValueError('nonnegative integer limit required')


class BM25:
    def __init__(self,chunks,*,k1=1.2,b=.75):
        if not math.isfinite(k1) or k1<=0 or not math.isfinite(b) or not 0<=b<=1:raise ValueError('BM25 parameters')
        self.chunks={chunk.identifier:chunk for chunk in chunks}
        if len(self.chunks)!=len(chunks):raise ValueError('duplicate chunk identifiers')
        self.k1,self.b=k1,b
        self.lengths={};self.postings=defaultdict(dict)
        for chunk in chunks:
            counts=Counter(tokenize(chunk.text));self.lengths[chunk.identifier]=sum(counts.values())
            for term,count in counts.items():self.postings[term][chunk.identifier]=count
        self.average=sum(self.lengths.values())/len(chunks) if chunks else 0

    def search(self,query,k=5):
        _limit(k);scores=defaultdict(float);n=len(self.chunks)
        for term in sorted(set(tokenize(query))):
            posting=self.postings.get(term,{})
            if not posting:continue
            idf=math.log1p((n-len(posting)+.5)/(len(posting)+.5))
            for key,count in posting.items():
                length=self.lengths[key]
                denominator=count+self.k1*(1-self.b+self.b*length/self.average)
                scores[key]+=idf*count*(self.k1+1)/denominator
        return [Scored(key,score) for key,score in sorted(scores.items(),key=lambda item:(-item[1],item[0]))[:k]]


class Tfidf:
    """Sparse term representation exposed as dense lists for arithmetic comparison.

    This is lexical TF-IDF, not a pretrained semantic embedding model.
    """
    def __init__(self,chunks):
        self.counts=[Counter(tokenize(chunk.text)) for chunk in chunks]
        self.vocabulary=sorted({term for counts in self.counts for term in counts})
        n=len(chunks)
        self.idf={term:math.log((n+1)/(sum(term in counts for counts in self.counts)+1))+1 for term in self.vocabulary}
        self.vectors={chunk.identifier:self.encode(chunk.text) for chunk in chunks}
    def encode(self,text):
        counts=Counter(tokenize(text));length=sum(counts.values()) or 1
        return [counts[term]/length*self.idf[term] for term in self.vocabulary]


class DenseIndex:
    """Exact cosine scan over supplied finite vectors; no learned model implied."""
    def __init__(self,vectors):
        self.vectors={key:tuple(vector) for key,vector in vectors.items()}
        self.width=len(next(iter(self.vectors.values()))) if self.vectors else 0
        for vector in self.vectors.values():self._validate(vector)
    def _validate(self,vector):
        if not vector or len(vector)!=self.width or any(not math.isfinite(v) for v in vector) or not any(vector):
            raise ValueError('equal-width finite nonzero vectors required')
    def search(self,query,k=5,*,approximate=False):
        _limit(k)
        if not self.vectors:return []
        self._validate(query)
        qnorm=math.sqrt(math.fsum(v*v for v in query));scores=[]
        for key,vector in self.vectors.items():
            # Deliberately crude sign bucket, to demonstrate ANN candidate loss.
            if approximate and (vector[0]>=0)!=(query[0]>=0):continue
            denominator=qnorm*math.sqrt(math.fsum(v*v for v in vector))
            scores.append(Scored(key,math.fsum(a*b for a,b in zip(query,vector))/denominator))
        return sorted(scores,key=lambda item:(-item.score,item.identifier))[:k]


def fuse(rankings,*,constant=60,k=5):
    _limit(k)
    if not math.isfinite(constant) or constant<=0:raise ValueError('positive finite RRF constant required')
    scores=defaultdict(float)
    for ranking in rankings:
        seen=set()
        for rank,item in enumerate(ranking,1):
            key=item.identifier if isinstance(item,Scored) else item
            if key in seen:raise ValueError('duplicate identifier inside one ranking')
            seen.add(key);scores[key]+=1/(constant+rank)
    return [Scored(key,score) for key,score in sorted(scores.items(),key=lambda item:(-item[1],item[0]))[:k]]


def rerank(query,ranking,chunks):
    """Transparent lexical-coverage reranker, not a learned cross-encoder."""
    terms=set(tokenize(query))
    if not terms:return []
    mapped={chunk.identifier:chunk for chunk in chunks}
    scores=[Scored(item.identifier,len(terms & set(tokenize(mapped[item.identifier].text)))/len(terms)) for item in ranking]
    return sorted(scores,key=lambda item:(-item.score,item.identifier))
