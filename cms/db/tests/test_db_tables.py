#-*- coding: UTF-8 -*-
from datetime import date
from datetime import datetime
import unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from cms.db.testing import INTEGRATION_TESTING
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

from cms.db.interfaces import IDbapi
from zope.component import queryUtility
from cms.db import  Session
from cms.db import  engine
from cms.db import ORMBase as Base
from cms.db.tests.base import TABLES

for tb in TABLES:
    import_str = "from %(p)s import %(t)s" % dict(p='cms.db.orm',t=tb) 
    exec import_str

class TestDatabase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def drop_tables(self,tbls=None):
        """drop all db tables
        """

        for tb in tbls:
            import_str = "from %(p)s import %(t)s" % dict(p='cms.db.orm',t=tb) 
            exec import_str
        Base.metadata.drop_all(engine)                                

    def empty_tables(self,tbls=None):
        """clear all db tables
        """

#         tbls = ['Yao_ChuFang_Asso','ChuFang','Yao_JingLuo_Asso','Yao','YaoWei','YaoXing','JingLuo']
        if not bool(tbls):
            tbls = TABLES       
        items = []
        for tb in tbls:
            if tb == "Yao_JingLuo_Asso":continue
            import_str = "from %(p)s import %(t)s as tablecls" % dict(p='cms.db.orm',t=tb) 
            exec import_str
            items.extend(Session.query(tablecls).all())

        for m in items:
            Session.delete(m)                    
        Session.commit()        


    def create_tables(self,tbls=None):
        """create all db tables
        """

        for tb in tbls:
            import_str = "from %(p)s import %(t)s as tablecls" % dict(p='cms.db.orm',t=tb) 
            exec import_str
#             tablecls.__table__.create(engine)
        Base.metadata.create_all(engine)

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        tbls = TABLES
#         tbls = ['Yao','YaoWei','YaoXing']
        self.empty_tables()
#         self.drop_tables(tbls)
#         self.create_tables(tbls)

    def test_dummy(self):
#         tbls = ['Yao_ChuFang_Asso','Yao_JingLuo_Asso','ChuFang','JingLuo','Yao','YaoWei','YaoXing']
        tbls = TABLES
