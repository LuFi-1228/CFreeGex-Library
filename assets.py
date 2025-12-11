def make_label(a, b, c):
    return f"({a}, {b}, {c})"

def operating(symbol):
    if symbol!='(' and symbol!=')' and not operator(symbol):
        return True
    return False

def operator(symbol):
    if symbol=='+' or symbol=='.' or symbol=='*' or symbol==':' or symbol=='#' or symbol==';':
        return True
    return False

def precedence(operator):
    if operator=='+':
        return 0
    if operator=='.':
        return 1
    if operator=='*': 
        return 2
    if operator==':':
        return 3
    if operator==';':
        return 4
    if operator=='#':
        return 5
    return -1