import unittest
import numpy as np
from mmd.plotterlib import OpCodePlotter

class PlotterLibTests(unittest.TestCase):
    
    def test_draw_opcode_matrix(self):
        plotter = OpCodePlotter()
        opcode_list = ['add', 'call', 'jmp', 'nop', 'sub']
        opcode_matrix = np.around(np.random.rand(5,5), 2)
        plotter.draw_opcode_matrix(opcode_matrix, opcode_list)
        
    def test_draw_opcode_graph(self):
        plotter = OpCodePlotter()
        opcode_list = ['add', 'call', 'jmp', 'nop', 'sub']
        opcode_matrix = np.around(np.random.rand(5,5), 2)
        #plotter.draw_opcode_matrix(opcode_matrix, opcode_list)
        plotter.draw_opcode_graph(opcode_matrix, opcode_list)
    
if __name__ == '__main__':
    unittest.main()
