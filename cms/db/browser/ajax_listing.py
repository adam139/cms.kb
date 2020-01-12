#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope.interface import implementer
from zope.schema import getFieldsInOrder
from zope.component import getMultiAdapter
from collective.z3cform.datagridfield import DataGridFieldFactory
from zope import component
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.CMFCore.interfaces import ISiteRoot
from plone.memoize.instance import memoize
from Products.Five.browser import BrowserView
from plone.directives import form
from z3c.form import form as z3f
from z3c.form import field, button

from z3c.form.interfaces import IFieldsAndContentProvidersForm
from z3c.form.contentprovider import ContentProviders
from cms.db.browser.content_providers import BingRenExtendedHelp
from cms.db.browser.content_providers import YiShengExtendedHelp
from cms.db.browser.content_providers import DanWeiExtendedHelp
from Products.statusmessages.interfaces import IStatusMessage
from cms.db.interfaces import InputError
from zope.component import queryUtility
from zope.component import provideAdapter
from cms.db.interfaces import IDbapi
# 有外键的表必须调用定制UI接口
from cms.db.browser.interfaces import IYaoUI
from cms.db.browser.interfaces import IYao_DanWei_AssoUI
from cms.db.browser.interfaces import IDanWeiUI
from cms.db.browser.interfaces import IYiShengUI
from cms.db.browser.interfaces import IBingRenUI
from cms.db.browser.interfaces import IChuFangUI
# association object table need a intermediate object for edit form 
from cms.db.browser.intermediate_objs import ChuFangUI
from cms.db.browser.intermediate_objs import BingRenUI
from cms.db.browser.intermediate_objs import YaoUI
from cms.db.browser.intermediate_objs import YiShengUI
from cms.db.browser.intermediate_objs import DanWeiUI
from cms.db.browser.intermediate_objs import EditChuFang_BingRen_AssoUI
from cms.db.browser.intermediate_objs import EditYao_ChuFang_AssoUI
from cms.db.browser.intermediate_objs import EditYao_DanWei_AssoUI
#register multiwidget for association object interfaces
from cms.db.browser.interfaces import IYao_ChuFang_AssoUI
from cms.db.browser.interfaces import IChuFang_BingRen_AssoUI
from cms.db.browser.intermediate_objs import ChuFang_BingRen_AssoUI
from cms.db.browser.intermediate_objs import Yao_ChuFang_AssoUI
from z3c.form.object import registerFactoryAdapter
registerFactoryAdapter(IYao_ChuFang_AssoUI, Yao_ChuFang_AssoUI)
registerFactoryAdapter(IChuFang_BingRen_AssoUI, ChuFang_BingRen_AssoUI)

from cms.db.browser.utility import filter_cln,to_utf_8
from cms.db.browser.utility import getDanWeiId
from cms.db.browser.utility import map_field2cls, get_container_by_type
from cms.db.dbutility import map_yao_chufang_list as mapf
from cms.db.orm import IYaoWei,YaoWei
from cms.db.orm import IYaoXing,YaoXing
from cms.db.orm import IJingLuo,JingLuo
from cms.db.orm import IYao
from cms.db.orm import Yao
from cms.db.orm import Person,IPerson
from cms.db.orm import IChuFang,ChuFang
from cms.db.orm import IDiZhi,IDanWeiDiZhi, IGeRenDiZhi, DiZhi,DanWeiDiZhi,GeRenDiZhi
from cms.db.orm import IDanWei,DanWei
from cms.db.orm import IYiSheng,YiSheng
from cms.db.orm import IBingRen,BingRen
from cms.db.orm import Yao_JingLuo_Asso,ChuFang_BingRen_Asso,Yao_ChuFang_Asso,Yao_DanWei_Asso


from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zExceptions import NotFound
from cms.db import InputDb
from cms.db import _


