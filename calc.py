from math import ceil, log2


def prob_to_info(probability):
    return -log2(probability)


def info_to_prob(information):
    return 2**-information


def entropy(char_map):
    return sum(prob[1]*prob_to_info(prob[1]) for prob in char_map)


def optimal_bits(entropy, length):
    return ceil(entropy) * length


def metric_entropy(entropy, length):
    return entropy / length


def char_mapping(string):
    char_map = dict.fromkeys(set(string))
    for char in set(string):
        probability = string.count(char) / len(string)
        char_map[char] = probability

    return sorted(char_map.items(), key=lambda x: x[1], reverse=True)
