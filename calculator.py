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
        defaultFont = font.nametofont("TkDefaultFont")
        defaultFont.configure(family="Fixedsys", size=10)
        self.pack()
        self.createWidgets()
        
    #creates child widgets
    def createWidgets(self):
        #self.display = tk.Label(self, text=" "*20, bg="white", anchor="w")
        self.display = tk.Entry(self)
        self.display.grid(row=0, column=0, columnspan=5)
        
        self.enterButton = tk.Button(self, height=1, width=4)
        self.enterButton["text"] = "Enter"
        self.enterButton.grid(row=5, column=4)
        self.enterButton.bind("<Button-1>", lambda e : self.compute())
        
        self.decimalButton = tk.Button(self, height=1, width=3)
        self.decimalButton["text"] = "."
        self.decimalButton.bind("<Button-1>", self.appendSymbol)
        self.decimalButton.grid(row=5, column=1)
        
        self.leftParenButton = tk.Button(self, height=1, width=3)
        self.leftParenButton["text"] = "("
        self.leftParenButton.bind("<Button-1>", self.appendSymbol)
        self.leftParenButton.grid(row=1, column=1)
        
        self.rightParenButton = tk.Button(self, height=1, width=3)
        self.rightParenButton["text"] = ")"
        self.rightParenButton.bind("<Button-1>", self.appendSymbol)
        self.rightParenButton.grid(row=1, column=2)
        
        self.answerButton = tk.Button(self, height=1, width=3)
        self.answerButton["text"] = "ans"
        self.answerButton.grid(row=5, column=2)
        
        self.clearButton = tk.Button(self, height=1, width=4)
        self.clearButton["text"] = "clear"
        self.clearButton.grid(row=4, column=4)
        self.clearButton.bind("<Button-1>", lambda e : self.display.delete(0, "end"))
        
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
        index = self.display.index("insert")
        self.display.insert(index, displayedChar)
        self.display.xview(index)
        
    #evaluates expression and displays answer or error message
    def compute(self):
        text = self.display.get()
        message = ev.evaluate(text)
        print(message)
        
        #checking if answer is integer to remove trailing .0
        if ev.isNumber(message):
            floatString = str(float(message))
            print(floatString)
            
            #integer
            if floatString[-2:] == ".0":
                message = floatString[:-2]
        
        self.updateDisplay(message)
        
    #updates display with a string. Will leave whitespace unless exceeds 50 chars
    #@param text - string to be displayed
    def updateDisplay(self, text):
        self.display.delete(0, "end")
        self.display.insert(0, text)