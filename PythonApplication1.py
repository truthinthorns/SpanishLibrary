import re
from os import system
from lxml import html
import requests


file = open("file.txt","r+")

choice = ""
listOfWords = []
listOfTranslations = []
listOfNotes = []
    
def ConvertFileToList():
    var = file.readlines()
    pattern = r"[', ']"
    for i in var:
        var2 = str(i.split())
        if("Word:" in var2):
            word = var2[11:len(var2)-2]
            if(re.search(pattern,word)):
                newWord = word.replace("', '"," ")
                listOfWords.append(newWord)
            else:
                listOfWords.append(word)
        elif("Translation:" in var2):
            sepTrans = var2[18:len(var2)-2]
            if(sepTrans.startswith("to', ")):
                sepTrans2 = sepTrans.replace("'","")
                sepTrans3 = sepTrans2.replace(",,",",")
                sepTrans4 = str(sepTrans3[0:2])
                sepTrans5 = str(sepTrans3[4:])
                sepTrans6 = sepTrans4 + " " + sepTrans5

                if(re.search(", to, ", sepTrans6,)):
                    sepTrans7 = sepTrans6.replace(", to, ", ", to ")
                    listOfTranslations.append(sepTrans7)
                elif(re.search(", ",sepTrans6)):
                    sepTrans8 = sepTrans6.replace(", ", " ")
                    listOfTranslations.append(sepTrans8)
                else:
                    listOfTranslations.append(sepTrans6)
            elif(not sepTrans.startswith("to', ")):
                if(re.search("', '",sepTrans)):
                    sepTrans9 = sepTrans.replace("', '", " ")
                    listOfTranslations.append(sepTrans9)
                else:
                    listOfTranslations.append(sepTrans)
        elif("Notes:" in var2):
            NotesMod1 = var2[12:len(var2)-2]
            NotesMod2 = NotesMod1.replace("', '"," ")
            listOfNotes.append(NotesMod2)
    return

def WriteSingleToFile():
    word = ""
    while word != "quit":
        word = input(str("Enter the word: "))
        if word != "quit":
            file.write("\nWord: " + word+ "\n")
            translation = input(str("Enter the translation: "))
            file.write("Translation: " + translation+ "\n")
            notes = input(str("Enter any notes on the word: "))
            file.write("Notes: " + notes + "\n")
            listOfWords.append(word)
            listOfTranslations.append(translation)
            listOfNotes.append(notes)
        else:
            break

def WriteListToFile(file, word,translation,notes):
    file.write("\nWord: " + word+ "\n")
    file.write("Translation: " + translation+ "\n")
    file.write("Notes: " + notes + "\n\n")

def SearchFile():
    search = ""
    while search != "quit":
        search = input(str("Enter WORD to search for: "))
        if search != "quit":
            if search in listOfWords:
                index = listOfWords.index(search)
                print("Word: " + listOfWords[index] + "\n" + "Translation: " + listOfTranslations[index] + 
                  "\n" + "Notes: " + listOfNotes[index] + "\n")
                return search
            else:
                 print("\"" + search + "\"" +" is not in your library")
        else:
            break

def SearchForWord():
    search = ""
    while search != "quit":
        search = input(str("Enter WORD to search for: "))
        if search != "quit":
            if search in listOfWords:
                index = listOfWords.index(search)
                return (listOfWords[index],listOfTranslations[index],listOfNotes[index],index)
            else:
                 print("\"" + search + "\"" +" is not in your library")
        else:
            break
    return (None,None,None,None)

