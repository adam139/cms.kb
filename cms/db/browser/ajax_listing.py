#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope.component import getMultiAdapter
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.CMFCore.interfaces import ISiteRoot
from plone.memoize.instance import memoize
from Products.Five.browser import BrowserView
# input data view
from plone.directives import form
from z3c.form import field, button
from Products.statusmessages.interfaces import IStatusMessage
from cms.db.interfaces import InputError
from zope.component import queryUtility
from cms.db.interfaces import IDbapi
# from cms.db.interfaces import IModelLocator,IFashejLocator,IJingLuoLocator,IChuFangLocator,IBingRenLocator
from cms.db.orm import IYaoWei,YaoWei
from cms.db.orm import IYaoXing,YaoXing
from cms.db.orm import IJingLuo,JingLuo
# 有外键的表必须调用定制UI接口
from cms.db.browser.interfaces import IYaoUI
from cms.db.browser.interfaces import IDanWeiUI
from cms.db.browser.interfaces import IYiShengUI
from cms.db.browser.interfaces import IBingRenUI
from cms.db.browser.interfaces import IChuFangUI
from cms.db.orm import Yao
from cms.db.orm import IChuFang,ChuFang
from cms.db.orm import IDiZhi,DiZhi
from cms.db.orm import IDanWei,DanWei
from cms.db.orm import IYiSheng,YiSheng
from cms.db.orm import IBingRen,BingRen
from cms.db.orm import Yao_JingLuo_Asso,ChuFang_BingRen_Asso,Yao_ChuFang_Asso

from cms.db.contents.ormfolder import Iormfolder
# update data view
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zExceptions import NotFound
from cms.db import InputDb
from cms.db import _

grok.templatedir('templates')

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
### log lib start
#yaoxing table
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


#user_logs table
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
### log lib end

### parameters lib start
# fashej table
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
    
# fashetx table
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
        recorders = locator.query(query)
        return recorders

# bingren table
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
        recorders = locator.query(query)
        return recorders


     
###### output class
 # ajax multi-condition search relation db
class YaoXingAjaxsearch(BrowserView):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """
#     grok.context(Interface)
#     grok.name('yaoxing_ajaxsearch')
#     grok.require('zope2.View')
#     grok.require('emc.project.view_projectsummary')
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

#         inputable= self.canbeInput()
        for i in resultDicLists:
            out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-2 text-left"><a href="%(edit_url)s">%(title)s</a></td>
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
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            num=str(k + 1),
                                            title=i[0],
                                            description= "",
                                            edit_url="%s/@@update_yaoxing/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_yaoxing/%s" % (contexturl,i[0]))
            outhtml = "%s%s" %(outhtml ,out)
            k = k + 1
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data


### parameters lib output class
class YaoWeiAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

#     grok.name('yaowei_ajaxsearch')

    def searchview(self,viewname="yaowei_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()       
        if self.searchview().canbeInput:
            for i in resultDicLists:

                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-2 text-left"><a href="%(edit_url)s">%(title)s</a></td>
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
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            num=str(k + 1),
                                            title=i[0],
                                            description= "",
                                            edit_url="%s/@@update_yaowei/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_yaowei/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(num)s</td>
                                <td class="col-md-3 text-left"><a href="%(edit_url)s">%(title)s</a></td>
                                <td class="col-md-8">%(description)s</td>                                
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            num=str(k + 1),
                                            title=i[0],
                                            description= "",
                                            edit_url="%s/@@update_yaowei/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_yaowei/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1                
                
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data
        
    
class JingLuoAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

#     grok.name('jingluo_ajaxsearch')

    def searchview(self,viewname="jingluo_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        if self.searchview().canbeInput:        
            for i in resultDicLists:
                k = k + 1
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(number)s</td>
                                <td class="col-md-3 text-left"><a href="%(edit_url)s">%(title)s</a></td>
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
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            number=k,
                                            title= i[1],
                                            description= '',
                                            edit_url="%s/@@update_jieshouj/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_jieshouj/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(number)s</td>
                                <td class="col-md-4 text-left">%(title)s</td>
                                <td class="col-md-7">%(description)s</td>                                
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            number=k,
                                            title= i[1],
                                            description= '')

                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data

class YaoAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """

