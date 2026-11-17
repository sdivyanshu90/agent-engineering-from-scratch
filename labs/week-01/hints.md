# Hints: open only the level you need

## Day 1
1. Characters and words count different things: whitespace is still a character.
2. Compute the length of the text and the length of its split result separately.
3. Put those two integers under the exact keys `characters` and `words`.

## Day 2
1. A token can become empty after punctuation removal.
2. Lowercase, split, strip edge punctuation, test whether anything remains.
3. Append only the cleaned, nonempty token to a fresh list.

## Day 3
1. A dictionary associates each token with the number seen so far.
2. At each iteration read the previous count, defaulting to zero.
3. Assign `old_count + 1` to the token key. Allocate the dictionary inside the function.

## Day 4
1. Separate selecting a file from reading its contents.
2. Sort immediate children; accept regular files whose suffix is exactly `.txt`.
3. `Path.read_text(encoding="utf-8")` returns text; append the filename and text as a tuple. Do not suppress its exceptions.

## Day 5
1. A tie must have a stable, explicit resolution independent of input order.
2. Compare the pair `(-count, path)` in ascending order.
3. Filter positive hits, sort a new list with that key, then slice. Validate the limit before slicing.

## Day 6
1. Separate business functions from command-line input and serialization.
2. Parse → load → search → serialize. Catch expected operational errors around load/search.
3. Return 2 on a handled failure; print successful JSON only after all work succeeds. Let the top-level wrapper convert the return value to an exit status.
