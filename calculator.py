# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:25:54 2020

@author: Grant Huang
"""

import tkinter as tk
from tkinter import font
import evaluate as ev

class Calculator(tk.Frame):
    #constructor
    #@param master - parent widget
    def __init__(self, master=None):
        #calling parent constructor
        super().__init__(master)
        self.master = master
        self.lastEquation = ""
        self.hasErrMessage = False
        defaultFont = font.nametofont("TkDefaultFont")
        defaultFont.configure(family="Fixedsys", size=10)
        self.pack()
        self.createWidgets()
        
    #creates child widgets
    def createWidgets(self):
        #self.display = tk.Label(self, text=" "*20, bg="white", anchor="w")
        self.display = tk.Entry(self)
        self.display.grid(row=0, column=0, columnspan=5)
        
        self.enterButton = tk.Button(self, text="Enter", height=1, width=4)
        self.enterButton.grid(row=5, column=4)
        self.enterButton.bind("<Button-1>", lambda e: self.compute())
        
        self.decimalButton = tk.Button(self, text=".", height=1, width=3)
        self.decimalButton.bind("<Button-1>", self.appendSymbol)
        self.decimalButton.grid(row=5, column=1)
        
        self.leftParenButton = tk.Button(self, text="(", height=1, width=3)
        self.leftParenButton.bind("<Button-1>", self.appendSymbol)
        self.leftParenButton.grid(row=1, column=1)
        
        self.rightParenButton = tk.Button(self, text=")", height=1, width=3)
        self.rightParenButton.bind("<Button-1>", self.appendSymbol)
        self.rightParenButton.grid(row=1, column=2)
        
        self.answer = 42
        self.answerButton = tk.Button(self, text="Ans", height=1, width=3)
        self.answerButton.bind("<Button-1>", self.appendSymbol)
        self.answerButton.grid(row=5, column=2)
        
        self.clearButton = tk.Button(self, text="Clear", height=1, width=4)
        self.clearButton.grid(row=4, column=4)
        self.clearButton.bind("<Button-1>", lambda e: self.clearDisplay())
        
        self.deleteButton = tk.Button(self, text="Del", height=1, width=4)
        self.deleteButton.grid(row=1, column=4)
        self.deleteButton.bind("<Button-1>", lambda e: self.deleteSymbol())
        
        self.createNumButtons()
        self.createOperatorButtons()
            
    #creates number buttons
    def createNumButtons(self):
        self.numButtons = []
        for i in range(10):
            button = tk.Button(self, height=1, width=3)
            
            #placing 0 button in bottom left
            if i == 0:
                button.grid(row = 5, column = 0)
            else:
                button.grid(row = (9-i)//3 + 2, column = (i-1)%3)
            
            button["text"] = i
            button.bind("<Button-1>", self.appendSymbol)
            self.numButtons.append(button)
            
    #creates operators
    def createOperatorButtons(self):
        self.operatorButtons = {}
        uniSymbols = [94, 247, 215, 43, 45]
        keys = ["exp", "div", "mult", "add", "sub"]
        
        for i in range(len(keys)):
            button = tk.Button(self, height=1, width=3)
            button["text"] = chr(uniSymbols[i])
            button.grid(row = i+1, column = 3)
            button.bind("<Button-1>", self.appendSymbol)
            self.operatorButtons[keys[i]] = button
            
    #appends button's symbol to calculator's display text
    #@param event - event object
    def appendSymbol(self, event):
        chart = {chr(247): "/", chr(215):"*"}
        
        button = event.widget
        symbol = button["text"]
        displayedChar = chart[symbol] if symbol in chart.keys() else symbol
        
        #calculator has error message displayed
        if self.hasErrMessage:
           self.clearErrorMessage()
        else:
            index = self.display.index("insert")
            self.display.insert(index, displayedChar)
            self.display.xview(index)
        
    #deletes symbol behind current location of text cursor
    def deleteSymbol(self):
        #calculator has error message displayed
        if self.hasErrMessage:
            self.clearErrorMessage()
        else:
            index = self.display.index("insert")
        
            #Ans variable precedes text cursor
            if self.display.get()[-3:] == "Ans":
                self.display.delete(index - 3, index)
            else:
                self.display.delete(index - 1)
        
    #evaluates expression and displays answer or error message
    def compute(self):
        #calculator displays error message
        if self.hasErrMessage:
            self.clearErrorMessage()
        else:
            text = self.display.get()
            self.lastEquation = text
            subbedString = text.replace("Ans", "(" + str(self.answer) + ")")
            message = ev.evaluate(subbedString)
            print(message)
        
            #checking if answer is number
            if ev.isNumber(message):
                self.answer = float(message)
                floatString = str(float(message))
                print(floatString)
            
                #removing trailing .0 for integers
                if floatString[-2:] == ".0":
                    message = floatString[:-2]
            else:
                self.hasErrMessage = True
        
            self.updateDisplay(message)
    
    #updates display with a string. Will leave whitespace unless exceeds 50 chars
    #@param text - string to be displayed
    def updateDisplay(self, text):
        self.display.delete(0, "end")
        self.display.insert(0, text)
            
    #removes displayed error message and replaces it with last inputted equation
    def clearErrorMessage(self):
         self.updateDisplay(self.lastEquation)
         self.hasErrMessage = False
         
    #wipes away everythin on display. if wiping error message, displays prev equation
    def clearDisplay(self):
        #display has error message
        self.clearErrorMessage() if self.hasErrMessage else self.display.delete(0, "end")