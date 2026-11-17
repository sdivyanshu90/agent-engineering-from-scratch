import asyncio
import math
import unittest

from forgeagent.async_ops import retry, TransientError
from forgeagent.math_basics import cosine, derivative, descend_square, dot, matvec, softmax


class RecoveryTests(unittest.IsolatedAsyncioTestCase):
    async def test_transient_exhaustion_and_delays(self):
        calls, delays = [], []
        async def operation():
            calls.append(1)
            raise TransientError("last")
        async def sleep(seconds):
            delays.append(seconds)
        with self.assertRaisesRegex(TransientError, "last"):
            await retry(operation, attempts=3, base_delay=0.1, sleep=sleep)
        self.assertEqual(len(calls), 3)
        self.assertEqual(delays, [0.1, 0.2])

    async def test_permanent_failure_not_retried(self):
        calls = []
        async def operation():
            calls.append(1)
            raise ValueError("permanent")
        with self.assertRaises(ValueError):
            await retry(operation)
        self.assertEqual(len(calls), 1)

    async def test_timeout_and_cancellation_cleanup(self):
        started = asyncio.Event()
        clean = asyncio.Event()
        calls = []
        async def operation():
            calls.append(1)
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                clean.set()
        with self.assertRaises(TimeoutError):
            await retry(operation, timeout=0.02)
        self.assertEqual(len(calls), 1)
        self.assertTrue(clean.is_set())
        started.clear()
        clean.clear()
        task = asyncio.create_task(retry(operation, timeout=10))
        await asyncio.wait_for(started.wait(), 1)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(clean.is_set())
        self.assertEqual(len(calls), 2)

    async def test_bad_configuration(self):
        async def operation():
            return 1
        for config in [{"attempts":0}, {"attempts":True}, {"timeout":0}, {"timeout":float("inf")}, {"base_delay":-1}]:
            with self.subTest(config=config), self.assertRaises(ValueError):
                await retry(operation, **config)

    async def test_taskgroup_cleans_failed_sibling(self):
        import importlib.util
        from pathlib import Path
        path = Path(__file__).resolve().parents[2] / "solutions/labs/week-02/concurrent.py"
        spec = importlib.util.spec_from_file_location("collector_reference", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        started, clean = asyncio.Event(), asyncio.Event()
        async def waits():
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                clean.set()
        async def fails():
            await started.wait()
            raise ValueError("fault")
        with self.assertRaises(ExceptionGroup):
            await module.collect([waits, fails])
        self.assertTrue(clean.is_set())


class MathematicalTests(unittest.TestCase):
    def test_vector_geometry_and_shapes(self):
        self.assertEqual(dot([1, 2], [3, 4]), 11)
        self.assertAlmostEqual(cosine([1, 0], [0, 1]), 0)
        self.assertAlmostEqual(cosine([1, 0], [-1, 0]), -1)
        self.assertAlmostEqual(cosine([3, 4], [0, 50]), 0.8)
        self.assertEqual(matvec([[1, 2], [3, 4]], [2, 1]), [4, 10])
        for operation in [lambda: dot([], []), lambda: dot([1], [1, 2]),
                          lambda: cosine([0], [1]), lambda: matvec([[1], [1, 2]], [1])]:
            with self.assertRaises(ValueError):
                operation()

    def test_softmax_translation_and_known_probabilities(self):
        expected = [1/3, 2/3]
        for shift in [0, 100, 1000]:
            actual = softmax([shift, shift + math.log(2)])
            for a, b in zip(actual, expected):
                self.assertAlmostEqual(a, b)
            self.assertAlmostEqual(sum(actual), 1)
        self.assertEqual(softmax([0]), [1])
        for invalid in [[], [float("inf")], [float("nan")]]:
            with self.assertRaises(ValueError):
                softmax(invalid)

    def test_derivative_chain_rule_and_descent(self):
        self.assertAlmostEqual(derivative(lambda x: (3*x+1)**2, 2), 42, places=5)
        history = descend_square(2, steps=20)
        self.assertEqual(len(history), 21)
        self.assertTrue(all(abs(b) < abs(a) for a, b in zip(history, history[1:])))
        self.assertEqual(descend_square(2, steps=0), [2])
        for rate in [0, -1, 1, 1.1]:
            with self.assertRaises(ValueError):
                descend_square(2, learning_rate=rate)
        with self.assertRaises(ValueError):
            derivative(lambda x: x, 2, h=0)
