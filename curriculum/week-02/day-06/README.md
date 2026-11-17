# Day 12 — Derivatives, logarithms, softmax, and optimization

## 1. Learning objectives

Interpret a derivative as local change, derive simple derivatives from finite
differences, apply the chain rule, and take measured gradient-descent steps.
Explain exponents/logarithms, derive stable softmax, and distinguish normalized
scores from calibrated belief. Required competency: Level 3 implementation and
Level 2 step-by-step mathematical understanding.

## 2. Required prerequisites

[Day 11](../day-05/README.md): vectors, probability, sums, and shape contracts.
[Week 1 / Day 2](../../week-01/day-02/README.md): loops and termination.
A function maps an input to an output; this mathematical use matches Python
functions without implying every Python function is differentiable. Fractions
mean division, x² means x×x, and x⁻¹ means 1/x for nonzero x. If these operations
are unfamiliar, work numeric examples before following symbolic derivations.

## 3. Problem motivation

Machine learning changes parameters to reduce a numerical error. Randomly
changing every parameter can be expensive and directionless. A derivative tells
how a small parameter change affects an output. Neural networks compose many
functions, so we need a way to combine their local rates of change. Models also
produce arbitrary scores, while language-model prediction needs a normalized
categorical distribution. Exponents and logs connect those two representations.

## 4. Intuitive explanation

Walking on a hill, the slope tells whether a small step raises or lowers your
height. Gradient descent takes a controlled step downhill in error, not necessarily
to the best point in one move. Too large a step overshoots. A logarithm answers
“what exponent produced this value?” Softmax turns scores into positive weights
and divides by their sum. It emphasizes differences while preserving order;
it does not check whether the underlying scores reflect truth.

## 5. Deep technical explanation

For a scalar function f, the derivative at x is the limit of
(f(x+h)−f(x))/h as nonzero h approaches zero, if the limit exists. A finite
central difference (f(x+h)−f(x−h))/(2h) approximates it. Very large h is not local;
very small h can amplify floating-point cancellation. A numerical check must
compare several reasonable h values, not treat the smallest as automatically best.

For f(x)=x², expand (x+h)²=x²+2xh+h². Subtract x², divide by h, and take h→0:
f′(x)=2x. For g(x)=3x+1, the change is 3h, so g′(x)=3. If y=f(g(x)), a small
change dx first changes g by approximately g′(x)dx, then f by approximately
f′(g(x)) times that change. Thus dy/dx=f′(g(x))g′(x). This is the chain rule.
For y=(3x+1)², derivative is 2(3x+1)×3. At x=2 it is 42. Forgetting the factor
3 is a common backpropagation mistake; a numerical derivative can expose it.

With several parameters θ₁,…,θₙ, a partial derivative changes one coordinate
while holding others fixed. The vector of those rates is the gradient ∇L.
Gradient descent uses θ_new=θ_old−η∇L, where η>0 is the learning rate. For a
smooth function and sufficiently small step it follows local descent; it is
not a universal global-minimum guarantee. At a nondifferentiable corner or a
saddle, more care is needed. Today we optimize a convex square with one parameter;
Week 3 will connect losses to datasets and generalization.

Exponential eˣ uses base e≈2.71828 and is positive for finite real x. The natural
log ln is its inverse on positive values: ln(eˣ)=x and e^(ln a)=a for a>0.
Products become sums: ln(ab)=ln a+ln b. Logs turn a product of many probabilities
into a sum and negative log makes unlikely target events have larger penalties.
For target probability p, −ln(p) is 0 at p=1 and increases without bound as
p approaches 0 from above. A probability zero cannot be logged as a finite
number; numerical handling must preserve that meaning rather than silently
pretend perfect confidence was harmless.

Softmax for finite scores z₁,…,zₙ is pᵢ=e^(zᵢ)/Σⱼe^(zⱼ). Every weight is positive
in exact arithmetic and the sum is 1. Direct exponentiation can overflow.
Subtract a shared maximum m before exponentiating. Since each numerator and
denominator has the same factor e^(−m), the ratio is unchanged. The largest
shifted exponent is zero, so its weight is 1 and the denominator cannot be
zero. Very negative differences can underflow to zero in floating-point arithmetic;
for log probabilities later use log-sum-exp rather than log of a rounded zero.

