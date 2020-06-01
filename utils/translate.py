
class Translator():
    def __init__(self, characters, keywords, tokens, productions):
        self.characters = characters
        self.keywords = keywords
        self.tokens = tokens
        self.productions = productions
    
    def CHARACTERS(self, f):
            f.write("#CHARACTERS\n")
            for key in self.characters.keys():
                values = []
                for value in self.characters[key]:
                    values = values + [value.__repr__()[1:-1]]
                if values != '':
                    f.write("%s = DFA('%s')\n" % (key ,'!'.join(list(values))))
            f.write("\n")
        
    def KEYWORDS(self, f):
        f.write("#KEYWORDS\n")
        f.write("keywords = {}\n")
        for key in self.keywords.keys():
            f.write('keywords["%s"] = "%s"\n' % (key, self.keywords[key]))
        f.write("\n")
    
    def TOKENS(self, f):
        f.write("#TOKENS\n")
        for key in self.tokens.keys():
            dependencies = ''
            for char in self.tokens[key][2]:
                if dependencies == '':
                    dependencies = "'"+char+"': "+char
                else:
                    dependencies = dependencies+", '"+char+"': "+char
            f.write('%s = DFA("%s", {%s})\n' % (key, ''.join(self.tokens[key][1]), dependencies))
        f.write("\n")
        f.write("tokens = {")
        for key in self.tokens.keys():
            f.write("'%s': (%s, 'A', [], %r)," % (key, key, self.tokens[key][0]))
        f.write("}")
        f.write("\n")
    
    def PRODUCTIONS(self, f):
        
        f.write("\n")
        f.write('class PRODUCTIONS():\n')
        f.write("\tdef __init__(self, tokens):\n")
        f.write("\t\tself.currentToken =  Node(tokens)\n")
        f.write("\t\tself.nextToken = self.currentToken\n")
        f.write("\t\tself.last = None\n")
        f.write("\n")
        f.write("\tdef Expect(self, dfa):\n")
        f.write("\t\tself.last = self.nextToken.value\n")
        f.write("\t\tif self.last != None and dfa.check(self.last):\n")
        f.write("\t\t\treturn True\n")
        f.write("\t\treturn False\n")
        f.write("\n")
        f.write("\tdef Get(self, dfa):\n")
        f.write("\t\tself.last = self.currentToken.value\n")
        f.write("\t\tself.currentToken = self.currentToken.next\n")
        f.write("\t\tself.nextToken = self.currentToken\n")
        f.write("\t\tif self.last != None and dfa.check(self.last):\n")
        f.write("\t\t\treturn self.last\n")
        f.write("\t\treturn False\n")
        f.write("\n")

        firsts = {}
        for name in list(self.productions.keys())[::-1]:
            firsts[name] = self.productions[name]['content'].calculateFirst(firsts)
        #print(firsts)
        for name in self.productions.keys():
            self.productions[name]['content'].calculateFollow()
            words = self.productions[name]['content'].translate()[0]
            f.write("\tdef %s%s:\n" % (name, self.productions[name]['params']))
            for line in words:
                f.write("\t\t%s" % (line))
            if 'return' in self.productions[name].keys():
                f.write("\t\treturn %s\n" % (self.productions[name]['return']))
            f.write("\n")

    def translate(self, target, inputFile, start):
        f = open('./%s.py' % (target), "w")
        f.write("from utils.dfa import DFA\n")
        f.write("from utils.evaluate import evaluate, Node\n")
        f.write('from utils.evaluate import Node\n')
        f.write("\n")
        if self.characters != {}:
            self.CHARACTERS(f)
        if self.keywords != {}:
            self.KEYWORDS(f)
        if self.tokens != {}:
            self.TOKENS(f)
        if self.productions != {}:
            self.PRODUCTIONS(f)
        
        #Read file
        f.write("file = open('%s', 'r')\n" % (inputFile))
        f.write("text = Node(''.join(file.read().splitlines()))\n")
        f.write("file.close()\n")

        f.write("words = evaluate(text, tokens, keywords)\n")
        f.write("test = PRODUCTIONS(words)\n")
        f.write("test.%s()" % start)
        f.close()