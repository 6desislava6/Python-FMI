from itertools import permutations, groupby, combinations

# If the grid width is odd, then the number of inversions in a solvable
# situation is even.

# If the grid width is even, and the blank is on an even row counting from
# the bottom (second-last, fourth-last etc), then the number of inversions in
#  a solvable situation is odd.
# If the grid width is even, and the blank is on an odd row counting from the
#  bottom (last, third-last, fifth-last etc) then the number of inversions in
#   a solvable situation is even.

# combinations(p, r)
# r-length tuples, in sorted order, no repeated elements

#  inversion_number(xs):
# combinations(range(len(xs)), 2)
# makes every single combination of indexes, where the first index is
# smaller than the second // sorted

# make_combinations(grid):
# Makes all possible permutations, counts the inversions for each and groups
# the permutations by the count of inversions


def chunkify(xs, size):
    return tuple(tuple(xs[i:i + size]) for i in range(0, len(xs), size))


def inversion_number(xs):
    without_zero = list(xs)
    without_zero.remove(0)
    return sum(1 for x, y in combinations(range(len(without_zero)), 2)
               if without_zero[x] > without_zero[y])


def make_combinations(size):
    return groupby(map(lambda xs: [inversion_number(xs) % 2, xs],
                       permutations(range(size))), key=lambda xs: xs[0])


def filter_zero(matrix, begin):
    searched_lines = [matrix[i] for i in range(begin, len(matrix), 2)]
    return any(map(lambda line: 0 in line, searched_lines))


def solvable_tiles(size=3):
    combs = make_combinations(size ** 2)
    for key, group in combs:

        # odd grid, even inversions
        if size % 2 == 1 and key == 0:
            for element in group:
                yield(chunkify(element[1], size))

        # even grid, odd inversions
        elif size % 2 == 0 and key == 1:
            for element in group:
                matrix = chunkify(element[1], size)
                if filter_zero(matrix, 0):
                    yield(matrix)

        # even grid, even inversions
        elif size % 2 == 0 and key == 0:
            for element in group:
                matrix = chunkify(element[1], size)
                if filter_zero(matrix, 1):
                    yield(matrix)



a = solvable_tiles(4)
for i in a:
    print(i)


#groups = defaultdict(list)
# for k, g in invers:
#    groups[k].append(list(g)[0][1])
# return groups