## 6. Mathematical foundations

At x=2, f(x)=x² is 4. With h=0.1, central difference is
(2.1²−1.9²)/0.2=(4.41−3.61)/0.2=4. This equality is special to the quadratic
under exact arithmetic, not evidence finite differences are exact for all functions.
The analytic derivative is also 2×2=4.

For L(x)=x² and η=0.1, update x₁=x₀−0.2x₀=0.8x₀. Starting x₀=2 gives 2,1.6,1.28;
losses are 4,2.56,1.6384. In general xₖ=(1−2η)ᵏx₀. Convergence to zero requires
|1−2η|<1, equivalent to 0<η<1. At η=1, the sign flips forever; above 1,
magnitude grows. The reference rejects rates outside the convergent range for
this particular function, not for every possible optimizer.

For scores [0, ln 2], exponentials are [1,2], denominator 3, probabilities
[1/3,2/3]. Add 1000 to both scores: direct exp is unsafe, but subtracting the
maximum recovers equivalent weights [1/2,1] and the same probabilities. For
an observed second-class target, loss is −ln(2/3)≈0.4055. If its predicted
probability were 1/3, loss would be ≈1.0986. This compares probability assignments,
not whether the category labels were well chosen.

## 7. Architecture and execution diagrams

```mermaid
flowchart LR
  P[Current parameter] --> L[Compute numerical loss]
  L --> G[Compute derivative or gradient]
  G --> U[Subtract learning rate times gradient]
  U --> P
  U --> V[Measure loss and stop at finite step budget]
```

The loop needs a finite budget and measurements. The derivative is a local signal;
the validation step checks actual progress. A later trained model's inference
will use fixed learned parameters rather than rerun this loop for every prediction.

## 8. Implementation from first principles

```python
import math
from forgeagent.math_basics import derivative, descend_square, softmax

f = lambda x: (3 * x + 1) ** 2
assert math.isclose(derivative(f, 2.0), 42.0, rel_tol=1e-6)
history = descend_square(2.0, learning_rate=0.1, steps=2)
assert all(math.isclose(a, b) for a, b in zip(history, [2.0, 1.6, 1.28]))
probabilities = softmax([1000.0, 1000.0 + math.log(2.0)])
assert math.isclose(sum(probabilities), 1.0)
assert math.isclose(probabilities[1], 2 / 3)
print("derivative, descent, and stable normalization passed")
```

[math_basics.py](../../../forgeagent/math_basics.py) contains full loop-based
implementations. Softmax rejects empty and non-finite inputs; it shifts before
exponentiating. The derivative helper requires positive finite h but otherwise
assumes a suitable scalar function near x. The descent returns its initial
value plus each update, allowing step-by-step loss analysis rather than only
a final number. These are CPU-sized educational mechanisms, not ML training infrastructure.

## 9. Worked execution walkthrough

For the composite function, the central-difference helper evaluates f at 2+h
and 2−h, subtracts, and divides by 2h. Compare against the independently derived
42. The descent loop stores x=2, computes gradient 4, subtracts 0.4, and stores
1.6; next it subtracts 0.32 and stores 1.28. Softmax finds maximum 1000+ln2,
shifts to [−ln2,0], exponentiates to [0.5,1], sums to 1.5, and divides. Check
normalization and expected class probability separately.

## 10. Independent laboratory

Implement central difference, stable softmax, and square-loss descent using
[the Week 2 contract](../../../labs/week-02/README.md). Do not use an autograd
library; that mechanism is next phase. Test translated scores, empty/non-finite
input, zero steps, valid learning rates, and the analytic composite derivative.
Run `python labs/week-02/checks.py --day 6 --module learner-work/week-02/optimization.py`.
Deliver numerical tables, a hand derivation, code, and tests. Acceptance requires
explaining why translating all softmax scores leaves probabilities unchanged.

