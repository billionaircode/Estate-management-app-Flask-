import random


def code_gen():

    strpool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    def verifyCode(string):
        confirmationCode = ''
        for i in range(6):
            confirmationCode += string[random.randint(0,len(string)-1)]
        return confirmationCode

    #print(verifyCode(strpool))