#     grok.name('yao_ajaxsearch')

    def searchview(self,viewname="yao_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        if self.searchview().canbeInput:        
            for i in resultDicLists:
                yaowei = api.pk_title(i[1],YaoWei,'wei')
                yaoxing = api.pk_title(i[2],YaoXing,'xing')
                guijin = api.pk_ass_title(i[0],Yao,Yao_JingLuo_Asso,JingLuo,'jingluo_id','mingcheng')
                out = """<tr class="text-left">
                                <td class="col-md-2 text-center">%(name)s</td>
                                <td class="col-md-1 text-left"><a href="%(edit_url)s">%(yaowei)s</a></td>
                                <td class="col-md-1">%(yaoxing)s</td>
                                <td class="col-md-1">%(jingluo)s</td>
                                <td class="col-md-5">%(zhuzhi)s</td>                                
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
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            name=i[3],
                                            yaowei= yaowei,
                                            yaoxing= yaoxing,
                                            jingluo= guijin,
                                            zhuzhi= i[4],
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
                                <td class="col-md-1">%(jingluo)s</td>
                                <td class="col-md-5">%(zhuzhi)s</td>  
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            name=i[3],
                                            yaowei= "",
                                            yaoxing= "",
                                            jingluo= "",
                                            zhuzhi= i[4])

                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data


class ChuFangAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """
#     grok.name('chufang_ajaxsearch')

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
        if self.searchview().canbeInput:
            for i in resultDicLists:
                yaoes = api.pk_ass_obj_title(i[0],ChuFang,Yao_ChuFang_Asso,Yao,'yao_id','mingcheng')
                yisheng = api.pk_title(i[1],YiSheng,'xingming')

                out = """<tr class="text-left">
                                <td class="col-md-2 text-center"><a href="%(edit_url)s">%(name)s</a></td>
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
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            name=i[2],
                                            jiliang= i[3],
                                            yizhu= i[4],
                                            yaoes= yaoes,
                                            yisheng= yisheng,
                                            edit_url="%s/@@update_chufang/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_chufang/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-center"><a href="%(edit_url)s">%(name)s</a></td>
                                <td class="col-md-5 text-left">%(yaoes)s</td>
                                <td class="col-md-1">%(yisheng)s</td>
                                <td class="col-md-1">%(jiliang)s</td>
                                <td class="col-md-3">%(yizhu)s</td>
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
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

    grok.name('bingren_ajaxsearch')

    def searchview(self,viewname="bingren_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        if self.searchview().canbeInput:        
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-center">%(cssbdm)s</td>
                                <td class="col-md-1 text-left"><a href="%(edit_url)s">%(cssbmc)s</a></td>
                                <td class="col-md-1">%(pcdm)s</td>
                                <td class="col-md-1">%(location)s</td>
                                <td class="col-md-1">%(gain)s</td>
                                <td class="col-md-1">%(polarization)s</td>
                                <td class="col-md-1">%(fwbskd)s</td>
                                <td class="col-md-1">%(fybskd)s</td>
                                <td class="col-md-1">%(txzxj)s</td>
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
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            cssbdm=i[1],
                                            cssbmc= i[2],
                                            pcdm= i[3],
                                            location= i[4],
                                            gain= i[5],
                                            polarization= i[6],
                                            fwbskd= i[7],
                                            fybskd= i[8],
                                            txzxj= i[9],
                                            edit_url="%s/@@update_bingren/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_bingren/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-center">%(cssbdm)s</td>
                                <td class="col-md-2 text-left"><%(cssbmc)s</td>
                                <td class="col-md-1">%(pcdm)s</td>
                                <td class="col-md-1">%(location)s</td>
                                <td class="col-md-1">%(gain)s</td>
                                <td class="col-md-1">%(polarization)s</td>
                                <td class="col-md-1">%(fwbskd)s</td>
                                <td class="col-md-1">%(fybskd)s</td>
                                <td class="col-md-1">%(txzxj)s</td>
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            cssbdm=i[1],
                                            cssbmc= i[2],
                                            pcdm= i[3],
                                            location= i[4],
                                            gain= i[5],
                                            polarization= i[6],
                                            fwbskd= i[7],
                                            fybskd= i[8],
                                            txzxj= i[9])
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1                
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data

### enviroment lib output class
class DiZhiAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """
    grok.name('dizhi_ajaxsearch')

    def searchview(self,viewname="dizhi_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        if self.searchview().canbeInput:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-center"><a href="%(edit_url)s">%(name)s</a></td>
                                <td class="col-md-1 text-left">%(bcdm)s</td>
                                <td class="col-md-1">%(location)s</td>
                                <td class="col-md-1">%(length)s</td>
                                <td class="col-md-1">%(width)s</td>
                                <td class="col-md-1">%(wk)s</td>
                                <td class="col-md-1">%(ti)s</td>
                                <td class="col-md-1">%(landform)s</td>
                                <td class="col-md-1">%(xh)s</td>                               
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
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            name=i[1],
                                            bcdm= i[2],
                                            location= i[3],
                                            length= i[4],
                                            width= i[5],
                                            wk= i[6],
                                            ti= i[7],
                                            landform= i[8],
                                            xh= i[9],
                                            edit_url="%s/@@update_bachang/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_bachang/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-center">%(name)s</td>
                                <td class="col-md-1 text-left">%(bcdm)s</td>
                                <td class="col-md-3">%(location)s</td>
                                <td class="col-md-1">%(length)s</td>
                                <td class="col-md-1">%(width)s</td>
                                <td class="col-md-1">%(wk)s</td>
                                <td class="col-md-1">%(ti)s</td>
                                <td class="col-md-1">%(landform)s</td>
                                <td class="col-md-1">%(xh)s</td>
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            name=i[1],
                                            bcdm= i[2],
                                            location= i[3],
                                            length= i[4],
                                            width= i[5],
                                            wk= i[6],
                                            ti= i[7],
                                            landform= i[8],
                                            xh= i[9])
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data


class DanWeiAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """
    grok.name('danwei_ajaxsearch')

    def searchview(self,viewname="danwei_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        if self.searchview().canbeInput:
            for i in resultDicLists:
                out = """<tr class="text-left">                                
                                <td class="col-md-1 text-left"><a href="%(edit_url)s">%(shelter_name)s</a></td>
                                <td class="col-md-1">%(lt_x)s</td>
                                <td class="col-md-1">%(lt_y)s</td>
                                <td class="col-md-1">%(lt_z)s</td>
                                <td class="col-md-1">%(ld_x)s</td>
                                <td class="col-md-1">%(ld_y)s</td>
                                <td class="col-md-1">%(ld_z)s</td>
                                <td class="col-md-1">%(rt_x)s</td>
                                <td class="col-md-1">%(rt_x)s</td>
                                <td class="col-md-1">%(rt_z)s</td>                               
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
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            shelter_name=i[1],
                                            lt_x= i[2],
                                            lt_y= i[3],
                                            lt_z= i[4],
                                            ld_x= i[5],
                                            ld_y= i[6],
                                            ld_z= i[7],
                                            rt_x= i[8],
                                            rt_y= i[9],
                                            rt_z= i[10],
                                            edit_url="%s/@@update_bachangzhdw/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_bachangzhdw/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">                                
                                <td class="col-md-2 text-left">%(shelter_name)s</td>
                                <td class="col-md-2">%(lt_x)s</td>
                                <td class="col-md-1">%(lt_y)s</td>
                                <td class="col-md-1">%(lt_z)s</td>
                                <td class="col-md-1">%(ld_x)s</td>
                                <td class="col-md-1">%(ld_y)s</td>
                                <td class="col-md-1">%(ld_z)s</td>
                                <td class="col-md-1">%(rt_x)s</td>
                                <td class="col-md-1">%(rt_x)s</td>
                                <td class="col-md-1">%(rt_z)s</td>
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            shelter_name=i[1],
                                            lt_x= i[2],
                                            lt_y= i[3],
                                            lt_z= i[4],
                                            ld_x= i[5],
                                            ld_y= i[6],
                                            ld_z= i[7],
                                            rt_x= i[8],
                                            rt_y= i[9],
                                            rt_z= i[10])
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1            
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}
        return data        
 
