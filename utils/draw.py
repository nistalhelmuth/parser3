from graphviz import Digraph

def drawPrettyGraph(start_states, states, transitions, accept_states, name):
    f = Digraph('finite_state_machine', filename=name)
    f.attr(rankdir='LR', size='8,5')
    f.attr('node', shape='doublecircle')
    for accept in accept_states:
        f.node(str(accept))
    f.attr('node', shape='circle')
    for state in transitions:
        for value in transitions[state]:
            for node in transitions[state][value]:
                f.edge(str(state), str(node), label=str(value))
    f.view()
