from pdogex import *
from parser import *

expression = "c*:a#b"
if __name__ == '__main__':
    exp, aut = convert_expression_in_PA(expression, "./expressao.jflap")
    print(aut.execute('accb'))

obj = pdogex()
obj.compile("a:(b#c)")

print(obj.replace_all('meu nome é bac bac bac', "nada"))