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
        self.equationHist = []
        self.prevAnswers = []
        self.answer = "42"
        self.equationIndex = -1
        defaultFont = font.nametofont("TkDefaultFont")
        defaultFont.configure(family="Fixedsys", size=10)
        self.pack()
        self.createWidgets()
        
    #creates child widgets
    def createWidgets(self):
        self.display = tk.Entry(self, width=30)
        self.display.grid(row=0, column=0, columnspan=6)
        self.display.focus_set()
        
        self.answerLine = tk.Label(self, text="=" + self.answer, width=20, anchor="e")
        self.answerLine.grid(row=1, column=0, columnspan=6)
        
        self.enterButton = tk.Button(self, text="Enter", height=1, width=5)
        self.enterButton.grid(row=7, column=4, columnspan=2)
        self.enterButton.bind("<Button-1>", lambda e: self.compute())
        
        self.decimalButton = tk.Button(self, text=".", height=1, width=3)
        self.decimalButton.bind("<Button-1>", self.appendSymbol)
        self.decimalButton.grid(row=7, column=1)
        
        self.leftParenButton = tk.Button(self, text="(", height=1, width=3)
        self.leftParenButton.bind("<Button-1>", self.appendSymbol)
        self.leftParenButton.grid(row=3, column=1)
        
        self.rightParenButton = tk.Button(self, text=")", height=1, width=3)
        self.rightParenButton.bind("<Button-1>", self.appendSymbol)
        self.rightParenButton.grid(row=3, column=2)
        
        self.answerButton = tk.Button(self, text="Ans", height=1, width=3)
        self.answerButton.bind("<Button-1>", self.appendSymbol)
        self.answerButton.grid(row=7, column=2)
        
        self.clearButton = tk.Button(self, text="Clear", height=1, width=5)
        self.clearButton.grid(row=6, column=4, columnspan=2)
        self.clearButton.bind("<Button-1>", lambda e: self.display.delete(0, "end"))
        
        self.deleteButton = tk.Button(self, text="Del", height=1, width=5)
        self.deleteButton.grid(row=2, column=4, columnspan=2)
        self.deleteButton.bind("<Button-1>", lambda e: self.deleteSymbol())
        
        self.createArrowButtons()
        self.createNumButtons()
        self.createOperatorButtons()
            
    #creates number buttons
    def createNumButtons(self):
        self.numButtons = []
        for i in range(10):
            button = tk.Button(self, height=1, width=3)
            
            #placing 0 button in bottom left
            if i == 0:
                button.grid(row = 7, column = 0)
            else:
                button.grid(row = (9-i)//3 + 4, column = (i-1)%3)
            
            button["text"] = i
            button.bind("<Button-1>", self.appendSymbol)
            self.numButtons.append(button)
            
    #creates arithmetic operators
    def createOperatorButtons(self):
        self.operatorButtons = {}
        uniSymbols = [94, 247, 215, 43, 45]
        keys = ["exp", "div", "mult", "add", "sub"]
        
        for i in range(len(keys)):
            button = tk.Button(self, height=1, width=3)
            button["text"] = chr(uniSymbols[i])
            button.grid(row = i+3, column = 3)
            button.bind("<Button-1>", self.appendSymbol)
            self.operatorButtons[keys[i]] = button
            
    #creates the four arrow buttons
    def createArrowButtons(self):
        self.leftButton = tk.Button(self, text="\u2190", height=1, width=2)
        self.leftButton.grid(row=4, column=4)
        self.leftButton.bind("<Button-1>", lambda e : self.shiftCursor(-1))
        
        self.rightButton = tk.Button(self, text="\u2192", height=1, width=2)
        self.rightButton.grid(row=4, column=5)
        self.rightButton.bind("<Button-1>", lambda e : self.shiftCursor(1))
          
        self.upButton = tk.Button(self, text="\u2191", height=1, width=5)
        self.upButton.grid(row=3, column=4, columnspan=2)
        self.upButton.bind("<Button-1>", lambda e : self.displayPrevEquation())
        
        self.downButton = tk.Button(self, text="\u2193", height=1, width=5)
        self.downButton.grid(row=5, column=4, columnspan=2)
        self.downButton.bind("<Button-1>", lambda e : self.displayNextEquation())
        
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
        
    #deletes symbol behind current location of text cursor
    def deleteSymbol(self):
        index = self.display.index("insert")
        
        #Ans variable precedes text cursor
        if self.display.get()[-3:] == "Ans":
            self.display.delete(index - 3, index)
        else:
            self.display.delete(index - 1)
        
    #shifts insertion cursor from its current position
    #@param n - number of spaces shifted forwards if positive, backwards if negative
    def shiftCursor(self, n):
        index = self.display.index("insert")
        self.display.icursor(index + n)
        
    #obtains and displays prev equation in equation history, if possible
    def displayPrevEquation(self):
        #at least one equation in history
        if self.equationIndex > 0:
            self.equationIndex -= 1
            self.updateDisplay(self.equationHist[self.equationIndex])
            self.answerLine["text"] = "=" + self.prevAnswers[self.equationIndex]
            self.updateAnswer()
            
    #obtains and displays next equation in equation history, if possible
    def displayNextEquation(self):
        #next equation to find
        if self.equationIndex < len(self.equationHist) - 1:
            self.equationIndex += 1
            self.updateDisplay(self.equationHist[self.equationIndex])
            self.answerLine["text"] = "=" + self.prevAnswers[self.equationIndex]
            self.updateAnswer()
        
    #evaluates expression and displays answer or error message
    def compute(self):
        text = self.display.get()
        subbedString = text.replace("Ans", "(" + str(self.answer) + ")")
        message = ev.evaluate(subbedString)
        print(message)
        
        #checking if answer is number
        if ev.isNumber(message):
            floatString = str(float(message))
            print(floatString)
            
            #removing trailing .0 for integers
            if floatString[-2:] == ".0":
                message = floatString[:-2]
        
        self.answerLine["text"] = "=" + message
        self.updateAnswer()
        self.equationHist.append(text)
        self.prevAnswers.append(message)
        self.equationIndex = len(self.equationHist) - 1
    
    #updates display with a string
    #@param text - string to be displayed
    def updateDisplay(self, text):
        self.display.delete(0, "end")
        self.display.insert(0, text)
        
    #updates self.answer to what's written on answer line. sets to 42 if error msg
    def updateAnswer(self):
        answerText = self.answerLine["text"][1:]
        self.answer = answerText if ev.isNumber(answerText) else "42"