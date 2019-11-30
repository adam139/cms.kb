#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from datetime import date
from datetime import datetime
from Products.CMFCore.utils import getToolByName
from cms.db.testing import FUNCTIONAL_TESTING  

from zope.component import getUtility
from zope.interface import alsoProvides
from plone.keyring.interfaces import IKeyManager

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest
from cms.db import  Session
from cms.theme.interfaces import IThemeSpecific
from cms.db.orm import YaoWei,YaoXing,JingLuo,Yao,DiZhi,YiSheng,DanWei
from cms.db.orm import ChuFang,YiSheng,BingRen,Yao_ChuFang_Asso,ChuFang_BingRen_Asso
from cms.db.tests.base import inputvalues

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
        
    def setUp(self):

        inputvalues()       
        portal = self.layer['portal']

        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('cms.db.folder', 'folder')
        portal['folder'].invokeFactory('cms.db.ormfolder', 'ormfolder')       
        self.portal = portal

    def tearDown(self):
        
        items = Session.query(YaoWei).all()
        items.extend(Session.query(YaoXing).all())
        items.extend(Session.query(JingLuo).all())
        items.extend(Session.query(Yao).all())
        items.extend(Session.query(ChuFang).all())
        items.extend(Session.query(BingRen).all())
        items.extend(Session.query(YiSheng).all())
        items.extend(Session.query(DanWei).all())
        items.extend(Session.query(DiZhi).all())                
        for item in items:
            Session.delete(item)            
        Session.commit()   

        
    def test_yaoxing(self):
        request = self.layer['request']
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'size': '10',
                        'start':'0' ,
                        'sortcolumn':'id',
                        'sortdirection':'desc',
                        'searchabletext':''                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['folder']['ormfolder']
        view = box.restrictedTraverse('@@yaoxing_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],6)

    def test_yaowei(self):
        request = self.layer['request']
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'size': '10',
                        'start':'0' ,
                        'sortcolumn':'id',
                        'sortdirection':'desc',
                        'searchabletext':''                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['folder']['ormfolder']
        view = box.restrictedTraverse('@@yaowei_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],5)

    def test_jingluo(self):
        request = self.layer['request']
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'size': '10',
                        'start':'0' ,
                        'sortcolumn':'id',
                        'sortdirection':'desc',
                        'searchabletext':''                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['folder']['ormfolder']
        view = box.restrictedTraverse('@@jingluo_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],6)                

    def test_yaoes(self):
        request = self.layer['request']
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'size': '10',
                        'start':'0' ,
                        'sortcolumn':'id',
                        'sortdirection':'desc',
                        'searchabletext':''                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['folder']['ormfolder']
        view = box.restrictedTraverse('@@yao_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],2)        

    def test_chufang(self):
        request = self.layer['request']
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'size': '10',
                        'start':'0' ,
                        'sortcolumn':'id',
                        'sortdirection':'desc',
                        'searchabletext':''                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['folder']['ormfolder']
        view = box.restrictedTraverse('@@chufang_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],1)        

    def test_dizhi(self):
        request = self.layer['request']
        alsoProvides(request, IThemeSpecific)        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'size': '10',
                        'start':'0' ,
                        'sortcolumn':'id',
                        'sortdirection':'desc',
                        'searchabletext':''                                                                       
                        }
# Look up and invoke the view via traversal
        box = self.portal['folder']['ormfolder']
        view = box.restrictedTraverse('@@dizhi_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],2) 


             