class YiShengAjaxsearch(YaoXingAjaxsearch):
    """AJAX action for search DB.
    receive front end ajax transform parameters
    """
    grok.name('yisheng_ajaxsearch')

    def searchview(self,viewname="yisheng_listings"):
        searchview = getMultiAdapter((self.context, self.request),name=viewname)
        return searchview

    def output(self,start,size,totalnum,resultDicLists,api):
        """根据参数total,resultDicLists,返回json 输出,resultDicLists like this:
        [(u'C7', u'\u4ed6\u7684\u624b\u673a')]"""
        outhtml = ""
        k = 0
        contexturl = self.context.absolute_url()
        if self.searchview().canbeInput:        
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-1 text-left"><a href="%(edit_url)s">%(sbmc)s</a></td>
                                <td class="col-md-1">%(x)s</td>
                                <td class="col-md-1">%(y)s</td>
                                <td class="col-md-1">%(z)s</td>
                                <td class="col-md-1">%(ft)s</td>
                                <td class="col-md-1">%(pt_u)s</td>
                                <td class="col-md-1">%(pt_l)s</td>
                                <td class="col-md-1">%(num)s</td>
                                <td class="col-md-1">%(fu)s</td>
                                <td class="col-md-1">%(fl)s</td>                               
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
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            sbmc=i[1],
                                            x= i[2],
                                            y= i[3],
                                            z= i[4],
                                            ft= i[5],
                                            pt_u= i[6],
                                            pt_l= i[7],
                                            num= i[8],
                                            fu= i[9],
                                            fl= i[10],
                                            edit_url="%s/@@update_bachangfshj/%s" % (contexturl,i[0]),
                                            delete_url="%s/@@delete_bachangfshj/%s" % (contexturl,i[0]))
                outhtml = "%s%s" %(outhtml ,out)
                k = k + 1
        else:
            for i in resultDicLists:
                out = """<tr class="text-left">
                                <td class="col-md-2 text-left">%(sbmc)s</td>
                                <td class="col-md-2">%(x)s</td>
                                <td class="col-md-1">%(y)s</td>
                                <td class="col-md-1">%(z)s</td>
                                <td class="col-md-1">%(ft)s</td>
                                <td class="col-md-1">%(pt_u)s</td>
                                <td class="col-md-1">%(pt_l)s</td>
                                <td class="col-md-1">%(num)s</td>
                                <td class="col-md-1">%(fu)s</td>
                                <td class="col-md-1">%(fl)s</td>
                                </tr> """% dict(objurl="%s/@@view" % contexturl,
                                            sbmc=i[1],
                                            x= i[2],
                                            y= i[3],
                                            z= i[4],
                                            ft= i[5],
                                            pt_u= i[6],
                                            pt_l= i[7],
                                            num= i[8],
                                            fu= i[9],
                                            fl= i[10])
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
    grok.context(Iormfolder)
    grok.name('delete_yaoxing')
    grok.require('cms.db.input_db')

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
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='yaoxing')
        #to do
        #fetch the pending deleting  record
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