class BaseView(BrowserView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    @memoize
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm

    def get_locator(self,name):
        "get db specify name table api"

        dbapi = queryUtility(IDbapi, name=name)
        return dbapi
    
    @property
    def canbeUpdate(self):
# checkPermission function must be use Title style permission
        canbe = self.pm().checkPermission("cms.db:Update db",self.context)
        return canbe
    
    @property
    def canbeInput(self):
# checkPermission function must be use Title style permission
        canbe = self.pm().checkPermission("cms.db:Input db",self.context)
        return canbe    
    
    def getPathQuery(self):

        """返回 db url
        """
        query = {}
        query['path'] = "/".join(self.context.getPhysicalPath())
        return query

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"

        locator = self.get_locator('model')
        recorders = locator.query(query)
        return recorders


class YaoXingsView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:admin_logs
    """
           
    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"

        locator = self.get_locator('yaoxing')
        recorders = locator.query(query)
        return recorders


class YaoWeiesView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:user_logs
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = self.get_locator('yaowei')
        recorders = locator.query(query)
        return recorders


class JingLuoesView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = self.get_locator('jingluo')
        recorders = locator.query(query)
        return recorders


class YaoesView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = self.get_locator('yao')
        recorders = locator.query(query)
        return recorders


class WoYaoesView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:wo_yao_listings
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
#         from cms.db.orm import Yao_DanWei_Asso
#         from cms.db.browser.utility import getDanWeiId
        locator = self.get_locator('yao')
        query['with_entities'] = 1
        recorders = locator.multi_query(query,Yao_DanWei_Asso,'yao_danwei','danwei_id',getDanWeiId(),'id','yao_id')
        return recorders


class ChuFangsView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = self.get_locator('chufang')
        recorders = locator.query(query)
        return recorders
    

class BingRensView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = self.get_locator('bingren')
        query['with_entities'] = 0
        recorders = locator.query(query)
        return recorders


class DiZhiesView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = self.get_locator('dizhi')
        recorders = locator.query(query)
        return recorders


class GeRenDiZhiesView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = self.get_locator('gerendizhi')
        query['with_entities'] = 0        
        recorders = locator.query(query)
        return recorders


class DanWeiDiZhiesView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = self.get_locator('danweidizhi')
        query['with_entities'] = 0        
        recorders = locator.query(query)
        return recorders


class DanWeiesView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = self.get_locator('danwei')
        recorders = locator.query(query)
        return recorders


class YiShengsView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"
        locator = self.get_locator('yisheng')
        query['with_entities'] = 0
        recorders = locator.query(query)
        return recorders


class NianGanZhisView(BaseView):
    """
    DB AJAX 查询，返回分页结果,这个class 调用数据库表 功能集 utility,
    从Ajaxsearch view 构造 查询条件（通常是一个参数字典），该utility 接受
    该参数，查询数据库，并返回结果。
    view name:db_listing
    """

    def search_multicondition(self,query):
        "query is dic,like :{'start':0,'size':10,'':}"

        locator = self.get_locator('nianganzhi')
#         query['with_entities'] = 0
        direction = query['sort_order'].strip()
        if direction == "reverse":
            query['sort_order'] = 'forward'
            
#         if query['start'] == None:
#             ty = datetime.datetime.today()
#             tsr = int(ty.strftime("%Y"))
#             id = self.gonglinian2ganzhi(tsr)
#             query['start'] = id
            
        recorders = locator.query(query)
        return recorders
    
    def gonglinian2ganzhi(self,nian):
        "公历年份转干支"
        yu = int(nian) % 60
        if yu >4:
            id = yu - 4 + 1
        else:
            id = yu + 60 - 4 + 1
        
        
    
     
###### output class
 # ajax multi-condition search relation db
class YaoXingAjaxsearch(BrowserView):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def Datecondition(self,key):
        "构造日期搜索条件"
        end = datetime.datetime.today()
#最近一周
        if key == 1:
            start = end - datetime.timedelta(7)
#最近一月
        elif key == 2:
            start = end - datetime.timedelta(30)
#最近一年
        elif key == 3:
            start = end - datetime.timedelta(365)
#最近两年
        elif key == 4:
            start = end - datetime.timedelta(365*2)
#最近五年
        else:
            start = end - datetime.timedelta(365*5)
#            return    { "query": [start,],"range": "min" }
        datecondition = { "query": [start, end],"range": "minmax" }
        return datecondition

    def searchview(self,viewname="yaoxing_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def __call__(self):
#        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = self.searchview()
 # datadic receive front ajax post data
        datadic = self.request.form

        start = int(datadic['start']) # batch search start position
        size = int(datadic['size'])      # batch search size
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()
#         origquery = searchview.getPathQuery()
        origquery = {}
        # default reverse,as is desc
        origquery['sort_on'] = sortcolumn
        # sql db sortt_order:asc,desc
        origquery['sort_order'] = sortdirection
 #模糊搜索
        if keyword != "":
            origquery['SearchableText'] = '%'+keyword+'%'
        else:
            origquery['SearchableText'] = ""
#origquery provide  batch search
        origquery['size'] = size
        origquery['start'] = start
#totalquery  search all
        totalquery = origquery.copy()
        totalquery['size'] = 0
        # search all   size = 0 return numbers of recorders
        totalnum = searchview.search_multicondition(totalquery)

        resultDicLists = searchview.search_multicondition(origquery)
        api = searchview.get_locator("yaoxing")
        del origquery
        del totalquery
#call output function
# resultDicLists like this:[(u'C7', u'\u4ed6\u7684\u624b\u673a')]
        data = self.output(start,size,totalnum, resultDicLists,api)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        跨表访问时需要api
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        base = get_container_by_type("cms.db.yaoxing").getURL()
        if self.searchview().canbeInput:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-2 text-left"><a href="%(obj_url)s">%(title)s</a></td>
                                <td class="col-md-7">%(description)s</td>
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(obj_url="%s/yaoxing%s/@@base_view" % (base,i[0]),
                                            num=str(k + 1),
                                            title=i[1],
                                            description= "",
                                            edit_url="%s/@@update_yaoxing/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_yaoxing/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-2 text-left"><a href="%(obj_url)s">%(title)s</a></td>
                                <td class="col-md-7">%(description)s</td>
                                </tr> """% dict(obj_url="%s/yaoxing%s/@@base_view" % (base,i[0]),
                                            num=str(k + 1),
                                            title=i[1],
                                            description= "")
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1                                                               
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data


class YaoWeiAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="yaowei_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        base = get_container_by_type("cms.db.yaowei").getURL()       
        if self.searchview().canbeInput:
            for i in resultDicLists:

                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-2 text-left"><a href="%(obj_url)s">%(title)s</a></td>
                                <td class="col-md-7">%(description)s</td>
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(obj_url="%s/yaowei%s/@@base_view" % (base,i[0]),
                                            num=str(k + 1),
                                            title=i[1],
                                            description= "",
                                            edit_url="%s/@@update_yaowei/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_yaowei/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-3 text-left"><a href="%(obj_url)s">%(title)s</a></td>
                                <td class="col-md-8">%(description)s</td>                                
                                </tr> """% dict(obj_url="%s/yaowei%s/@@base_view" % (base,i[0]),
                                            num=str(k + 1),
                                            title=i[1],
                                            description= "")
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1                
                
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data
        
    
class JingLuoAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="jingluo_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        base = get_container_by_type("cms.db.jingluo").getURL()
        if self.searchview().canbeInput:        
            for i in resultDicLists:
                k = k + 1
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(number)s</td>
                                <td class="col-md-3 text-left"><a href="%(obj_url)s">%(title)s</a></td>
                                <td class="col-md-6">%(description)s</td>
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(obj_url="%s/jingluo%s/@@base_view" % (base,i[0]),
                                            number=k,
                                            title= i[1],
                                            description= '',
                                            edit_url="%s/@@update_jingluo/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_jingluo/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)

        else:
            for i in resultDicLists:
                k = k + 1
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(number)s</td>
                                <td class="col-md-4 text-left">%(title)s</td>
                                <td class="col-md-7">%(description)s</td>                                
                                </tr> """% dict(obj_url="%s/jingluo%s/@@base_view" % (base,i[0]),
                                            number=k,
                                            title= i[1],
                                            description= '')

                outhtml = "%s%s" %(outhtml ,out)
          
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data

class YaoAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="yao_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        base = get_container_by_type("cms.db.yao").getURL()
        if self.searchview().canbeInput:        
            for i in resultDicLists:
                yaowei = api.pk_title(i[1],YaoWei,'wei')
                yaoxing = api.pk_title(i[2],YaoXing,'xing')
                guijin = api.pk_ass_title(i[0],Yao,Yao_JingLuo_Asso,JingLuo,'jingluo_id','mingcheng')
                out = """<tr class="text-left">
                                <td class="col-md-2 text-center"><a href="%(obj_url)s">%(name)s</a></td>
                                <td class="col-md-1 text-left">%(yaowei)s</td>
                                <td class="col-md-1">%(yaoxing)s</td>
                                <td class="col-md-1">%(jingluo)s</td>
                                <td class="col-md-4">%(zhuzhi)s</td>
                                <td class="col-md-1">%(yongliang)s</td>                                
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i[0]),
                                            name=i[3],
                                            yaowei= yaowei,
                                            yaoxing= yaoxing,
                                            jingluo= guijin,
                                            zhuzhi= i[4],
                                            yongliang= i[5],
                                            edit_url="%s/@@update_yao/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_yao/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-center">%(name)s</td>
                                <td class="col-md-1 text-left"><a href="%(edit_url)s">%(yaowei)s</a></td>
                                <td class="col-md-1">%(yaoxing)s</td>
                                <td class="col-md-2">%(jingluo)s</td>
                                <td class="col-md-5">%(zhuzhi)s</td>
                                <td class="col-md-1">%(yongliang)s</td>  
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i[0]),
                                            name=i[3],
                                            yaowei= yaowei,
                                            yaoxing= yaoxing,
                                            jingluo= guijin,
                                            zhuzhi= i[4],
                                            yongliang= i[5])

                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data


class WoYaoAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="wo_yao_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        base = get_container_by_type("cms.db.yao").getURL()
        if self.searchview().canbeInput:        
            for i in resultDicLists:
#                 i = (13L, 10L, 9L, u'\u9ebb\u9ec4', None, None, 13L, 4L, 1200L, 0.76)
                yaowei = api.pk_title(i[1],YaoWei,'wei')
                yaoxing = api.pk_title(i[2],YaoXing,'xing')
                guijin = api.pk_ass_title(i[0],Yao,Yao_JingLuo_Asso,JingLuo,'jingluo_id','mingcheng')
                out = """<tr class="text-left">
                                <td class="col-md-2 text-center"><a href="%(obj_url)s">%(name)s</a></td>
                                <td class="col-md-1 text-left">%(yaowei)s</td>
                                <td class="col-md-1">%(yaoxing)s</td>
                                <td class="col-md-1">%(jingluo)s</td>
                                <td class="col-md-2">%(zhuzhi)s</td>
                                <td class="col-md-1">%(danjia)s</td>
                                <td class="col-md-1">%(kucun)s</td>
                                <td class="col-md-1">%(yongliang)s</td>                                
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i[0]),
                                            name=i[3],
                                            yaowei= yaowei,
                                            yaoxing= yaoxing,
                                            jingluo= guijin,
                                            zhuzhi= i[4],
                                            yongliang= i[5],
                                            danjia = i[9],
                                            kucun = i[8],
                                            edit_url="%s/@@update_wo_yao/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_wo_yao/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-center">%(name)s</td>
                                <td class="col-md-1 text-left"><a href="%(obj_url)s">%(yaowei)s</a></td>
                                <td class="col-md-1">%(yaoxing)s</td>
                                <td class="col-md-2">%(jingluo)s</td>
                                <td class="col-md-3">%(zhuzhi)s</td>
                                <td class="col-md-1">%(danjia)s</td>
                                <td class="col-md-1">%(kucun)s</td>
                                <td class="col-md-1">%(yongliang)s</td>  
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i[0]),
                                            name=i[3],
                                            yaowei= yaowei,
                                            yaoxing= yaoxing,
                                            jingluo= guijin,
                                            zhuzhi= i[4],
                                            yongliang= i[5],
                                            danjia = i[9],
                                            kucun = i[8]                                          
                                            )

                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data


class ChuFangAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="chufang_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]
        (2L, 2L, u'\u6842\u679d\u6c64', 5L, u'\u52a0\u70ed\u7a00\u7ca5')
        """
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        base = get_container_by_type("cms.db.chufang").getURL()
        if self.searchview().canbeInput:
            for i in resultDicLists:
                yaoes = api.pk_ass_obj_title(i[0],ChuFang,Yao_ChuFang_Asso,Yao,'yao_id','mingcheng',mapf)
                yisheng = api.pk_title(i[1],YiSheng,'xingming')

                out = """<tr class="text-left">
                                <td class="col-md-2 text-center"><a href="%(obj_url)s">%(name)s</a></td>
                                <td class="col-md-5 text-left">%(yaoes)s</td>
                                <td class="col-md-1">%(yisheng)s</td>
                                <td class="col-md-1">%(jiliang)s</td>
                                <td class="col-md-1">%(yizhu)s</td>                              
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(
                                            name=i[2],
                                            jiliang= i[3],
                                            yizhu= i[4],
                                            yaoes= yaoes,
                                            yisheng= yisheng,
                                            obj_url="%s/%s/@@base_view" % (base,i[0]),
                                            edit_url="%s/@@update_chufang/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_chufang/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-center"><a href="%(obj_url)s">%(name)s</a></td>
                                <td class="col-md-5 text-left">%(yaoes)s</td>
                                <td class="col-md-1">%(yisheng)s</td>
                                <td class="col-md-1">%(jiliang)s</td>
                                <td class="col-md-3">%(yizhu)s</td>
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i[0]),
                                            name=i[2],
                                            jiliang= i[3],
                                            yizhu= i[4],
                                            yaoes= yaoes,
                                            yisheng= yisheng)
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data


class BingRenAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="bingren_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        base = get_container_by_type("cms.db.bingren").getURL()
        if self.searchview().canbeInput:        
            for i in resultDicLists:
                if bool(i.xingbie):
                    xingbie = u'男'
                else:
                    xingbie = u'女'                 
                out = """<tr class="text-left">
                                <td class="col-md-4 text-left"><a href="%(obj_url)s">%(xingming)s</a></td>
                                <td class="col-md-1 text-center">%(xingbie)s</td>
                                <td class="col-md-1">%(nianling)s</td>
                                <td class="col-md-4">%(dianhua)s</td>
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i.id),
                                            xingming=i.xingming,
                                            xingbie= xingbie,
                                            nianling= i.shengri,
                                            dianhua= i.dianhua,                                            
                                            edit_url="%s/@@update_bingren/%s" % (contexturl,i.id),
                                            delete_url="%s/@@delete_bingren/%s" % (contexturl,i.id))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-4 text-left"><a href="%(obj_url)s">%(xingming)s</a></td>
                                <td class="col-md-2 text-center">%(xingbie)s</td>
                                <td class="col-md-2">%(nianling)s</td>
                                <td class="col-md-4">%(dianhua)s</td>
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i.id),
                                            xingming=i.xingming,
                                            xingbie= i.xingbie,
                                            nianling= i.shengri,
                                            dianhua= i.dianhua)
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1                
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data


class DiZhiAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="dizhi_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
#         base = get_container_by_type("cms.db.dizhi").getURL()
        if self.searchview().canbeInput:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-left">%(guojia)s</td>
                                <td class="col-md-2">%(sheng)s</td>
                                <td class="col-md-2">%(shi)s</td>
                                <td class="col-md-5">%(jiedao)s</td>                            
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(
                                            guojia=i[1],
                                            sheng= i[2],
                                            shi= i[3],
                                            jiedao= i[4],
                                            edit_url="%s/@@update_dizhi/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_dizhi/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-left">%(guojia)s</td>
                                <td class="col-md-2">%(sheng)s</td>
                                <td class="col-md-3">%(shi)s</td>
                                <td class="col-md-5">%(jiedao)s</td>                          
                                </tr> """% dict(
                                            guojia=i[1],
                                            sheng= i[2],
                                            shi= i[3],
                                            jiedao= i[4],)
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data


class GeRenDiZhiAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="gerendizhi_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
#         base = get_container_by_type("cms.db.dizhi").getURL()
        if self.searchview().canbeInput:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-left">%(guojia)s</td>
                                <td class="col-md-2">%(sheng)s</td>
                                <td class="col-md-2">%(shi)s</td>
                                <td class="col-md-5">%(jiedao)s</td>                            
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(
                                            guojia=i.guojia,
                                            sheng= i.sheng,
                                            shi= i.shi,
                                            jiedao= i.jiedao,
                                            edit_url="%s/@@update_gerendizhi/%s" % (contexturl,i.id),
                                            delete_url="%s/@@delete_gerendizhi/%s" % (contexturl,i.id))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-left">%(guojia)s</td>
                                <td class="col-md-2">%(sheng)s</td>
                                <td class="col-md-3">%(shi)s</td>
                                <td class="col-md-5">%(jiedao)s</td>                          
                                </tr> """% dict(
                                            guojia=i.guojia,
                                            sheng= i.sheng,
                                            shi= i.shi,
                                            jiedao= i.jiedao)
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data
    

class DanWeiDiZhiAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="danweidizhi_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
#         base = get_container_by_type("cms.db.dizhi").getURL()
        if self.searchview().canbeInput:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-left">%(guojia)s</td>
                                <td class="col-md-2">%(sheng)s</td>
                                <td class="col-md-2">%(shi)s</td>
                                <td class="col-md-5">%(jiedao)s</td>                            
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(
                                            guojia=i.guojia,
                                            sheng= i.sheng,
                                            shi= i.shi,
                                            jiedao= i.jiedao,
                                            edit_url="%s/@@update_danweidizhi/%s" % (contexturl,i.id),
                                            delete_url="%s/@@delete_danweidizhi/%s" % (contexturl,i.id))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-left">%(guojia)s</td>
                                <td class="col-md-2">%(sheng)s</td>
                                <td class="col-md-3">%(shi)s</td>
                                <td class="col-md-5">%(jiedao)s</td>                          
                                </tr> """% dict(
                                            guojia=i.guojia,
                                            sheng= i.sheng,
                                            shi= i.shi,
                                            jiedao= i.jiedao)
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data    


class DanWeiAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="danwei_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        base = get_container_by_type("cms.db.danwei").getURL()        
        if self.searchview().canbeInput:
            for i in resultDicLists:
                out = """<tr class="text-left">                                
                                <td class="col-md-1">%(num)s</td>
                                <td class="col-md-9 text-left">
                                <a href="%(obj_url)s">%(mingcheng)s</a>
                                </td>                                                               
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i[0]),
                                            num = str(k+1),
                                            mingcheng=i[2],
                                            edit_url="%s/@@update_danwei/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_danwei/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">                                
                                <td class="col-md-1">%(num)s</td>
                                <td class="col-md-11 text-left">
                                <a href="%(obj_url)s">%(mingcheng)s</a>
                                </td>                                                              
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i[0]),
                                            num = str(k+1),
                                            mingcheng=i[2])
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data        

 
class YiShengAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="yisheng_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        base = get_container_by_type("cms.db.yisheng").getURL()        
        if self.searchview().canbeInput:        
            for i in resultDicLists:
                if bool(i.xingbie):
                    xingbie = u'男'
                else:
                    xingbie = u'女'                    
                out = """<tr class="text-left">
                                <td class="col-md-4 text-left"><a href="%(obj_url)s">%(xingming)s</a></td>
                                <td class="col-md-1 text-center">%(xingbie)s</td>
                                <td class="col-md-1">%(nianling)s</td>
                                <td class="col-md-4">%(dianhua)s</td>
                                <td class="col-md-1 text-center">
                                <a href="%(edit_url)s" title="edit">
                                  <span class="glyphicon glyphicon-pencil" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                <td class="col-md-1 text-center">
                                <a href="%(delete_url)s" title="delete">
                                  <span class="glyphicon glyphicon-trash" aria-hidden="true">
                                  </span>
                                </a>
                                </td>
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i.id),
                                            xingming=i.xingming,
                                            xingbie= xingbie,
                                            nianling= i.shengri,
                                            dianhua= i.dianhua,
                                            edit_url="%s/@@update_yisheng/%s" % (contexturl,i.id),
                                            delete_url="%s/@@delete_yisheng/%s" % (contexturl,i.id))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-4 text-left"><a href="%(obj_url)s">%(xingming)s</a></td>
                                <td class="col-md-2 text-center">%(xingbie)s</td>
                                <td class="col-md-2">%(nianling)s</td>
                                <td class="col-md-4">%(dianhua)s</td>
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i.id),
                                            xingming=i.xingming,
                                            xingbie= i.xingbie,
                                            nianling= i.shengri,
                                            dianhua= i.dianhua)
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data
    
 
class NianGanZhiAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

    def searchview(self,viewname="nianganzhi_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        base = get_container_by_type("cms.db.wuyun").getURL()        
        if self.searchview().canbeInput:        
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-left"><a href="%(obj_url)s">%(ganzhi)s</a></td>
                                <td class="col-md-1 text-center">%(sitian)s</td>
                                <td class="col-md-1">%(zaiquan)s</td>
                                <td class="col-md-1">%(dayun)s</td>
                                <td class="col-md-1">%(zhuyun)s</td>
                                <td class="col-md-1">%(keyun)s</td>
                                <td class="col-md-3">%(zhuqi)s</td>
                                <td class="col-md-3">%(keqi)s</td>                                
                                </tr> """% dict(obj_url="%s/%s/@@base_view" % (base,i[0]),
                                            ganzhi=i[1],
                                            sitian= i[2],
                                            zaiquan= i[3],
                                            dayun= i[4],
                                            zhuyun=i[5],
                                            keyun= i[6],
                                            zhuqi= i[7],
                                            keqi= i[8],
                                            )
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data
    
                          
###### database actions
# Delete Update Input block
### yaoxing table
class DeleteYaoXing(form.Form):
    "delete the specify yao xing recorder"
    
    implements(IPublishTraverse)
    label = _(u"delete yao xing data")
    fields = field.Fields(IYaoXing).omit('id')
    ignoreContext = False
    id = None
    #receive url parameters
    def publishTraverse(self, request, name):
        if self.id is None:
            self.id = name
            return self
        else:
            raise NotFound()

    def getContent(self):
        locator = queryUtility(IDbapi, name='yaoxing')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        #Let z3c.form do its magic
        super(DeleteYaoXing, self).update()

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete yaoxing recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yaoxing')
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')

class InputYaoXing(form.Form):
    """input db yao xing table data
    """
    label = _(u"Input yao xing data")
    fields = field.Fields(IYaoXing).omit('id')
    ignoreContext = True

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(InputYaoXing, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit yao xing recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yaoxing')
        try:
            funcations.add(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')

class UpdateBase(z3f.EditForm):
    """
    """
    implements(IPublishTraverse)
    
    ignoreContext = False
    id = None


    def update(self):
        self.request.set('disable_border', True)
        self.request.set('disable_plone.rightcolumn',1)
        self.request.set('disable_plone.leftcolumn',1)
        super(UpdateBase, self).update()
    
    def publishTraverse(self, request, name):
        if self.id is None:
            self.id = name
            return self
        else:
            raise NotFound()
                
    
class UpdateYaoXing(form.Form):
    """update yaoxing table row data
    """

    implements(IPublishTraverse)

    label = _(u"update yao xing data")
    fields = field.Fields(IYaoXing).omit('id')
    ignoreContext = False
    id = None
    #receive url parameters
    # reset content
    def getContent(self):
        locator = queryUtility(IDbapi, name='yaoxing')
        return locator.getByCode(self.id)

    def publishTraverse(self, request, name):
        if self.id is None:
            self.id = name
            return self
        else:
            raise NotFound()

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateYaoXing, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update yao xing recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yaoxing')
        if not ('id' in data.keys()):
            data['id'] = self.id
        try:
            funcations.updateByCode(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')


class DeleteYaoWei(DeleteYaoXing):
    "delete the specify yaowei recorder"

    label = _(u"delete yao wei data")
    fields = field.Fields(IYaoWei).omit('id')

    def getContent(self):
        locator = queryUtility(IDbapi, name='yaowei')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        #Let z3c.form do its magic
        super(DeleteYaoWei, self).update()

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete yaowei recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yaowei')
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yaowei_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaowei_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaowei_listings')


class InputYaoWei(InputYaoXing):
    """input db yaowei table data
    """

    label = _(u"Input yao wei data")
    fields = field.Fields(IYaoWei).omit('id')

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(InputYaoWei, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit yaowei recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yaowei')
        try:
            funcations.add(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yaowei_listings')

        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaowei_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaowei_listings')


class UpdateYaoWei(UpdateYaoXing):
    """update yaowei table row data
    """
    label = _(u"update yao wei data")
    fields = field.Fields(IYaoWei).omit('id')

    def getContent(self):
        locator = queryUtility(IDbapi, name='yaowei')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateFashej, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update yaowei recorder
        """

        data, errors = self.extractData()
        data['id'] = self.id
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yaowei')
        try:
            funcations.updateByCode(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yaowei_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaowei_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaowei_listings')


class DeleteYao(DeleteYaoXing):
    "delete the specify yao recorder"

    label = _(u"delete yao data")
    fields = field.Fields(IYao).omit('id','yaowei_id','yaoxing_id','yaowei','yaoxing','guijing')

    def getContent(self):
        locator = queryUtility(IDbapi, name='yao')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)

        #Let z3c.form do its magic
        super(DeleteYao, self).update()


    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete yao recorder
        """

        data, errors = self.extractData()      
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yao')
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')

class InputYao(InputYaoXing):
    """input db yao table data
    """

    label = _(u"Input yao data")
    fields = field.Fields(IYaoUI).omit('id','yaowei_id','yaoxing_id')

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(InputYao, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit yao recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yao')
        columns = filter_cln(Yao)        
        #过滤非本表的字段
        yao_data = dict()
        for i in columns:
            yao_data[i] = data[i]                  
        yaowei_id = data['yaowei']
        yaoxing_id = data['yaoxing']
        guijing = data['guijing']
        fk_tables = [(yaowei_id,YaoWei,'yaowei'),(yaoxing_id,YaoXing,'yaoxing')]
        if bool(guijing):
            asso_tables = [(guijing,JingLuo,'guijing')]            
        else:
            asso_tables = []
        try:
            funcations.add_multi_tables(yao_data,fk_tables,asso_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')

        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')


class UpdateYao(UpdateYaoXing):
    """update yao table row data
    """

    label = _(u"update yao data")
    fields = field.Fields(IYaoUI).omit('id','yaowei_id','yaoxing_id')

    def getContent(self):
        # create a temp obj that provided IYaoUI
        #assemble the obj from those association tables fetch data
        locator = queryUtility(IDbapi, name='yao')
        yao_obj = locator.getByCode(self.id)
        # ignore fields list
        ignore = ['id','yaoxing_id','yaowei_id']
        # obj fields list
        objfd = ['yaowei','yaoxing']
        listobjfd = ['guijing']
        data = dict()
        for name, f in getFieldsInOrder(IYaoUI):            
            p = getattr(yao_obj, name, '')
            if name in ignore:continue
            elif name in objfd:
                data[name] = getattr(p,'id',1)
            elif name in listobjfd:
                data[name] = [getattr(j,'id',1) for j in p]
            else:
                if isinstance(p,str):
                    p = p.decode('utf-8')
                data[name] = p                         
        return YaoUI(**data)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateYao, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update yao recorder
        """

        data, errors = self.extractData()       
        yao_clmns = filter_cln(Yao)        
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yao')
        #过滤非本表的字段
        yao_data = dict()
        for i in yao_clmns:
            yao_data[i] = data[i]                               
        yao_data['id'] = self.id
        yaowei_id = data['yaowei']
        yaoxing_id = data['yaoxing']
        guijing = data['guijing']
        fk_tables = [(yaowei_id,YaoWei,'yaowei'),(yaoxing_id,YaoXing,'yaoxing')]

        if bool(guijing):
            asso_tables = [(guijing,JingLuo,'guijing')]            
        else:
            asso_tables = []
        try:
            funcations.update_multi_tables(yao_data,fk_tables,asso_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')


class DeleteWoYao(DeleteYaoXing):
    "delete the specify yao recorder"

    label = _(u"delete yao data")
    fields = field.Fields(IYao_DanWei_AssoUI).omit('danwei_id')

    def getContent(self):
        locator = queryUtility(IDbapi, name='yao_danwei')
        danwei_id = getDanWeiId()
        _obj = locator.getByKwargs(yao_id=self.id,danwei_id=danwei_id)
        # ignore fields list
        ignore = ['danwei_id']
        data = dict()
        for name, f in getFieldsInOrder(IYao_DanWei_AssoUI):            
            p = getattr(_obj, name, '')
            if name in ignore:continue
            else:
                if isinstance(p,str):
                    p = p.decode('utf-8')
                data[name] = p                         
        return EditYao_DanWei_AssoUI(**data)

    def update(self):
        self.request.set('disable_border', True)
        #Let z3c.form do its magic
        super(DeleteWoYao, self).update()

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete yao recorder
        """

        data, errors = self.extractData()       
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yao_danwei')
        danwei_id = getDanWeiId()
        try:
            funcations.deleteByKwargs(yao_id=self.id,danwei_id=danwei_id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@wo_yao_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@wo_yao_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@wo_yao_listings')

class InputWoYao(InputYaoXing):
    """input db yao table data
    """

    label = _(u"Input yao data")
    fields = field.Fields(IYao_DanWei_AssoUI).omit('danwei_id')

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(InputWoYao, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit yao recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yao_danwei')
        columns = filter_cln(Yao_DanWei_Asso)        
        #过滤非本表的字段
        _data = dict()
        for i in columns:
            _data[i] = data[i]
        danwei_id = getDanWeiId()
        yao_id = data['yao_id']
        fk_tables = [(danwei_id,DanWei,'danwei'),(yao_id,Yao,'yao')]
        try:
            funcations.add_multi_tables(_data,fk_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@wo_yao_listings')

        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@wo_yao_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@wo_yao_listings')


class UpdateWoYao(UpdateYaoXing):
    """update yao table row data
    """

    label = _(u"update yao data")
    fields = field.Fields(IYao_DanWei_AssoUI).omit('danwei_id')
    

    def getContent(self):
        # create a temp obj that provided IYaoUI
        #assemble the obj from those association tables fetch data
        locator = queryUtility(IDbapi, name='yao_danwei')
        danwei_id = getDanWeiId()
        _obj = locator.getByKwargs(yao_id=self.id,danwei_id=danwei_id)
        # ignore fields list
        ignore = ['danwei_id']
        data = dict()
        for name, f in getFieldsInOrder(IYao_DanWei_AssoUI):            
            p = getattr(_obj, name, '')
            if name in ignore:continue
            else:
                if isinstance(p,str):
                    p = p.decode('utf-8')
                data[name] = p                         
        return EditYao_DanWei_AssoUI(**data)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateWoYao, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update yao recorder
        """

        data, errors = self.extractData()       
        _clmns = filter_cln(Yao_DanWei_Asso)        
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yao_danwei')
        #过滤非本表的字段
        _data = dict()
        for i in _clmns:
            _data[i] = data[i]                              

        danwei_id = getDanWeiId()
        searchcnd = {"yao_id":data['yao_id'],"danwei_id":danwei_id}
        try:
            funcations.update_asso_table(_data,searchcnd)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@wo_yao_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@wo_yao_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@wo_yao_listings')


class DeleteJingLuo(DeleteYaoXing):
    "delete the specify jingluo recorder"

    label = _(u"delete jing luo data")
    fields = field.Fields(IJingLuo).omit('id')

    def getContent(self):
        locator = queryUtility(IDbapi, name='jingluo')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        #Let z3c.form do its magic
        super(DeleteJingLuo, self).update()


    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete jingluo recorder
        """

        data, errors = self.extractData()     
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='jingluo')
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@jingluo_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@jingluo_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@jingluo_listings')

class InputJingLuo(InputYaoXing):
    """input db jingluo table data
    """

    label = _(u"Input jing luo data")
    fields = field.Fields(IJingLuo).omit('id')

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(InputJingLuo, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit jingluo recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='jingluo')
        try:
            funcations.add(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@jingluo_listings')

        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@jingluo_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@jingluo_listings')

class UpdateJingLuo(UpdateYaoXing):
    """update jingluo table row data
    """
    label = _(u"update jingluo data")
    fields = field.Fields(IJingLuo).omit('id')

    def getContent(self):

        locator = queryUtility(IDbapi, name='jingluo')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateJingLuo, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update jingluo recorder
        """
        data, errors = self.extractData()
        data['id'] = self.id
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='jingluo')
        try:
            funcations.updateByCode(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@jingluo_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@jingluo_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@jingluo_listings')


class DeleteChuFang(DeleteYaoXing):
    "delete the specify chu fang recorder"

    label = _(u"delete chu fang data")
    fields = field.Fields(IChuFang).omit('id','yisheng_id')

    def getContent(self):

        locator = queryUtility(IDbapi, name='chufang')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)

        #Let z3c.form do its magic
        super(DeleteChuFang, self).update()

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete chu fang recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='chufang')
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@chufang_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@chufang_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@chufang_listings')


