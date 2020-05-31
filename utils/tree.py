import re
from utils.dfa import DFA

class LL(): 
    def __init__ (self, tree, terminals):
        self.tree = tree
        self.terminals = terminals
        self.first = set()
        self.follow = set()
        self.name = None
        self.value = None
        self.childs = []
        self.tabs = 0
    
    def generateTree(self, stack, inputs):
        x = stack[0]
        a = inputs[0]
        if x in self.terminals:
            self.name = stack.pop(0)
            self.value = inputs.pop(0)
        elif x in self.tree.keys():
            for option in self.tree[x]:
                if option[0].check(a):
                    self.name = stack.pop(0)
                    for prod in option[1]:
                        kid = LL(self.tree, self.terminals)
                        stack,inputs = kid.generateTree([prod] + stack, inputs)
                        self.childs.append(kid)
        else:
            print("error parsing production")
        return stack, inputs
    
    def calculateFirst(self, firsts):
        if self.name == 'ia':
            index = self.value.find('<.')
            name = self.value[:index]
            if name in firsts.keys():
                self.first = self.first.union(firsts[name])
            else:
                self.first.add(self.value)
        elif self.name == 'i':
            if self.value in firsts.keys():
                self.name = 'ia'
                self.first = self.first.union(firsts[self.value])
            else:
                self.first.add(self.value)
        
        elif self.name not in ['|', '[', '(', '(.', 'x', '.)', '{'] and self.name in self.terminals:
            self.first.add(self.value)
            return self.first
        for child in self.childs:
            first = child.calculateFirst(firsts)
            if self.childs[0].name == "F'" and child.name == "T'":
                self.first = self.childs[0].first.union(first)
            if child.name == "E'" or child.name == 'F':
                self.first = self.first.union(first)
            if len(first) != 0 and len(self.first) == 0:
                self.first = first
        return self.first

    def calculateFollow(self):
        if self.name in self.terminals:
            return
        for i in range(len(self.childs)):
            child = self.childs[i]
            child.calculateFollow()
            if child.name and (i+1) < len(self.childs):
                child.follow = child.follow.union(self.childs[i+1].first)

    def translate2(self, tabs=0):
        tabString = '\t'*tabs
        values = []
        if self.name == 'i' or self.name == 's' or self.name == 'c':
            for element in list(self.first):
                values.append("%sself.Get(%s)\n" % (tabString , element))
        elif self.name == 'ia':
            if self.value.find('<.') > -1:
                line = self.value.replace('<.', '(').replace('.>',')').replace('ref','').replace(' ','')
                ref = ','.join(re.findall(r'ref+\s([\w\-]+)', self.value)) + ' = '
            else:
                line = self.value+'()'
                ref = ''

            values.append(('%s%sself.%s\n') % (tabString, ref, line))
        elif self.name == '{': #
            tabs += 1
            expression = []
            for element in list(self.follow):
                expression.append('self.Expect(%s)' % element)
            values = ['%swhile(%s):\n' % (tabString, ' or '.join(expression))]
        elif self.name == '[': 
            tabs += 1
            expression = []
            for element in list(self.follow):
                expression.append('self.Expect(%s)' % element)
            values = ['%sif(%s):\n' % (tabString, ' or '.join(expression))]
        elif self.name == '|': #
            tabString = '\t'*(tabs-1)
            expression = []
            for element in list(self.follow):
                expression.append('self.Expect(%s)' % element)
            values = ['%selif(%s):\n' % (tabString, ' or '.join(expression))]
        elif self.name in [']', '}']:
            tabs -= 1
            values = ['\n']
        elif self.name in ['.)']:
            values = ['\n']
        elif self.name in ['(' ,')', '(.']:
            values = []
        elif self.name in self.terminals:
            values.append(tabString+self.value)
            
        else:
            if self.name == 'E' and len(self.childs[1].childs) > 0:
                tabs += 1
                expression = []
                for element in list(self.childs[0].first):
                    expression.append('self.Expect(%s)' % element)
                values = ['%sif(%s):\n' % (tabString, ' or '.join(expression))]
            for child in self.childs:
                vals, tabs = child.translate2(tabs)
                values = values + vals
        return values, tabs

