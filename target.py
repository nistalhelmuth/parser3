from utils.dfa import DFA
from utils.evaluate import evaluate, Node

file = open('./inputs/input1.txt', 'r')
text = Node(''.join(file.read().splitlines()))
file.close()
evaluate(text, tokens, keywords)
