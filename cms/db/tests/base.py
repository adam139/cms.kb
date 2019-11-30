#-*- coding: UTF-8 -*-
from datetime import date
from datetime import datetime
from cms.db import  Session
from cms.db.orm import YaoWei,YaoXing,JingLuo,Yao,DiZhi,YiSheng,DanWei
from cms.db.orm import ChuFang,YiSheng,BingRen,Yao_ChuFang_Asso,ChuFang_BingRen_Asso


def inputvalues():
        "input init data to db"
        
        yaowei1 = YaoWei("酸")
        yaowei2 = YaoWei("苦")
        yaowei3 = YaoWei("甘")
        yaowei4 = YaoWei("辛")
        yaowei5 = YaoWei("咸")
        Session.add_all([yaowei1,yaowei2,yaowei3,yaowei4,yaowei5])
        yaoxing1 = YaoXing("大热")
        yaoxing2 = YaoXing("热")
        yaoxing3 = YaoXing("温")
        yaoxing4 = YaoXing("凉")
        yaoxing5 = YaoXing("寒")
        yaoxing6 = YaoXing("大寒")
        Session.add_all([yaoxing1,yaoxing2,yaoxing3,yaoxing4,yaoxing5,yaoxing6])
        jingluo1 = JingLuo("足太阳膀胱经")
        jingluo2 = JingLuo("足阳明胃经")
        jingluo3 = JingLuo("足少阳胆经")
        jingluo4 = JingLuo("足厥阴肝经")
        jingluo5 = JingLuo("足少阴肾经")
        jingluo6 = JingLuo("足太阴脾经")
        Session.add_all([jingluo1,jingluo2,jingluo3,jingluo4,jingluo5,jingluo6])
        yao1 = Yao("白芍")
        yao1.yaowei = yaowei1
        yao1.yaoxing = yaoxing1
        yao1.guijing = [jingluo1]         
        yao2 = Yao("桂枝")
        yao2.yaowei = yaowei2
        yao2.yaoxing = yaoxing2
        yao2.guijing = [jingluo2]
        yao3 = Yao("大枣")
        yao3.yaowei = yaowei2
        yao3.yaoxing = yaoxing2
        yao3.guijing = [jingluo2]
        yao4 = Yao("生姜")
        yao4.yaowei = yaowei2
        yao4.yaoxing = yaoxing2
        yao4.guijing = [jingluo2]
        yao5 = Yao("甘草")
        yao5.yaowei = yaowei3
        yao5.yaoxing = yaoxing3
        yao5.guijing = [jingluo2]
        yao6 = Yao("麻黄")
        yao6.yaowei = yaowei4
        yao6.yaoxing = yaoxing2
        yao6.guijing = [jingluo2]                                
        Session.add_all([yao1,yao2,yao3,yao4,yao5,yao6])        
        dizhi = DiZhi("中国","湖南","湘潭市","湘潭县云湖桥镇北岸村道林组83号")
        bingren = BingRen('张三',1, date(2015, 4, 2),'13673265899')
        bingren.dizhi = dizhi
        dizhi2 = DiZhi("中国","湖北","十堰市","茅箭区施洋路83号")
        dizhi3 = DiZhi("中国","湖南","湘潭市","湘潭县云湖桥镇北岸村道林组38号")
        danwei = DanWei("任之堂")
        danwei2 = DanWei("润生堂")
        yisheng = YiSheng('余浩',1, date(2015, 4, 2),'13673265859')
        danwei.yishengs = [yisheng]
        danwei.dizhi = dizhi2
        danwei2.dizhi = dizhi3
        chufang = ChuFang("桂枝汤","加热稀粥",5)
        yao_chufang = Yao_ChuFang_Asso(yao1,chufang,7,"晒干")
        yao_chufang2 = Yao_ChuFang_Asso(yao2,chufang,10,"掰开")
        chufang_bingren = ChuFang_BingRen_Asso(bingren,chufang,datetime.now())
        yisheng.chufangs = [chufang]
        Session.add_all([dizhi,bingren,danwei,danwei2,dizhi2,dizhi3,\
                         yisheng,chufang,yao_chufang,yao_chufang2,chufang_bingren])                         
        Session.commit()
        
def cleardb():
    "remove all recorders from db"
    items = Session.query(YaoWei).all()
    items.extend(Session.query(YaoXing).all())
    items.extend(Session.query(JingLuo).all())
    items.extend(Session.query(Yao).all())
    items.extend(Session.query(ChuFang).all())
    items.extend(Session.query(BingRen).all())
    items.extend(Session.query(YiSheng).all())
    items.extend(Session.query(DanWei).all())
    items.extend(Session.query(DiZhi).all())
               
    for item in items:
        Session.delete(item)            
    Session.commit()    
    
            
