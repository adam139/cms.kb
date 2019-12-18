#-*- coding: UTF-8 -*-
from plone import api
from z3c.form import field
import json
from zope.event import notify
from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.interface import Interface
from Products.Five.browser import BrowserView 
from zope.component import getMultiAdapter
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize.instance import memoize
from zope.interface import Interface
# from plone.directives import dexterity
from plone.memoize.instance import memoize
from Products.CMFPlone.resources import add_bundle_on_request
from Products.CMFPlone.resources import add_resource_on_request
from cms.db.interfaces import IDbapi
from cms.db.contents.yaofolder import IYaofolder
from cms.db.contents.ormfolder import IOrmfolder
from cms.db.contents.yao import IYao
from cms.db.orm import ChuFang
from cms.db.orm import YaoWei,YaoXing,JingLuo,Yao_JingLuo_Asso
from cms.db.orm import Yao,Yao_ChuFang_Asso,ChuFang
from cms.db.orm import ChuFang_BingRen_Asso, BingRen
from cms.db import  Session
from cms.db.dbutility import map_yao_chufang_table as mapf
from cms.db.dbutility import map_chufang_bingren_table as mapcb

from cms.theme.interfaces import IThemeSpecific

from cms.db import _


class BaseView(BrowserView):
    "base view"  
    
    def __init__(self,context, request):
        # Each view instance receives context and request as construction parameters
        self.context = context
        self.request = request
#         add_resource_on_request(self.request, 'load-more')    
    
    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm    
            
    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ManagePortal,self.context)
       
    def getobj_url(self,type):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type=type)
        if bool(brains):
            return brains[0].getURL()
        else:
            return ''
    
    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')

        title = translation_service.translate(
                                                  value,
                                                  domain='plone',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default='')
        return title
    
    def getags(self):
        "get context's subject and output"
        context = self.context
        base = context.aq_parent.absolute_url()
        sts = context.subject
        label = u"标签".encode('utf-8')
        items = ['<li class="first">%s:</li>' % label]
        for j in sts:
            item = """<li>
            <a class="btn btn-default" href='%s/@@sysajax_listings?subject=%s'>%s</a></li>""" % (base,j,j)
            items.append(item)
        return "".join(items)       
         
    
class YaoView(BaseView):
    "content type:yao view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    
    @memoize
    def get_chufang(self,yaoid):
        "search this some chufangs that contained the yao,"
        "return chufangs list"
        
        yaoid = long(yaoid)
        chufangs = Session.query(ChuFang).filter(ChuFang.yaoes.any(id = yaoid)).all()
        rt =[]

        if bool(chufangs):
            base = self.getobj_url("cms.db.chufangfolder")
            for j in chufangs:
                url = "%s/%s" % (base,str(j.id))
                item = "<li><a href=%s>%s</a></li>" % (url,j.mingcheng)
                rt.append(item)
            return ''.join(rt) 
        
        return "<li>None</li>"    
    
    @memoize
    def get_yaowei(self,yaoid):
        "search this some chufangs that contained the yao,"
        "return chufangs list"
        
        yaoid = long(yaoid)
        locator = queryUtility(IDbapi, name='yao')
        wei =locator.pk_obj_property(yaoid,'yaowei','wei')
        return wei
    
    @memoize
    def get_yaoxing(self,yaoid):
        "search this some chufangs that contained the yao,"
        "return chufangs list"
        
        yaoid = long(yaoid)
        locator = queryUtility(IDbapi, name='yao')   
        xing =locator.pk_obj_property(yaoid,'yaoxing','xing')        
        return xing
    
    @memoize    
    def get_guijing(self,yaoid):
        
        yaoid = long(yaoid)
        locator = queryUtility(IDbapi, name='yao')        
        out = locator.pk_ass_title(yaoid,Yao,Yao_JingLuo_Asso,JingLuo,'jingluo_id','mingcheng')
        return out


class BingRenView(BaseView):
    "content type:yao view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    @memoize
    def relative_chufang(self,id):
        ""
        cnlist = self.get_chufang(id)
        if cnlist[0]:
            rt =[]        
            base = self.getobj_url("cms.db.bingrenfolder")
            for j in cnlist[1]:
                url = "%s/%s" % (base,str(j.id))
                item = "<li><a href=%s>%s</a></li>" % (url,j.mingcheng)
                rt.append(item)
            return ''.join(rt)             
        return False
        
    
    
    def get_chufang(self,id):
        "get all chufang by bingren id"
        id = long(id)
        chufangs = Session.query(ChuFang).filter(ChuFang.bingrens.any(id = id)).all()
        if bool(chufangs):
            return (True,chufangs)
        else:
            return (False,[])
       

class ChuFangView(BaseView):
    "content type:chufang view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    @memoize
    def chufang_structure(self,id):
        ""
        
        _id = long(id)
        locator = queryUtility(IDbapi, name='chufang')        
        out = locator.pk_ass_obj_title(_id,ChuFang,Yao_ChuFang_Asso,Yao,'yao_id','mingcheng',mapf)
        out = out.replace(";","</tr><tr>")
        out = "<tr>%s</tr>" % out       
        return out

    
    def bingrens_table(self,id):
        "output bingren list"
        
        _id = long(id)
        locator = queryUtility(IDbapi, name='chufang')        
        out = locator.pk_ass_obj_title(_id,ChuFang,ChuFang_BingRen_Asso,BingRen,'bingren_id','xingming',mapcb)

        out = out.replace(";","</tr><tr>")
        out = "<tr>%s</tr>" % out       
        return out            


class YaoWeiView(BaseView):
    "content type:yaowei view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
class YaoXingView(BaseView):
    "content type:yaoxing view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
        
class JingLuoView(BaseView):
    "content type:jingluo view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True) 
        
class YiShengView(BaseView):
    "content type:jingluo view"

    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)                                               
