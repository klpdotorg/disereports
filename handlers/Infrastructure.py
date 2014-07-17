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

class Infrastructure:

  def generateData(self,cons_type, constid):
    data = {}
    avgdata = {}
    avgdata = self.getAverages()

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

    data.update(self.constituencyData(constype,constid))
    data.update(self.getAngInfra(constype,constid,avgdata))
    data.update(self.getSchoolInfra(constype,constid,avgdata))
    return data

  def getAverages(self):
    data = {}
    querykeys = ['get_dise_count_blore','get_sch_count_blore','get_ai_count_blore','get_ang_count_blore']
    for key in querykeys:
      result = cursor.query(db.Queries.getDictionary("common_queries")[key])
      for row in result:
        data[key.replace("get_","")] = row.count
    querykeys = ['get_dise_avg_blore','get_ai_avg_blore']
    for key in querykeys:
      tabledata = {}
      result = cursor.query(db.Queries.getDictionary("common_queries")[key])
      for row in result:
        if 'dise' in key:
          tabledata[row.a1] = str(int(row.count) * 100/int(data['dise_count_blore']))
        else:
          tabledata[row.a1] = str(int(row.count) * 100/int(data['ai_count_blore']))
      data[key.replace("get_","")] = tabledata
    return data

  def getAngInfra(self,constype,constid,data):
    tabledata = {}
    
    blore_count = data['ai_count_blore']
    blore_infra = data['ai_avg_blore']

    querykey = 'infra_count'
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
     infra_count = row.count
    data[querykey] = infra_count

    querykey = 'ang_infra' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      if row.ai_metric in ['waste_basket','toilet','toilet_roof','akshara_kits']:
        pass
      else:
        if row.ai_group in tabledata:
          tabledata[row.ai_group][row.ai_metric]=[str(int(row.count)*100/int(infra_count)),str(blore_infra[row.ai_metric])]
        else:
          tabledata[row.ai_group] = {row.ai_metric:[str(int(row.count)*100/int(infra_count)),str(blore_infra[row.ai_metric])]}
    data[querykey] = tabledata
    return data

  def getSchoolInfra(self,constype,constid,data):
    tabledata = {}

    blore_count = data['dise_count_blore']
    blore_dise = data['dise_avg_blore']

    querykey = 'dise_count'
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
     dise_count = row.count
    data[querykey] = dise_count

    querykey = 'dise_facility' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      if row.df_metric in ['toilet_all','ramp','medical']:
        pass
      else:
        if row.df_group in tabledata:
          tabledata[row.df_group][row.df_metric]=[str(int(row.count)*100/int(dise_count)),str(blore_dise[row.df_metric])]
        else:
          tabledata[row.df_group] = {row.df_metric:[str(int(row.count)*100/int(dise_count)),str(blore_dise[row.df_metric])]}
    data[querykey] = tabledata
    return data


  def neighboursData(self, neighbours, constype, constid):
    data = {}
    constype_str = constype
    try:
      querykey = 'neighbours_df_count'
      result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':tuple(neighbours)})
      dise_count = {} 
      for row in result:
        dise_count[row.const_ward_name] = int(row.count)
      data[querykey] = dise_count

      querykey = 'neighbours_ai_count'
      result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':tuple(neighbours)})
      infra_count = {} 
      for row in result:
        infra_count[row.const_ward_name] = int(row.count)
      data[querykey] = infra_count

      if len(neighbours) > 0:
        crit='neighbours_'
        query_keys = ['dise','anginfra']
        for key in query_keys:
          tabledata = {}
          counts_dict = {}
          if key == 'dise' :
            counts_dict = dise_count
          else:
            counts_dict = infra_count
          result = cursor.query(db.Queries.getDictionary(constype)[constype_str+'_'+crit+key], {'s':tuple(neighbours)})
          for row in result:
            if row.a1 in ['waste_basket','toilet','toilet_roof','akshara_kits','toilet_all','ramp','medical']:
              pass
            else:
              if row.const_ward_name.strip() in tabledata.keys():
                  tabledata[row.const_ward_name.strip()][row.a2 + '|' + row.a1] = int(row.count)*100/counts_dict[row.const_ward_name.strip()]
              else:
                tabledata[row.const_ward_name.strip()]={row.a2+'|'+ row.a1:int(row.count)*100/counts_dict[row.const_ward_name.strip()]}

          newtable = {}

          for tabkey in tabledata.keys():
            moddata = {}
            moddata = tabledata[tabkey]
            for each in moddata.keys():
              if each in newtable.keys():
                newtable[each][tabkey] = moddata[each] 
              else:
                newtable.update({ each:{tabkey:moddata[each]}})
          data[crit+key] = newtable


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
    neighboursdata  = self.neighboursData(ret_data[1],ret_data[2],constid)
    if neighboursdata:
      data.update(neighboursdata)
    return data
