import calc


def main(chars):
    char_map = calc.char_mapping(chars)
    for char, probability in char_map:
        information = calc.prob_to_info(probability)
        print(char,
              "| Probability:", probability,
              "\t| Information:", information)
    entropy = calc.entropy(char_map)
    print("Entropy:", entropy)
    print("Metric entropy:", calc.metric_entropy(entropy, len(chars)))
    print("Optimal encoding:", calc.optimal_bits(entropy, len(chars)), "bits")

if __name__ == "__main__":
    string = input("Input: ")
    main(string)