@component.adapter(IChuFangUI)
class InputChuFang(z3f.AddForm):
# class InputChuFang(InputYaoXing):
    """input db chufang table data
    """

    label = _(u"Input chu fang data")
    fields = field.Fields(IChuFangUI).omit('id','yisheng_id')
    fields['yaoes'].widgetFactory = DataGridFieldFactory
    fields['bingrens'].widgetFactory = DataGridFieldFactory

    def update(self):
        self.request.set('disable_border', True)
        self.request.set('disable_plone.rightcolumn',1)
        self.request.set('disable_plone.leftcolumn',1)
        super(InputChuFang, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit chufang recorder
        """
        #todo z3c.form.converter add adapter
        # Collection Sequence Data Converter
        #https://z3cform.readthedocs.io/en/latest/informative/converter.html        
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='chufang')             
        columns = filter_cln(ChuFang)        
        #过滤非本表的字段
        _data = dict()
        for i in columns:
            _data[i] = data[i]                  
        _id = data['yisheng']
        fk_tables = [(_id,YiSheng,'yisheng')]
        #[<cms.db.browser.interfaces.Yao_ChuFang_AssoUI object at 0x7fb156e389d0>]
        #Yao_ChuFang_Asso(yao1,chufang,7,"晒干")
        # asso_obj_tables:[(pk,targetcls,attr,[property1,property2,...]),...]
        bingrens = data['bingrens']
        if not bool(bingrens):bingrens = []        
        bingren_asso_columns = filter_cln(ChuFang_BingRen_Asso)        
        yaoes = data['yaoes']
        if not bool(yaoes):yaoes = []        
        asso_columns = filter_cln(Yao_ChuFang_Asso)
        asso_obj_tables = []
        for i in yaoes:
            pk = getattr(i,'yao_id',1)
            pk_cls = Yao
            pk_attr = 'yao'            
            asso_cls = Yao_ChuFang_Asso
            asso_attr = 'chufang'
            vls = [getattr(i,k,'') for k in asso_columns ]
            ppt = dict(zip(asso_columns,vls))
            asso_obj_tables.append((pk,pk_cls,pk_attr,asso_cls,asso_attr,ppt))                    
        for i in bingrens:
            pk = getattr(i,'bingren_id',1)
            pk_cls = BingRen
            pk_attr = 'bingren'            
            asso_cls = ChuFang_BingRen_Asso
            asso_attr = 'chufang'
            vls = [getattr(i,k,'') for k in bingren_asso_columns ]
            ppt = dict(zip(bingren_asso_columns,vls))
            asso_obj_tables.append((pk,pk_cls,pk_attr,asso_cls,asso_attr,ppt))        
        asso_tables = []
        try:
            funcations.add_multi_tables(_data,fk_tables,asso_tables,asso_obj_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@chufang_listings')

        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@chufang_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@chufang_listings')


@component.adapter(IChuFangUI)
class UpdateChuFang(UpdateBase):
    """update chufang table row data
    """

    label = _(u"update chu fang data")
    fields = field.Fields(IChuFangUI).omit('id','yisheng_id')
    fields['yaoes'].widgetFactory = DataGridFieldFactory
    fields['bingrens'].widgetFactory = DataGridFieldFactory

    def getContent(self):
        # create a temp obj that provided IYaoUI
        #assemble the obj from those association tables fetch data
        locator = queryUtility(IDbapi, name='chufang')
        _obj = locator.getByCode(self.id)
        # ignore fields list
        ignore = ['id','yisheng_id']
        # obj fields list
        objfd = ['yisheng']
        data = dict()
        bingrenlist = getattr(_obj, 'bingrens', [])
        yaolist = getattr(_obj, 'yaoes', [])
        for name, f in getFieldsInOrder(IChuFangUI):
            if name in ignore:continue
            elif name=="bingrens":
                p = bingrenlist
            elif name == "yaoes":
                p = yaolist                          
            else:
                p = getattr(_obj, name, '')                                                                          

            if name in objfd:
                data[name] = getattr(p,'id',1)
                continue
            elif name == 'yaoes':
                objs = []
                fields = ['yao_id','yaoliang','paozhi']                
                for i in p:
                    id = i.id
                    chufangid = self.id
                    qdt = {'yao_id':id,'chufang_id':chufangid} 
                    # query Yao_ChuFang_Asso obj
                    asso_obj = queryUtility(IDbapi, name='yao_chufang').\
                    get_asso_obj(qdt)
                    vls = [getattr(asso_obj,j,"") for j in fields]                   
                    vls = to_utf_8(vls)                        
                    value = dict(zip(fields,vls))
                    obj = EditYao_ChuFang_AssoUI(**value)
                    objs.append(obj)                                                         
                data[name] = objs
                continue
            elif name == 'bingrens':
                objs = []
                fields = ['bingren_id','shijian','maixiang','shexiang','zhusu']                
                for i in p:
                    id = i.id
                    chufangid = self.id
                    qdt = {'bingren_id':id,'chufang_id':chufangid} 
                    # query ChuFang_BingRen_Asso obj
                    asso_obj = queryUtility(IDbapi, name='chufang_bingren').\
                    get_asso_obj(qdt)
                    vls = [getattr(asso_obj,j,"") for j in fields]
                    vls = to_utf_8(vls)                        
                    value = dict(zip(fields,vls))
                    obj = EditChuFang_BingRen_AssoUI(**value)
                    objs.append(obj)                                                          
                data[name] = objs
                continue
            else:
                if isinstance(p,str):
                    p = p.decode('utf-8')
                data[name] = p
                continue                        

        tmp = data['jiliang']
        if isinstance(tmp,long) and bool(tmp):
            data['jiliang'] = int(tmp)
        else:
            data['jiliang'] = 0
#         import pdb
#         pdb.set_trace()
#         return data
        return ChuFangUI(**data)

#     def update(self):
#         self.request.set('disable_border', True)
#         # Let z3c.form do its magic
#         super(UpdateChuFang, self).update()

    def updateActions(self):
        """Bypass the baseclass editform - it causes problems"""
        super(z3f.EditForm, self).updateActions()

    def updateWidgets(self):
        super(UpdateChuFang, self).updateWidgets()
        self.widgets['yaoes'].allow_reorder = False
        self.widgets['yaoes'].auto_append = False
        self.widgets['bingrens'].allow_reorder = False
        self.widgets['bingrens'].auto_append = False

#     def datagridUpdateWidgets(self, subform, widgets, widget):
# 
#         if widget.name == 'form.widgets.bingrens':
#             widgets['shijian'].size = 8
#             widgets['bingren_id'].size = 8


    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update chufang recorder
        """

        data, errors = self.extractData()
        _clmns = filter_cln(ChuFang)
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='chufang')
        #过滤非本表的字段
        _data = dict()
        for i in _clmns:
            _data[i] = data[i]                               
        _data['id'] = self.id
        yisheng_id = data['yisheng']
        yaoes = data['yaoes']
        bingrens = data['bingrens']        
        fk_tables = [(yisheng_id,YiSheng,'yisheng')]
        if not bool(bingrens):bingrens = []        
        bingren_asso_columns = filter_cln(ChuFang_BingRen_Asso)        
        yaoes = data['yaoes']
        if not bool(yaoes):yaoes = []        
        asso_columns = filter_cln(Yao_ChuFang_Asso)
        asso_obj_tables = {}
        tlist = []
        for i in yaoes:
            pk = getattr(i,'yao_id',1)
            pk_cls = Yao
            pk_attr = 'yao'            
            asso_cls = Yao_ChuFang_Asso
            asso_attr = 'chufang'
            vls = [getattr(i,k,'') for k in asso_columns ]
            ppt = dict(zip(asso_columns,vls))
            tlist.append((pk,pk_cls,pk_attr,asso_cls,asso_attr,ppt)) 
        asso_obj_tables['yaoes']= tlist                   
        tlist = []
        for i in bingrens:
            pk = getattr(i,'bingren_id',1)
            pk_cls = BingRen
            pk_attr = 'bingren'            
            asso_cls = ChuFang_BingRen_Asso
            asso_attr = 'chufang'
            vls = [getattr(i,k,'') for k in bingren_asso_columns ]
            ppt = dict(zip(bingren_asso_columns,vls))
            tlist.append((pk,pk_cls,pk_attr,asso_cls,asso_attr,ppt))
        asso_obj_tables['bingrens']= tlist
        
        asso_tables = []
        try:
            funcations.update_multi_tables(_data,fk_tables,asso_tables,asso_obj_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@chufang_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@chufang_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@chufang_listings')


class DeleteBingRen(DeleteYaoXing):
    "delete the specify bing ren recorder"


    label = _(u"delete bing ren data")
    fields = field.Fields(IBingRen).omit('id','dizhi_id','dizhi')

    def getContent(self):
        locator = queryUtility(IDbapi, name='bingren')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)

        #Let z3c.form do its magic
        super(DeleteBingRen, self).update()


    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete bingren recorder
        """

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='bingren')
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@bingren_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@bingren_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@bingren_listings')

@implementer(IFieldsAndContentProvidersForm)
class InputBingRen(InputYaoXing):
    """input db bingren table data
    """

    label = _(u"Input bing ren data")
    contentProviders = ContentProviders()
    contentProviders['bingreninputHelp'] = BingRenExtendedHelp
    contentProviders['bingreninputHelp'].position = 0
    fields = field.Fields(IBingRenUI).omit('id','type','dizhi_id')

    def update(self):
        self.request.set('disable_border', True)

        # Let z3c.form do its magic
        super(InputBingRen, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit bingren recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='bingren')
        _clmns = filter_cln(BingRen)
        # type is joined inheritance polymorphic_on,should be filtered
        if "type" in _clmns:
              _clmns.remove("type")      
        #过滤非本表的字段
        _data = dict()
        for i in _clmns:
            _data[i] = data[i]                 
        _id = data['dizhi']
        fk_tables = [(_id,GeRenDiZhi,'dizhi')]
        asso_tables = []
        try:
            funcations.add_multi_tables(_data,fk_tables,asso_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@bingren_listings')

        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@bingren_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@bingren_listings')

class UpdateBingRen(UpdateYaoXing):
    """update bingren table row data
    """

    label = _(u"update bing ren data")
    fields = field.Fields(IBingRenUI).omit('id','dizhi_id','type')

    def getContent(self):

        locator = queryUtility(IDbapi, name='bingren')
        _obj = locator.getByCode(self.id)
        # ignore fields list
        ignore = ['id','dizhi_id','type']
        # obj fields list
        objfd = ['dizhi']
        data = dict()
        for name, f in getFieldsInOrder(IBingRenUI):            
            p = getattr(_obj, name, '')
            if name in ignore:continue
            elif name in objfd:
                data[name] = getattr(p,'id',1)
            else:
                if isinstance(p,str):
                    p = p.decode('utf-8')
                data[name] = p                        
        return BingRenUI(**data)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateBingRen, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update bing ren recorder
        """

        data, errors = self.extractData()       
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='bingren')
        #过滤非本表的字段
        _clmns = filter_cln(BingRen)
        if "type" in _clmns:
            _clmns.remove("type")        
        _data = dict()
        for i in _clmns:
            _data[i] = data[i]                               
        _data['id'] = self.id
        _id = data['dizhi']
        fk_tables = [(_id,GeRenDiZhi,'dizhi')]
        try:
            funcations.update_multi_tables(_data,fk_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@bingren_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@bingren_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@bingren_listings')


class DeleteDiZhi(DeleteYaoXing):
    "delete the specify di zhi recorder"

    label = _(u"delete di zhi data")
    fields = field.Fields(IDiZhi).omit('id')

    def getContent(self):

        locator = queryUtility(IDbapi, name='dizhi')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        super(DeleteDiZhi, self).update()

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete dizhi recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='dizhi')
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@dizhi_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@dizhi_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@dizhi_listings')

