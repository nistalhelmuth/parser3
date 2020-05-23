import copy

class Node():
    def __init__(self, words):
        self.value = None
        self.next = None
        if len(words) != 0:
            self.value = words[0]
            self.next = Node(words[1:])

def evaluate(text, tokens, keywords):
    start = copy.deepcopy(tokens)
    currentValue = text
    nextValue = text
    last = {}
    pull = []
    while currentValue.next != None:
        for name in tokens.keys():
            token = tokens[name]
            newState, accepted = token[0].slowCheck(nextValue.value, token[1])
            if newState != None:
                token[2].append(nextValue.value)
                tokens[name] = (token[0], newState, copy.deepcopy(token[2]), token[3])
                if accepted:
                    test = nextValue.value
                    last = {
                        'name': name,
                        'text': ''.join(copy.deepcopy(token[2])),
                        'token': (token[0], newState, token[2]),
                        'keywords': token[3],
                    }
            else:
                pull.append(name)

        for name in pull:
            del tokens[name]
            pull = []

        
        if len(tokens) == 0:
            if last != {}:
                test = ''
                for value in last['text']:
                    if value == currentValue.value:
                        currentValue = currentValue.next
                        test = test + value
                if last['keywords'] and last['text'] in keywords.keys():
                    print('FOUND KEYWORD', keywords[last['text']])
                else:
                    print('TOKEN FOUND', last)
                last = {}
            else:
                print('ERORR WITH', currentValue.value)
                currentValue = currentValue.next
            tokens = copy.deepcopy(start)
            nextValue = currentValue
        else:
            nextValue = nextValue.next