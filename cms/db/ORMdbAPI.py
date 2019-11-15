#-*- coding: UTF-8 -*-
from five import grok
from datetime import datetime
from zope import schema
from zope.interface import implements
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func
from cms.db import Session as session
from cms.db.interfaces import IDbapi
import datetime
from cms.policy import fmt
from cms.db import linkstr
from cms.db import _

class Dbapi(object):
    """Sqlalchemy ORM format db API base class"""
    implements(IDbapi)
    
    def __init__(self,session,package,table,factorycls,columns=None,fullsearch_clmns=None):
        """
        parameters:
        :session db mapper session,
        :package the package where table class in here. for example:'cms.db.orm',
        :table the table name that will be query, 'admin_logs',
        :factorycls the class name that will be create table object instance,'AdminLog',
        :columns will return table columns,
        :fullsearch_clmns the columns that will been used keyword full text search
        """
        
        self.session = session
        self.package = package
        self.table = table
        self.factorycls = factorycls
        self.columns = columns
        self.fullsearch_clmns = fullsearch_clmns
        
        import os
        os.environ['NLS_LANG'] = '.AL32UTF8'        


    def search_clmns2sqltxt(self,clmns):
        """get columns that will been used keyword full text search
        :input:clmns = ['tit','des']
        :output:" tit LIKE :x OR des LIKE :x "
                                  
        """
        if self.fullsearch_clmns == None:
            return ""                       
        else:
            srt=''
            for i in clmns:
                if not bool(srt):
                    srt = "%(c)s LIKE :x" % dict(c=i)
                    continue
                else:
                    srt = "%(pre)s OR %(c)s LIKE :x" % dict(c=i,pre=srt)
            return srt        
        
    def pk_title(self,pk,factorycls,title):
        "primary key to row recorder 's title"
        #根据主键提取指定表对象的属性
       
        recorder = session.query(factorycls).filter(factorycls.id==pk).one()
        return getattr(recorder,title,"")

    def pk_ass_title(self,pk,factorycls,asso,targetcls,fk,title):
        "通过主键查关联表,获取多对多的对象属性 "
        #pk本地表主键  integer
        #factorycls 本地表类 
        #asso 关联表类
        #targetcls 目标表类 
        #fk关联表指向目标表外键名称 string
        #title目标表字段/属性    string       
    
        recorders = session.query(asso).join(factorycls).filter(factorycls.id==pk).all()
#       recorders:  [(37L, 109L)]
        def mapf(recorder):
            fkv = set(list(recorder))
            fkv.remove(pk)
            target = session.query(targetcls).filter(targetcls.id ==list(fkv)[0]).one()
            return getattr(target,title,"")
        more = map(mapf,recorders)
        out = ",".join(more)
        return out
            
    def pk_ass_obj_title(self,pk,factorycls,asso,targetcls,fk,title):
        "通过主键查关联表对象,获取多对多关联对象的属性 "
        #pk本地表主键  integer
        #factorycls 本地表类 
        #asso 关联表类
        #targetcls 目标表类 
        #fk关联表指向目标表外键名称 string
        #title目标表字段/属性    string       
    
        recorders = session.query(asso).join(factorycls).filter(factorycls.id==pk).all()