class InputDiZhi(InputYaoXing):
    """input db dizhi table data
    """

    label = _(u"Input dizhi data")
    fields = field.Fields(IDiZhi).omit('id')

    def update(self):
        self.request.set('disable_border', True)

        # Let z3c.form do its magic
        super(InputDiZhi, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit dizhi recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='dizhi')
        try:
            funcations.add(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@dizhi_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@dizhi_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@dizhi_listings')

class UpdateDiZhi(UpdateYaoXing):
    """update dizhi table row data
    """

    label = _(u"update di zhi data")
    fields = field.Fields(IDiZhi).omit('id')

    def getContent(self):

        locator = queryUtility(IDbapi, name='dizhi')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateDiZhi, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update dizhi recorder
        """
        data, errors = self.extractData()
        data['id'] =self.id
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='dizhi')
        try:
            funcations.updateByCode(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@dizhi_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@dizhi_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@dizhi_listings')

class DeleteDanWeiDiZhi(DeleteYaoXing):
    "delete the specify danweidizhi recorder"

    label = _(u"delete dan wei di zhi data")
    fields = field.Fields(IDanWeiDiZhi).omit('id')

    def getContent(self):

        locator = queryUtility(IDbapi, name='danweidizhi')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        super(DeleteDanWeiDiZhi, self).update()

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete danweidizhi recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='danweidizhi')
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@danweidizhi_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danweidizhi_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danweidizhi_listings')

class InputDanWeiDiZhi(InputYaoXing):
    """input danweidizhi table data
    """

    label = _(u"Input danwei dizhi data")
    fields = field.Fields(IDanWeiDiZhi).omit('id')

    def update(self):
        self.request.set('disable_border', True)

        # Let z3c.form do its magic
        super(InputDanWeiDiZhi, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit danweidizhi recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='danweidizhi')
        try:
            funcations.add(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@danweidizhi_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danweidizhi_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danweidizhi_listings')

class UpdateDanWeiDiZhi(UpdateYaoXing):
    """update danweidizhi table row data
    """

    label = _(u"update danwei dizhi data")
    fields = field.Fields(IDanWeiDiZhi).omit('id')

    def getContent(self):

        locator = queryUtility(IDbapi, name='danweidizhi')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateDanWeiDiZhi, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update danweidizhi recorder
        """
        data, errors = self.extractData()
        data['id'] =self.id
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='danweidizhi')
        try:
            funcations.updateByCode(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@danweidizhi_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danweidizhi_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danweidizhi_listings')
        
        
class DeleteGeRenDiZhi(DeleteYaoXing):
    "delete the specify ge ren di zhi recorder"

    label = _(u"delete ge ren di zhi data")
    fields = field.Fields(IGeRenDiZhi).omit('id')

    def getContent(self):

        locator = queryUtility(IDbapi, name='gerendizhi')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        super(DeleteGeRenDiZhi, self).update()

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete geren dizhi recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='gerendizhi')
        rt = funcations.DeleteByCode(self.id)
        if rt != True:
            IStatusMessage(self.request).add(str(rt), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@gerendizhi_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@gerendizhi_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@gerendizhi_listings')

class InputGeRenDiZhi(InputYaoXing):
    """input gerendizhi table data
    """

    label = _(u"Input geren dizhi data")
    fields = field.Fields(IGeRenDiZhi).omit('id')

    def update(self):
        self.request.set('disable_border', True)

        # Let z3c.form do its magic
        super(InputGeRenDiZhi, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit geren dizhi recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='gerendizhi')
        try:
            funcations.add(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@gerendizhi_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@gerendizhi_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@gerendizhi_listings')

class UpdateGeRenDiZhi(UpdateYaoXing):
    """update gerendizhi table row data
    """

    label = _(u"update ge ren di zhi data")
    fields = field.Fields(IGeRenDiZhi).omit('id')

    def getContent(self):

        locator = queryUtility(IDbapi, name='gerendizhi')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateGeRenDiZhi, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update dizhi recorder
        """
        data, errors = self.extractData()
        data['id'] =self.id
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='gerendizhi')
        try:
            funcations.updateByCode(data)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@gerendizhi_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@gerendizhi_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@gerendizhi_listings')        


class DeleteDanWei(DeleteYaoXing):
    "delete the specify dan wei recorder"

    label = _(u"delete dan wei data")
    fields = field.Fields(IDanWei).omit('id','dizhi_id','dizhi')

    def getContent(self):

        locator = queryUtility(IDbapi, name='danwei')
        return locator.getByCode(self.id)

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete dan wei recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='danwei')
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')

@implementer(IFieldsAndContentProvidersForm)
class InputDanWei(InputYaoXing):
    """input dan wei table data
    """

    label = _(u"Input dan wei data")
    contentProviders = ContentProviders()
    contentProviders['danweiinputHelp'] = DanWeiExtendedHelp
    contentProviders['danweiinputHelp'].position = 0    
    fields = field.Fields(IDanWeiUI).omit('id','dizhi_id')

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit danwei recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='danwei')
        _clmns = filter_cln(DanWei)        
        #过滤非本表的字段
        danwei_data = dict()
        for i in _clmns:
            danwei_data[i] = data[i]                 
        dizhi_id = data['dizhi']
        fk_tables = [(dizhi_id,DanWeiDiZhi,'dizhi')]
        asso_tables = []
        try:
            funcations.add_multi_tables(danwei_data,fk_tables,asso_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')

class UpdateDanWei(UpdateYaoXing):
    """update dan wei table row data
    """

    label = _(u"update dan wei data")
    fields = field.Fields(IDanWeiUI).omit('id','dizhi_id')

    def getContent(self):

        locator = queryUtility(IDbapi, name='danwei')
        _obj = locator.getByCode(self.id)
        # ignore fields list
        ignore = ['id','dizhi_id']
        # obj fields list
        objfd = ['dizhi']
        data = dict()
        for name, f in getFieldsInOrder(IDanWeiUI):            
            p = getattr(_obj, name, '')
            if name in ignore:continue
            elif name in objfd:
                data[name] = getattr(p,'id',1)
            else:
                if isinstance(p,str):
                    p = p.decode('utf-8')                
                data[name] = p                         
        return DanWeiUI(**data)


    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update model recorder
        """
        data, errors = self.extractData()
        _clmns = filter_cln(DanWei)       
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='danwei')
        #过滤非本表的字段
        _data = dict()
        for i in _clmns:
            _data[i] = data[i]                               
        _data['id'] = self.id
        _id = data['dizhi']
        fk_tables = [(_id,DanWeiDiZhi,'dizhi')]
        try:
            funcations.update_multi_tables(_data,fk_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')


class DeleteYiSheng(DeleteYaoXing):
    "delete the specify yi sheng recorder"


    label = _(u"delete yi sheng data")
    fields = field.Fields(IYiSheng).omit('id','danwei_id','danwei')

    def getContent(self):

        locator = queryUtility(IDbapi, name='yisheng')
        return locator.getByCode(self.id)

    @button.buttonAndHandler(_(u"Delete"))
    def submit(self, action):
        """Delete yisheng recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yisheng')
        try:
            funcations.DeleteByCode(self.id)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')
        confirm = _(u"Your data  has been deleted.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data delete
        """
        confirm = _(u"Delete cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')

@implementer(IFieldsAndContentProvidersForm)
class InputYiSheng(InputYaoXing):
    """input db yisheng table data
    """

    label = _(u"Input yi sheng data")
    contentProviders = ContentProviders()
    contentProviders['yishenginputHelp'] = YiShengExtendedHelp
    contentProviders['yishenginputHelp'].position = 0    
    fields = field.Fields(IYiShengUI).omit('id','danwei_id','type')

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit yisheng recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yisheng')
        _clmns = filter_cln(YiSheng)
        if "type" in _clmns:
            _clmns.remove("type")       
        #过滤非本表的字段
        _data = dict()
        for i in _clmns:
            _data[i] = data[i]
                 
        _id = data['danwei']
        fk_tables = [(_id,DanWei,'danwei')]
        try:
            funcations.add_multi_tables(_data,fk_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')

class UpdateYiSheng(UpdateYaoXing):
    """update yisheng table row data
    """

    label = _(u"update yi sheng data")
    fields = field.Fields(IYiShengUI).omit('id','danwei_id','type')

    def getContent(self):

        locator = queryUtility(IDbapi, name='yisheng')
        _obj = locator.getByCode(self.id)
        # ignore fields list
        ignore = ['id','danwei_id','type']
        # obj fields list
        objfd = ['danwei']
        data = dict()
        for name, f in getFieldsInOrder(IYiShengUI):            
            p = getattr(_obj, name, '')
            if name in ignore:continue
            elif name in objfd:
                data[name] = getattr(p,'id',1)
            else:
                if isinstance(p,str):
                    p = p.decode('utf-8')
                data[name] = p                        
        return YiShengUI(**data)

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update yisheng recorder
        """
        data, errors = self.extractData()     
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yisheng')
        #过滤非本表的字段
        _clmns = filter_cln(YiSheng)
        if "type" in _clmns:
            _clmns.remove("type")          
        _data = dict()
        for i in _clmns:
            _data[i] = data[i]                               
        _data['id'] = self.id
        _id = data['danwei']
        fk_tables = [(_id,DanWei,'danwei')]
        try:
            funcations.update_multi_tables(_data,fk_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')


