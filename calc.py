"""
Utilities for entropy-related calculations.
"""


from math import ceil, log2


__all__ = [
    'entropy',
    'info_to_prob',
    'metric_entropy',
    'optimal_bits',
    'prob_to_info',
]


def prob_to_info(probability):
    """Converts probability into information, measured in bits.

    Notes:
      Uses the dual logarithm.

    Args:
      probability (float): In the range from 0 to 1.

    Returns:
      float [or None if the probability is equal to zero]."""
    if probability == 0:
        return None
    elif probability == 1:
        return 0
    else:
        return -log2(probability)


def info_to_prob(information):
    """Converts information measured in bits to probablity.

    Args:
      information (float)

    Returns:
      float in the range from 0 to 1."""
    return 2**-information


def entropy(iterable):
    """Calculates the Shannon entropy of the given iterable.

    Args:
      iterable: Any iterable; list, dictionary, set...

    Returns:
      float"""
    return sum(prob[1]*prob_to_info(prob[1]) for prob in char_mapping(iterable))


def optimal_bits(iterable):
    """Calculates the optimal usage of bits for decoding the iterable.

    Args:
      iterable: Any iterable; list, dictionary, set...

    Returns:
      int"""
    return ceil(entropy(iterable)) * len(iterable)


def metric_entropy(iterable):
    """Calculates the metric entropy of the iterable.

    Args:
      iterable: Any iterable; list, dictionary, set...

    Returns:
      float"""
    return entropy(iterable) / len(iterable)


def char_mapping(iterable):
    """Creates a dictionary of the unique chararacters and their probability
    in the given iterable.

    Notes:
      Internal use.

    Args:
      iterable: Any iterable; list, dictionary, set...

    Returns:
      dictionary: Characters are keys, their corresponding probabilities
                  are values."""
    char_map = dict.fromkeys(set(iterable))
    for char in set(iterable):
        probability = iterable.count(char) / len(iterable)
        char_map[char] = probability

    return sorted(char_map.items(), key=lambda x: x[1], reverse=True)
