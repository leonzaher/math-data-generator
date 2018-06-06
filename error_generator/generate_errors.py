import random
import numpy as np


class ErrorGenerator(object):
    def __init__(self, probabilities_map_path: str):
        self.probabilities_map = ErrorGenerator.__load_probabilities_map(probabilities_map_path)

        self.probabilities = dict()

        # calculate probability for each error to happen and store it in a convenient way:
        #  {a: {errors: [a, b, c, ...], probabilities: [0, 0.02, 0.03, ...]}, ...}
        for error_source in self.probabilities_map.keys():

            total_weights = float(sum(self.probabilities_map[error_source].values()))
            self.probabilities[error_source] = dict()

            possible_errors_list = list()
            error_probabilities_list = list()

            for error_destination_name, error_destination_value in self.probabilities_map[error_source].items():
                possible_errors_list.append(error_destination_name)
                error_probabilities_list.append(error_destination_value / total_weights)

            self.probabilities[error_source]["errors"] = possible_errors_list
            self.probabilities[error_source]["probabilities"] = error_probabilities_list

    def generate_errors(self, string: str, error_count: int) -> str:
        # generate a sample from all indexes of string with a count of error_count
        for index in random.sample(range(len(string)), error_count):
            print("Chosen index", index)

            char = string[index]

            # choose an error based on probability
            error = np.random.choice(a=self.probabilities[char]["errors"], p=self.probabilities[char]["probabilities"])

            # change the character at index into error
            string = string[:index] + error + string[index + 1:]

        return string

    def generate_from_originals(self, originals: list, error_count_range: range, generated_count_range) -> dict:
        for original in originals:
            generated_strings = list()

            for i in range(random.sample(generated_count_range, 1)):
                error_count = random.sample(error_count_range, 1)

                generated_strings.append(self.generate_errors(original, error_count))

    @staticmethod
    def __load_probabilities_map(filePath: str) -> dict:
        with open(filePath) as map_file:
            # read header row into array
            header_row = map_file.readline()[:-1]
            characters_array = header_row.split(" ")
            del characters_array[0:2]

            probabilities_dict = dict()

            for row in map_file.readlines():
                target_character = row[0:1]

                probabilities_dict[target_character] = dict()

                row = row[2:len(row)]

                for index, weight in enumerate(row.split(" ")):
                    probabilities_dict[target_character][characters_array[index]] = int(weight)

        return probabilities_dict
