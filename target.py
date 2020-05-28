from utils.dfa import DFA
from utils.evaluate import evaluate, Node

#CHARACTERS
letterLo = DFA('s!b!f!x!a!h!q!w!y!g!o!j!z!p!l!e!v!r!i!n!t!c!d!k!u!m')
letterUp = DFA('T!L!X!K!D!M!G!U!Y!W!J!B!Q!Z!A!S!E!N!F!P!V!O!C!H!R!I')
letter = DFA('s!T!L!X!K!b!D!M!G!U!Y!f!W!x!J!a!h!q!w!y!B!Q!g!Z!o!j!A!z!S!p!l!E!e!N!F!v!r!P!V!O!i!n!C!t!H!c!d!k!u!m!R!I')
vowels = DFA('O!i!a!u!E!e!I!U!o!A')
consonants = DFA('s!T!L!X!K!b!D!M!G!Y!f!W!x!J!h!q!w!y!B!Q!g!Z!j!z!S!p!l!N!F!v!r!P!V!n!C!t!H!c!d!k!m!R')
digit = DFA('7!8!6!3!0!9!2!4!5!1')
sign = DFA('+!-')
hexdigit = DFA('7!8!6!C!3!A!D!E!0!9!B!2!4!F!5!1')
tab = DFA('\t')
eol = DFA('\n')
space = DFA(' ')
whitespace = DFA('\n!\r! !\t')

#KEYWORDS
keywords = {}
keywords["if"] = "if"
keywords["while"] = "while"
keywords["switch"] = "switch"
keywords["do"] = "do"
keywords["for"] = "for"
keywords["exit"] = "exit"
keywords["class"] = "class"
keywords["import"] = "import"
keywords["from"] = "from"
keywords["try"] = "try"
keywords["except"] = "except"
keywords["lambda"] = "lambda"

#TOKENS
string = DFA('letter{letter}', {'letter': letter})
name = DFA('letterUp(letterLo){letterLo}', {'letterUp': letterUp, 'letterLo': letterLo})
var = DFA('letter{letter|digit}digit', {'letter': letter, 'digit': digit})
signInt = DFA('[sign]digit{digit}', {'sign': sign, 'digit': digit})
int = DFA('digit{digit}', {'digit': digit})
float = DFA('digit{digit}"."digit{digit}', {'digit': digit})
hexnumber = DFA('hexdigit{hexdigit}"(H)"', {'hexdigit': hexdigit})
space = DFA('whitespace{whitespace}', {'whitespace': whitespace})

tokens = {'string': (string, 'A', [], True),'name': (name, 'A', [], True),'var': (var, 'A', [], True),'signInt': (signInt, 'A', [], False),'int': (int, 'A', [], False),'float': (float, 'A', [], False),'hexnumber': (hexnumber, 'A', [], True),'space': (space, 'A', [], False),}
file = open('./inputs/input1.txt', 'r')
text = Node(''.join(file.read().splitlines()))
file.close()
evaluate(text, tokens, keywords)
