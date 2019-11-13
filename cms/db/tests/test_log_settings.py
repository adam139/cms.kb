import unittest 
import transaction

from emc.kb.testing import INTEGRATION_TESTING
from emc.kb.testing import FUNCTIONAL_TESTING

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry
from emc.kb.interfaces import ILogSettings

class TestSetup(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    

    
    def test_setting_configured(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILogSettings)
        self.assertEqual(settings.timeout, 180)
        self.assertEqual(settings.max, 10000)
        self.assertEqual(settings.bsize, 2000)


class TestRenderingConfiglet(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    
    def test_render_plone_page(self):
        app = self.layer['app']
        portal = self.layer['portal']
        
        transaction.commit()
        
        browser = Browser(app)
        #open('/tmp/test.html','w').write(browser.contents)    
        browser.open(portal.absolute_url() + "/@@log-settings")
        self.assertTrue('<aside id="global_statusmessage">' in browser.contents)

