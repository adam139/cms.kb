# -*- coding: utf-8 -*-
from plone import api
from zope.component import getUtility
from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from AccessControl.User import nobody
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser 
# define content type child to parent mapping
CONTAINER2TYPES = {'cms.db.yao':"cms.db.yaofolder",
                   'cms.db.yaowei':"cms.db.yaofolder",
                   'cms.db.yaoxing':"cms.db.yaofolder",
                   'cms.db.jingluo':"cms.db.yaofolder",
                   'cms.db.chufang':"cms.db.chufangfolder",
                   'cms.db.bingren':"cms.db.bingrenfolder",
                   'cms.db.yisheng':"cms.db.yishengfolder",
                   'cms.db.danwei':"cms.db.danweifolder",
                   'cms.db.wuyun':"cms.db.wuyunfolder",                                       
                   }

def getDanWeiId():
    "get danwei id from plone.app.registry setting"
    from plone.registry.interfaces import IRegistry
    from cms.db.browser.interfaces import IAutomaticTypesSettings
    registry = getUtility(IRegistry)        
    settings = registry.forInterface(IAutomaticTypesSettings, check=False)
    return settings.danweiid    


class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return self.getUserName()


def gonglinian2ganzhi(nian):
    "公历年份转干支"
    yu = int(nian) % 60
    if yu >4:
        id = yu - 4 + 1
    else:
        id = yu + 60 - 4 + 1
    return id

def execute_under_special_role(portal, role, function, *args, **kwargs):
    """ Execute code under special role privileges.

    Example how to call::

        execute_under_special_role(portal, "Manager",
            doSomeNormallyNotAllowedStuff,
            source_folder, target_folder)

    @param portal: Reference to ISiteRoot object whose access controls we are using

    @param function: Method to be called with special privileges

    @param role: User role for the security context when calling the privileged code; e.g. "Manager".

    @param args: Passed to the function

    @param kwargs: Passed to the function
    """

    sm = getSecurityManager()
    try:
        try:
            # Clone the current user and assign a new role.
            # Note that the username (getId()) is left in exception
            # tracebacks in the error_log,
            # so it is an important thing to store.
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(), '', [role], ''
                )

            # Wrap the user in the acquisition context of the portal
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)

            # Call the function
            return function(*args, **kwargs)

        except:
            # If special exception handlers are needed, run them here
            raise
    finally:
        # Restore the old security manager
        setSecurityManager(sm)

def chown(context,userid):
        # Grant Ownership and Owner role to Member
    user = api.user.get(userid)
    context.changeOwnership(user)
    context.__ac_local_roles__ = None
    context.manage_setLocalRoles(userid, ['Owner'])
    context.reindexObject()
    
def get_container_by_type(type):
    "get first parent container by object's content type"
    if type in CONTAINER2TYPES.keys():
        type = CONTAINER2TYPES[type]
        catalog = api.portal.get_tool('portal_catalog')
        brain = catalog(portal_type=type)
        return brain[0]        
    else:
        return None

    
    
def to_utf_8(lts):
    rt = []
    for i in lts:
        if isinstance(i,str):            
            rt.append(i.decode('utf-8'))
            continue
        else:
            rt.append(i)
    return rt
            
        

def map_field2cls(fieldname):
    "为编辑表单的getcontent()提供字段名到中间对象class name映射"
    dt = {'yaoes':"Yao_ChuFang_AssoUI",'bingrens':"ChuFang_BingRen_AssoUI"}
    return dt[fieldname]

def filter_cln(cls):
    "过滤指定表类的列,只保留基本属性列"            

    from sqlalchemy.inspection import inspect
    table = inspect(cls)
    columns = [column.name for column in table.c]
    #过滤主键,外键
    columns = filter(lambda elem: not elem.endswith("id"),columns)
    return columns 