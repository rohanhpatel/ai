import sys
import math
import random as rand
import requests
import re
import bs4
from bs4 import BeautifulSoup

class WordLink():
    def __init__(self, word):
        if word[:12] == '/dictionary/':
            self.word = word[12:]
        else:
            self.word = word
        self.link = "https://www.merriam-webster.com/dictionary/" + self.word
    def __str__(self):
        return self.link
    def __repr__(self):
        return "WordLink: " + self.link

def dictEntry(tag):
    return tag.name == 'div' and tag.get('id') != None and tag['id'][:16] == 'dictionary-entry'

def getWordLinkContents(wordLink):
    page = requests.get(wordLink.link)
    soup = BeautifulSoup(page.content, "html.parser")
    wordSections = soup.find_all(dictEntry)
    sectionDict = dict()
    for section in wordSections:
        typ = section.find('h2', class_='parts-of-speech')
        fullType = "direct"
        if typ != None:
            fullType = typ.string.split(" ")[0]
            vg = section.find('div', class_='vg')
            sectionSoup = vg.find_all('div', class_='vg-sseq-entry-item')
            textSearch = ['dtText', 'unText']
        else:
            sectionSoup = [section.find('p', class_="cxl-ref")]
            textSearch = ['text-uppercase']
        combinedBulletList = list()
        linkList = list()
        for bullet in sectionSoup:
            bullEntries = None
            for txts in textSearch:
                bullEntries = bullet.find_all('span', class_=txts)
                if bullEntries != None and bullEntries != list():
                    break
            childList = list()
            for entry in bullEntries:
                separators = [',', ':', ';']
                tmpList = list()
                flat = False
                isSep = False
                for child in entry.children:
                    if isinstance(child, bs4.element.NavigableString):
                        text = child.strip()
                        if text not in separators:
                            if ';' in text:
                                tmpSplit = text.split(';')
                                for elem in tmpSplit:
                                    tmpList.append(elem.strip())
                                flat = True
                            else:
                                tmpList.append(text)
                                if fullType == "direct":
                                    linkList.append(WordLink(text))
                        else:
                            isSep = True
                    elif isinstance(child, bs4.element.Tag):
                        if child.text.strip() not in separators:
                            tmpList.append(child.text.strip())
                            if child.name == 'a':
                                linkList.append(WordLink(child.attrs['href']))
                        else:
                            isSep = True
                    if isSep:
                        if tmpList != list():
                            if '' in tmpList:
                                tmpList.remove('')
                            if not flat:
                                string = ' '.join(tmpList)
                                childList.append(string)
                            else:
                                childList += tmpList
                        tmpList = list()
                        isSep = False
                if tmpList != list():
                    if '' in tmpList:
                        tmpList.remove('')
                    if not flat:
                        string = ' '.join(tmpList)
                        childList.append(string)
                    else:
                        childList += tmpList
            combinedBulletList += childList
        if fullType in sectionDict:
            sectionDict[fullType] += combinedBulletList
        else:
            sectionDict[fullType] = combinedBulletList
        if 'link' in sectionDict:
            sectionDict['link'] += linkList
        else:
            sectionDict['link'] = linkList
    return sectionDict

def parseFile(fileName):
    f = open(fileName, 'r')
    wordList = list()
    for line in f:
        wordList.append(line.strip())
    return wordList

def printWordDefns(wordDefns):
    for word in wordDefns:
        print("------- " + word + " ---------")
        for key in wordDefns[word]:
            print("------- " + key + " --------")
            print(wordDefns[word][key])
        print('\n')
    
def getWordData(fileName):
    words = parseFile(fileName)
    # let's just test words[0] for now
    wordDefns = dict()
    for word in words:
        wordDefns[word] = getWordLinkContents(WordLink(word))
    printWordDefns(wordDefns)
    return wordDefns

def clpFromTo(word1, word2):
    # common letter percentage
    common = 0
    for char in word1:
        if char in word2:
            common += 1
    return float(common)/len(word2)

def main():
    wordDefs = getWordData(sys.argv[1])
    words = list(wordDefs.keys())
    clpDict = dict()
    for i in range(len(words)):
        clpDict[words[i]] = dict()
        for j in range(len(words)):
            if i == j:
                continue
            else:
                clpDict[words[i]][words[j]] = clpFromTo(words[j], words[i])
    
main()
