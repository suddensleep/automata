from graph_tool import Graph
from graph_tool.draw import graph_draw

def new_ind_to_power_set(ind, nfa_size):
    return list(a for (a, b) in zip(range(nfa_size), format(ind, f"0{nfa_size}b")) if b=="1")

def power_set_to_new_ind(nfa_state_subset, nfa_size):
    bin_str = ''
    for state in range(nfa_size):
        if state in nfa_state_subset:
            bin_str += "1"
        else:
            bin_str += "0"
    return int(bin_str, 2)

def epsilon_set(state_set, delta):
    return set().union(*[delta[state]["_"] for state in state_set])

def epsilon_closure(state_set, delta):
    eps_set = epsilon_set(state_set, delta)
    if eps_set.issubset(state_set):
        return state_set
    return epsilon_closure(state_set.union(eps_set), delta)

def connected_to_initial(full_dfa):
    connected_to_init = [full_dfa.initial_state]
    to_check = [full_dfa.delta[full_dfa.initial_state][symbol] for symbol in full_dfa.alphabet]
    while len(to_check) > 0:
        check = to_check.pop()
        for symbol in full_dfa.alphabet:
            next_state = full_dfa.delta[check][symbol]
            if next_state not in connected_to_init:
                connected_to_init.append(next_state)
                if next_state not in to_check:
                    to_check.append(next_state)
    return connected_to_init

def reduce_dfa(full_dfa):
    delta_range = connected_to_initial(full_dfa)
    if len(delta_range) == len(full_dfa.states):
        return full_dfa
    new_delta = full_dfa.delta
    new_final_states = full_dfa.final_states
    for state in full_dfa.states:
        if state not in delta_range:
            del(new_delta[state])
            if state in new_final_states:
                new_final_states.remove(state)
    new_dfa = DFA(delta_range, full_dfa.alphabet, new_delta, full_dfa.initial_state, new_final_states)
    return reduce_dfa(new_dfa)

def reindex_dfa(reduced_dfa):
    reindexing_dict = dict(zip(reduced_dfa.states, range(len(reduced_dfa.states))))
    new_states = [reindexing_dict[state] for state in reduced_dfa.states]
    new_delta = dict()
    for state in reduced_dfa.states:
        state_trans = dict()
        for symbol in reduced_dfa.alphabet:
            state_trans[symbol] = reindexing_dict[reduced_dfa.delta[state][symbol]]
        new_delta[reindexing_dict[state]] = state_trans
    new_initial_state = reindexing_dict[reduced_dfa.initial_state]
    new_final_states = [reindexing_dict[final_state] for final_state in reduced_dfa.final_states]
    return DFA(new_states, reduced_dfa.alphabet, new_delta, new_initial_state, new_final_states)

class DFA:
    def __init__(self, states, alphabet, delta, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.delta = delta
        self.initial_state = initial_state
        self.final_states = final_states
        
    @classmethod
    def from_nfa(cls, nfa):
        states = list(range(2 ** len(nfa.states)))
        alphabet = nfa.alphabet[:-1]
        delta = dict()
        for state in states:
            state_trans = dict()
            power_subset = new_ind_to_power_set(state, len(nfa.states))
            print(power_subset)
            for symbol in alphabet:
                next_power_subset = set().union(*[epsilon_closure(nfa.delta[nfa_state][symbol], nfa.delta) for nfa_state in power_subset])
                state_trans[symbol] = power_set_to_new_ind(next_power_subset, len(nfa.states))
            delta[state] = state_trans
        initial_state = power_set_to_new_ind(epsilon_closure({nfa.initial_state}, nfa.delta), len(nfa.states))
        final_states = [state for state in states if len(set(new_ind_to_power_set(state, len(nfa.states))).intersection(nfa.final_states)) > 0]

        full_dfa = cls(states, alphabet, delta, initial_state, final_states)
        reduced_dfa = reduce_dfa(full_dfa)
        return reindex_dfa(reduced_dfa)
        
    def compute(self, input_string, verbose=False):
        states = [self.initial_state]
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
        vprop_dict_1 = g.new_vertex_property("string")
        vprop_dict_2 = g.new_vertex_property("string")
        eprop_dict = g.new_edge_property("string")
        for state in self.states:
            if state in self.final_states:
                vprop_dict_1[g.vertex(state)] = "red"
            else:
                vprop_dict_1[g.vertex(state)] = "grey"
            if state == self.initial_state:
                vprop_dict_2[g.vertex(state)] = "green"
            else:
                vprop_dict_2[g.vertex(state)] = "white"
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
            vertex_color=vprop_dict_1,
            vertex_fill_color=vprop_dict_2,
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
    
    
