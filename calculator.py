# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:25:54 2020

@author: Grant Huang
"""

import tkinter as tk
import evaluate as ev

class Calculator(tk.Frame):
    #constructor
    #@param master - parent widget
    def __init__(self, master=None):
        #calling parent constructor
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidgets()
        
    #creates child widgets
    def createWidgets(self):
        self.display = tk.Label(self, bg="white", anchor="w")
        self.display.grid(row=0, column=0, columnspan=4)
        
        self.enterButton = tk.Button(self)
        self.enterButton["text"] = "Enter"
        self.enterButton.grid(row=5, column=4)
        self.enterButton.bind("<Button-1>", lambda e : self.compute())
        
        self.decimalButton = tk.Button(self)
        self.decimalButton["text"] = "."
        self.decimalButton.bind("<Button-1>", self.appendSymbol)
        self.decimalButton.grid(row=5, column=1)
        
        self.answerButton = tk.Button(self)
        self.answerButton["text"] = "ans"
        self.answerButton.grid(row=5, column=2)
        
        self.clearButton = tk.Button(self)
        self.clearButton["text"] = "clear"
        self.clearButton.grid(row=4, column=4)
        self.clearButton.bind("<Button-1>", lambda e : self.clearDisplay())
        
        self.createNumButtons()
        self.createOperatorButtons()
            
    #creates number buttons
    def createNumButtons(self):
        self.numButtons = []
        for i in range(10):
            button = tk.Button(self)
            
            #placing 0 button in bottom left
            if i == 0:
                button.grid(row = 5, column = 0)
            else:
                button.grid(row = (9-i)//3 + 2, column = (i-1)%3)
            
            button["text"] = i
            button.bind("<Button-1>", self.appendSymbol)
            self.numButtons.append(button)
            
    #creates operator buttons
    def createOperatorButtons(self):
        self.operatorButtons = {}
        symbols = ["^", "/", "*", "+", "-"]
        keys = ["exp", "div", "mult", "add", "sub"]
        
        for i in range(len(keys)):
            button = tk.Button(self)
            button["text"] = symbols[i]
            button.grid(row = i+1, column = 3)
            button.bind("<Button-1>", self.appendSymbol)
            self.operatorButtons[keys[i]] = button
            
    #appends button's symbol to calculator's display text
    #@param event - event object
    def appendSymbol(self, event):
        button = event.widget
        symbol = button["text"]
        self.display["text"] += str(symbol)
        
    #evaluates expression and displays answer or error message
    def compute(self):
        text = self.display["text"]
        message = ev.evaluate(text)
        self.display["text"] = message
        
    #clears all text from display
    def clearDisplay(self):
        self.display["text"] = ""