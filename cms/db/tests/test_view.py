#-*- coding: UTF-8 -*-
import unittest
import transaction
from plone.testing.z2 import Browser
from zope import event

from cms.db.testing import FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID,TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles,login,logout

from cms.db.contents.folder import Ifolder
from cms.db.contents.ormfolder import Iormfolder

from cms.db import  Session
from cms.db.orm import YaoWei,YaoXing,JingLuo


class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):

        yaowei1 = YaoWei("酸")
        yaowei2 = YaoWei("苦")
        yaowei3 = YaoWei("甘")
        yaowei4 = YaoWei("辛")
        yaowei5 = YaoWei("咸")
        Session.add_all([yaowei1,yaowei2,yaowei3,yaowei4,yaowei5])
        yaoxing1 = YaoXing("大热")
        yaoxing2 = YaoXing("热")
        yaoxing3 = YaoXing("温")
        yaoxing4 = YaoXing("凉")
        yaoxing5 = YaoXing("寒")
        yaoxing6 = YaoXing("大寒")
        Session.add_all([yaoxing1,yaoxing2,yaoxing3,yaoxing4,yaoxing5,yaoxing6])
        
        Session.commit()        
        portal = self.layer['portal']

        setRoles(portal, TEST_USER_ID, ('Manager',))


        portal.invokeFactory('cms.db.folder', 'folder')
        portal['folder'].invokeFactory('cms.db.ormfolder', 'ormfolder')       
        self.portal = portal

    def tearDown(self):
        
        items = Session.query(YaoWei).all()
        items.extend(Session.query(YaoXing).all())        
        for item in items:
            Session.delete(item)            
        Session.commit()
                
        
    def testfolderView(self):

        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        transaction.commit()

        browser.open(portal['folder'].absolute_url())
        
        self.assertTrue('class="pat-structure"' in browser.contents)

   
    def testormfolderView(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
#         browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))

        transaction.commit()
        browser.open(portal['folder']['ormfolder'].absolute_url())
        
        self.assertTrue('class="pat-structure"' in browser.contents)
    
    def testYaoXingView(self):
        # add data to yaoxing table

        suan = Session.query(YaoXing).filter(YaoXing.xing=="温").all()
        self.assertEqual(len(suan),1)
        
        
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
#         browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))

        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()

        browser.open(base + "/@@yaoxing_listings")
        
        self.assertTrue(u"温" in browser.contents)
        
    def testYaoWeiView(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        browser.open(base + "/@@yaowei_listings")
        import pdb
        pdb.set_trace()
        self.assertTrue(u"甘" in browser.contents)
        suan = Session.query(YaoWei).filter(YaoWei.wei=="甘").all()
        self.assertEqual(len(suan),1)

    def testInputYaoXingForm(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()

        # Open form
        browser.open("%s/@@input_yaoxing" % base)
        
        # Fill in the form 

#         browser.getControl(name=u"form.widgets.id").value = 1
        browser.getControl(name=u"form.widgets.xing").value = u"微寒"
        
        # Submit
        browser.getControl(u"Submit").click()
        suan = Session.query(YaoXing).filter(YaoXing.xing==u"微寒").all()
        self.assertEqual(len(suan),1)
#         self.assertTrue(u"Invalid email address" in browser.contents)        
#         self.assertTrue("row table table-striped table-bordered table-condensed listing" in browser.contents)
        

    def testJieshoujView(self):
        app = self.layer['app']
        portal = self.layer['portal']

        browser = Browser(app)
        browser.handleErrors = False             
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
#         browser.addHeader('Authorization', 'Basic %s:%s' % ('user3', 'secret',))
        import transaction
        transaction.commit()
        base = portal['folder']['ormfolder'].absolute_url()
        browser.open(base + "/jieshouj_listings")
        
        self.assertTrue("row table table-striped table-bordered table-condensed listing" in browser.contents)
        

