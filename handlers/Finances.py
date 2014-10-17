import web
import psycopg2
import traceback
import sys, os,traceback
from operator import itemgetter
import db.KLPDB
import db.Queries_dise
from utils.CommonUtil import CommonUtil

#connection = db.KLPDB.getConnection()
#cursor = connection.cursor()
cursor = db.KLPDB.getWebDbConnection1()

class Finances:

  def generateData(self,cons_type, constid):
    data = {}
    constype = "mp"
    if cons_type == 1:
      data["const_type"]='MP'
      constype = "mp"
    elif cons_type == 2:
      data["const_type"]='MLA'
      constype = "mla"
    elif cons_type == 3:
      data["const_type"]='Corporator'
      constype = "corporator"
    elif cons_type == 4:
      data["const_type"]='District'
      constype = "district"
    elif cons_type == 5:
      data["const_type"]='Block'
      constype = "block"
    elif cons_type == 6:
      data["const_type"]='Cluster'
      constype = "cluster"
    data["const_name"]=str(constid[0])
    data.update(self.constituencyData(constype,constid))
    data.update(self.getTLMGrant(constype,constid))
    data.update(self.getAnnualGrant(constype,constid))
    data.update(self.getMaintenanceGrant(constype,constid))
    return data

  def getTLMGrant(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'tlmgrant_sch' 
    result = cursor.query(db.Queries_dise.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      tabledata['grant_amount'] = str(row.total_grant)
      tabledata['teacher_count'] = str(int(row.total_grant)/int(row.grant_amount))
    data[querykey] = tabledata
    data['total_tlm']=int(tabledata['grant_amount'])
    return data
  
  def getAnnualGrant(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'annualgrant_sch' 
    result = cursor.query(db.Queries_dise.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    total_grant = 0
    for row in result:
      tabledata[row.cat] = [str(row.count),str(row.total_grant)]
      total_grant = total_grant + int(row.total_grant)
    data[querykey] = tabledata
    data['total_annual'] = total_grant
    return data
   
  def getMaintenanceGrant(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'mtncgrant_sch' 
    result = cursor.query(db.Queries_dise.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    total_grant = 0
    for row in result:
      tabledata[row.classroom_count] = [str(row.count), str(row.total_grant)]
      total_grant = total_grant + int(row.total_grant)
    data[querykey] = tabledata
    data['total_mntc'] = total_grant
    return data

  def neighboursData(self, neighbours, constype):
    data = {}
    constype_str = constype 
    tabledata = {}
    try:
      if len(neighbours) > 0:
        crit='neighbor_'
        query_keys = ['tlm','annual','mntnc'] 
        for key in query_keys:
          result = cursor.query(db.Queries_dise.getDictionary(constype)[constype_str+'_'+crit+key], {'s':tuple(neighbours)})
          for row in result:
            if row.const_ward_name.strip() in tabledata.keys():
              if key in tabledata[row.const_ward_name.strip()].keys():
                addedup = int(tabledata[row.const_ward_name.strip()][key]) + int(row.total_grant)
                tabledata[row.const_ward_name.strip()][key] = addedup
              else:
                tabledata[row.const_ward_name.strip()][key] = row.total_grant
            else:
              tabledata[row.const_ward_name.strip()]={key:row.total_grant}
      data['neighbours_grant'] = tabledata
      return data
    except:
      print 'Error occurred'
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      return None

  def constituencyData(self,constype,constid):
    data = {}
    util = CommonUtil()
    ret_data = util.constituencyData(constype,constid)
    data.update(ret_data[0])
    neighbors = self.neighboursData(ret_data[1],ret_data[2])
    if neighbors:
      data.update(neighbors)
    return data
