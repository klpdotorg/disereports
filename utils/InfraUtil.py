import csv
import traceback

import sys, os,traceback

def getInfraText(data,lang,constype):
    transDict = {}
    f = open(os.path.join(os.getcwd(),'translations/infra_translations_text.csv'),'r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 2:
        transDict[str(text[0])] = text[1]
      else:
        transDict[str(text[0])] = text[2]
    if constype == 4:
       transDict['1']=transDict['22']
       transDict['19']=transDict['28']
    elif constype == 5:
       transDict['1']=transDict['23']
       transDict['19']=transDict['29']
    elif constype == 6:
       transDict['1']=transDict['24']
       transDict['19']=transDict['30']
    intro_txt_str=transDict['1'] 
    ang_infra_txt_str=transDict['17']
    dise_facility_txt_str=transDict['17']
    #lib_infra_txt_str=transDict['17']
    source_txt_str=transDict['13']
    note_txt_str=transDict['18']
    neighbours_txt_str=transDict['17']
    conclusion_txt_str=transDict['21']
    
    data['intro_txt'] = intro_txt_str 
    data['source_txt'] = source_txt_str 
    data['note_txt'] = note_txt_str 
    data['conclusion_txt'] = conclusion_txt_str

    """if int(data["infra_count"]) > 0:
      ang_infra_txt_str = transDict['2'] + str(data["infra_count"]) +  transDict['3'] + str(data["inst_counts"]["abs_preschcount"]) + transDict['4'] 
      for each in data["ang_infra"]:
        keys = data["ang_infra"][each].keys()
        for key in keys:
          #if key in ['walls','floor','roof']:
          #  data["ang_infra"][each][transDict[key]] = [str(100 - int(data["ang_infra"][each][key][0])), data["ang_infra"][each][key][1]]
          #else:
          data["ang_infra"][each][transDict[key]] = [data["ang_infra"][each][key][0],data["ang_infra"][each][key][1]]
          del data["ang_infra"][each][key]
    data["ang_infra_txt"] = ang_infra_txt_str"""

    if int(data["dise_count"]) > 0:
      dise_facility_txt_str = transDict['5'] + str(data["dise_count"]) +  transDict['6'] + str(data["inst_counts"]["abs_schcount"]) + transDict['7'] 
      for each in data["dise_facility"]:
        keys = data["dise_facility"][each].keys()
        for key in keys:
          if key in ['classroom_repair']:
            data["dise_facility"][each][transDict[key]] = [str(100 - int(data["dise_facility"][each][key][0])),str(100- int(data["dise_facility"][each][key][1]))]
          else:
            data["dise_facility"][each][transDict[key]] = [data["dise_facility"][each][key][0],data["dise_facility"][each][key][1]]
          del data["dise_facility"][each][key]

    data["dise_facility_txt"] = dise_facility_txt_str
    #if int(data["lib_count"]) > 0:
    #  lib_infra_txt_str = transDict['8'] + transDict['9'] + str(data["lib_count"]) +  transDict['10'] + str(data["inst_counts"]["abs_schcount"]) + transDict['11'] 
    #  data["lib_infra_txt"] = lib_infra_txt_str
    #  keys = data["lib_status"].keys()
    #  for key in keys:
    #    data["lib_status"][transDict[key]] = data["lib_status"][key]
    #    del data["lib_status"][key]
    #  keys = data["lib_summary"].keys()
    #  for key in keys:
    #    data["lib_summary"][transDict[key]] = data["lib_summary"][key]
    #    del data["lib_summary"][key]

#---------------------- Neighbours
    if("neighbours_anginfra" in data.keys()):
      newDict = {}
      for each in data["neighbours_anginfra"].keys():
        keys = each.split('|')
        transStr = transDict[keys[1]].split(';')
        #if keys[1] in ['walls','floor','roof']:
        #  newInnerDict ={}
        #  for const in data["neighbours_anginfra"][each].keys():
        #    newInnerDict[const] = str(100-int(data["neighbours_anginfra"][each][const]))
        #  newDict[keys[0] +'|' + transStr[1]] = newInnerDict
        #else:
        newDict[keys[0] +'|' + transStr[1]] = data["neighbours_anginfra"][each]
      data["neighbours_anginfra"] = newDict
    if("neighbours_dise" in data.keys()):
      newDict = {}
      #print data["neighbours_dise"]
      for each in data["neighbours_dise"].keys():
        keys = each.split('|')
        transStr = transDict[keys[1]].split(';')
        #print transDict[keys[1]]
        if keys[1] in ['classroom_repair']:
          newInnerDict ={}
          for const in data["neighbours_dise"][each].keys():
            newInnerDict[const] = str(100-int(data["neighbours_dise"][each][const]))
          newDict[keys[0] +'|' + transStr[1].decode('utf-8')] = newInnerDict
        else:
          newDict[keys[0] +'|' + transStr[1].decode('utf-8')] = data["neighbours_dise"][each]
      data["neighbours_dise"] = newDict
      
      
      neighbours = data["neighbours_dise"][data["neighbours_dise"].keys()[0]].keys()
      if neighbours:
        neighbours.remove(data['const_name'])
        neighbours_txt_str = '<br/>' + str(data['const_name']) + ' ' + transDict['19'] + ', '.join([str(x) for x in neighbours]) + '. ' + transDict['20']
    data['neighbours_txt'] = neighbours_txt_str 
    print "hello"
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
