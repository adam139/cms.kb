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

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING

    def setUp(self):

#         yaowei1 = YaoWei("酸")
#         yaowei2 = YaoWei("苦")
#         yaowei3 = YaoWei("甘")
#         yaowei4 = YaoWei("辛")
#         yaowei5 = YaoWei("咸")
#         Session.add_all([yaowei1,yaowei2,yaowei3,yaowei4,yaowei5])
#         yaoxing1 = YaoXing("大热")
#         yaoxing2 = YaoXing("热")
#         yaoxing3 = YaoXing("温")
#         yaoxing4 = YaoXing("凉")
#         yaoxing5 = YaoXing("寒")
#         yaoxing6 = YaoXing("大寒")
#         Session.add_all([yaoxing1,yaoxing2,yaoxing3,yaoxing4,yaoxing5,yaoxing6])
#         jingluo1 = JingLuo("足太阳膀胱经")
#         jingluo2 = JingLuo("足阳明胃经")
#         jingluo3 = JingLuo("足少阳胆经")
#         jingluo4 = JingLuo("足厥阴肝经")
#         jingluo5 = JingLuo("足少阴肾经")
#         jingluo6 = JingLuo("足太阴脾经")
#         Session.add_all([jingluo1,jingluo2,jingluo3,jingluo4,jingluo5,jingluo6])
#         yao1 = Yao("白芍")
#         yao1.yaowei = yaowei1
#         yao1.yaoxing = yaoxing1
#         yao1.guijing = [jingluo1]         
#         yao2 = Yao("大枣")
#         yao2.yaowei = yaowei2
#         yao2.yaoxing = yaoxing2
#         yao2.guijing = [jingluo2]
#         Session.add_all([yao1,yao2])
#         dizhi = DiZhi("中国","湖南","湘潭市","湘潭县云湖桥镇北岸村道林组83号")
#         bingren = BingRen('张三',1, date(2015, 4, 2),'13673265899')
#         bingren.dizhi = dizhi
#         dizhi2 = DiZhi("中国","湖北","十堰市","茅箭区施洋路83号")
#         danwei = DanWei("任之堂")
#         yisheng = YiSheng('余浩',1, date(2015, 4, 2),'13673265859')
#         danwei.yishengs = [yisheng]
#         danwei.dizhi = dizhi2        
#         chufang = ChuFang("桂枝汤","加热稀粥",5)
#         yao_chufang = Yao_ChuFang_Asso(yao1,chufang,7,"晒干")
#         yao_chufang2 = Yao_ChuFang_Asso(yao2,chufang,10,"掰开")
#         chufang_bingren = ChuFang_BingRen_Asso(bingren,chufang,datetime.now())
#         yisheng.chufangs = [chufang]
#         Session.add_all([dizhi,bingren,danwei,dizhi2,yisheng,chufang,yao_chufang,yao_chufang2,chufang_bingren])                                
#         Session.commit()        
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


             