#     grok.context(Iormfolder)
#     grok.name('input_yaoxing')
#     grok.require('cms.db.input_db')
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
#         self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')

    @button.buttonAndHandler(_(u"Cancel"))
    def cancel(self, action):
        """Cancel the data input
        """
        confirm = _(u"Input cancelled.")
        IStatusMessage(self.request).add(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url() + '/@@yaoxing_listings')

class UpdateYaoXing(form.Form):
    """update yaoxing table row data
    """

    implements(IPublishTraverse)
#     grok.context(Iormfolder)
#     grok.name('update_yaoxing')
#     grok.require('cms.db.input_db')

    label = _(u"update yao xing data")
    fields = field.Fields(IYaoXing).omit('id')
    ignoreContext = False
    id = None
    #receive url parameters
    # reset content
    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='yaoxing')
        # to do
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

##发射机数据库操作
class DeleteYaoWei(DeleteYaoXing):
    "delete the specify yaowei recorder"

    grok.name('delete_yaowei')
    label = _(u"delete yao wei data")
    fields = field.Fields(IYaoWei).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='yaowei')
        # to do
        # fetch first record as sample data
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

    grok.name('input_fashej')

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
#         self.request.response.redirect(self.context.absolute_url() + '/@@yaowei_listings')

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
#     grok.name('update_yaowei')
    label = _(u"update yao wei data")
    fields = field.Fields(IYaoWei).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='yaowei')
        # to do
        # fetch first record as sample data
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

