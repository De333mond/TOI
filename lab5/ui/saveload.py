import pickle


def save_to(filename: str, data: dict):
    try:
        with open(filename, 'wb') as file:
            pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print('Error during pickling object (Possibly unsupported)', ex)


def load_from(filename: str) -> dict:
    with open(filename, 'rb') as file:
        return pickle.load(file)
