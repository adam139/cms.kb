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
        portal['folder']['yaofolder'].invokeFactory('cms.db.yao', 'yao')          

        self.portal = portal
    
    def test_item_types(self):

      
        self.assertEqual(self.portal['folder'].id,'folder')
             
        self.assertEqual(self.portal['folder']['ormfolder'].id,'ormfolder')
        self.assertEqual(self.portal['folder']['yaofolder'].id,'yaofolder')
        self.assertEqual(self.portal['folder']['yaofolder']['yao'].id,'yao') 

                                     
                  
       
        