from typing import List

# this function returns the row n'th row of the pascal triangle
def pascal_triangle(n: int) -> List[int]:
    if n == 0:
        return [1]
    elif n == 1:
        return [1,1]
    else:
        row = pascal_triangle(n - 1)
        return [1] + [row[i] + row[i+1] for i in range(len(row[:-1]))] + [1]
        
# this function recursively computes the sum of a list        
def sum(l: List[int]) -> int:
    if len(l) > 0:
        return l[0] + sum(l[1:])
    return 0

# same as above but for multiplication
def prod(l: List[int]) -> int:
    if len(l) > 0:
        return l[0] * prod(l[1:])
    return 1

# compute fibonnaci number
def fib(n: int) -> int:
    if n == 0: return 0
    if n == 1: return 1
    return fib(n-1) + fib(n-2)

def fast_fib(n: int) -> int:
    cache = {}
    def r_fib(n: int) -> int:
        if n in cache:
            return cache[n]
        if n < 2: return n
        return r_fib(n-1) + r_fib(n-2)
    return r_fib(n)
