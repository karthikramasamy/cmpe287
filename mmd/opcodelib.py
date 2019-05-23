import numpy as np
import math
from mmd.plotterlib import OpCodePlotter


class OpCodeExtractor:
    def extract_opcode(self, filename):
        if not (filename and filename.strip()):
            raise ValueError("Invalid File Name. It can't be null or empty")

        opcode_list = [str(line).lower().strip().rstrip('\n')
                       for line in open(filename) if (line and line.strip())]
        return opcode_list, self.get_sorted_distinct_list(opcode_list)

    def get_sorted_distinct_list(self, opcode_list):
        opcode_set = set(opcode_list)
        unique_opcode_list = list(opcode_set)
        unique_opcode_list.sort()
        return unique_opcode_list


class OpCodeProcessor:
    def create_opcode_count_matrix(self, opcode_list, unique_opcode_list):
        distinct_opcode_count = len(unique_opcode_list)
        opcode_count_matrix = np.zeros(
            shape=(distinct_opcode_count, distinct_opcode_count), dtype='int')

        prev_op_index = -1
        for op in opcode_list:
            current_op_index = unique_opcode_list.index(op)

            if(prev_op_index > -1 and current_op_index > -1):
                opcode_count_matrix[prev_op_index, current_op_index] += 1
            prev_op_index = current_op_index
        return opcode_count_matrix

    def create_opcode_probability_matrix(self, opcode_count_matrix, unique_opcode_list):
        self.is_valid_opcode_matrix(opcode_count_matrix)
        opcode_probability = np.apply_along_axis(
            lambda x: x/np.sum(x), 1, opcode_count_matrix)
        opcode_probability = np.around(opcode_probability, 2)
        return opcode_probability

    def create_opcode_similarity_score(self, model_matrix, new_matrix):
        self.is_valid_opcode_matrix(model_matrix)
        self.is_valid_opcode_matrix(new_matrix)

        cumulative_sum = 0

        for i, j in np.ndindex(model_matrix.shape):
            aminusb = abs(model_matrix[i, j] - new_matrix[i, j])
            cumulative_sum += aminusb

        cumulative_sum_square = math.pow(cumulative_sum, 2)

        similarity_score = (1/math.pow(np.size(model_matrix, 0), 2)
                            ) * cumulative_sum_square

        return similarity_score

    def is_valid_opcode_matrix(self, matrix):
        if np.size(matrix) <= 0:
            raise ValueError("Invalid OpCode Matrix. It shouldn't be empty.")
        if np.size(matrix, 0) != np.size(matrix, 1):
            raise ValueError(
                "Invalid OpCode Matrix. Given matrix isn't a square matrix.")


if __name__ == "__main__":
    import os

    opcode_extractor = OpCodeExtractor()
    opcode_processor = OpCodeProcessor()

    read_directory = os.path.join(os.getcwd(), 'asm/sample')
    files = []

    for (dirpath, dirnames, filenames) in os.walk(read_directory):
        files.extend(os.path.join(dirpath, x) for x in filenames if x.endswith(".txt"))

    print(files)

    matrices = []
    for filename in files:
        opcode_list, unique_opcode_list = opcode_extractor.extract_opcode(filename)

        opcode_count_matrix = opcode_processor.create_opcode_count_matrix(
            opcode_list, unique_opcode_list)
        opcode_probability = opcode_processor.create_opcode_probability_matrix(
            opcode_count_matrix, unique_opcode_list)

        plotter = OpCodePlotter()
        print("\n OpCode Count Matrix: \n")
        plotter.draw_opcode_matrix(opcode_count_matrix, unique_opcode_list)

        print("\n Probability Matrix: \n")
        plotter.draw_opcode_matrix(opcode_probability, unique_opcode_list)

        print("\n OpCode Graph: \n")
        plotter.draw_opcode_graph(opcode_probability, unique_opcode_list)

        matrices.append(opcode_probability)

    print(matrices)

    similarity_score = opcode_processor.create_opcode_similarity_score(matrices[0], matrices[len(matrices)-1])
    print("\n similarity_score: ", similarity_score)
