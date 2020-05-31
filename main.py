import string
import string as strDefinition
from utils.dfa import DFA
from utils.evaluate import Node
from utils.translate import Translator
from utils.tree import LL
import re

class Token():
    def __init__(self, code, val, pos=None, charPos=None, line=None, col=None):
        self.code = code                   # token code (EOF has the code 0)
        self.val = val                     # token value
        self.pos = pos                     # token position in the source text // (in bytes starting at 0)
        self.charPos = charPos             # token position in the source text // (in characters starting at 0)
        self.line = line                   # line number (starting at 1)
        self.col = col                     # column number (starting at 1)

class Buffer():
    def __init__ (self, stream):
        def clean(phrase):
            buffer = ''
            line = []
            flag = True
            specialFlag = True
            i = 0
            while i < len(phrase):
                letter = phrase[i]
                if (letter == '(' and phrase[i+1:i+2] == '.') and specialFlag:
                    specialFlag = False
                    if buffer != '':
                        line.append(buffer)
                    buffer = ''
                    line.append(letter+'.')
                    i += 1
                elif (letter == '.' and phrase[i+1:i+2] == ')') and not specialFlag:
                    specialFlag = True
                    if buffer != '':
                        line.append(buffer)
                    buffer = ''
                    line.append('.'+phrase[i+1:i+2])
                    i += 1
                elif (letter == '<' and phrase[i+1:i+2] == '.') and specialFlag:
                    specialFlag = False
                    buffer = buffer + letter
                elif (letter == '.' and phrase[i+1:i+2] == '>') and not specialFlag:
                    specialFlag = True
                    line.append(buffer+'.'+phrase[i+1:i+2])
                    buffer = ''
                    i += 1
                elif (letter == '"' or letter == "'") and specialFlag:
                    if flag:
                        if buffer != '':
                            line.append(buffer)
                        buffer = letter
                    else:
                        line.append(buffer+letter)
                        buffer= ''
                    flag = not flag
                elif (letter == '(' or letter == '[' or letter == '{' or letter == '|' or letter == ')' or letter == ']' or letter == '}') and flag and specialFlag:
                    if buffer != '':
                        line.append(buffer)
                    line.append(letter)
                    buffer = ''
                elif letter == ' ' and flag and specialFlag:
                    if buffer != '':
                        line.append(buffer)
                    buffer = ''
                elif letter == '.' and phrase[i+1:i+2] == '.' and flag and specialFlag:
                    if buffer != '':
                        line.append(buffer)
                    buffer = ''
                    line.append('..')
                    i += 1
                elif letter == '.' and flag and specialFlag:
                    if buffer != '':
                        line.append(buffer)
                    buffer = letter
                elif letter in ['+', '-', '='] and flag and specialFlag:
                    if buffer != '':
                        line.append(buffer)
                    buffer = ''
                    line.append(letter)
                else:
                    buffer = buffer + letter
                i += 1

            if buffer != '':
                line.append(buffer)
            print(line)
            return line

        file = open(stream, 'r')
        words = []
        for text in file.readlines():
            line = text.split()
            #print(' '.join(line))
            words = words + clean(' '.join(line))
        file.close()
        self.currentWord =  Node(words)
        self.nextWord = self.currentWord
    
    def definition(self, value):
        code = None
        if value == '':
            code = 0
        if value == '.':
            code = 0
        if value == '=':
            code = 0
        if value == '+':
            code = 0
        if value == '-':
            code = 0
        elif value == 'COMPILER':
            code = 50
        elif value == 'CHARACTERS':
            code = 60
        elif value == 'KEYWORDS':
            code = 70
        elif value == 'TOKENS':
            code = 80
        elif value == 'PRODUCTIONS':
            code = 90
        elif value == 'END':
            code = 100
        else:
            code = -1
        return code

    def read(self):
        word = self.currentWord.value
        self.currentWord = self.currentWord.next
        self.nextWord = self.currentWord
        return Token(self.definition(word), word)

    def peek(self):
        word = self.nextWord.value
        self.nextWord = self.nextWord.next
        return Token(self.definition(word), word)
    
    def resetPeek(self):
        self.nextWord = self.currentWord

