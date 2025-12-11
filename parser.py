from Stack import Stack
from assets import operator, operating, precedence
from automata_generator import *

def explicit_concatenation(infix):
    lenght=len(infix)
    string=""
    i=0
    while i<lenght:
        if infix[i]=='\\' and i<lenght-1:
            if i>0 and infix[i-2]!='\\' and (infix[i-1]=='(' or infix[i-1]=='+' or infix[i-1]=='.' or infix[i-1]==':' or infix[i-1]=='#'):
                string=string+infix[i]+infix[i+1]
            else:
                if string!="":
                    string=string+"."
                string=string+infix[i]+infix[i+1]
            i=i+1
        else: 
            if i>1 and infix[i-2]=='\\' and operating(infix[i]):
                string=string+"."+infix[i]
            else:
                if ((operating(infix[i]) or infix[i]=='(')) and (operating(infix[i-1]) or infix[i-1]==')' or infix[i-1]=='*' or infix[i-2]=='\\'):
                    if string=="":
                        string=infix[i]
                    else:
                        string=string+"."+infix[i]
                else: 
                    string=string+infix[i]
        i=i+1
    return string

def infix_to_postfix(infix):
    postfix=""
    stack = Stack()
    flag=0
    
    for item in infix:
        if item=='\\':
            postfix+=item
            flag=1
        else:
            if flag==1:
                postfix+=item
                flag=0
            else:
                if operating(item):
                    postfix+=item
                else:
                    if item=='(':
                        stack.push(item)
                    else:
                        if item == '*':
                            postfix += item
                        elif item==')':
                            if stack.len()>0:
                                while stack.top()!='(':
                                    postfix+=stack.pop()
                                    if stack.len()==0:
                                        return -1
                                stack.pop()
                            else:
                                return -2
                        else:
                            if operator(item):
                                while stack.len()>0 and precedence(stack.top())>=precedence(item) and item!='#':
                                    if item in ['.', '+', '*']:
                                        return -4
                                    postfix+=stack.pop()
                                stack.push(item)
    while stack.len()>0:
        if operator(stack.top()):
            postfix+=stack.pop()
        else:
            return -3
    return postfix

def execute_postfix(postfix):
    stack=[]
    i=0
    while i<len(postfix):
        if postfix[i]=='\\':
            stack.append(base(postfix[i+1]))
            i=i+1
        else: 
            if operating(postfix[i]):
                stack.append(base(postfix[i]))
            else: 
                if len(stack)>0:
                    op2=stack.pop()
                    if postfix[i]=='*': 
                        stack.append(kleene_star(op2))
                    else: 
                        if len(stack)==0:
                            print("A1")
                            break
                        else:
                            op1=stack.pop()
                            if postfix[i]=='+': 
                                stack.append(union(op1,op2))
                            else:
                                if postfix[i]=='.':  
                                    stack.append(concatenation(op1,op2))
                                else:
                                    if postfix[i]=='#':
                                        stack.append(sharp(op1,op2))
                                    else:
                                        if postfix[i]==':':
                                            stack.append(two_points(op1,op2))
                                        elif postfix[i]==';':
                                            stack.append(sharp(op1,op2))
                else: 
                    print("A2")
                    break
        i=i+1
    if len(stack)==1:
        return stack.pop()
    
    else:
        print(stack)
        print("A4")
        return -1

def convert_expression_in_PA(expression,path=None):
    response = None
    postfix=infix_to_postfix(explicit_concatenation(expression))

    if postfix==-1:
        print("Está faltando fechar algum parêntese")
        response = "Está faltando fechar algum parêntese"
    else:
        if postfix==-2:
            print("Estão faltando operandos")
            response = "Estão faltando operandos"
        else:
            if postfix==-3:
                print("Está faltando abrir algum parêntese")
                response = "Está faltando abrir algum parêntese"
            elif postfix==-4:
                print("Expressão inválida!")
                response = "Expressão inválida!"
            else: 
                print(postfix)
                automata = execute_postfix(postfix)
                if automata == -1:
                    print("Erro na execução da expressão")
                    return False
                automata.print_image()
                if(path!=None):
                    path = './static/'+path
                    automata.save_xml(path)
                stack_vars_reset()
                return postfix, automata
 
    return False, response