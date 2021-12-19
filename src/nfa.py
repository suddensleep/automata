from graph_tool import Graph
from graph_tool.draw import graph_draw

class NFA:
    def __init__(self, states, alphabet, delta, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet + ["_"]
        self.delta = delta
        self.initial_state = initial_state
        self.final_states = final_states

    def epsilon_set(self, state_set):
        return set().union(*[self.delta[state]["_"] for state in state_set])
        
    def epsilon_closure(self, state_set):
        eps_set = self.epsilon_set(state_set)
        if eps_set.issubset(state_set):
            return state_set
        return self.epsilon_closure(state_set.union(eps_set))
        
    def compute(self, input_string, verbose=False):
        states = [self.epsilon_closure(set([self.initial_state]))]
        for symbol in input_string:
            states.append(self.epsilon_closure(set().union(*[self.delta[state][symbol] for state in states[-1]])))
        if verbose:
            print(states)
        return len(states[-1].intersection(self.final_states)) > 0

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
                for destination in self.delta[state][symbol]:
                    e = g.add_edge(
                        g.vertex(state),
                        g.vertex(destination)
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
    d = NFA([0, 1, 2, 3],
            ["0", "1"],
            {
                0: {"0": {0}, "1": {0, 1}, "_": set()},
                1: {"0": {2}, "1": set(), "_": {2}},
                2: {"0": set(), "1": {3}, "_": set()},
                3: {"0": {3}, "1": {3}, "_": set()}
            },
            0,
            [3]
    )
    input_1 = "111"
    input_2 = "000"
    input_3 = "10101"
    print(f"d {d.verdict(input_1)}s the string 111")
    print(f"d {d.verdict(input_2)}s the string 000")
    print(f"d {d.verdict(input_3)}s the string 10101")
    d.graph("../output/test.png")
