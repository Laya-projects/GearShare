# Recursion notes

## 1. Which is clearer: recursive or iterative?
For the category tree, the recursive version is clearer. A category is a node
with child categories, so "count this node's items plus the count of each
child" matches the shape of the data and takes only a few lines. The
iterative version needs an explicit stack that I manage myself (push the root,
pop a node, add its items, push its children), so there is more bookkeeping
and it is easier to get wrong. For factorial and sum_of_digits, the loop is
just as clear as the recursion.

## 2. Which would I use at depth 10,000?
The iterative version. Python's default recursion limit is about 1000 calls,
so a recursive function 10,000 levels deep raises RecursionError. The
iterative version keeps its stack in a normal list on the heap, which can grow
to hold 10,000 entries (or far more) without hitting the call-stack limit.

## 3. What does sys.setrecursionlimit change, and what does it not fix?
It only raises the number of nested calls Python allows before it raises
RecursionError. It does not give each call more memory, and it does not make
recursion cheaper: every call still creates a stack frame. If I set the limit
too high, the program can crash the whole interpreter with a real stack
overflow (a segmentation fault) instead of a clean RecursionError. It also
does not fix slow or wasteful recursion, such as the naive fibonacci that
recomputes the same values many times. For very deep problems, the right fix
is an iterative version, not a bigger limit.