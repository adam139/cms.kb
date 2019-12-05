import unittest as unittest

from cms.db.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
#from plone.namedfile.file import NamedImage

class Allcontents(unittest.TestCase):
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('cms.db.folder', 'folder')

        portal['folder'].invokeFactory('cms.db.ormfolder', 'ormfolder')
        portal['folder'].invokeFactory('cms.db.yaofolder', 'yaofolder')
        portal['folder'].invokeFactory('cms.db.chufangfolder', 'chufangfolder')
        portal['folder'].invokeFactory('cms.db.bingrenfolder', 'bingrenfolder')
        portal['folder'].invokeFactory('cms.db.yishengfolder', 'yishengfolder')
        portal['folder'].invokeFactory('cms.db.danweifolder', 'danweifolder')        
        portal['folder']['yaofolder'].invokeFactory('cms.db.yao', 'yao')
        portal['folder']['chufangfolder'].invokeFactory('cms.db.chufang', 'chufang')
        portal['folder']['bingrenfolder'].invokeFactory('cms.db.bingren', 'bingren')
        portal['folder']['yishengfolder'].invokeFactory('cms.db.yisheng', 'yisheng')
        portal['folder']['danweifolder'].invokeFactory('cms.db.danwei', 'danwei')                           

        self.portal = portal
    
    def test_item_types(self):

      
        self.assertEqual(self.portal['folder'].id,'folder')
             
        self.assertEqual(self.portal['folder']['ormfolder'].id,'ormfolder')
        self.assertEqual(self.portal['folder']['yaofolder'].id,'yaofolder')
        self.assertEqual(self.portal['folder']['chufangfolder'].id,'chufangfolder')
        self.assertEqual(self.portal['folder']['bingrenfolder'].id,'bingrenfolder')
        self.assertEqual(self.portal['folder']['yishengfolder'].id,'yishengfolder')
        self.assertEqual(self.portal['folder']['danweifolder'].id,'danweifolder')        
        self.assertEqual(self.portal['folder']['yaofolder']['yao'].id,'yao')
        self.assertEqual(self.portal['folder']['chufangfolder']['chufang'].id,'chufang')
        self.assertEqual(self.portal['folder']['bingrenfolder']['bingren'].id,'bingren')
        self.assertEqual(self.portal['folder']['yishengfolder']['yisheng'].id,'yisheng')         
        self.assertEqual(self.portal['folder']['danweifolder']['danwei'].id,'danwei')
                                     
                  
       
        