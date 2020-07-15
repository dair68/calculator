# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 23:05:31 2020

@author: Grant Huang
"""

import re

#evaluates a mathematical expression
#@param expression - a string consisting of the expression
#returns a string with answer to expression or error message
def evaluate(expression):
    #parentheses
    if "(" in expression or ")" in expression:
        #checking parentheses syntax
        if not correctParentheses(expression):
            return "syntax error"
        
        #expression is of form ([number])
        if isNumber(expression):
            return str(parseFloat(expression))
        
        pattern = r"\([^\(\)]*?\)"
        matches = re.findall(pattern, expression)
        print(matches)
        newExpression = expression
        
        #computing expressions
        for part in matches:
            inside = part[1:-1]
            
            #parentheses does not contain number literal
            if not isNumber(inside):
                num = evaluate(inside)
            
                #error
                if not isNumber(num):
                    return num if errorMessage(num) else "syntax error" 
            
                print(num)
                newExpression = newExpression.replace(inside, num)
                print(newExpression)
            
        #simplifying occured
        if newExpression != expression:
            return evaluate(newExpression)
        
        expandedExpression = addMultiSymbols(expression)
        #multiplication symbols added
        if(expandedExpression != expression):
            return evaluate(expandedExpression)
    
    #addition
    if "+" in expression:
        print("adding")
        terms = expression.split("+")
        total = 0
        
        #adding
        for term in terms:
            part = evaluate(term)
            
            #error
            if not isNumber(part):
                return part if errorMessage(part) else "syntax error"  
            
            total += parseFloat(part)
            
        return str(total)
    
    subPattern = r"(?<=[^^(/*-])-"
    
    #subtraction
    if re.search(subPattern, expression):
        print("subtracting")
        terms = re.split(subPattern, expression)
        total = 0
        
        #subtracting
        for i in range(len(terms)):
            part = evaluate(terms[i])
            
            #error
            if not isNumber(part):
                return part if errorMessage(part) else "syntax error" 
            elif i == 0:
                total = parseFloat(part)
            else:
                total -= parseFloat(part)
                
        return str(total)
    
    #multiplication
    if "*" in expression:
        print("multiplying")
        factors = expression.split("*")
        product = 1
        
        #multiplying expressions together
        for f in factors:
            part = evaluate(f)
            
            #error
            if not isNumber(part):
                return part if errorMessage(part) else "syntax error"
            
            product *= parseFloat(part)
            
        return str(product)
         
    #division
    if "/" in expression:
        print("dividing")
        parts = expression.split("/")
        quotient = 0
        
        #dividing expressions
        for i in range(len(parts)):
            part = evaluate(parts[i])
            
            #error
            if not isNumber(part):
                return part if errorMessage(part) else "syntax error"
        
            #setting number as dividend or dividing if possible
            if i == 0:
                quotient = parseFloat(part)
            elif parseFloat(part) == 0:
                return "divide by 0 error"
            else:
                quotient /= parseFloat(part)
                
        return str(quotient)
    
    #exponent
    if "^" in expression:
        print("exponentiation")
        parts = expression.split("^")
        answer = evaluate(parts[-1])
        
        #error
        if not isNumber(answer):
                return answer if errorMessage(answer) else "syntax error"
        
        #raising powers
        for i in range(len(parts)-2, -1, -1):
            baseString = parts[i]
            base = baseString
            
            #simplifying base if needed
            if not isNumber(base):
                base = evaluate(baseString)
            
            #error
            if not isNumber(base):
                return base if errorMessage(base) else "syntax error"
    
            a = parseFloat(base)
            b = parseFloat(answer)
            
            #base surrounded by parentheses
            if base[0] == "(" and base[-1] == ")":
                answer = str(a ** b)
            else:
                answer = str(-((-a) ** b)) if a < 0 else str(a ** b)
            
        return answer
    
    return expression if isNumber(expression) else "error. can't compute"
        
        
#checks if a string is a calculator error message
#@param string - string in question
#returns true if string is a recorded error message
def errorMessage(string):
    messages = ["syntax error", "error. can't compute", "divided by 0 error"]
    return string in messages

#checks if a string is a number
#@param numString - string in question
#returns true if string is a number or number surrounded by parentheses
def isNumber(numString):
    testString = numString
    
    #string of form ([number])
    if len(numString) >= 2:
        if numString[0] == "(" and numString[-1] == ")":
            testString = numString[1:-1]
    
    try:
        float(testString)
        return True
    except ValueError:
        return False
    
#parses float from string, if possible
#@param numString - string in question
#returns number contained in number string or string of form ([number])
def parseFloat(numString):
    trimmedString  = numString
    
    #string of form ([number])
    if numString[0] == "(" and numString[-1] == ")":
        trimmedString = numString[1:-1]
        
    return float(trimmedString)

#checks if the parentheses in expression follow correct syntax
#@param string - string in question
#returns true if parentheses are balanced and in proper order
def correctParentheses(string):
    left = 0
    right = 0
    #checking for correct parentheses syntax
    for char in string:
        if char == "(":
            left += 1
        elif char == ")":
            right +=1
            
        #syntax error
        if right > left:
            return False
        
    return right == left

#adds multiplication symbols to expression if possible. 
#@param expression - string with mathematical expression
#returns new string with * operator added. ex: (2)4 -> (2)*4
def addMultiSymbols(expression):
    leftPattern = r"(?<=[^\s^(+*/-])\("
    #indexes = [m.start() for m in re.finditer(pattern1, expression)]    
    #print(indexes)
    newExpression = ""
    start = 0
    
    #adding operators to new expression
    for match in re.finditer(leftPattern, expression):
        index = match.start()
        newExpression = newExpression[:start + 1] + expression[start:index] + "*"
        start = index
    
    newExpression = newExpression + expression[start:]
    print(newExpression)
    
    rightPattern = r"\)(?=[^\s^)+*/-])"
    finalExpression = ""
    start = 0
    
    #adding operators to final expression
    for match in re.finditer(rightPattern, newExpression):
        index = match.start()
        finalExpression = finalExpression[:start + 2] + newExpression[start:index + 1] + "*"
        start = index + 1
        
    finalExpression = finalExpression + newExpression[start:]
    print(finalExpression)
    
    return finalExpression