def ChangeEntry():
        word,translation,notes,index = SearchForWord()
        if(word != None):
           part = str(input("Which part would you like to change? ((W)ord,(T)ranslation,(N)otes,(C)ancel)\n"))
           if part == "w":
               newWord = str(input("Enter the new word:\n"))
               confirm = str(input("Are you sure you want to change \"" + word + "\" to \"" + newWord + "\" ? ((Y)es/(N)o)"))
               if(confirm == "y"):
                   listOfWords[index] = newWord
                   file = open("file.txt","w")
                   for i in range(len(listOfWords)):
                       WriteListToFile(file, listOfWords[i],listOfTranslations[i],listOfNotes[i])
                   file.close()
           elif part == "t":
               newTranslation = str(input("Enter the new translation:\n"))
               confirm = str(input("Are you sure you want to change \"" + translation + "\" to \"" + newTranslation + "\" ? ((Y)es/(N)o)"))
               if(confirm == "y"):
                   listOfTranslations[index] = newTranslation
                   file = open("file.txt","w")
                   for i in range(len(listOfWords)):
                       WriteListToFile(file, listOfWords[i],listOfTranslations[i],listOfNotes[i])
                   file.close()
           elif part == "n":
               newNotes = str(input("Enter the new notes:\n"))
               confirm = str(input("Are you sure you want to change \"" + notes + "\" to \"" + newNotes + "\" ? ((Y)es/(N)o)"))
               if(confirm == "y"):
                   listOfNotes[index] = newNotes
                   file = open("file.txt", "w")
                   for i in range(len(listOfWords)):
                       WriteListToFile(file, listOfWords[i],listOfTranslations[i],listOfNotes[i])
                   file.close()
           elif part == "c":
               return
           return
        else:
           return

def DeleteEntry():
        word,translation,notes,index = SearchForWord()
        if(word != None):
            print("Word: " + word + "\n" + "Translation: " + translation + 
                          "\n" + "Notes: " + notes + "\n")
            answer = str(input("Are you sure you want to delete this entry? ((Y)es/(N)o)"))
            if answer == "y":
                listOfWords.remove(word)
                listOfTranslations.remove(translation)
                listOfNotes.remove(notes)
                file = open("file.txt","w").close()
                file = open("file.txt","r+")
                file.truncate(0)
                for i in range(len(listOfWords)):
                        WriteListToFile(file, listOfWords[i],listOfTranslations[i],listOfNotes[i])
            else:
                return
        return

def GetWordAndPage():
    word = str(input("Enter the word to look for: "))
    word = word.replace(" ","%20")
    return('http://www.spanishdict.com/translate/' + word + "/")

def GetContentFromPage(page):
    pg = requests.get(page)
    if(pg.ok):
        tree = html.fromstring(pg.content)
        searchedWord = tree.xpath('//h1[@class="source-text"]/text()')
        searchedTranslation = tree.xpath('//a[@class="dictionary-neodict-translation-translation"]/text()')
        good = True
        if(searchedTranslation == []):
            searchedWord = tree.xpath('//textarea[@class="search-form-input"]/text()')
            searchedTranslation = tree.xpath('//div[@class="spelling-row"]/text()')
            good = False
    return (searchedWord,searchedTranslation,good)

def FormatSearch(y,z,good):
    a = y
    a = str(a)
    a = a.replace("['","")
    a = a.replace("']","")
    a = a.replace("', '"," ")
    b = z
    b = str(b)
    if(not good):
        print("Search:    " + a)
        b = b[2:63]
        print(b+"\n")
    else:
        b = b.replace("', '","\n")
        b = b.replace("['","")
        b = b.replace("']","")

        print("Search:    " + a)
        print("\nTranslation(s):\n")
        print(b + "\n")

ConvertFileToList()
    
while True:
        spam = input(str("(R)ead contents  \t(W)rite to file  \t(S)earch  \t(C)hange Entry  \t(D)elete Entry  \t(L)ook Up Word  \t(Q)uit\n"))
        choice = spam.lower()
        if choice == "r":
            system('cls')
            if not file.closed:
                file.close()
            file = open("file.txt","r+")
            read = file.read()
            print(read)
            continue
        elif choice == "w":
            system('cls')
            WriteSingleToFile()
            continue
        elif choice == "s":
            system('cls')
            SearchFile()
        elif choice == "c":
            system('cls')
            ChangeEntry()
        elif choice == "d":
            system('cls')
            DeleteEntry()
        elif choice == "l":
            system('cls')
            x  = GetWordAndPage()
            y,z,good = GetContentFromPage(x)
            search = FormatSearch(y,z,good)
        elif choice == "q":
              break
if not file.closed:
    file.close()