
from mmd.opcodelib import OpCodeProcessor, OpCodeExtractor
from mmd.modellib import MalawareModelTrainer
from argparse import RawDescriptionHelpFormatter
import os

class Analyser:

    trainer = MalawareModelTrainer()
    
    def __init__(self, logger, subparsers):
        self.__logger = logger
        self.__build_menu(subparsers)

    def __build_menu(self, subparsers):

        desc = "performs mmd analysis for the given file against the selected category of the trained modles \n" \
               "\n Usage Examples:" \
               "\n\n   analyse -file <path> -category <model category> \n"

        sub_parser = subparsers.add_parser("analyse", description=desc, formatter_class=RawDescriptionHelpFormatter)
        sub_parser.add_argument("-file", dest="file", type=str, required=True, help="File to analyse.")
        sub_parser.add_argument("-category", dest="category", type=str, required=True, help="Category to compare.")

        sub_parser.set_defaults(func=self.__menu_handler)
        

    def __menu_handler(self, args):

        self.__logger.info("analyse command invoked with file : " + args.file + " and category : " + args.category)

        filename = args.file
        if not filename or not os.path.isfile(filename):
            raise ValueError("Not a valid input file.")
        
        category = args.category
        if not category:
            raise ValueError("Not a valid model category.")
            
        self.analyse(filename, category)
        
            
    def analyse(self, file, category):
            
        self.__logger.info("load the pre-trained model for " + category)
        trained_model = dict()
        trained_model = self.trainer.load(category)
        
        if not trained_model:
            raise ValueError("No trained models found for the category " + category)

        try:
            print("Begin analysis of " + file + " against the trained models for " + category + " category.")
            opcode_extractor = OpCodeExtractor()
            opcode_list, unique_opcode_list = opcode_extractor.extract_opcode(file)

            opcode_processor = OpCodeProcessor()
            opcode_count_matrix = opcode_processor.create_opcode_count_matrix(opcode_list, unique_opcode_list)
            opcode_probability = opcode_processor.create_opcode_probability_matrix(opcode_count_matrix, unique_opcode_list)

            print("\n Calculating similarity scores against the models... \n")

            for model_file, model_matrix in trained_model.items():
                similarity_score = opcode_processor.create_opcode_similarity_score(model_matrix, opcode_probability)
                print(model_file, ":", similarity_score)

        except Exception as ex:
            self.__logger.info("Exception: " + str(ex))

        self.__logger.info("analysis completed without errors")
        
        
if __name__ == "__main__":
    
    analyser = Analyser()
    analyser.analyse(self, 'asm/malware/1b5413aefc1325af9480c69498b69ab22c8dd292.asm.txt', 'WinRescue')