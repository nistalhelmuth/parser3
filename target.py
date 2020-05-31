from utils.dfa import DFA
from utils.evaluate import evaluate, Node

#CHARACTERS
letter = DFA('X!i!w!G!B!J!Z!H!h!o!S!m!a!c!n!K!t!r!e!l!N!Q!U!v!y!A!E!F!R!C!W!P!Y!b!u!z!I!D!V!q!d!j!p!g!T!M!f!L!k!s!x!O')
digit = DFA('2!5!7!4!8!0!1!6!3!9')
tab = DFA('\t')
eol = DFA('\n')

#KEYWORDS
keywords = {}
keywords["while"] = "while"
keywords["do"] = "do"
keywords["if"] = "if"

#TOKENS
ident = DFA('letter{letter!digit}', {'letter': letter, 'digit': digit})
number = DFA('digit{digit}', {'digit': digit})

tokens = {'ident': (ident, 'A', [], True),'number': (number, 'A', [], False),}
file = open('./inputs/sum.txt', 'r')
text = Node(''.join(file.read().splitlines()))
file.close()
evaluate(text, tokens, keywords)
