from math import fsum
from pprint import pprint


def calculate_p(message):
    symbols = {}
    for el in message:
        if el not in symbols.keys():
            symbols.update({el: 1})
        else:
            symbols[el] += 1

    for key, value in symbols.items():
        symbols[key] = value / len(message)

    symbols = sorted(symbols.items(), key=lambda x: x[1], reverse=True)
    return dict(symbols)


def encode(message: str) -> float:
    bounds = [0, 1]
    symbols = calculate_p(message)
    message = [*message]

    while len(message) > 0:
        length = bounds[1] - bounds[0]

        interval = {}
        prev = None

        for key, value in symbols.items():
            s = value * length + (prev if prev else 0)

            if not prev:
                s += bounds[0]
                interval.update({key: [bounds[0], s]})
            else:
                interval.update({key: [prev, s]})

            prev = s

        c = message.pop(0)

        bounds = interval[c]

    return sum(bounds) / 2


def decode(number: float, symbols: dict, message_length: int):
    message = ''
    bounds = [0, 1]
    for i in range(message_length):
        prev = 0
        for c, p in symbols.items():
            if number < prev + p:
                message += c
                bounds = [prev, prev + p]
                break
            prev += p

        number = (number - bounds[0]) / (bounds[1] - bounds[0])

    return message


if __name__ == "__main__":
    message = input("Input message to encode: ")
    encoded = encode(message)
    print(f'Encoded: {encoded}')
    print(f'Decoded: {decode(encoded, calculate_p(message), len(message))}')
