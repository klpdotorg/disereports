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

class Demographics:

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
    data["const_name"]=str(constid[0])

    queries = ['gend_sch','gend_presch']
    data.update(self.genderGraphs(constype,constid,queries))
    queries = ['mt_sch','mt_presch']
    data.update(self.mtGraphs(constype,constid,queries))
    queries = ['moi_sch','cat_sch','enrol_sch','enrol_presch']
    data.update(self.pieGraphs(constype,constid,queries))
    data.update(self.constituencyData(constype,constid))
    return data


  def genderGraphs(self,constype,constid,qkeys):
    data = {}
    for querykey in qkeys:
      result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
      chartdata ={}
      for row in result:
        chartdata[str(row.sex.strip())] = int(row.sum)
      if len(chartdata.keys()) > 0:
        total = chartdata['Boy']+chartdata['Girl']
        percBoys = round(float(chartdata['Boy'])/total*100,0)
        percGirls = round(float(chartdata['Girl'])/total*100,0)
        data[querykey+"_tb"]=chartdata
      else:
        data[querykey+"_hasdata"] = 0
    return data

  def mtGraphs(self,constype,constid,qkeys):
    data = {}
    for querykey in qkeys:
      result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
      tabledata = {}
      invertdata = {}
      order_lst = []
      for row in result:
        invertdata[int(row.sum)] = str(row.mt.strip().title())
      if len(invertdata.keys()) > 0:
        checklist = sorted(invertdata)
        others = 0
        for i in checklist[0:len(checklist)-4]:
          others = others + i
          del invertdata[i]
        invertdata[others] = 'Others'
        tabledata = dict(zip(invertdata.values(),invertdata.keys()))
        if 'Other' in tabledata.keys():
          tabledata['Others'] = tabledata['Others'] + tabledata['Other']
          del tabledata['Other']
      for i in sorted(tabledata,key=tabledata.get,reverse=True):
        order_lst.append(i)
      if len(tabledata.keys()) > 0:
        data[querykey + "_tb"] = tabledata
        data[querykey + "_ord_lst"] = order_lst 
      else:
        data[querykey + "_hasdata"] = 0
    return data

  def pieGraphs(self,constype,constid,qkeys):
    data = {}
    for querykey in qkeys:
      result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
      tabledata = {}
      for row in result:
        tabledata[str(row.a1.strip().title())] = str(int(row.a2))
      sorted_x = sorted(tabledata.items(), key=itemgetter(1))
      tabledata = dict(sorted_x)
      if len(tabledata.keys()) > 0:
        data[querykey + "_tb"] = tabledata
      else:
        data[querykey + "_hasdata"] = 0
    return data

  def constituencyData(self,constype,constid):
    data = {}
    util = CommonUtil()
    ret_data = util.constituencyData(constype,constid)
    data.update(ret_data[0])
    neighbors = self.neighboursData(ret_data[1],ret_data[2])
    if neighbors:
      data.update(neighbors)
    return data


  def neighboursData(self, neighbours, constype):
    data = {}
    constype_str = constype 
    try:
      if len(neighbours) > 0:
        neighbours_sch = {}
        neighbours_presch = {}
        
        result = cursor.query(db.Queries.getDictionary(constype)[constype_str + '_neighbour_sch'], {'s':tuple(neighbours)})
        for row in result:
          neighbours_sch[row.const_ward_name.strip()]={'schcount':str(row.count)}

        result = cursor.query(db.Queries.getDictionary(constype)[constype_str + '_neighbour_presch'], {'s':tuple(neighbours)})
        for row in result:
          neighbours_presch[row.const_ward_name.strip()] = {'preschcount':str(row.count)}
         
        result = cursor.query(db.Queries.getDictionary(constype)[constype_str + '_neighbour_gendsch'],{'s':tuple(neighbours)})
        for row in result:
          neighbours_sch[row.const_ward_name.strip()][row.sex.strip()] = str(row.sum)
        
        result = cursor.query(db.Queries.getDictionary(constype)[constype_str + '_neighbour_gendpresch'],{'s':tuple(neighbours)})
        for row in result:
          neighbours_presch[row.const_ward_name.strip()][row.sex.strip()] = str(row.sum)
        
        if len(neighbours_sch.keys()) > 0: 
          data["neighbours_sch"] = neighbours_sch          
        else:
          data["neighbours_sch_hasdata"] = 0

        if len(neighbours_presch.keys()) > 0: 
          data["neighbours_presch"] = neighbours_presch          
        else:
          data["neighbours_presch_hasdata"] = 0
      else:
        data["neighbours_sch_hasdata"] = 0
        data["neighbours_presch_hasdata"] = 0

      return data
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      return None
