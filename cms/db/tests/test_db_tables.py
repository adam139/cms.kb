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
from cms.db.orm import Yao_JingLuo_Asso, Yao_ChuFang_Asso

class TestDatabase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def drop_tables(self,tbls=None):
        """drop all db tables
        """

        for tb in tbls:
            import_str = "from %(p)s import %(t)s as tablecls" % dict(p='cms.db.orm',t=tb) 
            exec import_str
        Base.metadata.drop_all(engine)                                

    def empty_tables(self,tbls=None):
        """drop all db tables
        """

#         tbls = ['Yao_ChuFang_Asso','ChuFang','Yao_JingLuo_Asso','Yao','YaoWei','YaoXing','JingLuo']
        tbls = ['YaoWei','YaoXing','JingLuo','Yao_JingLuo_Asso','Yao','Yao_ChuFang_Asso',
                'ChuFang_BingRen_Asso','ChuFang','YiSheng','DanWei','DiZhi','BingRen']        
        items = []
        for tb in tbls:
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
        tbls = ['YaoWei','YaoXing','JingLuo','Yao_JingLuo_Asso','Yao','Yao_ChuFang_Asso',
                'ChuFang_BingRen_Asso','ChuFang','YiSheng','DanWei','DiZhi','BingRen']
#         tbls = ['Yao','YaoWei','YaoXing']
#         self.empty_tables()
#         self.drop_tables(tbls)
        self.create_tables(tbls)

    def ptest_dummy(self):
#         tbls = ['Yao_ChuFang_Asso','Yao_JingLuo_Asso','ChuFang','JingLuo','Yao','YaoWei','YaoXing']
        tbls = ['YaoWei','YaoXing','JingLuo','Yao_JingLuo_Asso','Yao','Yao_ChuFang_Asso',
                'ChuFang_BingRen_Asso','ChuFang','YiSheng','DanWei','DiZhi','BingRen']
