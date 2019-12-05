#-*- coding: UTF-8 -*-
import unittest
import transaction
from datetime import date
from datetime import datetime
from plone.testing.z2 import Browser
from zope import event

from cms.db.testing import FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID,TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles,login,logout
from plone.app.textfield.value import RichTextValue
from cms.db.contents.folder import IFolder
from cms.db.contents.ormfolder import IOrmfolder
from cms.db.contents.yaofolder import IYaofolder
from cms.db.contents.yao import IYao

from sqlalchemy import and_

from cms.db import  Session
from cms.db.orm import YaoWei,YaoXing,JingLuo,Yao
from cms.db.orm import ChuFang,BingRen,DiZhi,DanWei,YiSheng
from cms.db.orm import Yao_ChuFang_Asso,ChuFang_BingRen_Asso
from cms.db.tests.base import inputvalues,cleardb

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
        yao_id = str(Session.query(Yao).filter(Yao.mingcheng=="白芍").one().id)
        bingren_id = str(Session.query(BingRen).filter(BingRen.xingming=="张三").one().id)
        portal['folder']['yaofolder'].invokeFactory('cms.db.yao', yao_id,
                                                    title=u"here is title",
                                                    description=u"here is description",
                                                    text=RichTextValue(
                                                                       u"here is rich text",
                                                                       'text/plain',
                                                                       'text/html'
                                                                       ),
                                                    report=RichTextValue(
                                                                       u"here is report",
                                                                       'text/plain',
                                                                       'text/html'
                                                                       )
                                                    )                                                    
        portal['folder']['bingrenfolder'].invokeFactory('cms.db.bingren', bingren_id,
                                                    title=u"here is title",
                                                    description=u"here is description",
                                                    text=RichTextValue(
                                                                       u"here is rich text",
                                                                       'text/plain',
                                                                       'text/html'
                                                                       ),
                                                    report=RichTextValue(
                                                                       u"here is report",
                                                                       'text/plain',
                                                                       'text/html'
                                                                       )
                                                    )                                                    

                                                                     
        self.portal = portal
        self.yao_id = yao_id
        self.bingren_id = bingren_id

    def tearDown(self):
        pass
        cleardb()                 
        

   
    def ormfolderView(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        browser.open(portal['folder']['ormfolder'].absolute_url())        
        self.assertTrue('class="pat-structure"' in browser.contents)
    

    def testyaoView(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        browser.open(portal['folder']['yaofolder'][self.yao_id].absolute_url() + "/@@base_view")
        self.assertTrue("here is title" in browser.contents)
        self.assertTrue(u"here is description" in browser.contents)        
        self.assertTrue("here is rich text" in browser.contents)        
        self.assertTrue("here is report" in browser.contents)
        self.assertTrue( "酸" in browser.contents)
        self.assertTrue( "足太阳膀胱经" in browser.contents)
        self.assertTrue( "桂枝汤" in browser.contents)        
  
    def testbingrenView(self):
        app = self.layer['app']
        portal = self.layer['portal']
        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        browser.open(portal['folder']['bingrenfolder'][self.bingren_id].absolute_url() + "/@@base_view")
        self.assertTrue("here is title" in browser.contents)
        self.assertTrue(u"here is description" in browser.contents)        
        self.assertTrue("here is rich text" in browser.contents)        
        self.assertTrue("here is report" in browser.contents)
        self.assertTrue( "桂枝汤" in browser.contents)
       
                                 