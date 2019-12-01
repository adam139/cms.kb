import unittest 
import transaction

from cms.db.testing import INTEGRATION_TESTING
from cms.db.testing import FUNCTIONAL_TESTING

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID,TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles

from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry
from cms.db.browser.interfaces import IAutomaticTypesSettings

class TestSetup(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    

    
    def test_setting_configured(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IAutomaticTypesSettings)
        self.assertEqual(settings.types, [])



class TestRenderingConfiglet(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING

    def setUp(self):
    
        portal = self.layer['portal']
        app = self.layer['app']
        setRoles(portal, TEST_USER_ID, ('Manager',))      
        self.portal = portal
        self.app = app    
    
    def test_render_plone_page(self):
        
        browser = Browser(self.app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        transaction.commit()
        
        browser.open(self.portal.absolute_url() + "/@@types-settings")
        self.assertTrue('<option value="cms.db.yao">yao</option>' in browser.contents)

