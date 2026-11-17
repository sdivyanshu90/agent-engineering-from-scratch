import asyncio
from dataclasses import asdict
import json
import math
from pathlib import Path
import unittest
from forgeagent.retrieval import chunk_text,BM25,Tfidf,DenseIndex,Scored,fuse,rerank
from forgeagent.grounding import ranking_metrics,Citation,verify_citation,extract_answer,parse_grounded,grounded_generate,benchmark
from forgeagent.llm_app import parse_classification
from forgeagent.models import FakeProvider,Reply,Usage

ROOT=Path(__file__).resolve().parents[2]


class RetrievalTests(unittest.TestCase):
    def test_chunk_spans_revision_and_invalid_stride(self):
        text='a\nb\nc\nd\ne\n'
        chunks=chunk_text('p',text,lines=3,overlap=1)
        self.assertEqual([(c.start_line,c.end_line) for c in chunks],[(1,3),(3,5)])
        self.assertEqual(chunks[0].text,'a\nb\nc\n')
        self.assertEqual(chunks,chunk_text('p',text,lines=3,overlap=1))
        self.assertNotEqual(chunks[0].revision,chunk_text('p',text+'f')[0].revision)
        self.assertEqual(chunk_text('p',''),[])
        for lines,overlap in [(0,0),(3,3),(3,-1),(True,0)]:
            with self.assertRaises(ValueError):chunk_text('p',text,lines=lines,overlap=overlap)

    def test_bm25_statistics_and_unknown_query(self):
        chunks=chunk_text('a','agent agent')+chunk_text('b','tests tests')
        index=BM25(chunks);result=index.search('AGENT',1)
        self.assertAlmostEqual(result[0].score,math.log(2)*1.375)
        self.assertEqual(index.search('agent agent'),index.search('agent'))
        self.assertEqual(index.search('unknown'),[])
        self.assertEqual(BM25([]).search('agent'),[])
        self.assertEqual(BM25(chunk_text('blank','   ')).search('agent'),[])
        with self.assertRaises(ValueError):BM25(chunks+[chunks[0]])
        with self.assertRaises(ValueError):index.search('agent',True)
        with self.assertRaises(ValueError):BM25(chunks,b=2)

    def test_tfidf_vocabulary_and_dense_lexical_search(self):
        chunks=chunk_text('a','agent agent')+chunk_text('b','tests tests')
        encoder=Tfidf(chunks)
        self.assertEqual(encoder.vocabulary,['agent','tests'])
        index=DenseIndex(encoder.vectors)
        self.assertEqual(index.search(encoder.encode('agent'),1)[0].identifier,chunks[0].identifier)
        with self.assertRaises(ValueError):index.search(encoder.encode('unknown'))

    def test_approximation_loss_and_vector_domains(self):
        index=DenseIndex({'near':[-.01,1],'far':[1,0]})
        self.assertEqual(index.search([.01,1],1)[0].identifier,'near')
        self.assertEqual(index.search([.01,1],1,approximate=True)[0].identifier,'far')
        for vectors in [{'x':[0,0]},{'x':[1,2],'y':[1]},{'x':[float('nan'),1]}]:
            with self.assertRaises(ValueError):DenseIndex(vectors)
        self.assertEqual(DenseIndex({}).search([1]),[])

    def test_fusion_rerank_and_duplicate_policy(self):
        fused=fuse([['x','y'],['y','z']],k=3)
        self.assertEqual([r.identifier for r in fused],['y','x','z'])
        self.assertAlmostEqual(fused[0].score,1/61+1/62)
        with self.assertRaises(ValueError):fuse([['x','x']])
        chunks=chunk_text('a','test')+chunk_text('b','test timeout')
        candidates=[Scored(c.identifier,1) for c in chunks]
        self.assertEqual(rerank('test timeout',candidates,chunks)[0].identifier,chunks[1].identifier)

    def test_metric_conventions_and_empty_cases(self):
        result=ranking_metrics(['b','x','a'],{'a':2,'b':1},3)
        self.assertAlmostEqual(result['precision'],2/3)
        self.assertEqual(result['recall'],1)
        self.assertAlmostEqual(result['ndcg'],2.5/(3+1/math.log2(3)))
        self.assertEqual(ranking_metrics(['a'],{'a':1},3)['precision'],1/3)
        self.assertEqual(ranking_metrics([],{},1),{'precision':0,'recall':0,'rr':0,'ndcg':0})
        with self.assertRaises(ValueError):ranking_metrics(['a','a'],{'a':1})
        with self.assertRaises(ValueError):ranking_metrics([],{'a':-1})

    def test_grounded_quotes_and_stale_or_unselected_evidence(self):
        chunks=chunk_text('p','Evidence.');chunk=chunks[0]
        citation=Citation(chunk.identifier,chunk.revision,'Evidence.')
        self.assertTrue(verify_citation(citation,chunks))
        self.assertFalse(verify_citation(Citation(chunk.identifier,'old','Evidence.'),chunks))
        value={'answer':'Evidence.','citations':[asdict(citation)]}
        self.assertFalse(parse_grounded(json.dumps(value),chunks).abstained)
        for change in [{'answer':'Evidence. Extra claim.'},{'citations':[dict(asdict(citation),quote='invented')]},
                       {'citations':[dict(asdict(citation),chunk_id='other')]},{'citations':[]}]:
            with self.assertRaises(ValueError):parse_grounded(json.dumps(dict(value,**change)),chunks)
        self.assertFalse(verify_citation(citation,chunk_text('p','Evidence.\nNew revision')))
        index=BM25(chunks)
        self.assertFalse(extract_answer('evidence',index).abstained)
        self.assertTrue(extract_answer('unseen',index).abstained)
        for parser in [lambda text:parse_grounded(text,chunks),parse_classification]:
            with self.assertRaises(ValueError):parser('['*1200+']'*1200)

    def test_fixed_visible_benchmark_and_denominator(self):
        fixture=json.loads((ROOT/'datasets/evaluation-fixtures/retrieval.json').read_text())
        report=benchmark(fixture)
        self.assertEqual(len(report['cases']),4)
        self.assertEqual(report['mean_rr'],.75)
        self.assertTrue(all(row['citation_valid'] and row['abstention_correct'] for row in report['cases']))
        self.assertEqual(report['cases'][-1]['recall'],0)


class ModelGroundingTests(unittest.IsolatedAsyncioTestCase):
    async def test_fake_quote_selection_and_no_evidence_skips_model(self):
        chunks=chunk_text('p','Evidence supports the test.');chunk=chunks[0]
        text=json.dumps({'answer':chunk.text,'citations':[{'chunk_id':chunk.identifier,'revision':chunk.revision,'quote':chunk.text}]})
        provider=FakeProvider([Reply(text,Usage(5,5))])
        result=await grounded_generate('evidence test',BM25(chunks),provider)
        self.assertFalse(result.abstained)
        self.assertEqual(provider.requests[0].messages[0].role,'developer')
        result=await grounded_generate('absentterm',BM25(chunks),provider)
        self.assertTrue(result.abstained);self.assertEqual(len(provider.requests),1)
