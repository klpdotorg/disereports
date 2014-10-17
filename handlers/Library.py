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

class Library:

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
      constype = "boundary"
    data["const_name"]=str(constid[0])

    data.update(self.constituencyData(constype,constid))
    data.update(self.getLibInfra(constype,constid))
    data.update(self.getLibMisc(constype,constid))
    data.update(self.getLibTxnsOverTime(constype,constid))
    data.update(self.getLibTxnsOverClass(constype,constid))
    return data

  def getLibInfra(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'lib_count' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      lib_count = row.count
    data[querykey] = lib_count
    querykey = 'lib_status' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    akshara_run = ['Working','Closed']
    akshara_exp = ['Working']
    teachers = ['Handed over','Not Working']
    librarian_count = 0
    teachers_count = 0
    library_exp = 0
    for row in result:
      if len(row.libstatus.strip()) == 0:
        tabledata['No Library Programme'] = row.count
      else:
        tabledata[row.libstatus] = row.count
      if row.libstatus.strip() in akshara_run:
        librarian_count = librarian_count + int(row.count)
      if row.libstatus.strip() in akshara_exp:
        library_exp = library_exp + int(row.count)
      if row.libstatus.strip() in teachers:
        teachers_count = teachers_count + int(row.count)
    data[querykey] = tabledata
    data['librarian_count'] = librarian_count
    data['teachers_count'] = teachers_count
    data['library_exp'] = library_exp
    tabledata = {}
    querykey = 'lib_summary' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      tabledata['total_books'] = row.totalbooks
      tabledata['total_racks'] = row.totalracks
      tabledata['total_tables'] = row.totaltables
      tabledata['total_chairs'] = row.totalchairs
      tabledata['total_comps'] = row.totalcomps
      tabledata['total_ups'] = row.totalups
    data[querykey] = tabledata
    return data

  def getLibMisc(self,constype,constid):
    data = {}
    querykey = 'gend_sch' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    chartdata ={}
    for row in result:
      chartdata[str(row.sex.strip())] = int(row.sum)
    total = chartdata['Boy']+chartdata['Girl']
    data["lib_stucount"] = total 

    querykey = 'moi_sch' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    tabledata = {}
    for row in result:
      tabledata[str(row.a1.strip().title())] = str(int(row.a2))
    sorted_x = sorted(tabledata.items(), key=itemgetter(1))
    tabledata = dict(sorted_x)
    if len(tabledata.keys()) > 0:
      data["lib_moicount"] = tabledata
    return data

  def getLibTxnsOverTime(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'lib_lang' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      if row.month in tabledata.keys():
	tabledata[row.month][row.book_lang]=row.txncount
      else:
      	tabledata[row.month]={row.book_lang:row.txncount}
    data[querykey] = tabledata
    tabledata = {}
    querykey = 'lib_level' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      if row.month in tabledata.keys():
	tabledata[row.month][row.book_level]=row.txncount
      else:
      	tabledata[row.month]={row.book_level:row.txncount}
    data[querykey] = tabledata
    return data
  
  def getLibTxnsOverClass(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'lib_class_lang' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      if row.clas:
        if row.clas in tabledata.keys():
	  tabledata[str(row.clas)][row.book_lang]=row.txncount
        else:
      	  tabledata[str(row.clas)]={row.book_lang:row.txncount}
    data[querykey] = tabledata
    tabledata = {}
    querykey = 'lib_class_level' 
    result = cursor.query(db.Queries.getDictionary(constype)[constype + '_' + querykey],{'s':constid})
    for row in result:
      if row.clas:
        if row.clas in tabledata.keys():
	  tabledata[row.clas][row.book_level]=row.txncount
        else:
      	  tabledata[row.clas]={row.book_level:row.txncount}
    data[querykey] = tabledata
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
    tabledata = {}
    try:
      if len(neighbours) > 0:
        crit='neighbours_'
        query_keys = ['libtxn','libinfra','libstu', 'libschcount']
        for key in query_keys:
          result = cursor.query(db.Queries.getDictionary(constype)[constype_str+'_'+crit+key], {'s':tuple(neighbours)})
          for row in result:
            if row.const_ward_name.strip() in tabledata.keys():
              tabledata[row.const_ward_name.strip()][key]=row.count
            else:
              tabledata[row.const_ward_name.strip()]={key:row.count}
      data['neighbours_lib'] = tabledata
      return data
    except:
      print 'Error occurred'
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      return None
