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
        #checking for balanced parentheses
        if expression.count("(") != expression.count(")"):
            return "syntax error"
        
        pattern = r"\([^\(\)]*?\)"
        matches = re.findall(pattern, expression)
        print(matches)
        newExpression = expression
        
        #computing expressions
        for part in matches:
            inside = part[1:-1]
            num = evaluate(inside)
            
            #error
            if not isNumber(num):
                return num if errorMessage(num) else "syntax error" 
            
            print(num)
            newExpression = newExpression.replace(part, num)
            print(newExpression)
            
        return evaluate(newExpression)
    
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
    
    subPattern = r"(?<=[^^/*-])-"
    
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
            base = evaluate(parts[i])
            
            #error
            if not isNumber(base):
                return base if errorMessage(base) else "syntax error"
    
            a = parseFloat(base)
            b = parseFloat(answer)
            answer = -((-a) ** b) if a < 0 else a ** b
            
        return str(answer)
    
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