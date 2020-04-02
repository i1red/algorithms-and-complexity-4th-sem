import random


BOUND = 1000

START_KEYS = [key for key in {random.randint(-BOUND, BOUND) for _ in range(BOUND)}]
SORTED_KEYS = sorted([key for key in {random.randint(BOUND, 10 * BOUND) for _ in range(BOUND)}])

START_INPUT = [(key, random.random()) for key in START_KEYS]
SORTED_INPUT = [(key, random.random()) for key in SORTED_KEYS]

SORTED_VALUES = sorted(START_INPUT + SORTED_INPUT, key=lambda x: x[0])
ALL_KEYS = {key for key, value in SORTED_VALUES}