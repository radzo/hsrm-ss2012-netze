# usr/bin/python
# -*- coding: utf-8 -*-

import os

"""
    liest einen Pfad ein unnd liefert ein Dictionary zurueck. Der Pfad wird
    zerstueckelt und bildet die Schluessel. Der Wert ist das Aenderungsdatum
    /gruppe/ordner/text.dat -> dict[gruppe][ordner][text.dat] = Datum
"""
def readPath(path):    
    dirList = {}
    
    cList = os.listdir(path + '/')
    cList.sort()    
    
    for sFile in cList:
        if sFile == ".svn":
            continue
        
        joined_path = os.path.join(path, sFile)
        if os.path.isdir(joined_path):
            dirList[sFile] = readPath(joined_path)
        elif os.path.isfile(joined_path):
            dirList[sFile] = os.stat(joined_path).st_mtime
    
    return dirList

"""
    Erhaelt ein Dictionary zum Schreiben, ein aktuelles Dict zum Abgleich und
    die ID vom zu vergleichenden Dict. Geht das neue Dict rekursiv durch und
    vergleicht alle Dateien und fuegt neue Dateien mit dem Urheber in die Liste
"""
def rekMerge(mList, dic, x):
    
    # durchlaufe alle Dateien in der aktuellen Ebene
    for sFile in dic:
        # falls die Datei ein Ordner ist, gehe rekursiv hinein
        if type(dic[sFile]) is dict:
            if not mList.has_key(sFile):
                mList[sFile] = {}
            rekMerge(mList[sFile], dic[sFile], x)
        # falls es die Datei noch nicht gibt, lege sie an
        elif not mList.has_key(sFile):
            mList[sFile] = [[dic[sFile], x], ]
        # falls es die Datei schon gibt, aber die aktuelle neuer ist, ersetze
        else:
            mList[sFile] += [[dic[sFile], x], ]
            mList[sFile] = sorted(mList[sFile], reverse=True)
    return mList

def mergeDicts(dicLis, ips):
    mList = {}
    x = 0
    
    for dic in dicLis:
        mList = rekMerge(mList, dic, ips[x])
        x += 1
        
    return mList
