from tabulate import tabulate
import networkx as nx
import matplotlib.pyplot as plt


class OpCodePlotter:

    def draw_opcode_matrix(self, matrix, headers):
        table = tabulate(matrix, headers, tablefmt="fancy_grid")
        print(table)

    def draw_opcode_graph(self, adjacency_matrix, unique_opcode_list):
        labels = self.make_label_dict(unique_opcode_list)
        G = nx.MultiDiGraph(adjacency_matrix)
        edge_labels = dict(((u, v), d["weight"]) for u, v, d in G.edges(data=True))
        pos = nx.spring_layout(G)
        nx.draw(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw(G, pos, node_size=1000, labels=labels, with_labels=True)
        plt.show()

    def make_label_dict(self, labels):
        l = {}
        for i, label in enumerate(labels):
            l[i] = label
        return l


if __name__ == "__main__":
    import numpy as np
    plotter = OpCodePlotter()
    opcode_list = ['add', 'call', 'jmp', 'nop', 'sub']
    opcode_matrix = np.around(np.random.rand(5, 5), 2)

    print("\n Node List: \n", opcode_list)
    print("\n Matrix: \n")
    plotter.draw_opcode_matrix(opcode_matrix, opcode_list)
    print("\n Grapth: \n")
    plotter.draw_opcode_graph(opcode_matrix, opcode_list)
