import csv
import traceback

import sys, os,traceback

def getLibText(data,lang):

    transDict = {}
    f = open(os.path.join(os.getcwd(),'translations/lib_translations_text.csv'),'r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 2:
        transDict[str(text[0])] = text[1]
      else:
        transDict[str(text[0])] = text[2]

    libintro_txt = transDict['1']
    libstatus_txt = transDict['2']
    libinfra_txt = transDict['3']
    libtxn_txt = transDict['4']
    libtxnlevel_txt = transDict['6']
    libtxnlang_txt = transDict['5']
    libneighbours_txt = transDict['10']
    libexp_txt = transDict['11']
    source_txt = transDict['8']
    collab_txt = transDict['13']
    logo_link = transDict['12']

    data['libintro_txt'] = libintro_txt
    data['libstatus_txt'] = libstatus_txt
    data['libinfra_txt'] = libinfra_txt
    data['libtxn_txt'] = libtxn_txt
    data['libtxnlevel_txt'] = libtxnlevel_txt
    data['libtxnlang_txt'] = libtxnlang_txt
    data['libneighbours_txt'] = libneighbours_txt
    data['libexp_txt'] = libexp_txt
    data['source_txt'] = source_txt
    data['collab_txt'] = collab_txt
    data['logo_link'] = logo_link 

    if int(data["lib_count"]) > 0:
      keys = data["lib_status"].keys()
      donated_count = 0
      for key in keys:
        if len(key.strip())> 0:
          if key in ['Not Working','No Information Obtained']:
            donated_count = donated_count + int(data["lib_status"][key])
          else:
            if key == 'Handed over':
              donated_count = donated_count + int(data["lib_status"][key])
            data["lib_status"][transDict[key]] = data["lib_status"][key]
          del data["lib_status"][key]
      data["lib_status"][transDict["Total Donated"]] = donated_count
      keys = data["lib_summary"].keys()
      for key in keys:
        data["lib_summary"][transDict[key]] = data["lib_summary"][key]
        del data["lib_summary"][key]
      libexp_txt = libexp_txt + formatIndian(35000*data["library_exp"]) + '.'
      data['libexp_txt'] = libexp_txt
#---------------------- Neighbours
    neighbours = data["neighbours_lib"].keys()
    if neighbours:
      neighbours.remove(data['const_name'])
      neighbourslib_txt = '<br/>' + data['const_name'] + ' ' + transDict['9'] + ', '.join(neighbours) + '. ' + transDict['7']
      data['libneighbours_txt'] = neighbourslib_txt 
    return data

def formatIndian(inputNum) :
  prefStr = ''
  outputString = ''
  minus = ''
  suf = ''
  lastThree = ''
  try:
    inputString = str(inputNum)
    if '.' in inputString:
      numberArray = inputString.split('.', 2)
      pref = int(numberArray[0])
      suf = numberArray[1]
    else:
      pref = inputString
      suf = ''
    outputString = ''
    minus = ''
    if pref < 0:
      minus = '-'
    prefStr = str(pref)
    if len(prefStr) > 3 :
      lastThree = prefStr[len(prefStr)-3: len(prefStr)]
      prefStr = prefStr[0: len(prefStr)-3]
    if len(prefStr) % 2 > 0 :
      outputString = outputString + prefStr[0:1] + ','
      prefStr = prefStr[1: len(prefStr)]

    while (len(prefStr) >= 2) :
      outputString = outputString +  prefStr[0:2] + ','
      prefStr = prefStr[2:len(prefStr)]

    outputString = minus + outputString +  lastThree + suf
    return outputString
  except:
    print 'Error occurred'
    print "Unexpected error:", sys.exc_info()
    traceback.print_exc(file=sys.stdout)
    return 'NaN'
