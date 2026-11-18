# Week 7 assessment

Complete the daily examinations in [D37](../../curriculum/week-07/day-01/README.md)
through [D42](../../curriculum/week-07/day-06/README.md). Submit one runnable
lab, six trace/evidence notes, and answers to the following transfer tasks:

1. A fixed sequence has three model calls; a proposed adaptive policy takes 1,
   2, or 4 calls with probabilities .5, .35, .15. Find expected and maximum calls.
2. Validate `{"code":"ééé","page":true}` for a closed schema with code max
   four UTF-8 bytes and page integer range 1..9. State every reason it rejects.
3. Give a two-request trace where a read failure is observed and the next model
   decision finishes. Mark untrusted observations and terminal state.
4. For A→C, B→C, C→D with durations .3,.5,.2,.1 seconds, compare serial and
   ideal concurrent-read latency. Explain what changes when B is a write.
5. Reconcile 9 input and 2 output tokens against a cap of 10. At rates $2/M and
   $8/M calculate the completed call cost and state what can still be charged.
6. Define recovery for a read timeout and for a write whose remote outcome is
   unknown. Include a trace metric that catches duplicate effects.

The fixed 100-point rubric, model answers and remediation plan are in the
[separate examination guide](../../solutions/examinations/week-07.md). Pass is
80 points with no critical authority or side-effect error.