#       recorders:  [(37L, 109L)]
        def mapf(recorder):

            yao_id = recorder.yao_id
            yao = session.query(targetcls).filter(targetcls.id ==yao_id).one()
            mingcheng = getattr(yao,title,"")
            yaoliang = u"%s克" % recorder.yaoliang
            paozhi = recorder.paozhi
            if bool(paozhi):
                paozhi = "(%s)" % recorder.paozhi
                return ",".join([mingcheng,yaoliang,paozhi])
            else:                
                return ",".join([mingcheng,yaoliang])

        more = map(mapf,recorders)
        out = ";".join(more)
        return out

    def get_columns(self):
        "get return columns by query"
        
        if self.columns == None:
            import_str = "from %(p)s import %(t)s as tablecls" % \
            dict(p=self.package,t=self.factorycls) 
            exec import_str
            from sqlalchemy.inspection import inspect
            table = inspect(tablecls)
            columns = [column.name for column in table.c]
            return columns                        
        else:
            return self.columns            
            
    def add(self,kwargs):
        
        import_str = "from %(p)s import %(t)s as tablecls" % dict(p=self.package,t=self.factorycls) 
        exec import_str
        recorder = tablecls()
        for kw in kwargs.keys():
            setattr(recorder,kw,kwargs[kw])
        session.add(recorder)
        try:
            session.commit()
        except:
            session.rollback()
            

    def query(self,kwargs):
        """分页查询
        columns = request.args.getlist('columns')
        stmt = select([column(c) for c in columns]).\
    select_from(some_table)
    stmt = select([table.c[c] for c in columns])
    results = db.session.execute(stmt).fetchall()
    session.query.with_entities(SomeModel.col1)
        """
        
        import_str = "from %(p)s import %(t)s as tablecls" % dict(p=self.package,t=self.factorycls) 
        exec import_str        
        start = int(kwargs['start']) 
        size = int(kwargs['size'])
        max = size + start + 1
        keyword = kwargs['SearchableText']        
        direction = kwargs['sort_order'].strip()        

        if size != 0:
            if keyword == "":
                if direction == "reverse":
                    if linkstr.startswith("oracle"):
                        sqltext = """SELECT * FROM 
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %s ORDER BY id DESC) a  
                    WHERE rownum < :max) WHERE rn > :start""" % self.table
                    else:                            
                        max = max - 1                        
                        sqltext = """SELECT * FROM %s 
                         ORDER BY id DESC limit :start,:max""" % self.table                    
                    selectcon = text(sqltext)
                else:
                    if linkstr.startswith("oracle"):
                        sqltext = """SELECT * FROM 
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %s ORDER BY id ASC) a  
                    WHERE rownum < :max) WHERE rn > :start""" % self.table
                    else:                  
                        max = max - 1                        
                        sqltext = """SELECT * FROM %s 
                         ORDER BY id ASC limit :start,:max""" % self.table                                        
                    selectcon = text(sqltext)                    
                clmns = self.get_columns()
                recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon.params(start=start,max=max)).all()
            else:
                keysrchtxt = self.search_clmns2sqltxt(self.fullsearch_clmns)
                if direction == "reverse":
                    if linkstr.startswith("oracle"):                                                                
                        sqltxt = """SELECT * FROM
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %(tbl)s WHERE %(ktxt)s  ORDER BY id DESC ) a 
                     WHERE rownum < :max) WHERE rn > :start
                    """ % dict(tbl=self.table,ktxt=keysrchtxt)
                    else:
                        max = max - 1
                        sqltext = """SELECT * FROM %(tbl)s
                        WHERE %(ktxt)s 
                        ORDER BY id DESC limit :start,:max
                         """ % dict(tbl=self.table,ktxt=keysrchtxt)                        
                    selectcon = text(sqltxt)
                else:
                    if linkstr.startswith("oracle"):                     
                        sqltxt = """SELECT * FROM
                    (SELECT a.*,rownum rn FROM 
                    (SELECT * FROM %(tbl)s WHERE %(ktxt)s  ORDER BY id ASC ) a 
                     WHERE rownum < :max) WHERE rn > :start
                    """ % dict(tbl=self.table,ktxt=keysrchtxt)
                    else:
                        max = max - 1
                        sqltext = """SELECT * FROM %(tbl)s
                        WHERE %(ktxt)s 
                        ORDER BY id ASC limit :start,:max
                         """ % dict(tbl=self.table,ktxt=keysrchtxt)                                                                 
                    selectcon = text(sqltxt)
                clmns = self.get_columns()
                recorders = session.query(tablecls).with_entities(*clmns).\
                                      from_statement(selectcon.params(x=keyword,start=start,max=max)).all()               
        else:
            if keyword == "":
                selectcon = text("SELECT * FROM %s ORDER BY id DESC " % self.table)
                clmns = self.get_columns()
                recorders = session.query(tablecls).with_entities(*clmns).\
                            from_statement(selectcon).all()
            else:
                keysrchtxt = self.search_clmns2sqltxt(self.fullsearch_clmns)
                sqltext = """SELECT * FROM %(tbl)s WHERE %(ktxt)s  
                 ORDER BY id DESC """ % dict(tbl=self.table,ktxt=keysrchtxt)
                selectcon = text(sqltext)
                clmns = self.get_columns()
                recorders = session.query(tablecls).with_entities(*clmns).\
                                      from_statement(selectcon.params(x=keyword)).all()                         
            nums = len(recorders)
            return nums
        try:
            return recorders
        except:
            return []    
    
    def init_table(self):
        "import table class"
        import_str = "from %(p)s import %(t)s as tablecls" % dict(p=self.package,t=self.factorycls) 
        exec import_str
        return tablecls           
    
    def DeleteByCode(self,id):
        "delete the specify id recorder"

        tablecls = self.init_table()
        if id != "":
            text = "SELECT * FROM %(tbl)s WHERE id=:id" % dict(tbl=self.table) 
            try:
                recorder = session.query(tablecls).\
                from_statement(text(sqltext)).\
                params(id=id).one()
                session.delete(recorder)
                session.commit()
                return True
            except:
                session.rollback()
                return False
        else:
            return None

    def updateByCode(self,kwargs):
        "update the speicy table recorder"
        """
        session.query(User).from_statement(text("SELECT * FROM users WHERE name=:name")).\
params(name='ed').all()
session.query(User).from_statement(
text("SELECT * FROM users WHERE name=:name")).params(name='ed').all()
        """

        id = kwargs['id']
        if id != "":
            tablecls = self.init_table()
            sqltext = "SELECT * FROM %s WHERE id=:id" % self.table
            try:
                recorder = session.query(tablecls).\
                from_statement(text(sqltext)).\
                params(id=id).one()
                updatedattrs = [kw for kw in kwargs.keys() if kw != 'id']
                for kw in updatedattrs:
                    setattr(recorder,kw,kwargs[kw])
                session.commit()
            except:
                session.rollback()
                pass
        else:
            return None

    def getByCode(self,id):
        import_str = "from %(p)s import %(t)s as tablecls" % dict(p=self.package,t=self.factorycls) 
        exec import_str        
        if id != "":
            sqltext = "SELECT * FROM %(tbl)s WHERE id=:id" % dict(tbl=self.table)            
            try:
                recorder = session.query(tablecls).\
                from_statement(text(sqltext)).\
                params(id=id).one()
                return recorder
            except:

                return None
        else:
            return None
    
    def get_rownumber(self):
        "fetch table's rownumber"
