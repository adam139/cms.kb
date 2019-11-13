import os
import tempfile

import sqlalchemy

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig

from zope.component import provideUtility


class Base(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import cms.db

        xmlconfig.file('configure.zcml', cms.db, context=configurationContext)      

    
    def tearDownZope(self, app):
        pass
        # Clean up the database
#        os.unlink(self.dbFileName)
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cms.db:default')


FIXTURE = Base()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="Base:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name="Base:Functional")
