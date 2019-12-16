#-*- coding: UTF-8 -*-
from plone import api
from zope import interface
from zope.component import getUtility
from cms.db.interfaces import IRecorderCreated

# we use this constant just for command line test
TYPES_LIST = ['cms.db.yao',
              'cms.db.danwei',
              'cms.db.yisheng',
              'cms.db.chufang']

class EventFilter(object):
    """
    if current user has 'manager' role,cancel log event
    """
    def __init__(self,id,cls,ttl=u""):
        self.id = id
        self.cls = cls
        self.ttl = ttl

    
    def available(self):
        "search automatic create content types list through registry settings"
        "if current cls is in the list,return True"

        from plone.registry.interfaces import IRegistry
        from cms.db.browser.interfaces import IAutomaticTypesSettings
        registry = getUtility(IRegistry)        
        settings = registry.forInterface(IAutomaticTypesSettings, check=False)
        types_list = settings.types
        # to do :registry.xml now can't import default value for IAutomaticTypesSettings
        # bypass check
        if not bool(types_list):
            if self.cls in TYPES_LIST:
                return True
            else:
                return False
        #work instance the following will work.
        return self.cls in TYPES_LIST

        
    def is_normal_user(self):

        try:
            roles = api.user.get_roles()
# SecAuditor audited by SecStaff
            roles2 = filter(lambda x: x not in ['SysAdmin','SecStaff'],roles)
            return roles == roles2
        except:
            return False        


class RecorderCreated(EventFilter):
    interface.implements(IRecorderCreated)
    
    
    