## 11. Experiments

Sweep h from 10⁻¹ to 10⁻¹² for a smooth non-quadratic function such as exp at 1.
Measure absolute derivative error against exp(1); expect an accuracy tradeoff,
not monotonic improvement. In a separate disposable script sweep descent rates
0.1,0.5,1.0,1.1 using the explicit update equation; measure loss after each step.
The reference rejects nonconvergent rates, so do not weaken its contract for the
experiment. Shift logits by 0,100,1000 and compare direct versus stable computation.

## 12. Failure analysis

Overflow in `exp(1000)` means the numerical form is unsuitable, not that the
mathematical softmax is undefined. Shift before exponentiation. A derivative
wrong by a factor can indicate a missing chain-rule contribution; derive each
local rate and compare with a finite-difference check. Divergent loss can reflect
learning rate, a sign bug, or an incorrect gradient; test a one-parameter square
before blaming the dataset. Reject NaN explicitly because ordinary comparisons
with NaN do not behave like ordered finite values.

## 13. Engineering tradeoffs

Finite differences are simple and useful for checking a small number of parameters
but require repeated evaluations and have precision limits. Analytic derivatives
are efficient but error-prone to hand-compose at scale; automatic differentiation
will mechanize the chain rule. Stable algebraic forms preserve the intended
calculation without requiring arbitrary clipping. A fixed step budget ensures
termination, but not convergence or a useful model; monitor actual losses and
later held-out performance.

## 14. Real-world connection

Neural training uses gradients; autoregressive inference typically does not
update parameters. Attention and class prediction use normalized scores.
Negative log probabilities motivate cross-entropy, which later chapters derive
for language modeling. None of those probabilities by itself proves generated
claims are grounded, authorized, or calibrated.

## 15. Common misconceptions

“A derivative is a large finite jump”: it describes local change. “Gradient
descent always finds the global best model”: only under additional conditions.
“Smaller h always improves accuracy”: floating-point cancellation intervenes.
“Softmax checks truth”: it normalizes scores. “Training loss proves generalization”:
a separate evaluation question remains.

## 16. Technical examination

1. Explain derivative, partial derivative, gradient, exponent, and logarithm.
2. Derive the derivative of (3x+1)² and two descent steps on x².
3. Implement stable softmax and a finite-difference gradient check.
4. Diagnose direct-exp overflow and a missing chain-rule factor.
5. Defend finite differences as a checker rather than a large-model training method.

[Answers](../../../solutions/examinations/week-02.md) are separate.

## 17. Daily mastery gate

Pass numerical/validation tests, reproduce both derivations, and score 4/5 with
implementation mandatory. Explain convergence assumptions and stable softmax
invariance. Then take the [weekly exam](../../../assessments/weekly/week-02.md)
and cumulative phase gate. Do not begin backpropagation while the chain rule
is still only a memorized phrase.

## 18. Resources

[Google ML Crash Course, gradient descent](https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent),
30 minutes after this chapter; compare the update mechanism with our square.
[Google sigmoid explanation](https://developers.google.com/machine-learning/crash-course/logistic-regression/sigmoid-function),
20 minutes optional, connects exponentials with a binary probability map.
[MIT introduction to derivatives](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/pages/1.-differentiation/part-a-definition-and-basic-rules/session-1-introduction-to-derivatives/),
David Jerison, optional 40 minutes, reinforces the rate-of-change interpretation.
These are verified primary educational source pages. They do not replace today's
original derivations or establish universal convergence guarantees.

## 19. Revision and retention

On review day derive square loss and softmax shift invariance closed book. In
three days reconstruct the composite gradient check. In one week compare
training versus inference and explain why parameter updates are a different
loop from an agent deciding which tool to call.

## 20. Next lesson connection

[Week 2 review](../weekly-review.md) integrates software and mathematics before
Week 3's regression, networks, and autograd. Later chapters are still planned;
see [the roadmap](../../../ROADMAP.md). The next phase will use these mechanisms
to learn parameters from examples rather than choose them by hand.
