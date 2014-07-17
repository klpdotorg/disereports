import web
import psycopg2
import traceback
import sys, os,traceback
from operator import itemgetter
import db.KLPDB
import db.Queries
from utils.CommonUtil import CommonUtil

#connection = db.KLPDB.getConnection()
#cursor = connection.cursor()
cursor = db.KLPDB.getWebDbConnection()

class Nutrition:

  def generateData(self,cons_type, constid):
    data = {}
    constype = "cluster"
    if cons_type == 4:
      data["const_type"]='CLUSTER'
      constype = "cluster"
    elif cons_type == 5:
      data["const_type"]='BLOCK'
      constype = "block"
    data["const_name"]=str(constid[0])
    try:
      data.update(self.getEnrollment(constype,constid))
      data.update(self.getMidDayMealData(constype,constid))
    except:
      print 'Error occurred....'
      traceback.print_exc(file=sys.stderr)
    return data

  def getEnrollment(self,constype,constid):
    data = {}
    querykeys = ['dise_enrol','klp_enrol'] 
    for querykey in querykeys:
      result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
      for row in result:
        data[querykey] = {'numboys':row.num_boys,'numgirls':row.num_girls} 
    querykey = 'sch_count'
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      data[querykey] = {'totsch':row.a1,'mdmsch':row.a2} 
    return data

  def getMidDayMealData(self,constype,constid):
    data = {}
    querykey = 'mdm_agg' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    tabledata ={}
    for row in result:
      if row.mon in tabledata:
        tabledata[row.mon][row.wk]=[row.indent,row.attend]
      else:
        tabledata[row.mon]={row.wk:[row.indent,row.attend]}
        data['const_name']=row.name
    data[querykey] = tabledata
    return data