#         query = "SELECT COUNT(*) FROM %(table)s;" % dict(table=self.table)
        import_str = "from %(p)s import %(t)s as tablecls" % dict(p=self.package,t=self.factorycls) 
        exec import_str
        try:
            num = self.session.query(func.count(tablecls.id)).scalar()         
            return num
        except:
            return 0            

    def fetch_oldest(self):
        "delete from(select * from <table_name>) where rownum<=1000;"
        
        s = self.session
        sql2 = """ 
        SELECT datetime FROM (
          SELECT * FROM %(tbl)s ORDER BY id ASC
         )
          WHERE rownum<= 1
        """ % dict(tbl=self.table)
        query2 = text(sql2)                                                                                                
        try:
            rownum = s.execute(query2).fetchone()
            if len(rownum):
                return datetime.strptime(rownum[0],fmt) 
            else:
                return datetime.datetime.now()
#             s.commit()
        except:
            return datetime.datetime.now()
    
    def bulk_delete(self,size):
        "delete from(select * from <table_name>) where rownum<=1000;"
        
        s = self.session
        sql2 = """
        DELETE %(tbl)s
         WHERE  id in (
        SELECT id FROM (
          SELECT * FROM %(tbl)s ORDER BY id ASC
         )
          WHERE rownum<= :max
        )
        """ % dict(tbl=self.table)
        query2 = text(sql2).params(max=size)                                                                                                 
        try:
            rownum = s.execute(query2)
            s.commit()
        except:
            s.rollback()

# yaoxing table       
yaoxing = Dbapi(session,'cms.db.orm','yaoxing','YaoXing')
# yaowei table       
yaowei = Dbapi(session,'cms.db.orm','yaowei','YaoWei')
# jingluo table       
jingluo = Dbapi(session,'cms.db.orm','jingluo','JingLuo')
dizhi = Dbapi(session,'cms.db.orm','dizhi','DiZhi')
yao =  Dbapi(session,'cms.db.orm','yao','Yao')
chufang = Dbapi(session,'cms.db.orm','chufang','ChuFang')
bingren = Dbapi(session,'cms.db.orm','bingren','BingRen')
danwei =  Dbapi(session,'cms.db.orm','danwei','DanWei')
yisheng =  Dbapi(session,'cms.db.orm','yisheng','YiSheng')
# clmns = ['userid','datetime','ip','type','operlevel','description','result']
# search_clmns = ['userid','datetime','ip','operlevel','description']
# yao =  Dbapi(session,'cms.db.orm','yao','Yao',columns=clmns,fullsearch_clmns=search_clmns)

