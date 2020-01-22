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

    def init_table():
        "import the table's mapper class named tablecls"
        
    def get_rownumber():
        "fetch table's rownumber"

    def bulk_delete():
        "bulk delete"
        
    def query(kwargs):
        """single table query 
        parameters:
        :kwargs's keys parameters:
            start:start location
            size:batch size
            keyword:full search keyword
            direction:sort direction
            max:batch size for Oracle
            with_entities:if using serial number fetch recorder's columns,1 True,0 False      
        """         
        
    def multi_query(kwargs,tmaper,tbl,tc,cv,key1,key2):
        """
        parameters:
        :kwargs's keys parameters:
            start:start location
            size:batch size
            keyword:full search keyword
            direction:sort direction
            max:batch size for Oracle
            with_entities:if using serial number fetch recorder's columns,1 True,0 False
        :tmaper: will joined table's mapper object
        :tbl: will joined table's name
        :tc:will be checked table column
        :cv:the tc should equal value
        :key1:first table primary key
        :key:second table fk's refer to first table         
        """

    def update_asso_table(kwargs,searchcnd):
        """
        parameters:
        :kwargs:will be update data :type dict
        :searchcnd:the search condition that located the recorder, type: dict
        """    

    def get_columns():
        "get all columns of single table"
        
    def join_columns(maper):
        "get two tables all columns when base table join the table that is provided by maper parameter"        
    
    def add(kwargs):
        "add single table recorder"
    
    def add_multi_tables(kwargs,fk_tables,asso_tables=[],asso_obj_tables=[]):
        """
        update all fk_tables,asso_tables and asso_obj_tables when add base table recorder
        fk_tables:[(pk,map_cls,attr),...]
        asso_tables:[([pk1,pk2,...],map_cls,attr),...]
        asso_obj_tables:{"asso_proxy_property1":[(pk,pk_cls,pk_attr,asso_cls,asso_attr,[property1,property2,...]),...],
                            "asso_proxy_property2":[(pk,pk_cls,pk_attr,asso_cls,asso_attr,[property1,property2,...]]
                            ,...}        
        """
    
    def update_multi_tables(kwargs,fk_tables=[],asso_tables=[],asso_obj_tables=[]):

        """
        update all fk_tables,asso_tables and asso_obj_tables when  update base table properties
        fk_tables:[(pk,map_cls,attr),...]
        asso_tables:[([pk1,pk2,...],map_cls,attr),...]
        asso_obj_tables:{"asso_proxy_property1":[(pk,pk_cls,pk_attr,asso_cls,asso_attr,[property1,property2,...]),...],
                            "asso_proxy_property2":[(pk,pk_cls,pk_attr,asso_cls,asso_attr,[property1,property2,...]]
                            ,...}
        """
        
    
    def fetch_oldest():
        "fetch the oldest recorder from db"
        
    def getByCode(id):
        "get the recorder by table's primary key id"
        
    def DeleteByCode(id):
        "delete the recorder"
        
    def deleteByKwargs(kwargs):
        "delete the first recorder where obey conditions that is provided by kwargs dictionary"
        
    def updateByCode(kwargs):
        "update the recorder by id that is provided by kwargs"
        
    def getByKwargs(**args):
        "get first recorder by multiple conditions that is provided by args dictionary"
        
    def getMultiByKwargs(**args):
         "get all recorders by multiple conditions that is provided by args dictionary"
        
        
        