class Scanner():

    def __init__(self, file):
        self.buffer = Buffer(file)

        self.any = DFA('{ANY}')
        self.hexdigit = DFA('!'.join(list(set('0123456789').union(set('ABCDEF')))))
        self.letter = DFA('a!b!c!d!e!f!g!h!i!j!k!l!m!n!o!p!q!r!s!t!u!v!w!x!y!z!A!B!C!D!E!F!G!H!I!J!K!L!M!N!O!P!Q!R!S!T!U!V!W!X!Y!Z')
        self.digit = DFA('0!1!2!3!4!5!6!7!8!9')
        self.ident = DFA('letter{letter!digit}', {'letter': self.letter, 'digit': self.digit})
        self.string =  DFA('"{noQuote}"')
        self.number =  DFA('digit{digit}', {'digit': self.digit})
        self.char =  DFA("' noApostrophe '")
        self.equal =  DFA("=")
        self.period =  DFA(".")
        self.plus =  DFA("+")
        self.minus =  DFA("-")

        self.characters = {}
        self.keywords = {}
        self.tokens = {}
        self.productions = {}


    def CHARACTERS(self):
        '''
            ["CHARACTERS" {SetDecl}]
            SetDecl = ident '=' Set.
            Set = BasicSet { ('+'!'-') BasicSet }.
            BasicSet = string ! ident ! Char [".." Char].
            Char = char ! "CHR" '(' number ')'.
        '''

        def letterList (start, end):
            a = ' ' + string.ascii_uppercase + string.ascii_lowercase
            direction = 1 if start < end else -1
            return a[a.index(start):a.index(end) + direction:direction]

        characters = {}
        token = self.peek()
        state = 0

        periods = DFA('. .')
        #startCHR = DFA("C H R '(' number* ')'", {'number': self.number})
        startCHR = DFA("C H R")
        signs = DFA('+!-')
        Char = DFA("char!Char", {'char': self.char, 'Char': startCHR})
        basicset = DFA('string!ident!Char[".." Char]', {'string': self.string, 'ident': self.ident, 'Char':Char})
        mySet = DFA('BasicSet{Signs BasicSet}',{'Signs': signs, 'BasicSet': basicset})

        M = {
            'S': [
                (self.string, ['B', "S'"]), 
                (startCHR, ['B', "S'"]),
                (self.ident, ['B',"S'"]), 
                (Char, ['B', "S'"])
                ], 
            'B': [
                (startCHR, ['C', "B'"]), 
                (self.string, ['s']), 
                (self.ident, ['i']), 
                (Char, ['C', "B'"])], 
            "B'": [
                (periods, ['..', 'C']), 
                (self.period, []), 
                (self.plus, []), 
                (self.minus, [])
                ],
            'C': [
                (self.char, ['c']), 
                (startCHR, ['CHR', '(', 'n', ')'])
                ],
            "S'": [
                (self.plus, ['+', 'B', "S'"]), 
                (self.minus, ['-', 'B', "S'"]), 
                (self.period, []), 
                (periods, []) 
                ]
        }
        while token.code < 50:
            token = self.scan()
            
            if state == 0 and self.ident.check(token.val):
                name = token.val
                state += 1
                token = self.peek()
                values = []
            elif state == 1 and self.equal.check(token.val):
                state += 1
                token = self.peek()            
            elif state == 2 and self.period.check(token.val):
                inputs = values + ['.']
                a = inputs[0]
                stack = ['S', '.']
                x = stack[0]
                error = True
                totalCharacters = set()
                operator = ''
                while 0 < len(stack) and error:
                    if x in ['i', 's', 'c', '+', '-', '..', 'CHR', '(' , ')', 'n']:
                        terminal = stack.pop(0)
                        value = inputs.pop(0)
                        if x == 'i' and value in characters.keys():
                            character = characters[value]
                        elif x == 's':
                            character = set(value[1:-1])
                        elif x == 'c':
                            character = set(value[1:-1])
                        elif x == 'n':
                            #character = set(chr(int(value[4:-1])))
                            character = set(chr(int(value)))
                        
                        if x in ['+','-','..']:
                            operator = x
                        elif operator == '' and x not in  ['CHR','(', ')']:
                            totalCharacters = character
                        elif operator == '+' and x not in  ['CHR','(', ')']:
                            operator = ''
                            totalCharacters = totalCharacters.union(character)
                        elif operator == '-' and x not in  ['CHR','(', ')']:
                            operator = ''
                            totalCharacters = totalCharacters.difference(character)
                        elif operator == '..' and x not in  ['CHR','(', ')']:
                            operator = ''
                            totalCharacters = set(letterList(list(totalCharacters)[0], list(character)[0]))
                        a = inputs[0]
                    elif x in M.keys():
                        for option in M[x]:
                            if option[0].check(a):
                                stack.pop(0)
                                stack = option[1] + stack
                                break
                    else:
                        error = False
                        
                    x = stack[0]
                    #print(stack)
                    #print(inputs)
                    #input()

                if error:
                    print("error")
                else:
                    characters[name] = totalCharacters
                    print("CHARACTER ", name, "ADDED")
                state = 0
                token = self.peek()

            elif state == 2 :
                values.append(token.val)
                token = self.peek()
            else: 
                errors = {0:'ident', 1:'equal', 2:'set', 3:'period'}
                print('CHARACTERS error: read', token.val, 'expected ', errors[state])
                state = 0

        print(characters)
        return characters

    def KEYWORDS(self):
        '''
            ["KEYWORDS" {KeyworDecl}]
            KeywordDecl = ident '=' string '.'
        '''
        keywords = {}
        token = self.peek()
        state = 0
        while token.code < 50:
            token = self.scan()
            if state == 0 and self.ident.check(token.val):
                name = token.val
                state += 1
                token = self.peek()
            elif state == 1 and self.equal.check(token.val):
                state += 1
                token = self.peek()
            elif state == 2 and self.string.check(token.val):
                value = token.val
                state += 1
                token = self.peek()
            elif state == 3 and self.period.check(token.val):
                keywords[value[1:-1]] = name
                print("KEYWORD ", name, "ADDED")
                state = 0
                token = self.peek()
            else: 
                errors = {0:'ident', 1:'equal', 2:'string', 3:'period'}
                print('KEYWORDS error: read', token.val, 'expected ', errors[state])
                state = 0
        
        print(keywords)
        return keywords
    
    def TOKENS(self):
        '''
            ["TOKENS" {TokenDecl}]
            TokenDecl = ident ['=' TokenExpr ] ["EXCEPT KEYWORDS"] '.'.
            TokenExpr = TokenTerm {'|' TokenTerm }.
            TokenTerm = TokenFactor {TokenFactor}
            TokenFactor = Symbol ! '(' TokenExpr ) ! '[' TokenExpr ] ! '{' TokenExpr '}'.
            Symbol = ident ! string ! char
        '''
        tokens = {}
        token = self.peek()
        state = 0

        parentesisA = DFA("(")
        parentesisC = DFA(")")
        corchetesA = DFA("[")
        corchetesC = DFA("]")
        llaveA = DFA("{")
        llaveC = DFA("}")
        orDFA = DFA("|") 
        excep = DFA("EXCEPT")
        keys = DFA("KEYWORDS")

        M = {
            'E': [
                (self.string, ['T',"E'"]), 
                (self.ident, ['T',"E'"]), 
                (self.char, ['T',"E'"]), 
                (llaveA, ['T',"E'"]), 
                (parentesisA, ['T',"E'"]), 
                (corchetesA, ['T',"E'"]), 
                (parentesisC, ['T',"E'"]), 
                (corchetesC, ['T',"E'"]), 
                (llaveC, ['T',"E'"])
                ], 
            "E'": [
                (orDFA, ['|','T',"E'"]), 
                (parentesisC, []), 
                (corchetesC, []), 
                (llaveC, []), 
                (self.period, [])
                ], 
            'T': [
                (self.string, ['F', "T'"]), 
                (self.ident, ['F', "T'"]), 
                (self.char, ['F', "T'"]), 
                (llaveA, ['F', "T'"]), 
                (parentesisA, ['F', "T'"]), 
                (corchetesA, ['F', "T'"])], 
            "T'": [
                (self.string, ['F', "T'"]), 
                (self.ident, ['F', "T'"]), 
                (self.char, ['F', "T'"]), 
                (llaveA, ['F', "T'"]), 
                (parentesisA, ['F', "T'"]), 
                (corchetesA, ['F', "T'"]), 
                (parentesisC, []), 
                (corchetesC, []), 
                (llaveC, []), 
                (self.period, []), 
                (orDFA, [])
                ], 
            'F': [
                (self.string, ['S']), 
                (self.ident, ['S']), 
                (self.char, ['S']), 
                (parentesisA, ['(', 'E', ')']), 
                (corchetesA, ['[', 'E', ']']), 
                (llaveA, ['{', 'E', '}'])
                ],
            'S': [
                (self.string, ['s']), 
                (self.ident, ['i']), 
                (self.char, ['c'])
                ],
        }

        while token.code < 50:
            token = self.scan()
            if state == 0 and self.ident.check(token.val):
                name = token.val
                state += 1
                token = self.peek()
                values = []
                flag = False
            elif state == 1 and self.equal.check(token.val):
                state += 1
                token = self.peek()
            elif state == 2 and excep.check([token.val]):
                token = self.peek()
                if keys.check([token.val]):
                    self.scan()
                    flag = True
                token = self.peek()
            elif state == 1 and self.period.check(token.val):
                dependencies = [name]
                token = [name]
                tokens[name] = ("true", token, dependencies)
                state = 0
                token = self.peek()
            elif state == 2 and self.period.check(token.val):
                inputs = values + ['.']
                a = inputs[0]
                stack = ['E', '.']
                x = stack[0]
                error = True
                token = []
                dependencies = []
                while 0 < len(stack) and error:
                    if x in ['i', 's', 'c', '|', '(', ')', '[', ']', '{', '}']:
                        terminal = stack.pop(0)
                        value = inputs.pop(0)
                        if x == 'i' and value not in dependencies:
                            dependencies = dependencies + [value]
                        if x == '|':
                            token = token + ['!']
                        else:
                            token = token + [value]
                        a = inputs [0]
                    elif x in M.keys():
                        for option in M[x]:
                            if option[0].check(a):
                                stack.pop(0)
                                stack = option[1] + stack
                                break
                    else:
                        error = False
                    x = stack[0]
                    #print(stack)
                    #print(inputs)
                    #input()
                
                if error:
                    print("error")
                else:
                    if flag:
                        tokens[name] = (True, token, dependencies)
                    else:
                        tokens[name] = (False, token, dependencies)

                    print("KEYWORD ", name, "ADDED")

                state = 0
                token = self.peek()
            elif state == 2:
                values.append(token.val)
                token = self.peek()
            else: 
                self.resetPeek()
                print('TOKEN error', token.val, token.code, state)
                state = 0
        print(tokens)
        return tokens
    
    def PRODUCTIONS(self):
        '''
            Production = ident [Attributes] [SemAction] '=' Expression '.'.
            Expression = Term { '|' Term }.
            Term = Factor {Factor}
            Factor = Symbol [Attributes] ! '(' Expression ')' ! '[' Expression ']' ! '{' Expression '}' ! SemAction.
            Attributes = "<." {ANY} ".>"
            SemAction = "(." {ANY} ".)"
        '''
        productions = {}
        token = self.peek()
        state = 0

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
        identExtra = DFA("ident < .{ANY}. >", {'ident': self.ident})

        M = {
            'E': [
                (self.string, ['T',"E'"]),
                (identExtra,['T',"E'"]), 
                (self.ident, ['T',"E'"]), 
                (self.char, ['T',"E'"]), 
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
                (self.period, [])
                ],
            'T': [
                (self.string, ['F', "T'"]),
                (identExtra,['F', "T'"]), 
                (self.ident, ['F', "T'"]), 
                (self.char, ['F', "T'"]), 
                (llaveA, ['F', "T'"]), 
                (parentesisA, ['F', "T'"]), 
                (semLeft, ['F', "T'"]),
                (corchetesA, ["F'", "T'"]),
                ],
            "T'": [
                (self.string, ['F', "T'"]), 
                (identExtra,['F', "T'"]), 
                (self.ident, ['F', "T'"]), 
                (self.char, ['F', "T'"]), 
                (llaveA, ['F', "T'"]), 
                (semLeft, ['F', "T'"]),
                (parentesisA, ['F', "T'"]), 
                (corchetesA, ["F'", "T'"]), 
                (parentesisC, []), 
                (corchetesC, []), 
                (llaveC, []), 
                (semRight, []),
                (orDFA, []),
                (self.period, []), 
                ],
            'F': [
                (self.string, ['S']),
                (identExtra,['S']), 
                (self.ident, ['S']), 
                (self.char, ['S']), 
                (parentesisA, ['(', 'E', ')']), 
                (corchetesA, ['[', 'E', ']']), 
                (llaveA, ['{', 'E', '}']),
                (semLeft, ['(.', 'x', '.)']), 
                ],
            "F'": [
                (corchetesA, ['[', 'E', ']']), 
            ],
            'S': [
                (self.string, ['s']), 
                (identExtra, ['ia']), 
                (self.ident, ['i']), 
                (self.char, ['c']),
                ],
        }

        while token.code < 50:
            token = self.scan()
            if state == 0 and (self.ident.check(token.val) or identExtra.check(token.val)):
                production = {}
                if self.ident.check(token.val):
                    name = token.val
                    params = '(self)'
                else:
                    index = token.val.find('<.')

                    name = token.val[:index]
                    params = '(self, '+token.val[index:].replace('<.', '').replace('.>',')')
                    production['return'] = ','.join(re.findall(r'ref+\s([\w\-]+)', params))
                    params = params.replace('ref','').replace(' ','')

                production['params'] = params

                token = self.peek()
                production['actions'] = ''
                if semLeft.check(token.val):
                    token = self.scan()
                    token = self.scan()
                    production['actions'] = token.val
                    token = self.scan()
                    token = self.peek()
                state += 1
                values = []

            elif state == 1 and self.equal.check(token.val):
                state += 1
                token = self.peek()

            elif state == 2 and self.period.check(token.val):
                test = LL(M, ['i', 'ia', 's', 'c', 'a', 'x', '|', '(', ')', '[', ']', '{', '}', '<.', '.>', '(.', '.)'])
                test.generateTree(['E', '.'], values + ['.'])
                #test.calculateFirst()
                #test.calculateFollow()
                production['content'] = test
                print(production)
                productions[name] = production
                print('PRODUCTION', name, 'ADDED')
                
                state = 0
                token = self.peek()
            
            elif state == 2:
                values.append(token.val)
                token = self.peek()
            else:
                self.resetPeek()
                print('PRODUCTIONS error', token.val, token.code, state)
                state = 0

        print(productions)
        return productions

    def COMPILER(self):
        token = self.scan()
        if token.val != 'COMPILER':
            print("expected compiler")
            return
        token = self.scan()
        print(token.val)
        if (self.ident.check(token.val)):
            print('COMPILER started')
            name = token.val
            token = self.scan()
            print(token.val)
            if (token.val == 'CHARACTERS'):
                print('CHARACTERS started')
                self.characters = self.CHARACTERS()
                token = self.scan()
                print('CHARACTERS ended')
            if (token.val == 'KEYWORDS'):
                print('KEYWORDS started')
                self.keywords = self.KEYWORDS()
                token = self.scan()
                print('KEYWORDS ended')
            if (token.val == 'TOKENS'):
                print('TOKENS started')
                self.tokens = self.TOKENS()
                token = self.scan()
                print('TOKENS ended')
            if (token.val == 'PRODUCTIONS'):
                print('PRODUCTIONS started')
                self.productions = self.PRODUCTIONS()
                token = self.scan()
                print('PRODUCTIONS ended')
            if (token.val == 'END'):
                token = self.scan()
                if(token.val == (name+'.')):
                    print("succesfully exit")
                else:
                    print("unexpected END")
            print('COMPILER ended')
        else:
            print("unexpected compiler name")
        return self.characters, self.keywords, self.tokens, self.productions
    
    def scan(self):
        token = self.buffer.read()
        return token
        
    def peek(self):
        return self.buffer.peek()
    
    def resetPeek(self):
        self.buffer.resetPeek()
    
    def goCharacters(self):
        f = open('./testGoal.py', "w")
        f.write('from utils.evaluate import Node\n')
        f.write("\n")
        f.write('class PRODUCTIONS():\n')
        f.write("\tdef __init__(self, tokens):\n")
        f.write("\t\tself.currentToken =  Node(tokens)\n")
        f.write("\t\tself.nextToken = self.currentToken\n")
        f.write("\n")
        f.write("\tdef Expect(self, dfa):\n")
        f.write("\t\ttoken = self.nextToken.value\n")
        f.write("\t\tif dfa.check(token):\n")
        f.write("\t\t\treturn True\n")
        f.write("\t\treturn False\n")
        f.write("\n")
        f.write("\tdef Get(self, dfa):\n")
        f.write("\t\ttoken = self.currentToken.value\n")
        f.write("\t\tself.currentToken = self.currentToken.next\n")
        f.write("\t\tself.nextToken = self.currentToken\n")
        f.write("\t\tif dfa.check(token):\n")
        f.write("\t\t\treturn token\n")
        f.write("\t\treturn False\n")
        f.write("\n")

        firsts = {}
        for name in list(self.productions.keys())[::-1]:
            firsts[name] = self.productions[name]['content'].calculateFirst(firsts)
        print(firsts)
        for name in self.productions.keys():
            self.productions[name]['content'].calculateFollow()
            words = self.productions[name]['content'].translate2()[0]
            f.write("\tdef %s%s:\n" % (name, self.productions[name]['params']))
            for line in words:
                f.write("\t\t%s" % (line))
            if 'return' in self.productions.keys():
                f.write("\treturn %s\n" % (self.productions[name]['return']))
            f.write("\n")
            
        f.close()
    

def main():
    scanner = Scanner("./tests/test1.txt")
    (c, k, t, p) = scanner.COMPILER()
    scanner.goCharacters()
    #translator = Translator(c, k, t, p)
    #translator.translate('target', './inputs/sum.txt')

main()