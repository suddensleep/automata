from nfa import NFA

d1 = NFA([0, 1, 2, 3], ["0", "1"], {0: {"0": {0}, "1": {0, 1}, "_": set()}, 1: {"0": {2}, "1": set(), "_": {2}}, 2: {"0": set(), "1": {3}, "_": set()}, 3: {"0": {3}, "1": {3}, "_": set()}}, 0, [3])
input_1 = "111"
input_2 = "000"
input_3 = "10101"
print(f"d1 {d1.verdict(input_1)}s the string 111")
print(f"d1 {d1.verdict(input_2)}s the string 000")
print(f"d1 {d1.verdict(input_3)}s the string 10101")
d1.graph("../output/nfa_test_1.png")

d2 = NFA([0, 1, 2, 3], ["0", "1"], {0: {"0": {0}, "1": {0, 1}, "_": set()}, 1: {"0": {2}, "1": {2}, "_": set()}, 2: {"0": {3}, "1": {3}, "_": set()}, 3: {"0": set(), "1": set(), "_": set()}}, 0, [3])
input_1 = "00111"
input_2 = "00011"
input_3 = "100"
print(f"d2 {d2.verdict(input_1)}s the string 00111")
print(f"d2 {d2.verdict(input_2)}s the string 00011")
print(f"d2 {d2.verdict(input_3)}s the string 100")
d2.graph("../output/nfa_test_2.png")

d3 = NFA([0, 1, 2, 3, 4, 5], ["0"], {0: {"0": set(), "_": {1, 3}}, 1: {"0": {2}, "_": set()}, 2: {"0": {1}, "_": set()}, 3: {"0": {4}, "_": set()}, 4: {"0": {5}, "_": set()}, 5: {"0": {3}, "_": set()}}, 0, [1, 3])
input_1 = "000"
input_2 = "0000"
input_3 = "00000"
print(f"d3 {d3.verdict(input_1)}s the string 000")
print(f"d3 {d3.verdict(input_2)}s the string 0000")
print(f"d3 {d3.verdict(input_3)}s the string 00000")
d3.graph("../output/nfa_test_3.png")

d4 = NFA([0, 1, 2], ["0", "1"], {0: {"0": set(), "1": {1}, "_": {2}}, 1: {"0": {1, 2}, "1": {2}, "_": set()}, 2: {"0": {0}, "1": set(), "_": set()}}, 0, [0])
input_1 = ""
input_2 = "1010"
input_3 = "10110"
print(f"d4 {d4.verdict(input_1)}s the string \"\"")
print(f"d4 {d4.verdict(input_2)}s the string 1010")
print(f"d4 {d4.verdict(input_3)}s the string 10110")
d4.graph("../output/nfa_test_4.png")
