#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope.interface import Attribute
from zope.component.interfaces import IObjectEvent
from zope import schema
from cms.db import _

class IRecorderCreated(Interface):
    """当关系数据库创建记录是,触发该事件,通知Plone创建关联的富文本对象"""
    id = Attribute("Recorder id")
    cls = Attribute("the Recorder relative content type class")
    ttl = Attribute("the Recorder relative content object title") 


class IRecorderDeleted(IRecorderCreated):
    """当关系数据库删除某记录时,触发该事件,通知Plone删除关联对象"""
 

class IDanWeiRecorderCreated(IRecorderCreated):
    """当关系数据库创建一条单位记录时,触发该事件,通知Plone创建包含富文本对象的单位"""

class IYiShengRecorderCreated(IRecorderCreated):
    """当关系数据库创建一条医生记录时,触发该事件,通知Plone创建包含富文本对象的医生"""

class IBingrenRecorderCreated(IRecorderCreated):
    """当关系数据库创建一条bingren记录时,触发该事件,通知Plone创建包含富文本对象的bingren"""
    
class IAutomaticTypesSettings(Interface):
    """automatic create content types setting"""
    

class ISysSettings(Interface):
    """ system settings
    """         

class InputError(Exception):
    """Exception raised if there is an error making a data input
    """

# db insterface
class IDbapi (Interface):
    """Db api """

    def get_rownumber():
        "fetch table's rownumber"

    def bulk_delete():
        "bulk delete"

    def fetch_oldest():
        "fetch the oldest recorder from db"
        
        
