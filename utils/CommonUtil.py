import web
import psycopg2
import traceback
import sys, os,traceback
import db.KLPDB
import db.Queries_dise


#connection = db.KLPDB.getConnection()
#cursor = connection.cursor()
cursor = db.KLPDB.getWebDbConnection1()
class CommonUtil:

  def constituencyData(self,constype,constid):
    data = {}
    result = []
    neighbours = []
    constype_str = constype 
    try:
      #constype_str = "mp"
      #if constype == 1:
      #  constype_str = "mp"
      #elif constype == 2:
      #  constype_str = "mla"
      #elif constype == 3:
      #  constype_str = "corporator"
      if constype_str!='boundary':
          result = cursor.query(db.Queries_dise.getDictionary(constype)[constype_str + '_const_details'],{'s':constid})
          for row in result:
            data['const_name'] = row.const_ward_name.strip() if row.const_ward_name != None else ''
            data['const_type'] = row.const_ward_type.strip() if row.const_ward_type != None else ''
            data['const_code'] = row.elec_comm_code if row.elec_comm_code != None else ''
            data['const_rep'] = row.current_elected_rep.strip() if row.current_elected_rep != None else ''
            data['const_party'] = row.current_elected_party.strip() if row.current_elected_party != None else ''
            data['const_dist'] = row.current_elected_rep.strip() if row.current_elected_rep != None else ''
            data['const_blck'] = row.current_elected_party.strip() if row.current_elected_party != None else ''
            if row.neighbours != None:
              neighbours = row.neighbours.strip().split('|')
              #neighbours.append(row.elec_comm_code)
          return [data,neighbours,constype_str]
      else:
          result = cursor.query(db.Queries_dise.getDictionary(constype)[constype_str + '_const_details'],{'s':constid})
          detail={}
          for row in result:
            detail[row.dist_id]=[row.district,'District','District']
            detail[row.blck_id]=[row.block,'Block','Project']
            detail[row.clst_id]=[row.clust,'Cluster','Circle']
            data['const_name'] = detail[int(constid[0])][0].upper()
            data['const_type'] = detail[int(constid[0])][row.type].upper()
            data['const_code'] = constid
            data['const_dist'] = row.district.title()
            data['const_blck'] = row.block.title()
            #if row.neighbours != None:
            #  neighbours = row.neighbours.strip().split('|')
            #  neighbours.append(row.elec_comm_code)
            print neighbours
          return [data,neighbours,constype_str]
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)

  def countsTable(self,cons_type,constid,qkeys):
    try:
      constype = "mp"
      if cons_type == 1:
        constype = "mp"
      elif cons_type == 2:
        constype = "mla"
      elif cons_type == 3:
        constype = "corporator"
      elif cons_type == 4:
        constype = "district"
      elif cons_type == 5:
        constype = "block"
      elif cons_type == 6:
        constype = "cluster"
      data = {}
      tabledata = {}
      for querykey in qkeys:
        result = cursor.query(db.Queries_dise.getDictionary(constype)[constype + '_' + querykey], {'s':constid})
        for row in result:
          tabledata[querykey] = str(row.count)
      data["inst_counts"] =  tabledata
      return data
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      return None

  def getTranslations(self, lang, constype):
    transDict = {}
    f = open(os.path.join(os.getcwd(),'translations/translations_heading.csv'),'r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 1:
        transDict['H' + str(text[0])] = text[2].strip('\n')
      else:
        transDict['H' + str(text[0])] = text[1]
    if constype == 4:
        transDict['H6']=transDict['H128']
        transDict['H68']=transDict['H131']
    elif constype == 5:
        transDict['H68']=transDict['H129']
        transDict['H68']=transDict['H132']
    elif constype == 6:
        transDict['H68']=transDict['H130']
        transDict['H68']=transDict['H133']    
    f = open(os.path.join(os.getcwd(),'translations/translations_dict.csv'),'r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 1:
        transDict[str(text[0])] = text[1].strip('\n')
      else:
        transDict[str(text[0])] = text[0]
    return transDict
