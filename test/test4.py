import itertools

permutations = list(itertools.permutations(['a', 'b', 'c']))
words = []
for permutation in permutations:
    words.append(''.join(permutation))
print(words)