##end发射机 数据库操作

##yao table 数据库操作
class DeleteYao(DeleteYaoXing):
    "delete the specify yao recorder"

    grok.name('delete_yao')
    label = _(u"delete yao data")
    fields = field.Fields(IYaoUI).omit('id')

    def getContent(self):
        # Get the model table query funcations
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

#     grok.name('input_yao')

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
        from sqlalchemy.inspection import inspect
        table = inspect(Yao)
        columns = [column.name for column in table.c]
        #过滤主键,外键
        columns = filter(lambda elem: not elem.endswith("id"),columns)        
        #过滤非本表的字段
        yao_data = dict()
        for i in columns:
            yao_data[i] = data[i]
#         yao_data = dict(filter(lambda elem: elem in columns,data.items()))       

# add_multi_tables(self,kwargs,fk_tables,asso_tables):
#         "添加表记录的同时,并关联其他表记录"
        #外键关联表 fk_tables: [(pk,map_cls,attr),...]
        # 多对多关联表 asso_tables:[([pk1,pk2,...],map_cls,attr),...]                   
        yaowei_id = data['yaowei']
        yaoxing_id = data['yaoxing']
        guijing = data['guijing']
        fk_tables = [(yaowei_id,'YaoWei','yaowei'),(yaoxing_id,'YaoXing','yaoxing')]

        if bool(guijing):
            asso_tables = [(guijing,'JingLuo','guijing')]            
        else:
            asso_tables = []
        try:
            funcations.add_multi_tables(yao_data,fk_tables,asso_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
#             self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')

        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
#         self.request.response.redirect(self.context.absolute_url() + '/@@yao_listings')

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
#     grok.name('update_yao')
    label = _(u"update yao data")
    fields = field.Fields(IYaoUI).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='yao')
        # to do
        # fetch first record as sample data
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateYao, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update yao recorder
        """

        data, errors = self.extractData()
        data['id'] = self.id
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yao')
        try:
            funcations.updateByCode(data)
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

##接收机 数据库操作
class DeleteJingLuo(DeleteYaoXing):
    "delete the specify jingluo recorder"

    grok.name('delete_jieshouj')
    label = _(u"delete jing luo data")
    fields = field.Fields(IJingLuo).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='jingluo')
        # to do
        # fetch first record as sample data
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

#     grok.name('input_jingluo')

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
#         self.request.response.redirect(self.context.absolute_url() + '/@@jingluo_listings')

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
    grok.name('update_jingluo')
    label = _(u"update jingluo data")
    fields = field.Fields(IJingLuo).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='jingluo')
        # to do
        # fetch first record as sample data
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
# end 接收机 数据库操作

## 发射天线 数据库操作
class DeleteChuFang(DeleteYaoXing):
    "delete the specify chu fang recorder"

    grok.name('delete_chufang')
    label = _(u"delete chu fang data")
    fields = field.Fields(IChuFang).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='chufang')
        # to do
        # fetch first record as sample data
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


#register multiwidget for IYao_ChuFang_AssoUI
# from z3c.form.widget import FieldWidget
from cms.db.browser.interfaces import Yao_ChuFang_AssoUI,IYao_ChuFang_AssoUI
from cms.db.browser.interfaces import ChuFang_BingRen_AssoUI,IChuFang_BingRen_AssoUI
from z3c.form.object import registerFactoryAdapter
registerFactoryAdapter(IYao_ChuFang_AssoUI, Yao_ChuFang_AssoUI)
registerFactoryAdapter(IChuFang_BingRen_AssoUI, ChuFang_BingRen_AssoUI)

class InputChuFang(InputYaoXing):
    """input db chufang table data
    """

#     grok.name('input_chufang')

    label = _(u"Input chu fang data")
    fields = field.Fields(IChuFangUI).omit('id','yisheng_id')

    def update(self):
        self.request.set('disable_border', True)

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
        def filter_cln(cls):
            "过滤指定表类的列,只保留基本属性列"
            
            from sqlalchemy.inspection import inspect
            table = inspect(cls)
            columns = [column.name for column in table.c]
            #过滤主键,外键
            columns = filter(lambda elem: not elem.endswith("id"),columns)
            return columns             
#         from sqlalchemy.inspection import inspect
#         table = inspect(ChuFang)
#         columns = [column.name for column in table.c]
#         #过滤主键,外键
#         columns = filter(lambda elem: not elem.endswith("id"),columns)
        columns = filter_cln(ChuFang)        
        #过滤非本表的字段
        _data = dict()
        for i in columns:
            _data[i] = data[i]
#         yao_data = dict(filter(lambda elem: elem in columns,data.items()))       

# add_multi_tables(self,kwargs,fk_tables,asso_tables):
#         "添加表记录的同时,并关联其他表记录"
        #外键关联表 fk_tables: [(pk,map_cls,attr),...]
        # 多对多关联表 asso_tables:[([pk1,pk2,...],map_cls,attr),...]                   
        _id = data['yisheng']
        fk_tables = [(_id,'YiSheng','yisheng')]
        #[<cms.db.browser.interfaces.Yao_ChuFang_AssoUI object at 0x7fb156e389d0>]
        #Yao_ChuFang_Asso(yao1,chufang,7,"晒干")
        # asso_obj_tables:[(pk,targetcls,attr,[property1,property2,...]),...]
#         import pdb
#         pdb.set_trace()
        bingrens = data['bingrens']
        if not bool(bingrens):bingrens = []        
        bingren_asso_columns = filter_cln(ChuFang_BingRen_Asso)        
        yaoes = data['yaoes']
        if not bool(yaoes):yaoes = []        
        asso_columns = filter_cln(Yao_ChuFang_Asso)
        asso_obj_tables = []
        for i in yaoes:
            pk = getattr(i,'yao_id',1)
            pk_cls = 'Yao'
            pk_attr = 'yao'            
            asso_cls = Yao_ChuFang_Asso
            asso_attr = 'chufang'
            vls = [getattr(i,k,'') for k in asso_columns ]
            ppt = dict(zip(asso_columns,vls))
            asso_obj_tables.append((pk,pk_cls,pk_attr,asso_cls,asso_attr,ppt))                    
        for i in bingrens:
            pk = getattr(i,'bingren_id',1)
            pk_cls = 'BingRen'
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

class UpdateChuFang(UpdateYaoXing):
    """update chufang table row data
    """
    grok.name('update_chufang')
    label = _(u"update chu fang data")
    fields = field.Fields(IChuFang).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='chufang')
        # to do
        # fetch first record as sample data
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateChuFang, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update chufang recorder
        """

        data, errors = self.extractData()
        data['id'] = self.id
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='chufang')
        try:
            funcations.updateByCode(data)
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
# end 发射天线 数据库操作
## 接收天线 数据库操作
class DeleteBingRen(DeleteYaoXing):
    "delete the specify bing ren recorder"

    grok.name('delete_bingren')
    label = _(u"delete bing ren data")
    fields = field.Fields(IBingRen).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='bingren')
        # to do
        # fetch first record as sample data
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

