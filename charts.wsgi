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
import os
from operator import itemgetter

# Needed to find the templates
import sys, os,traceback
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import db.KLPDB
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

cache_location = '/tmp/klp_reports'
render = web.template.render('templates/')

urls = (
     '/','Index',
     '/errors','Errors',
     '/charts/(.*)/(.*)/(.*)/(.*)','Charts',
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
  def GET(self):
    data = treemenu('klp')
    data.update({"errormsg":"Sorry! This report is currently unavailable due to insufficient data."})
    return render.index(simplejson.dumps(data,sort_keys=True))

class Charts:
  
  """Returns the main template"""
  def GET(self,searchby,constid,rep_lang,rep_type):
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
      util = CommonUtil()

      report_str = '-'.join([searchby, str(constid), rep_lang, rep_type])
      cache_file = os.path.join(cache_location, report_str + '.json')

      def check_file(html_file):
          data = ''
          if os.path.isfile(html_file):
              print ('Found Cache', report_str)
              with open(html_file, 'r') as cache:
                  data = cache.read()
          return data

      def write_file(html_file, data):
          with open(html_file, 'w') as cache:
              cache.write(data)

      data_json = check_file(cache_file)
      data.update({'transdict':util.getTranslations(lang)})
      if rep_type.lower() == 'demographics':
        if data_json == '':
          demographics = Demographics()
          queries = ['schcount','preschcount']
          data.update(util.countsTable(constype,[constid],queries))
          data.update(demographics.generateData(constype,[constid]))
          data.update(utils.DemographicsUtil.getDemographicsText(data,lang,constype))
          data_json = simplejson.dumps(data, sort_keys=True)
          write_file(cache_file, data_json)
        web.header('Content-Type','text/html; charset=utf-8')
        return render.demographics(data_json)
      elif rep_type.lower() == 'finance':
        if data_json == '':
          finances = Finances()
          queries = ['abs_schcount','fin_schcount']
          data.update(util.countsTable(constype,[constid],queries))
          data.update(finances.generateData(constype,[constid]))
          data.update(utils.FinancesUtil.getFinancesText(data,lang,constype))
          data_json = simplejson.dumps(data, sort_keys=True)
          write_file(cache_file, data_json)
        web.header('Content-Type','text/html; charset=utf-8')
        return render.finances(data_json)
      elif rep_type.lower() == 'infrastructure':
        if data_json == '':
          infra = Infrastructure()
          queries = ['abs_schcount','abs_preschcount']
          data.update(util.countsTable(constype,[constid],queries))
          data.update(infra.generateData(constype,[constid]))
          data.update(utils.InfraUtil.getInfraText(data,lang,constype))
          data_json = simplejson.dumps(data, sort_keys=True)
          write_file(cache_file, data_json)
        web.header('Content-Type','text/html; charset=utf-8')
        return render.infrastructure(data_json)
      elif rep_type.lower() == 'library':
        if data_json == '':
          library = Library()
          queries = ['abs_schcount','abs_preschcount']
          data.update(util.countsTable(constype,[constid],queries))
          data.update(library.generateData(constype,[constid]))
          data.update(utils.LibraryUtil.getLibText(data,lang,constype))
          data_json = simplejson.dumps(data, sort_keys=True)
          write_file(cache_file, data_json)
        web.header('Content-Type','text/html; charset=utf-8')
        return render.library(data_json)
      elif rep_type.lower() == 'nutrition':
        if data_json == '':
          nutrition = Nutrition()
          data.update(nutrition.generateData(constype,[constid]))
          data.update(utils.NutritionUtil.getNutriText(data,lang))
          data_json = simplejson.dumps(data, sort_keys=True)
          write_file(cache_file, data_json)
        web.header('Content-Type','text/html; charset=utf-8')
        return render.nutrition(data_json)
      elif rep_type.lower() == 'learning':
        if data_json == '':
          queries = ['abs_schcount','abs_preschcount']
          data.update(util.countsTable(constype,[constid],queries))
          learning = Learning()
          data.update(learning.generateData(constype,[constid]))
          data.update(utils.LearningUtil.getLearningText(data,lang,constype))
          data_json = simplejson.dumps(data, sort_keys=True)
          write_file(cache_file, data_json)
        web.header('Content-Type','text/html; charset=utf-8')
        return render.learning(data_json)
      else:
        pass
    except:
      traceback.print_exc(file=sys.stderr)
      raise web.seeother('/errors')


