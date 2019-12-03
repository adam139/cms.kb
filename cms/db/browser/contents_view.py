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
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize.instance import memoize
from zope.interface import Interface
# from plone.directives import dexterity
from plone.memoize.instance import memoize
from Products.CMFPlone.resources import add_bundle_on_request
from Products.CMFPlone.resources import add_resource_on_request
from cms.db.contents.yaofolder import IYaofolder
from cms.db.contents.ormfolder import IOrmfolder
from cms.db.contents.yao import IYao
from cms.db.orm import ChuFang
from cms.db import  Session

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
    
class Yao(BaseView):
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
        import pdb
        pdb.set_trace()
        if bool(chufangs):
            base = self.getobj_url("cms.db.chufangfolder")
            for j in chufangs:
                url = "%s/%s" % (base,str(j.id))
                item = "<li><a href=%s>%s</a></li>" % (url,j.mingcheng)
                rt.append(item)
            return ''.join(rt) 
        
        return "chufang1"    
    

        
