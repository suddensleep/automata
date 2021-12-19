from graph_tool import Graph
from graph_tool.draw import graph_draw

class DFA:
    def __init__(self, states, alphabet, delta, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.delta = delta
        self.initial_state = initial_state
        self.final_states = final_states

    def compute(self, input_string, verbose=False):
        states = [self.states[0]]
        for symbol in input_string:
            states.append(self.delta[states[-1]][symbol])
        if verbose:
            print(states)
        return states[-1] in self.final_states

    def verdict(self, input_string):
        if self.compute(input_string):
            return "ACCEPT"
        return "REJECT"

    def graph(self, file_out=None):
        g = Graph(directed=True)
        g.add_vertex(n=len(self.states))
        vprop_dict = g.new_vertex_property("string")
        eprop_dict = g.new_edge_property("string")
        for state in self.states:
            if state in self.final_states:
                vprop_dict[g.vertex(state)] = "red"
            else:
                vprop_dict[g.vertex(state)] = "white"
            for symbol in self.alphabet:
                e = g.add_edge(
                    g.vertex(state),
                    g.vertex(self.delta[state][symbol])
                )
                eprop_dict[e] = symbol
        graph_draw(
            g,
            vertex_text=g.vertex_index,
            edge_text=eprop_dict,
            vertex_size=40,
            vertex_fill_color=vprop_dict,
            adjust_aspect=False,
            output_size=(1000,1000),
            output=file_out
        )

if __name__ == "__main__":
    d = DFA([0, 1, 2],
            ["0", "1"],
            {
                0: {"0": 2, "1": 2},
                1: {"0": 0, "1": 1},
                2: {"0": 1, "1": 1}
            },
            0,
            [0]
    )
    input_1 = "111"
    input_2 = "000"
    print(f"d {d.verdict(input_1)}s the string 111")
    print(f"d {d.verdict(input_2)}s the string 000")
    d.graph("../output/test.png")
    
