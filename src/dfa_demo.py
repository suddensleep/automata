from dfa import DFA

d1 = DFA([0, 1, 2], ["0", "1"], {0: {"0": 2, "1": 2}, 1: {"0": 0, "1": 1}, 2: {"0": 1, "1": 1}}, 0, [0])
input_1 = "111"
input_2 = "000"
print(f"d1 {d1.verdict(input_1)}s the string 111")
print(f"d1 {d1.verdict(input_2)}s the string 000")
d1.graph("../output/dfa_test_1.png")

d2 = DFA([0, 1, 2], ["0", "1"], {0: {"0": 0, "1": 1}, 1: {"0": 2, "1": 1}, 2: {"0": 1, "1": 1}}, 0, [1])
input_1 = "111"
input_2 = "000"
input_3 = "100"
print(f"d2 {d2.verdict(input_1)}s the string 111")
print(f"d2 {d2.verdict(input_2)}s the string 000")
print(f"d2 {d2.verdict(input_3)}s the string 100")
d2.graph("../output/dfa_test_2.png")

d3 = DFA([0, 1, 2, 3], ["0", "1"], {0: {"0": 1, "1": 0}, 1: {"0": 2, "1": 0}, 2: {"0": 2, "1": 3}, 3: {"0": 3, "1": 3}}, 0, [3])
input_1 = "10010"
input_2 = "0001"
input_3 = "100"
print(f"d3 {d3.verdict(input_1)}s the string 10010")
print(f"d3 {d3.verdict(input_2)}s the string 0001")
print(f"d3 {d3.verdict(input_3)}s the string 100")
d3.graph("../output/dfa_test_3.png")