#         tbls = ['Yao']
#         self.drop_tables(tbls)

    def test_yao_danwei_asso(self):
        "test for yao_danwei table"
        yaowei = YaoWei("酸")
        yaoxing = YaoXing("寒")
        jingluo = JingLuo("足厥阴肝经")
        yao = Yao("白芍")        
        yao.yaowei = yaowei
        yao.yaoxing = yaoxing
        yao.guijing = [jingluo]
        dizhi2 = DanWeiDiZhi(guojia="中国",sheng="湖北",shi="十堰市",jiedao="茅箭区施洋路83号")        
        danwei = DanWei("任之堂")
        yisheng = YiSheng(xingming='余浩',xingbie=1,shengri=date(2015, 4, 2),dianhua='13673265859')
        danwei.yishengs = [yisheng]
        danwei.dizhi = dizhi2
        yao_danwei = Yao_DanWei_Asso(yao,danwei,700,0.26)
        Session.add_all([danwei,dizhi2,yao_danwei,\
                         yisheng,yaowei,yaoxing,jingluo])                         
        Session.commit()       
        rds = Session.query(Yao_DanWei_Asso).all()
        self.assertEqual(len(rds),1)

        tbs = ['DanWei', 'DanWeiDiZhi', 'YaoWei', 'YaoXing','JingLuo','Yao','YiSheng','Yao_DanWei_Asso']
        self.empty_tables(tbs)

    def test_joined_inheritance_dizhi(self):
        "test for joined inheritance table"

        dizhi = DiZhi(guojia="中国",sheng="湖北",shi="十堰市",jiedao="茅箭区施洋路83号")
        gdizhi = GeRenDiZhi(guojia="中国",sheng="湖南",shi="湘潭市",
                            jiedao="湘潭县云湖桥镇北岸村道林组83号")
        ddizhi = DanWeiDiZhi(guojia="中国",sheng="湖南",shi="湘潭市",
                             jiedao="湘潭县云湖桥镇北岸村道林组38号",
                             wangzhi="http://www.315ok.org/",
                             gongzhonghao="zhongyi")
        
        Session.add_all([dizhi,gdizhi,ddizhi])
        Session.commit()
        rds = Session.query(DiZhi).filter(DiZhi.sheng=="湖南").all()
        self.assertEqual(len(rds),2)        
        rds = Session.query(GeRenDiZhi).filter(GeRenDiZhi.sheng=="湖南").all()
        self.assertEqual(len(rds),1)
        rds = Session.query(DanWeiDiZhi).filter(DanWeiDiZhi.gongzhonghao=="zhongyi").all()

        self.assertEqual(len(rds),1)
        tbs = ['DiZhi', 'DanWeiDiZhi', 'GeRenDiZhi']
        self.empty_tables(tbs)
        

    def test_yaowei(self):

        yaowei = YaoWei("酸")
        Session.add(yaowei)
        Session.commit()
        suan = Session.query(YaoWei).filter(YaoWei.wei=="酸").all()
        self.assertEqual(len(suan),1)
        for xing in suan:
            Session.delete(xing)            
        Session.commit()
        suan = Session.query(YaoWei).all()        
        self.assertEqual(bool(suan),False)
        
    def test_yaoxing(self):

        yaoxing = YaoXing("寒")
        Session.add(yaoxing)
        Session.commit()
        suan = Session.query(YaoXing).filter(YaoXing.xing=="寒").all()
        self.assertEqual(len(suan),1)                     
        suan = Session.query(YaoXing).all()
        for xing in suan:
            Session.delete(xing)            
        Session.commit()
        suan = Session.query(YaoXing).all()
        self.assertEqual(bool(suan),False)
 
    def test_jingluo(self):

        item = JingLuo("足少阳胆经")
        Session.add(item)
        Session.commit()
        items = Session.query(JingLuo).filter(JingLuo.mingcheng=="足少阳胆经").all()
        self.assertEqual(len(items),1)             
        for m in items:
            Session.delete(m)            
        Session.commit()
        items = Session.query(JingLuo).all()
        self.assertEqual(bool(items),False)               

    def test_yaoes(self):
        
        yaowei = YaoWei("酸")
        yaoxing = YaoXing("寒")
        jingluo = JingLuo("足厥阴肝经")
        yao = Yao("白芍")        
        yao.yaowei = yaowei
        yao.yaoxing = yaoxing
        yao.guijing = [jingluo]
        Session.add(yao)
        Session.add(yaowei)
        Session.add(yaoxing)
        Session.add(jingluo)                                     
        Session.commit()
        items = Session.query(Yao.mingcheng,YaoWei.wei).filter(YaoWei.wei=="酸").all()
        self.assertEqual(len(items),1)           
        items = Session.query(JingLuo).all()
        self.assertEqual(len(items),1)
        items = Session.query(Yao).all()
        items.extend(Session.query(YaoXing).all())
        items.extend(Session.query(YaoWei).all())
        items.extend(Session.query(JingLuo).all())
        for m in items:
            Session.delete(m)            
        Session.commit()        

    def test_chufang_yao(self):
        
       
        yaowei = YaoWei("酸")
        yaoxing = YaoXing("寒")
        jingluo = JingLuo("足厥阴肝经")
        yao = Yao("白芍")
        chufang = ChuFang("桂枝汤")
        yao_chufang = Yao_ChuFang_Asso(yao,chufang,7,"加热稀粥")        
        yao.yaowei = yaowei
        yao.yaoxing = yaoxing
        yao.guijing = [jingluo]
        Session.add(yao)
        Session.add(yaowei)
        Session.add(yaoxing)
        Session.add(jingluo)
        Session.add(yao_chufang)
                                     
        Session.commit()
        items = Session.query(Yao.mingcheng,YaoWei.wei).filter(YaoWei.wei=="酸").all()
        self.assertEqual(len(items),1)           
        items = Session.query(JingLuo).all()
        self.assertEqual(len(items),1)        
        items = Session.query(Yao).all()
        items.extend(Session.query(YaoXing).all())
        items.extend(Session.query(YaoWei).all())
        items.extend(Session.query(JingLuo).all())
        items.extend(Session.query(ChuFang).all())
        for m in items:
            Session.delete(m)            
        Session.commit()        

    def test_dizhi(self):
        
        dizhi = DiZhi(guojia="中国",sheng="湖南",shi="湘潭市",jiedao="湘潭县云湖桥镇北岸村道林组83号")
        Session.add(dizhi)                                     
        Session.commit()
        items = Session.query(DiZhi.jiedao).filter(DiZhi.sheng=="湖南").first()
        self.assertEqual(items[0],u"湘潭县云湖桥镇北岸村道林组83号")           
        items = Session.query(DiZhi).all()
        for m in items:
            Session.delete(m)            
        Session.commit()
    
    def test_danwei(self):
        
        dizhi = DanWeiDiZhi(guojia="中国",sheng="湖南",shi="湘潭市",jiedao="湘潭县云湖桥镇北岸村道林组83号")
        danwei = DanWei("任之堂")
        danwei.dizhi = dizhi
        Session.add(danwei)                                    
        Session.commit()
        items = Session.query(DanWei).filter(DanWei.mingcheng=="任之堂").first()
        self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")          
        items = Session.query(DanWei).all()
        items.extend(Session.query(GeRenDiZhi).all())
        items.extend(Session.query(DanWeiDiZhi).all())         
        items.extend(Session.query(DiZhi).all())

        for m in items:
            Session.delete(m)            
        Session.commit()
 
    def test_yisheng(self):
        
        dizhi = DanWeiDiZhi(guojia="中国",sheng="湖南",shi="湘潭市",jiedao="湘潭县云湖桥镇北岸村道林组83号")
        danwei = DanWei("任之堂")
        yisheng = YiSheng(xingming='余浩',xingbie=1,shengri=date(2015, 4, 2),dianhua='13673265859')
        danwei.yishengs = [yisheng]
        danwei.dizhi = dizhi
        Session.add(danwei)                                    
        Session.commit()
        items = Session.query(DanWei).filter(DanWei.mingcheng=="任之堂").first()
        self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")

        items = Session.query(YiSheng).join(DanWei).filter(DanWei.mingcheng=="任之堂").first()
        self.assertEqual(items.danwei.dizhi.jiedao,"湘潭县云湖桥镇北岸村道林组83号")
        self.assertEqual(items.danwei.yishengs[0],items)
                         
        items = Session.query(DanWei).all()
        items.extend(Session.query(GeRenDiZhi).all())
        items.extend(Session.query(DanWeiDiZhi).all())         
        items.extend(Session.query(DiZhi).all())
        items.extend(Session.query(YiSheng).all())
        
        for m in items:
            Session.delete(m)            
        Session.commit()

    def test_bingren(self):
        
        dizhi = GeRenDiZhi(guojia="中国",sheng="湖南",shi="湘潭市",jiedao="湘潭县云湖桥镇北岸村道林组83号")
        bingren = BingRen(xingming='张三',xingbie=1, shengri=date(2015, 4, 2),dianhua='13673265899')
        bingren.dizhi = dizhi
        Session.add(bingren)                                    
        Session.commit()
        items = Session.query(BingRen).filter(BingRen.dianhua=="13673265899").first()
        self.assertEqual(items.dizhi.jiedao,"湘潭县云湖桥镇北岸村道林组83号")

        items = Session.query(BingRen).join(GeRenDiZhi).filter(GeRenDiZhi.sheng=="湖南").first()
        self.assertEqual(items.dizhi.jiedao,"湘潭县云湖桥镇北岸村道林组83号")
                         
        items = Session.query(BingRen).all()
        items.extend(Session.query(GeRenDiZhi).all())
        items.extend(Session.query(DanWeiDiZhi).all())         
        items.extend(Session.query(DiZhi).all()) 
        
        for m in items:
            Session.delete(m)            
        Session.commit()

    def test_asso_chufang_bingren(self):
        
        dizhi = GeRenDiZhi(guojia="中国",sheng="湖南",shi="湘潭市",jiedao="湘潭县云湖桥镇北岸村道林组83号")
        bingren = BingRen('张三',1, date(2015, 4, 2),'13673265899')
        bingren.dizhi = dizhi
        dizhi2 = DanWeiDiZhi(guojia="中国",sheng="湖北",shi="十堰市",jiedao="茅箭区施洋路83号")
        danwei = DanWei("任之堂")
        yisheng = YiSheng('余浩',1, date(2015, 4, 2),'13673265859')
        danwei.yishengs = [yisheng]
        danwei.dizhi = dizhi2
        yaowei = YaoWei("酸")
        yaoxing = YaoXing("寒")
        jingluo = JingLuo("足厥阴肝经")
        yao = Yao("白芍")
        chufang = ChuFang("桂枝汤")
        yao.yaowei = yaowei
        yao.yaoxing = yaoxing
        yao.guijing = [jingluo]        
        yao_chufang = Yao_ChuFang_Asso(yao,chufang,7,"加热稀粥")        
                
        chufang_bingren = ChuFang_BingRen_Asso(bingren,chufang,datetime.now())