letter = DFA('a!b!c!d!e!f!g!h!i!j!k!l!m!n!o!p!q!r!s!t!u!v!w!x!y!z!A!B!C!D!E!F!G!H!I!J!K!L!M!N!O!P!Q!R!S!T!U!V!W!X!Y!Z')
digit = DFA('0!1!2!3!4!5!6!7!8!9')
ident = DFA('letter{letter!digit}', {'letter': letter, 'digit': digit})
string =  DFA('"{noQuote}"')
char =  DFA("' noApostrophe '")
period =  DFA(".")
parentesisA = DFA("(")
parentesisC = DFA(")")
corchetesA = DFA("[")
corchetesC = DFA("]")
llaveA = DFA("{")
llaveC = DFA("}")
semLeft = DFA("'(' .")
semRight = DFA(". ')'")
orDFA = DFA("|") 
attributes =  DFA("< .{ANY}. >")
semAction =  DFA("'(' .{ANY}. ')'")
identExtra = DFA("ident < .{ANY}. >", {'ident': ident})

data = {
    'E': [
        (string, ['T',"E'"]),
        (identExtra,['T',"E'"]), 
        (ident, ['T',"E'"]), 
        (char, ['T',"E'"]), 
        (llaveA, ['T',"E'"]), 
        (parentesisA, ['T',"E'"]), 
        (corchetesA, ['T',"E'"]), 
        (semLeft, ['T', "E'"]),
        ],
    "E'": [
        (orDFA, ['|','T',"E'"]),
        (parentesisC, []), 
        (corchetesC, []), 
        (llaveC, []), 
        (semRight, []),
        (period, [])
        ],
    'T': [
        (string, ['F', "T'"]),
        (identExtra,['F', "T'"]), 
        (ident, ['F', "T'"]), 
        (char, ['F', "T'"]), 
        (llaveA, ['F', "T'"]), 
        (parentesisA, ['F', "T'"]), 
        (corchetesA, ["F'", "T'"]),
        (semLeft, ['F', "T'"])
        ],
    "T'": [
        (string, ['F', "T'"]), 
        (identExtra,['F', "T'"]), 
        (ident, ['F', "T'"]), 
        (char, ['F', "T'"]), 
        (llaveA, ['F', "T'"]), 
        (parentesisA, ['F', "T'"]), 
        (corchetesA, ["F'", "T'"]), 
        (semLeft, ['F', "T'"]),
        (parentesisC, []), 
        (corchetesC, []), 
        (llaveC, []), 
        (semRight, []),
        (orDFA, []),
        (period, []), 
        ],
    'F': [
        (string, ['S']),
        (identExtra,['S']), 
        (ident, ['S']), 
        (char, ['S']), 
        (parentesisA, ['(', 'E', ')']), 
        (corchetesA, ['[', 'E', ']']), 
        (llaveA, ['{', 'E', '}']),
        (semLeft, ['(.', 'x', '.)']), 
        ],
    "F'": [
        (corchetesA, ['[', 'E', ']']), 
    ],
    'S': [
        (string, ['s']), 
        (identExtra, ['ia']), 
        (ident, ['i']), 
        (char, ['c']),
        ],
}

#test = Node(data, ['i', 'ia', 's', 'c', 'a', 'x', '|', '(', ')', '[', ']', '{', '}', '<.', '.>', '(.', '.)'])
#test.generateTree(['E', '.'], ['[', '"-"', ']', "tests", '.'])
#test.generateTree(['E', '.'], ['[','[', '"-"', ']',']', "tests", '.'])
#test.generateTree(inputs=['(.', 'a', '.)', '{', '"*"', 'Factor<.ref result2.>', '(.', 'a', '.)', '|', '"/"', 'Factor<.ref result2.>', '(.', 'a', '.)', '}', '(.', 'result=result1;', '.)', '.'])
#test.generateTree(['E', '.'], ['number', '|', 'test', '(.', 'result = int.Parse(lastToken.Value)', '.)', '.'])
#test.generateTree(['E', '.'], ['(', 'Number<.ref result.>', '|', '"("', 'Expression<. ref result.>', '")"', ')', '.'])
#test.calculateFirst()
#test.calculateFollow()
#print(test.childs)
#print((test.translate()))
