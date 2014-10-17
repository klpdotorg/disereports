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

class Learning:

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
      data["const_type"]='Boundary'
      constype = 'boundary'
    data["const_name"]=str(constid[0])

    data.update(self.constituencyData(constype,constid))
    data.update(self.getSchoolAssessment(constype,constid))
    data.update(self.getAngAssessment(constype,constid))
    return data

  def getSchoolAssessment(self,constype,constid):
    data = {}
    queries = ['sch_assess_class','sch_assess_gender'] 
    for querykey in queries:
      tabledata = {}
      result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
      for row in result:
        if row.a1 in tabledata.keys():
          tabledata[row.a1][row.grade] = row.count
        else:
          tabledata[row.a1] = {row.grade:row.count}
      for each in tabledata.keys():
        tabledata[each]["total"] = sum(tabledata[each].values())
      data[querykey] = tabledata
    queries = ['sch_assess_bang','sch_assess_const'] 
    for querykey in queries:
      tabledata = {}
      result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
      for row in result:
        if row.grade not in tabledata.keys():
          tabledata[row.grade] = row.count
      tabledata["total"] = sum(tabledata.values())
      data[querykey] = tabledata
    querykey = 'sch_assess_cnt' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      data[querykey] = row.schcount
      data['sch_assess_stucnt'] = row.stucount
    querykey = 'sch_assess_bang_cnt' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      data[querykey] = row.count
    return data
  
  def getAngAssessment(self,constype,constid):
    data = {}
    queries = ['ang_assess_score','ang_assess_bang']
    for querykey in queries:
      tabledata = {}
      result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
      for row in result:
        data[querykey] = row.res
    queries = ['ang_assess_gender','ang_assess_bang_gender']
    for querykey in queries:
      tabledata = {}
      result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
      for row in result:
        tabledata[row.gender] = row.res
      data[querykey] = tabledata
    querykey = 'ang_assess_cnt' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      data[querykey] = row.count
      data['ang_assess_stucnt'] = row.sum
    querykey = 'ang_assess_bang_cnt' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      data[querykey] = row.count
    return data

  def constituencyData(self,constype,constid):
    data = {}
    util = CommonUtil()
    ret_data = util.constituencyData(constype,constid)
    data.update(ret_data[0])
    data.update(self.neighboursData(ret_data[1],ret_data[2]))
    return data

  def neighboursData(self, neighbours, constype):
    data = {}
    constype_str = constype
    tabledata = {}
    try:
      if len(neighbours) > 0:
        query_keys = ['ang_assess_neighbor']
        for key in query_keys:
          result = cursor.query(db.Queries.getDictionary(constype)[constype_str+'_'+key], {'s':tuple(neighbours)})
          for row in result:
            if row.const_ward_name.strip() in tabledata.keys():
              tabledata[row.const_ward_name.strip()][row.gender]=row.res
            else:
              tabledata[row.const_ward_name.strip()]={row.gender:row.res}
          data[key] = tabledata
      return data
    except:
      print 'Error occurred'
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      return None