class InputBingRen(InputYaoXing):
    """input db bingren table data
    """

#     grok.name('input_bingren')
    label = _(u"Input bing ren data")
    fields = field.Fields(IBingRenUI).omit('id')

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
        from sqlalchemy.inspection import inspect
        table = inspect(BingRen)
        columns = [column.name for column in table.c]
        #过滤主键,外键
        columns = filter(lambda elem: not elem.endswith("id"),columns)        
        #过滤非本表的字段
        _data = dict()
        for i in columns:
            _data[i] = data[i]
                 
        _id = data['dizhi_id']
        fk_tables = [(_id,'DiZhi','dizhi')]
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
    grok.name('update_bingren')
    label = _(u"update bing ren data")
    fields = field.Fields(IBingRen).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='bingren')
        # to do
        # fetch first record as sample data
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateBingRen, self).update()

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update model recorder
        """

        data, errors = self.extractData()
        data['id'] =self.id
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='bingren')
        try:
            funcations.updateByCode(data)
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
# end 接收天线 数据库操作

## 滤波器 数据库操作
class DeleteDiZhi(DeleteYaoXing):
    "delete the specify di zhi recorder"

    grok.name('delete_dizhi')
    label = _(u"delete di zhi data")
    fields = field.Fields(IDiZhi).omit('id')

    def getContent(self):
        # Get the model table query funcations
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
#     grok.name('input_dizhi')
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
#         self.request.response.redirect(self.context.absolute_url() + '/@@dizhi_listings')

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
    grok.name('update_dizhi')
    label = _(u"update di zhi data")
    fields = field.Fields(IDiZhi).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='dizhi')
        return locator.getByCode(self.id)

    def update(self):
        self.request.set('disable_border', True)
        # Let z3c.form do its magic
        super(UpdateBingRen, self).update()

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
# end 滤波器 数据库操作

## 典型天线增益子库 数据库操作
class DeleteDanWei(DeleteYaoXing):
    "delete the specify dan wei recorder"

    grok.name('delete_danwei')
    label = _(u"delete dan wei data")
    fields = field.Fields(IDanWei).omit('id')

    def getContent(self):
        # Get the model table query funcations
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

class InputDanWei(InputYaoXing):
    """input dan wei table data
    """
#     grok.name('input_danwei')
    label = _(u"Input dan wei data")
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
        from sqlalchemy.inspection import inspect
        table = inspect(DanWei)
        columns = [column.name for column in table.c]
        #过滤主键,外键
        columns = filter(lambda elem: not elem.endswith("id"),columns)        
        #过滤非本表的字段
        danwei_data = dict()
        for i in columns:
            danwei_data[i] = data[i]
                 
        dizhi_id = data['dizhi']
#         import pdb
#         pdb.set_trace()
        fk_tables = [(dizhi_id,'DiZhi','dizhi')]
        asso_tables = []
        try:
            funcations.add_multi_tables(danwei_data,fk_tables,asso_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
#         self.request.response.redirect(self.context.absolute_url() + '/@@danwei_listings')

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
    grok.name('update_dizhi')
    label = _(u"update dan wei data")
    fields = field.Fields(IDanWei).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='danwei')
        return locator.getByCode(self.id)


    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update model recorder
        """
        data, errors = self.extractData()
        data['id'] =self.id
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='danwei')
        try:
            funcations.updateByCode(data)
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
# end 典型天线增益子库 数据库操作

