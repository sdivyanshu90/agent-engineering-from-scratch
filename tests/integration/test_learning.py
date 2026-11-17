import math
import unittest
from forgeagent.autograd import Value,cross_entropy
from forgeagent.learning import Example,split_examples,predict,mse,regression_step,MLP,train_xor,BigramModel
from forgeagent.math_basics import derivative,softmax


class GradientTests(unittest.TestCase):
    def test_shared_paths_and_reset(self):
        x=Value(3);a=x*x;y=a+a+x
        y.backward()
        self.assertEqual(x.grad,13)
        y.backward()
        self.assertEqual(x.grad,13)

    def test_composed_operations_against_finite_difference(self):
        cases=[(lambda x:(3*x+1)**2,lambda x:(3*x+1)**2,2),
               (lambda x:x.exp().log()+x.tanh(),lambda x:x+math.tanh(x),.7),
               (lambda x:1/x+x.relu(),lambda x:1/x+max(0,x),2)]
        for graph,numeric,value in cases:
            with self.subTest(value=value):
                x=Value(value);y=graph(x);y.backward()
                self.assertAlmostEqual(x.grad,derivative(numeric,value),places=5)
        with self.assertRaises(ValueError): Value(0).log()

    def test_stable_cross_entropy_gradient(self):
        logits=[Value(1000),Value(1001)]
        loss=cross_entropy(logits,1);loss.backward()
        probabilities=softmax([1000,1001])
        self.assertAlmostEqual(loss.data,-math.log(probabilities[1]))
        self.assertAlmostEqual(logits[0].grad,probabilities[0])
        self.assertAlmostEqual(logits[1].grad,probabilities[1]-1)
        with self.assertRaises(ValueError): cross_entropy([],0)
        with self.assertRaises(ValueError): cross_entropy(logits,-1)


class LearningTests(unittest.TestCase):
    def test_partitions_cover_once_and_do_not_mutate(self):
        rows=[Example(str(i),(i,),i) for i in range(20)]
        original=list(rows);parts=split_examples(rows)
        ids=[row.identifier for group in parts.values() for row in group]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(set(ids),{row.identifier for row in rows})
        self.assertEqual(rows,original)
        self.assertEqual(parts,split_examples(rows))
        with self.assertRaises(ValueError): split_examples(rows+[rows[0]])

    def test_regression_fit_and_gradient(self):
        xs=[-1,-.5,0,.5,1];ys=[2*x+1 for x in xs]
        w,b=0,0
        for _ in range(300): w,b=regression_step(xs,ys,w,b,.1)
        self.assertAlmostEqual(w,2,places=6)
        self.assertAlmostEqual(b,1,places=6)
        self.assertLess(mse([predict(x,w,b) for x in xs],ys),1e-10)
        with self.assertRaises(ValueError): mse([],[])

    def test_network_parameter_check_and_xor(self):
        model=MLP(seed=7)
        self.assertEqual(len(model.parameters()),17)
        parameter=model.parameters()[0]
        loss=(model([.3,.7])-.2)**2;loss.backward()
        analytic=parameter.grad
        original=parameter.data
        def objective(value):
            parameter.data=value
            return ((model([.3,.7])-.2)**2).data
        numeric=derivative(objective,original)
        parameter.data=original
        self.assertAlmostEqual(analytic,numeric,places=5)
        model,losses=train_xor()
        self.assertLess(losses[-1],losses[0])
        for x,y in [([-1,-1],-1),([-1,1],1),([1,-1],1),([1,1],-1)]:
            self.assertEqual(model(x).data>0,y>0)

    def test_bigram_likelihood_and_read_only_generation(self):
        model=BigramModel('ab').fit('abab')
        self.assertEqual(model.distribution('a'),{'a':.25,'b':.75})
        self.assertAlmostEqual(model.nll('aba'),-math.log(.5)/2)
        before={k:dict(v) for k,v in model.counts.items()}
        self.assertEqual(model.generate('a',seed=7),model.generate('a',seed=7))
        self.assertEqual(model.counts,before)
        with self.assertRaises(ValueError): model.fit('abc')
        self.assertEqual(model.counts,before)
        with self.assertRaises(ValueError): model.nll('a')
