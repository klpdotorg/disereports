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
    if rep_db=='dise':
        result = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_mp_ids'])
    else:
        result = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_mp_ids'])
    for row in result:
      mps[row['const_ward_name']] = [row['mp_const_id'],row['mp_const_id'],row['parent']]
    return mps
        
  def getMLAreports(self,rep_db):
    mlas = {}
    if rep_db=='dise':
        result = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_mla_ids'])
    else:
        result = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_mla_ids'])
    for row in result:
      mlas[row['const_ward_name']] = [row['mla_const_id'],row['mla_const_id'],row['parent']]
    return mlas

  def getWardreports(self,rep_db):
    wards = {}
    if rep_db=='dise':
        result = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_ward_ids'])
    else:
        result = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_ward_ids'])
    for row in result:
        wards[row['const_ward_name']] = [row['ward_id']]
    return wards

  def getSchDistreports(self,rep_db):
    schldists = {}
    if rep_db=='dise':
        result = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_schdist'])
    else:
        result = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_schdist'])
    for row in result:
      schldists[row['district']] = [row['dist_id'],row['dist_id'],row['parent']]
    return schldists

  def getBlkreports(self,rep_db):
    blks = {}
    if rep_db=='dise':
        result = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_block'])
    else:
        result = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_block'])
    for row in result:
      blks[row['block']] = [row['blck_id'],row['blck_id'],row['parent']]
    return blks 

  def getClusreports(self,rep_db):
    clus = {}
    if rep_db=='dise':
        result = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_cluster'])
    else:
        result = cursor_klp.query(db.Queries_klp.getDictionary("common")['get_cluster'])
    for row in result:
      clus[row['clust']] = [row['clst_id'],row['clst_id'],row['parent']]
    return clus 

  def getPreDistreports(self,rep_db):
    predists = {}
    result = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_preschdist'])
    for row in result:
      predists[row['district']] = [row['dist_id']]
    return predists

  def getProjreports(self,rep_db):
    proj = {}
    result = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_proj'])
    for row in result:
       proj[row['block']] = [row['blck_id']]
    return proj

  def getCircreports(self,rep_db):
    circ = {}
    result = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_cluster'])
    for row in result:
      circ[row['clust']] = [row['clst_id']]
    return circ

  def getYearreports(self, rep_db):
    year = {}
    result = cursor_dise.query(db.Queries_dise.getDictionary("common")['get_year'])
    for row in result:
      year[row['year']] = [row['id'],row['year'],row['parent']]
    return year


