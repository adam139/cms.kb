#-*- coding: UTF-8 -*-
import sys
from datetime import datetime
from zope import schema
from cms.db.events import RecorderCreated
from cms.db.events import RecorderDeleted
from zope import event
from zope.interface import implements
from sqlalchemy.dbapi.ORMdbAPI  import Dbapi  as baseapi
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy import or_
from cms.db import Session as session
from sqlalchemy.dbapi.interfaces import IDbapi
import datetime
from cms.policy import fmt
from cms.db import linkstr
from cms.db import _

class Dbapi(baseapi):
    """Sqlalchemy ORM format db API base class"""
    implements(IDbapi)


    def add(self,kwargs):
        
        tablecls = self.init_table()
        recorder = tablecls()
        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        session.add(recorder)
        try:
            session.commit()
            self.fire_event(RecorderCreated,recorder)
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def add_multi_tables(self,kwargs,fk_tables,asso_tables=[],asso_obj_tables=[]):
        "添加表记录的同时,并关联其他表记录"
        # 外键关联表 fk_tables: [(pk,map_cls,attr),...]
        # 多对多关联表 asso_tables:[([pk1,pk2,...],map_cls,attr),...]
        # 多对多关联表(asso table has itself properties) 
        # asso_obj_tables:[(pk,targetcls,attr,[property1,property2,...]),...]
        tablecls = self.init_table() 
        recorder = tablecls()

        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        for i in fk_tables:
            mapcls = i[1]
            linkobj = session.query(mapcls).filter(mapcls.id ==i[0]).one()
            setattr(recorder,i[2],linkobj)
        for i in asso_tables:
            mapcls = i[1]
            #主键到map对象(表记录) 的map function 
            objs = []
            for j in i[0]:
                objs.append(session.query(mapcls).filter(mapcls.id ==j).one())                
            if bool(objs):setattr(recorder,i[2],objs)
        session.add(recorder)
        
        for i in asso_obj_tables:
            mapcls = i[1]
            #主键到map对象(表记录) 的map function
            obj1 = session.query(mapcls).filter(mapcls.id ==i[0]).one()
            obj2 = recorder
            setvalues = i[5]
            #add source obj
            setvalues[i[2]] = obj1
            # add target obj
            setvalues[i[4]]= obj2
            # instance association obj
            link_obj = i[3]()
            for kw in setvalues.keys():
                setattr(link_obj,kw,setvalues[kw])
            #submit to db
            session.add(link_obj)                   
        try:
            session.commit()
            self.fire_event(RecorderCreated,recorder)
        except:
            session.rollback()
            raise
        finally:
            session.close()                        

    def fire_event(self,eventcls,recorder):
            if getattr(recorder,'id','') == '':return
            cls = "cms.db.%s" % self.table
            ttl = getattr(recorder,'mingcheng',u'') or getattr(recorder,'xingming',u'') or \
             getattr(recorder,'xing',u'') or getattr(recorder,'wei',u'')
            eventobj = eventcls(id=recorder.id,cls=cls,ttl=ttl) 
            if eventobj.available():event.notify(eventobj)               

    def DeleteByCode(self,id):
       "delete the specify id recorder"

       if id != "":
           try:
               recorder = self.getByCode(id)                
               session.delete(recorder)
               session.commit()
               self.fire_event(RecorderDeleted,recorder)
               rt = True
           except:
               session.rollback()
               rt = sys.exc_info()[1]
           finally:
               session.close()
               return rt
       else:
           return "id can't be empty"


