import web
import psycopg2
import traceback
import sys, os,traceback
import db.KLPDB
import db.Queries_dise
import db.Queries_klp

cursor_dise = db.KLPDB.getWebDbConnection1()
cursor_klp = db.KLPDB.getWebDbConnection()
class Links:

  def getMPreports(self,rep_db):
    mps = {}
    temp = {}
    result_dise = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_mp_ids'])
    result_klp = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_mp_ids'])
    for row in result_dise:
      temp[row['const_ward_name']] = [row['mp_const_id'],row['const_ward_name'],row['parent']]
    mps['dise']=temp
    temp = {}
    for row in result_klp:
      temp[row['const_ward_name']] = [row['mp_const_id'],row['const_ward_name'],row['parent']]
    mps['klp']=temp    
    #mps[row[row['const_ward_name']]] = [row['mp_const_id'],row['mp_const_id'],row['parent']]
    return mps
        
  def getMLAreports(self,rep_db):
    mlas = {}
    temp = {}
    result_dise = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_mla_ids'])
    result_klp = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_mla_ids'])
    for row in result_dise:
      temp[row['const_ward_name']] = [row['mla_const_id'],row['const_ward_name'],row['parent']]
    mlas['dise']=temp
    temp = {}
    for row in result_klp:
      temp[row['const_ward_name']] = [row['mla_const_id'],row['const_ward_name'],row['parent']]
    mlas['klp']=temp
    return mlas

  def getWardreports(self,rep_db):
    wards = {}
    temp = {}
    #result_dise = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_ward_ids'])
    result_klp = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_ward_ids'])
    #for row in result_dise:
    temp['const_ward_name'] = ['hello','hi','okay']
    wards['dise']=temp
    temp = {}
    for row in result_klp:
      temp[row['const_ward_name']] = [row['ward_id'],row['const_ward_name'],row['parent']]
    wards['klp']=temp
    return wards

  def getSchDistreports(self,rep_db):
    schldists = {}
    temp = {}
    result_dise = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_schdist'])
    result_klp = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_schdist'])
    for row in result_dise:
      temp[row['district']] = [row['dist_id'],row['district'],row['parent']]
    schldists['dise']=temp
    temp = {}
    for row in result_klp:
      temp[row['district']] = [row['dist_id'],row['district'],row['parent']]
    schldists['klp']=temp
    return schldists

  def getBlkreports(self,rep_db):
    blks = {}
    temp = {}
    result_dise = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_block'])
    result_klp = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_block'])
    for row in result_dise:
      temp[row['block']] = [row['blck_id'],row['block'],row['parent']]
    blks['dise']=temp
    temp = {}
    for row in result_klp:
      temp[row['block']] = [row['blck_id'],row['block'],row['parent']]
    blks['klp']=temp
    return blks 

  def getClusreports(self,rep_db):
    clus = {}
    temp = {}
    result_dise = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_cluster'])
    result_klp = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_cluster'])
    for row in result_dise:
      temp[row['clust']] = [row['clst_id'],row['clust'],row['parent']]
    clus['dise']=temp
    temp = {}
    for row in result_klp:
      temp[row['clust']] = [row['clst_id'],row['clust'],row['parent']]
    clus['klp']=temp
    return clus 

  def getPreDistreports(self,rep_db):
    predists = {}
    result_dise = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_preschdist'])
    for row in result:
      predists[row['district']] = [row['dist_id']]
    return predists

  def getProjreports(self,rep_db):
    proj = {}
    result_dise = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_proj'])
    for row in result:
       proj[row['block']] = [row['blck_id']]
    return proj

  def getCircreports(self,rep_db):
    circ = {}
    result_dise = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_cluster'])
    for row in result:
      circ[row['clust']] = [row['clst_id']]
    return circ

  def getYearreports(self, rep_db):
    year = {}
    temp = {}
    result_dise = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_year'])
    for row in result_dise:
      temp[row['year']] = [row['id'],row['year'],row['parent']]
    year['dise'] = temp
    year['klp'] = temp
    return year


