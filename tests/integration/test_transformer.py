import math
import random
import unittest
from forgeagent.autograd import Value
from forgeagent.tokenization import learn_merges,merge_pair,encode,decode
from forgeagent.transformer import TinyDecoder,normalize,attention,sample,train_toy


class TokenizationTests(unittest.TestCase):
    def test_overlap_order_unicode_and_empty(self):
        self.assertEqual(merge_pair(list('aaa'),('a','a')),['aa','a'])
        merges=learn_merges('abab',2)
        self.assertEqual(merges,[('a','b'),('ab','ab')])
        self.assertEqual(encode('abab',merges),['abab'])
        for text in ['', ' é\n', 'unseen words!']:
            self.assertEqual(decode(encode(text,merges)),text)
        with self.assertRaises(ValueError):learn_merges('a',-1)


class DecoderTests(unittest.TestCase):
    def test_attention_values_and_shapes(self):
        result=attention([Value(1)],[[Value(0)],[Value(1)]],[[Value(2)],[Value(6)]])
        self.assertAlmostEqual(result[0].data,(2+6*math.e)/(1+math.e))
        with self.assertRaises(ValueError):attention([Value(1)],[],[])

    def test_normalization_and_residual_gradient(self):
        result=normalize([Value(1),Value(3)])
        self.assertAlmostEqual(result[0].data,-1/math.sqrt(1.00001))
        self.assertEqual([v.data for v in normalize([Value(2),Value(2)])],[0,0])
        for epsilon in [0,-1,float('inf'),float('nan')]:
            with self.assertRaises(ValueError):normalize([Value(1)],epsilon)
        x=Value(2);y=x+x*x;y.backward();self.assertEqual(x.grad,5)

    def test_full_causal_invariance_and_gradient(self):
        model=TinyDecoder(3,context=6)
        a,b=model([0,1,2]),model([0,1,0])
        for position in (0,1):
            self.assertEqual([v.data for v in a[position]],[v.data for v in b[position]])
        sum(a[0]).backward()
        self.assertTrue(all(parameter.grad==0 for parameter in model.embeddings[2]))

    def test_cached_full_equivalence_and_context_limit(self):
        model=TinyDecoder(3,context=6)
        for tokens in [[0],[1,2,0],[0,1,2,0,1,2]]:
            full=model(tokens);cache={'keys':[],'values':[]}
            for index,token in enumerate(tokens):
                cached=model.cached_step(token,cache)
                for a,b in zip(cached,full[index]):self.assertAlmostEqual(a.data,b.data,places=10)
        with self.assertRaises(ValueError):model.cached_step(0,cache)
        with self.assertRaises(ValueError):model([3])
        with self.assertRaises(ValueError):TinyDecoder(3,width=3,heads=2)

    def test_training_loss_falls_with_valid_gradients(self):
        model,history=train_toy(steps=8)
        self.assertEqual(len(model.parameters()),176)
        self.assertTrue(all(math.isfinite(loss) for loss in history))
        self.assertLess(history[-1],history[0])
        parameter=model.lm_head[0][0]
        loss=model.loss([0,1],[1,2]);loss.backward();analytic=parameter.grad
        original,h=parameter.data,1e-5
        parameter.data=original+h;plus=model.loss([0,1],[1,2]).data
        parameter.data=original-h;minus=model.loss([0,1],[1,2]).data
        parameter.data=original
        self.assertAlmostEqual(analytic,(plus-minus)/(2*h),places=5)

    def test_sampling_support_and_validation(self):
        self.assertEqual(sample([1,1],temperature=0),0)
        for seed in range(20):
            self.assertEqual(sample([0,1,2],top_k=1,rng=random.Random(seed)),2)
            self.assertEqual(sample([math.log(.1),math.log(.3),math.log(.6)],top_p=.5,rng=random.Random(seed)),2)
        for settings in [{'temperature':-1},{'top_k':0},{'top_p':0},{'temperature':float('nan')}]:
            with self.assertRaises(ValueError):sample([0,1],**settings)
