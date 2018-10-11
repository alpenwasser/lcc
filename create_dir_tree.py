#!/usr/bin/env python3

"""
Create simplified directory tree with main categories and one level of subcategories.
"""

import sys
import json
import unicodedata
import re
import pathlib

CATSEP = ' --- ' # separator for category and its description in the directory name
DIRSEP = '/'     # directory path separator

def loadJSON(filepath):
    with open(filepath) as JSONFile:
        JSONData = json.load(JSONFile)
    return JSONData

def getMainCategories(JSONData):
    mainCategories = {}
    for letter in JSONData.keys():
        mainCategories[letter] = JSONData[letter]["description"]
    for letter,description in mainCategories.items():
        print(letter + ' --> ' + mainCategories[letter])

def slugify(value, allow_unicode=False):
    """
    Taken from the Django Project. BSD-style license:
    https://github.com/django/django/blob/master/LICENSE
    https://github.com/django/django/blob/master/django/utils/text.py

    Based on this SO post:
    https://stackoverflow.com/questions/295135/
    """
    """
    Convert to ASCII if 'allow_unicode' is False.  Remove characters that 
    aren't alphanumerics, underscores, spaces, or hyphens.  Convert to 
    lowercase (currently disabled) . Also strip leading and trailing 
    whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    #value = re.sub(r'[^\w\s-]', '', value).strip()#.lower()
    #return re.sub(r'[-\s]+', ' ', value).strip()
    # Strip trailing period because Windows is fucking stupid.
    # https://superuser.com/questions/585097/
    value = re.sub(r'\.$', '', value) 
    return re.sub(r':',' -', value).strip()

def createDirTreeCategories(JSONData):
    dirTreeCats = {}
    for letter in JSONData.keys():
        #print(letter + ' --> ' + JSONData[letter]['description'])

        dirTreeCats[letter] = {}
        dirTreeCats[letter]['description'] = slugify(JSONData[letter]['description'], allow_unicode=True)
        dirTreeCats[letter]['subclasses'] = {}

        for subclassLetter in JSONData[letter]['subclasses'].keys():
            dirTreeCats[letter]['subclasses'][subclassLetter] = slugify(JSONData[letter]['subclasses'][subclassLetter][0]['description'], allow_unicode=True)
            #dirTreeCats[letter]['subclasses'][subclassLetter] = JSONData[letter]['subclasses'][subclassLetter][0]['description']

    #print(json.dumps(dirTreeCats, indent=4))
    return dirTreeCats


def createDirStructure(dirTreeCats, mainDir):
    # https://stackoverflow.com/a/14364249/9105632
    for letter in dirTreeCats.keys():
        #print(letter + ' --> ' + dirTreeCats[letter]['description'])

        path = mainDir + DIRSEP + letter + CATSEP + dirTreeCats[letter]['description']
        #pathlib.Path(path).mkdir(parents=True, exist_ok = True)

        for subletter in dirTreeCats[letter]['subclasses'].keys():
            #print(letter + subletter + ' --> ' + dirTreeCats[letter]['subclasses'][subletter])

            subpath = path + DIRSEP + letter + subletter + CATSEP + dirTreeCats[letter]['subclasses'][subletter]
            pathlib.Path(subpath).mkdir(parents=True, exist_ok = True)

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print("USAGE: \n" + str(sys.argv[0]) + ' [JSON file] [out directory]')
    JSONData = loadJSON(sys.argv[1])
    mainDir = sys.argv[2]

    dirTreeCats = createDirTreeCategories(JSONData)
    createDirStructure(dirTreeCats, mainDir)
