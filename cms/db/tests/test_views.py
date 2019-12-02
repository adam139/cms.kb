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

from cms.db.contents.folder import Ifolder
from cms.db.contents.ormfolder import Iormfolder
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
#         inputvalues()
   
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('cms.db.folder', 'folder')
        portal['folder'].invokeFactory('cms.db.ormfolder', 'ormfolder')
        portal['folder'].invokeFactory('cms.db.yaofolder', 'yaofolder')
        portal['folder']['yaofolder'].invokeFactory('cms.db.yao', 'yao',
                                                             text=u"here is rich text",
                                                             title="analysis document",
                                                             report="this is report")         
        self.portal = portal

    def tearDown(self):
        pass
#         cleardb()                 
        

   
    def testormfolderView(self):
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
        browser.open(portal['folder']['yaofolder']['yao'].absolute_url() + "/@@base_view")        
        self.assertTrue("here is rich text" in browser.contents)        
  
        
                                 