#         tbls = ['Yao']
        self.drop_tables(tbls)

    def test_yaowei(self):
        
        from cms.db.orm import YaoWei
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
        
        from cms.db.orm import YaoXing
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
        
        from cms.db.orm import JingLuo
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
        
        from cms.db.orm import Yao,YaoXing,YaoWei,JingLuo
        
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
        
        from cms.db.orm import Yao,YaoXing,YaoWei,JingLuo,ChuFang,Yao_ChuFang_Asso
        
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
        
        from cms.db.orm import DiZhi
        
        dizhi = DiZhi("中国","湖南","湘潭市","湘潭县云湖桥镇北岸村道林组83号")
        Session.add(dizhi)                                     
        Session.commit()
        items = Session.query(DiZhi.jiedao).filter(DiZhi.sheng=="湖南").first()
        self.assertEqual(items[0],u"湘潭县云湖桥镇北岸村道林组83号")           
        items = Session.query(DiZhi).all()
        for m in items:
            Session.delete(m)            
        Session.commit()
    
    def test_danwei(self):
        
        from cms.db.orm import DiZhi,DanWei
        
        dizhi = DiZhi("中国","湖南","湘潭市","湘潭县云湖桥镇北岸村道林组83号")
        danwei = DanWei("任之堂")
        danwei.dizhi = dizhi
        Session.add(danwei)                                    
        Session.commit()
        items = Session.query(DanWei).filter(DanWei.mingcheng=="任之堂").first()
        self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")          
        items = Session.query(DanWei).all()
        items.extend(Session.query(DiZhi).all())

        for m in items:
            Session.delete(m)            
        Session.commit()
 
    def test_yisheng(self):
        
        from cms.db.orm import DiZhi,DanWei,YiSheng
        
        dizhi = DiZhi("中国","湖南","湘潭市","湘潭县云湖桥镇北岸村道林组83号")
        danwei = DanWei("任之堂")
        yisheng = YiSheng('余浩',1, date(2015, 4, 2),'13673265859')
        danwei.yishengs = [yisheng]
        danwei.dizhi = dizhi
        Session.add(danwei)                                    
        Session.commit()
        items = Session.query(DanWei).filter(DanWei.mingcheng=="任之堂").first()
        self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")

        items = Session.query(YiSheng).join(DanWei).filter(DanWei.mingcheng=="任之堂").first()
        self.assertEqual(items.danwei.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")
        self.assertEqual(items.danwei.yishengs[0],items)
                         
        items = Session.query(DanWei).all()
        items.extend(Session.query(DiZhi).all())
        items.extend(Session.query(YiSheng).all())
        
        for m in items:
            Session.delete(m)            
        Session.commit()

    def test_bingren(self):
        
        from cms.db.orm import ChuFang,BingRen,DiZhi
        
        dizhi = DiZhi("中国","湖南","湘潭市","湘潭县云湖桥镇北岸村道林组83号")
        bingren = BingRen('张三',1, date(2015, 4, 2),'13673265899')
        bingren.dizhi = dizhi
        Session.add(bingren)                                    
        Session.commit()
        items = Session.query(BingRen).filter(BingRen.dianhua=="13673265899").first()
        self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")

        items = Session.query(BingRen).join(DiZhi).filter(DiZhi.sheng=="湖南").first()
        self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")
                         
        items = Session.query(BingRen).all()
        items.extend(Session.query(DiZhi).all()) 
        
        for m in items:
            Session.delete(m)            
        Session.commit()

    def test_asso_chufang_bingren(self):
        
        from cms.db.orm import ChuFang,DanWei,\
        BingRen,DiZhi,YiSheng,ChuFang_BingRen_Asso,YaoWei,YaoXing,JingLuo,Yao,Yao_ChuFang_Asso
        
        dizhi = DiZhi("中国","湖南","湘潭市","湘潭县云湖桥镇北岸村道林组83号")
        bingren = BingRen('张三',1, date(2015, 4, 2),'13673265899')
        bingren.dizhi = dizhi
        dizhi2 = DiZhi("中国","湖北","十堰市","茅箭区施洋路83号")
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
        items = Session.query(BingRen).filter(BingRen.dianhua=="13673265899").first()
        self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")

        items = Session.query(BingRen).join(DiZhi).filter(DiZhi.sheng=="湖南").first()
        self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")
        
        items = Session.query(Yao).all()
        items.extend(Session.query(YaoXing).all())
        items.extend(Session.query(YaoWei).all())
        items.extend(Session.query(JingLuo).all())
        items.extend(Session.query(ChuFang).all())
        items.extend(Session.query(BingRen).all())
        items.extend(Session.query(YiSheng).all())
        items.extend(Session.query(DanWei).all())
        items.extend(Session.query(DiZhi).all())        
        for m in items:
            Session.delete(m)            
        Session.commit()                       


    def test_all_tables(self):
        
        from cms.db.orm import ChuFang,DanWei,\
        BingRen,DiZhi,YiSheng,ChuFang_BingRen_Asso,YaoWei,YaoXing,JingLuo,Yao,Yao_ChuFang_Asso
        
        dizhi = DiZhi("中国","湖南","湘潭市","湘潭县云湖桥镇北岸村道林组83号")
        bingren = BingRen('张三',1, date(2015, 4, 2),'13673265899')
        bingren.dizhi = dizhi
        dizhi2 = DiZhi("中国","湖北","十堰市","茅箭区施洋路83号")
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
        items = Session.query(BingRen).filter(BingRen.dianhua=="13673265899").first()
        self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")

        items = Session.query(BingRen).join(DiZhi).filter(DiZhi.sheng=="湖南").first()
        self.assertEqual(items.dizhi.jiedao,u"湘潭县云湖桥镇北岸村道林组83号")
        items = Session.query(ChuFang).join(YiSheng).filter(YiSheng.xingming=="余浩").first()
        import pdb
        pdb.set_trace()
        
        self.assertEqual(len(items.yaoes),2)
        self.assertEqual(items.yishengxm,"余浩")
                
        items = Session.query(Yao).all()
        items.extend(Session.query(YaoXing).all())
        items.extend(Session.query(YaoWei).all())
        items.extend(Session.query(JingLuo).all())
        items.extend(Session.query(ChuFang).all())
        items.extend(Session.query(BingRen).all())
        items.extend(Session.query(YiSheng).all())
        items.extend(Session.query(DanWei).all())
        items.extend(Session.query(DiZhi).all())        
        for m in items:
            Session.delete(m)            
        Session.commit() 
        
    
    def mtest_dbapi_yaowei(self):
# oracle env setting        
#         import os
#         os.environ['NLS_LANG'] = '.AL32UTF8'            
#         self.create_tables(tbls=['Fashej'])
#         self.drop_tables(tbls=['Fashej'])
#         import pdb
#         pdb.set_trace()
        
# ('333333002','发射机01','asd2w23sds212211111','m',2.4,0,2.8,10,0,2.8,20,1.1,'AM-V',2,1,' 常用发射机1')
        values = dict(sbdm="333333003",sbmc=u"发射机02",pcdm="asd2w23sds212211111",location=u"m",
                      freq=2.4,pd_upper=0,pd_lower=2.8,num=10,
                      freq_upper=0,freq_lower=2.8,bw=20,base_power=1.1,
                      tzlx="AM-V",bzf=2,mid_freq=1,comment1=u"常用发射机1")        
        dbapi = queryUtility(IDbapi, name='fashej')
        dbapi.add(values)
        nums = dbapi.query({'start':0,'size':1,'SearchableText':'','sort_order':'reverse'})
        id = nums[0].id        
        rt = dbapi.getByCode(id)
        self.assertTrue(nums is not None)
        self.assertEqual(len(nums),1)
#         rt = dbapi.DeleteByCode(id)
        self.assertTrue(rt)

