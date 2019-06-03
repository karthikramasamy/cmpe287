import os
import pickle
from mmd.opcodelib import OpCodeExtractor, OpCodeProcessor

class MalawareModelTrainer:

    model_folder = os.path.join(os.path.expanduser("~"), ".mmd")

    def load(self, category):
        matrices = dict()
        model_file_name = os.path.join(self.model_folder, category.lower() + ".p")

        if os.path.isfile(model_file_name):
            matrices = pickle.load(open(model_file_name, "rb"))
        return matrices

    def train(self, category, folder):

        if not os.path.isdir(folder):
            ValueError("Invalid folder path.")
        
        files = []
        for (dirpath, dirnames, filenames) in os.walk(folder):
            files.extend(os.path.join(dirpath, x) for x in filenames if x.endswith(".txt"))

        opcode_extractor = OpCodeExtractor()
        opcode_processor = OpCodeProcessor()
        matrices = dict()
        for filename in files:
            opcode_list, unique_opcode_list = opcode_extractor.extract_opcode(filename)

            opcode_count_matrix = opcode_processor.create_opcode_count_matrix(
                opcode_list, unique_opcode_list)
            opcode_probability = opcode_processor.create_opcode_probability_matrix(
                opcode_count_matrix, unique_opcode_list)

            matrices[filename] = opcode_probability

        if not os.path.exists(self.model_folder):
            os.makedirs(self.model_folder)

        model_file_name = os.path.join(self.model_folder, category.lower() + ".p")
        print("saving the trained model to : ", model_file_name)
        pickle.dump(matrices, open(model_file_name, "wb"))
        print(matrices)


if __name__ == "__main__":
    trainer = MalawareModelTrainer()
    print("Training the model.")
    trainer.train("CLUSTER912343210", 'asm/CLUSTER912343210')
    trainer.train("WinRescue", 'asm/WinRescue')
    trainer.train("benign", 'asm/benign')
    trainer.train("cridex", 'asm/cridex')
    trainer.train("ransomNoaouy", 'asm/ransomNoaouy')
    trainer.train("securityshield", 'asm/securityshield')
    trainer.train("smarthdd", 'asm/smarthdd')

    print("Loading the model.")
    matrices = trainer.load("CLUSTER912343210")
    matrices = trainer.load("WinRescue")
    matrices = trainer.load("benign")
    matrices = trainer.load("cridex")
    matrices = trainer.load("ransomNoaouy")
    matrices = trainer.load("securityshield")
    matrices = trainer.load("smarthdd")
    print(matrices)