## 天线子库 数据库操作
class DeleteYiSheng(DeleteYaoXing):
    "delete the specify yi sheng recorder"

    grok.name('delete_yisheng')
    label = _(u"delete yi sheng data")
    fields = field.Fields(IYiSheng).omit('id')

    def getContent(self):
        # Get the model table query funcations
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

class InputYiSheng(InputYaoXing):
    """input db yisheng table data
    """
#     grok.name('input_yisheng')
    label = _(u"Input yi sheng data")
    fields = field.Fields(IYiShengUI).omit('id','danwei_id')

    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Submit yisheng recorder
        """
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yisheng')
        from sqlalchemy.inspection import inspect
        table = inspect(YiSheng)
        columns = [column.name for column in table.c]
        #过滤主键,外键
        columns = filter(lambda elem: not elem.endswith("id"),columns)        
        #过滤非本表的字段
        _data = dict()
        for i in columns:
            _data[i] = data[i]
                 
        _id = data['danwei']
        fk_tables = [(_id,'DanWei','danwei')]
        asso_tables = []
        try:
            funcations.add_multi_tables(_data,fk_tables,asso_tables)
        except InputError, e:
            IStatusMessage(self.request).add(str(e), type='error')
            self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')
        confirm = _(u"Thank you! Your data  will be update in back end DB.")
        IStatusMessage(self.request).add(confirm, type='info')
#         self.request.response.redirect(self.context.absolute_url() + '/@@yisheng_listings')

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
    grok.name('update_yisheng')
    label = _(u"update yi sheng data")
    fields = field.Fields(IYiSheng).omit('id')

    def getContent(self):
        # Get the model table query funcations
        locator = queryUtility(IDbapi, name='yisheng')
        return locator.getByCode(self.id)


    @button.buttonAndHandler(_(u"Submit"))
    def submit(self, action):
        """Update model recorder
        """
        data, errors = self.extractData()
        data['id'] =self.id
        if errors:
            self.status = self.formErrorsMessage
            return
        funcations = queryUtility(IDbapi, name='yisheng')
        try:
            funcations.updateByCode(data)
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
# end 典型天线增益子库 数据库操作
