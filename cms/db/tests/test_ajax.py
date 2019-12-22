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
from cms.db.tests.base import inputvalues,cleardb
from cms.db.tests.base import TABLES
for tb in TABLES:
    import_str = "from %(p)s import %(t)s" % dict(p='cms.db.orm',t=tb) 
    exec import_str


class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
        
    def setUp(self):

        inputvalues()       
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('cms.db.folder', 'folder')
        portal['folder'].invokeFactory('cms.db.ormfolder', 'ormfolder')
        portal['folder'].invokeFactory('cms.db.yaofolder', 'yaofolder')
        portal['folder'].invokeFactory('cms.db.chufangfolder', 'chufangfolder')
        portal['folder'].invokeFactory('cms.db.bingrenfolder', 'bingrenfolder')
        portal['folder'].invokeFactory('cms.db.yishengfolder', 'yishengfolder')
        portal['folder'].invokeFactory('cms.db.danweifolder', 'danweifolder')      
        self.portal = portal

    def tearDown(self):
        cleardb()

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
        self.assertEqual(json.loads(result)['total'],6)        

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
        self.assertEqual(json.loads(result)['total'],4) 

    def test_gerendizhi(self):
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
        view = box.restrictedTraverse('@@gerendizhi_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],1)
        
    def test_danweidizhi(self):
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
        view = box.restrictedTraverse('@@danweidizhi_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],2)        

    def test_danwei(self):
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
        view = box.restrictedTraverse('@@danwei_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],2)

    def test_yisheng(self):
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
        view = box.restrictedTraverse('@@yisheng_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],1)             

    def test_bingren(self):
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
        view = box.restrictedTraverse('@@bingren_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],1)             

    def test_nianganzhi(self):
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
        view = box.restrictedTraverse('@@nianganzhi_ajaxsearch')
        result = view()       
        self.assertEqual(json.loads(result)['total'],60)