import numpy as np
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
        opcode_probability = np.apply_along_axis(lambda x: x/np.sum(x), 1, opcode_count_matrix)
        opcode_probability = np.around(opcode_probability, 2)
        return opcode_probability


if __name__ == "__main__":
    import os
    
    read_directory = os.path.join(os.getcwd(), 'asm/sample')
    files = []
    for (dirpath, dirnames, filenames) in os.walk(read_directory):
        files.extend(os.path.join(dirpath, x) for x in filenames if x.endswith(".txt"))

    matrices = {}
    for filename in files:
        opcode_extractor = OpCodeExtractor()
        opcode_list, unique_opcode_list = opcode_extractor.extract_opcode(filename)
        
        opcode_processor = OpCodeProcessor()
        opcode_count_matrix = opcode_processor.create_opcode_count_matrix(opcode_list, unique_opcode_list)
        opcode_probability = opcode_processor.create_opcode_probability_matrix(opcode_count_matrix, unique_opcode_list)

        plotter = OpCodePlotter()
        print("\n OpCode Count Matrix: \n")
        plotter.draw_opcode_matrix(opcode_count_matrix, unique_opcode_list)
        
        print("\n Probability Matrix: \n")
        plotter.draw_opcode_matrix(opcode_probability, unique_opcode_list)
        
        print("\n OpCode Graph: \n")
        plotter.draw_opcode_graph(opcode_probability, unique_opcode_list)
        
        
        matrices[filename] = [len(unique_opcode_list), unique_opcode_list]

    print(matrices)
