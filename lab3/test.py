from random import random


def choices(items, weights):
    l = []
    s = 0
    for el in weights:
        l.append(s + el)
        s += el

    num = s * random()

    i = 0
    while l[i] <= num:
        i += 1

    return items[i]


choices([1, 2, 3, 4], [1, 2, 3, 4])

nums = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
}
for i in range(100000):
    num = choices([1, 2, 3, 4], [1, 2, 3, 4])
    nums[num] += 1

print(nums)