# many to many association table don't add to session
#         Session.add(Yao_ChuFang_Asso)        
#         Session.add(ChuFang_BingRen_Asso)        
        Session.add(yaowei)
        Session.add(yaoxing)
        Session.add(jingluo)
        Session.add(yao)
        Session.add(chufang)
        Session.add(yao_chufang)
        Session.add(dizhi)
        Session.add(bingren)
        Session.add(dizhi2)
        Session.add(danwei)        
        Session.add(yisheng)
        Session.add(chufang_bingren)
                                    
        Session.commit()
        try:
            items = Session.query(BingRen).filter(BingRen.dianhua=="13673265899").first()
            self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")
            items = Session.query(BingRen).join(GeRenDiZhi).filter(GeRenDiZhi.sheng=="湖南").first()
            self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")
        except:
            Session.rollback()
        
        items = Session.query(Yao).all()
        items.extend(Session.query(YaoXing).all())
        items.extend(Session.query(YaoWei).all())
        items.extend(Session.query(JingLuo).all())
        items.extend(Session.query(ChuFang).all())
        items.extend(Session.query(BingRen).all())
        items.extend(Session.query(YiSheng).all())
        items.extend(Session.query(DanWei).all())
        items.extend(Session.query(GeRenDiZhi).all())
        items.extend(Session.query(DanWeiDiZhi).all())         
        items.extend(Session.query(DiZhi).all())        
        for m in items:
            Session.delete(m)            
        Session.commit()                       


    def test_all_tables(self):
        
        dizhi = GeRenDiZhi(guojia="中国",sheng="湖南",shi="湘潭市",jiedao="湘潭县云湖桥镇北岸村道林组83号")
        bingren = BingRen('张三',1, date(2015, 4, 2),'13673265899')
        bingren.dizhi = dizhi
        dizhi2 = DanWeiDiZhi(guojia="中国",sheng="湖北",shi="十堰市",jiedao="茅箭区施洋路83号")
        danwei = DanWei("任之堂")
        yisheng = YiSheng('余浩',1, date(2015, 4, 2),'13673265859')
        danwei.yishengs = [yisheng]
        danwei.dizhi = dizhi2
        yaowei = YaoWei("酸")
        yaoxing = YaoXing("寒")
        jingluo = JingLuo("足厥阴肝经")
        yao = Yao("白芍")
        yaowei2 = YaoWei("甘")
        yaoxing2 = YaoXing("温")
        jingluo2 = JingLuo("足太阴脾经")
        yao2 = Yao("大枣")        
        chufang = ChuFang("桂枝汤")
        yao2.yaowei = yaowei2
        yao2.yaoxing = yaoxing2
        yao2.guijing = [jingluo2]
        yao.yaowei = yaowei
        yao.yaoxing = yaoxing
        yao.guijing = [jingluo]                
        yao_chufang = Yao_ChuFang_Asso(yao,chufang,7,"加热稀粥")
        yao_chufang2 = Yao_ChuFang_Asso(yao2,chufang,10,"掰开")        
                
        chufang_bingren = ChuFang_BingRen_Asso(bingren,chufang,datetime.now())
        yisheng.chufangs = [chufang]
        
        Session.add_all([yaowei,yaoxing,jingluo,yao,chufang,yao_chufang])
        Session.add_all([yaowei2,yaoxing2,jingluo2,yao2,yao_chufang2])
        Session.add(dizhi)
        Session.add(bingren)
        Session.add(dizhi2)
        Session.add(danwei)        
        Session.add(yisheng)
        Session.add(chufang_bingren)                                    
        Session.commit()
        try:
            items = Session.query(BingRen).filter(BingRen.dianhua=="13673265899").first()
            self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")
            items = Session.query(BingRen).join(GeRenDiZhi).filter(GeRenDiZhi.sheng=="湖南").first()
            self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")
            items = Session.query(ChuFang).join(YiSheng).filter(YiSheng.xingming=="余浩").first()        
            self.assertEqual(len(items.yaoes),2)
            self.assertEqual(items.yishengxm,"余浩")
        except:
            Session.rollback()
                
        items = Session.query(Yao).all()
        items.extend(Session.query(YaoXing).all())
        items.extend(Session.query(YaoWei).all())
        items.extend(Session.query(JingLuo).all())
        items.extend(Session.query(ChuFang).all())
        items.extend(Session.query(BingRen).all())
        items.extend(Session.query(YiSheng).all())
        items.extend(Session.query(DanWei).all())
        items.extend(Session.query(GeRenDiZhi).all())
        items.extend(Session.query(DanWeiDiZhi).all())                
        items.extend(Session.query(DiZhi).all())        
        for m in items:
            Session.delete(m)            
        Session.commit() 
  
