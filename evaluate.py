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
            
            total += float(part)
            
        return str(total)
    
    #subtraction
    if re.search(r"(?<=[^/*-])-", expression):
        print("subtracting")
        terms = re.split(r"(?<=[^/*-])-", expression)
        total = 0
        
        #subtracting
        for i in range(len(terms)):
            part = evaluate(terms[i])
            
            #error
            if not isNumber(part):
                return part if errorMessage(part) else "syntax error" 
            elif i == 0:
                total = float(part)
            else:
                total -= float(part)
                
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
            
            product *= float(part)
            
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
                quotient = float(part)
            elif float(part) == 0:
                return "divide by 0 error"
            else:
                quotient /= float(part)
                
        return str(quotient)
    
    return expression if isNumber(expression) else "error. can't compute"
        
        
#checks if a string is a calculator error message
#@param str - string in question
#returns true if string is a recorded error message
def errorMessage(str):
    messages = ["syntax error", "error. can't compute", "divided by 0 error"]
    return str in messages

#checks if a string is a number
#@param str - string in question
#returns true if string is a number, false if clearly not
def isNumber(str):
    try:
        float(str)
        return True
    except ValueError:
        return False