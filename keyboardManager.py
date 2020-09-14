import time

import keyboard


class keyboardManager():
    def __init__(self, actions):
        self.action = ''
        self.block = False
        self.actions = actions

    def executeInput(self):
        if self.block or len(self.action) == 0:
            return
        if self.action[len(self.action) - 1:] == '+':
            self.action = self.action[:-1]

        keyboard.press(self.action)
        time.sleep(0.5)
        keyboard.release(self.action)

    def addAction(self, gesture):
        if gesture == 'nothing':
            return
        if gesture == 'palm_close':
            self.block = True
            return
        self.action += self.actions[gesture] + '+'

    def updateActions(self, actions):
        self.actions = actions
