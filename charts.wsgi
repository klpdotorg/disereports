import web
import psycopg2
import decimal
import jsonpickle
import csv
import re
from web import form
import datetime
import traceback
import simplejson
import codecs
from operator import itemgetter

# Needed to find the templates
import sys, os,traceback
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import db.KLPDB
import db.Queries_dise
import utils.DemographicsUtil
import utils.FinancesUtil
import utils.InfraUtil
import utils.LibraryUtil
import utils.NutritionUtil
import utils.LearningUtil

from utils.CommonUtil import CommonUtil
from utils.Links import Links 

from handlers.Demographics import Demographics
from handlers.Infrastructure import Infrastructure
from handlers.Finances import Finances
from handlers.Library import Library
from handlers.Nutrition import Nutrition 
from handlers.Learning import Learning

render = web.template.render('templates/')

urls = (
     '/','Index',
     '/errors','Errors',
     '/charts/(.*)/(.*)/(.*)/(.*)/(.*)','Charts',
)

#import newrelic.agent
#newrelic.agent.initialize(abspath + '/config/newrelic.ini')

application = web.application(urls,globals()).wsgifunc()
#application = newrelic.agent.WSGIApplicationWrapper(application)

def treemenu(rep_db):
  data = {}
  links = Links()
  data.update({"mp":links.getMPreports(rep_db)})
  data.update({"mla":links.getMLAreports(rep_db)})
  data.update({"corporator":links.getWardreports(rep_db)})
  data.update({"district":links.getSchDistreports(rep_db)})
  data.update({"block":links.getBlkreports(rep_db)})
  data.update({"cluster":links.getClusreports(rep_db)})
  data.update({"year":links.getYearreports(rep_db)})
  #data.update({"pre_dist":links.getPreDistreports(rep_db)})
  #data.update({"project":links.getProjreports(rep_db)})
  #data.update({"circle":links.getCircreports(rep_db)})
  return data

"""def treemenu(rep_db):
  data = {}
  links = Links()
  data.update({"mp":links.getMPreports(rep_db)[rep_db]})
  data.update({"mla":links.getMLAreports(rep_db)[rep_db]})
  #data.update({"corporator":links.getWardreports(rep_db)[rep_db]})
  data.update({"district":links.getSchDistreports(rep_db)[rep_db]})
  data.update({"block":links.getBlkreports(rep_db)[rep_db]})
  data.update({"cluster":links.getClusreports(rep_db)[rep_db]})
  data.update({"year":links.getYearreports(rep_db)})
  #data.update({"pre_dist":links.getPreDistreports(rep_db)[rep_db]})
  #data.update({"project":links.getProjreports(rep_db)[rep_db]})
  #data.update({"circle":links.getCircreports(rep_db)[rep_db]})
  return data"""

class Index:
  def GET(self,rep_db='dise'):
    data = {}
    links = Links()
    """data.update({"mp":links.getMPreports(rep_db)[rep_db]})
    data.update({"mla":links.getMLAreports(rep_db)[rep_db]})
    #data.update({"corporator":links.getWardreports(rep_db)[rep_db]})
    data.update({"district":links.getSchDistreports(rep_db)[rep_db]})
    data.update({"block":links.getBlkreports(rep_db)[rep_db]})
    data.update({"cluster":links.getClusreports(rep_db)[rep_db]})
    data.update({"year":links.getYearreports(rep_db)})
    #data.update({"pre_dist":links.getPreDistreports(rep_db)[rep_db]})
    #data.update({"project":links.getProjreports(rep_db)[rep_db]})
    #data.update({"circle":links.getCircreports(rep_db)[rep_db]})"""
    return render.index(simplejson.dumps(treemenu(rep_db),sort_keys=True))

class Errors:
  def GET(self,rep_db='klp'):
    data = treemenu(rep_db)
    data.update({"errormsg":"Sorry! This report is currently unavailable due to insufficient data."})
    return render.index(simplejson.dumps(data,sort_keys=True))

class Charts:
  
  """Returns the main template"""
  def GET(self,searchby,constid,rep_lang,rep_type,year):
    try:
      if searchby.lower() == 'mp':
        constype = 1
      elif searchby.lower() == 'mla':
        constype = 2
      elif searchby.lower() == 'corporator':
        constype = 3
      elif searchby.lower() == 'district':
        constype = 4
      elif searchby.lower() == 'block':
        constype = 5
      elif searchby.lower() == 'cluster':
        constype = 6
      lang = 2
      if rep_lang.lower()=='kannada':
        lang = 1
      data = {}
      db.Queries_dise.select_year(year)
      util = CommonUtil()
      data.update({'transdict':util.getTranslations(lang, constype)})
      if rep_type.lower() == 'demographics':
        demographics = Demographics()
        queries = ['schcount']
        #if rep_db == 'klp':
        #    queries.append('preschcount')
        data.update(util.countsTable(constype,[constid],queries))
        data.update(demographics.generateData(constype,[constid]))
        data.update(utils.DemographicsUtil.getDemographicsText(data,lang,constype))
        web.header('Content-Type','text/html; charset=utf-8')
        return render.demographics_dise(simplejson.dumps(data,sort_keys=True))
      elif rep_type.lower() == 'finance':
        finances = Finances()
        queries = ['abs_schcount','fin_schcount']
        data.update(util.countsTable(constype,[constid],queries))
        data.update(finances.generateData(constype,[constid]))
        data.update(utils.FinancesUtil.getFinancesText(data,lang,constype))
        web.header('Content-Type','text/html; charset=utf-8')
        return render.finances(simplejson.dumps(data,sort_keys=True))
      elif rep_type.lower() == 'infrastructure':
        infra = Infrastructure()
        queries = ['abs_schcount']
        data.update(util.countsTable(constype,[constid],queries))
        data.update(infra.generateData(constype,[constid]))
        data.update(utils.InfraUtil.getInfraText(data,lang,constype))
        web.header('Content-Type','text/html; charset=utf-8')
        return render.infrastructure(simplejson.dumps(data,sort_keys=True))
      elif rep_type.lower() == 'library':
        library = Library()
        queries = ['abs_schcount','abs_preschcount']
        data.update(util.countsTable(constype,[constid],queries))
        data.update(library.generateData(constype,[constid]))
        data.update(utils.LibraryUtil.getLibText(data,lang))
        web.header('Content-Type','text/html; charset=utf-8')
        return render.library(simplejson.dumps(data,sort_keys=True))
      elif rep_type.lower() == 'nutrition':
        nutrition = Nutrition()
        data.update(nutrition.generateData(constype,[constid]))
        data.update(utils.NutritionUtil.getNutriText(data,lang))
        web.header('Content-Type','text/html; charset=utf-8')
        return render.nutrition(simplejson.dumps(data,sort_keys=True))
      elif rep_type.lower() == 'learning':
        queries = ['abs_schcount','abs_preschcount']
        data.update(util.countsTable(constype,[constid],queries))
        learning = Learning()
        data.update(learning.generateData(constype,[constid]))
        data.update(utils.LearningUtil.getLearningText(data,lang))
        web.header('Content-Type','text/html; charset=utf-8')
        return render.learning(simplejson.dumps(data,sort_keys=True))
        #web.header('Content-Type', 'application/json')
        #return jsonpickle.encode(data)
      else:
        pass
    except:
      traceback.print_exc(file=sys.stderr)
      raise web.seeother('/errors')


