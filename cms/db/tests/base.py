#-*- coding: UTF-8 -*-
from zope import event
from datetime import date
from datetime import datetime
from zope.component import getUtility
from cms.db import  Session
from cms.db.events import RecorderCreated

TABLES = ['YaoWei','YaoXing','JingLuo','Yao_JingLuo_Asso','Yao','Yao_ChuFang_Asso',
        'ChuFang_BingRen_Asso','ChuFang','Person','YiSheng','DanWei','DiZhi', 
        'DanWeiDiZhi', 'GeRenDiZhi', 'BingRen', 'Yao_DanWei_Asso']

for tb in TABLES:
    import_str = "from %(p)s import %(t)s" % dict(p='cms.db.orm',t=tb) 
    exec import_str

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
        yao1 = Yao("白芍","降胆火",15)
        yao1.yaowei = yaowei1
        yao1.yaoxing = yaoxing1
        yao1.guijing = [jingluo1]         
        yao2 = Yao("桂枝","升发",15)
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
        dizhi0 = DiZhi(guojia="中国",sheng="湖南",shi="湘潭市",jiedao="湘潭县云湖桥镇北岸村道林组183号")        
        dizhi = GeRenDiZhi(guojia="中国",sheng="湖南",shi="湘潭市",jiedao="湘潭县云湖桥镇北岸村道林组83号")
        bingren = BingRen(xingming='张三',xingbie=1, shengri=date(2015, 4, 2),dianhua='13673265899')
        bingren.dizhi = dizhi
        dizhi2 = DanWeiDiZhi(guojia="中国",sheng="湖北",shi="十堰市",jiedao="茅箭区施洋路83号")
        dizhi3 = DanWeiDiZhi(guojia="中国",sheng="湖南",shi="湘潭市",jiedao="湘潭县云湖桥镇北岸村道林组38号")
        danwei = DanWei("任之堂")
        danwei2 = DanWei("润生堂")
        yisheng = YiSheng(xingming='余浩',xingbie=1,shengri=date(2015, 4, 2),dianhua='13673265859')
        danwei.yishengs = [yisheng]
        danwei.dizhi = dizhi2
        danwei2.dizhi = dizhi3
        chufang = ChuFang("桂枝汤","加热稀粥",5)
        yao_chufang = Yao_ChuFang_Asso(yao1,chufang,7,"晒干")
        yao_chufang2 = Yao_ChuFang_Asso(yao2,chufang,10,"掰开")
        yao_danwei = Yao_DanWei_Asso(yao1,danwei,700,0.26)
        yao_danwei2 = Yao_DanWei_Asso(yao2,danwei,800,0.36)
        yao_danwei3 = Yao_DanWei_Asso(yao3,danwei,900,0.46)
        yao_danwei4 = Yao_DanWei_Asso(yao4,danwei,1000,0.56)
        yao_danwei5 = Yao_DanWei_Asso(yao5,danwei,1100,0.66)
        yao_danwei6 = Yao_DanWei_Asso(yao6,danwei,1200,0.76)
        maixiang = "两关郁,左寸小,右寸大"
        shexiang = "舌苔淡青,有齿痕"
        zhusu = "小腹冷痛,右肋痛"
        chufang_bingren = ChuFang_BingRen_Asso(bingren,chufang,datetime.now(),maixiang,shexiang,zhusu)
        yisheng.chufangs = [chufang]
        Session.add_all([dizhi0,dizhi,bingren,danwei,danwei2,dizhi2,dizhi3,\
                         yao_danwei,yao_danwei2,yao_danwei3,yao_danwei4,yao_danwei5,yao_danwei6,\
                         yisheng,chufang,yao_chufang,yao_chufang2,chufang_bingren])                         
        Session.commit()
        
def fire_created_event():
    "if add recorder to db is successful,fire the event"
    from plone.registry.interfaces import IRegistry
    from cms.db.browser.interfaces import IAutomaticTypesSettings
    
    recorder = Session.query(YaoXing).filter(YaoXing.xing=="温").first()
    if bool(recorder):
        cls = "cms.db.yaoxing"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.xing)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(YaoXing).filter(YaoXing.xing=="凉").first()
    if bool(recorder):
        cls = "cms.db.yaoxing"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.xing)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(YaoXing).filter(YaoXing.xing=="寒").first()
    if bool(recorder):
        cls = "cms.db.yaoxing"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.xing)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(YaoXing).filter(YaoXing.xing=="热").first()
    if bool(recorder):
        cls = "cms.db.yaoxing"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.xing)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(YaoXing).filter(YaoXing.xing=="大热").first()
    if bool(recorder):
        cls = "cms.db.yaoxing"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.xing)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(YaoXing).filter(YaoXing.xing=="大寒").first()
    if bool(recorder):
        cls = "cms.db.yaoxing"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.xing)
        if eventobj.available():event.notify(eventobj)        
                                        
    recorder = Session.query(YaoWei).filter(YaoWei.wei=="甘").first()
    if bool(recorder):
        cls = "cms.db.yaowei"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.wei)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(YaoWei).filter(YaoWei.wei=="酸").first()
    if bool(recorder):
        cls = "cms.db.yaowei"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.wei)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(YaoWei).filter(YaoWei.wei=="苦").first()
    if bool(recorder):
        cls = "cms.db.yaowei"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.wei)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(YaoWei).filter(YaoWei.wei=="辛").first()
    if bool(recorder):
        cls = "cms.db.yaowei"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.wei)
        if eventobj.available():event.notify(eventobj) 
    recorder = Session.query(YaoWei).filter(YaoWei.wei=="咸").first()
    if bool(recorder):
        cls = "cms.db.yaowei"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.wei)
        if eventobj.available():event.notify(eventobj)                                               
    recorder = Session.query(Yao).filter(Yao.mingcheng=="白芍").first()
    if bool(recorder):
        cls = "cms.db.yao"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(Yao).filter(Yao.mingcheng=="桂枝").first()
    if bool(recorder):
        cls = "cms.db.yao"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(Yao).filter(Yao.mingcheng=="生姜").first()
    if bool(recorder):
        cls = "cms.db.yao"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(Yao).filter(Yao.mingcheng=="大枣").first()
    if bool(recorder):
        cls = "cms.db.yao"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(Yao).filter(Yao.mingcheng=="甘草").first()
    if bool(recorder):
        cls = "cms.db.yao"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(Yao).filter(Yao.mingcheng=="麻黄").first()
    if bool(recorder):
        cls = "cms.db.yao"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)                                                
    recorder = Session.query(JingLuo).filter(JingLuo.mingcheng=="足太阳膀胱经").first()
    if bool(recorder):
        cls = "cms.db.jingluo"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(JingLuo).filter(JingLuo.mingcheng=="足阳明胃经").first()
    if bool(recorder):
        cls = "cms.db.jingluo"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(JingLuo).filter(JingLuo.mingcheng=="足少阳胆经").first()
    if bool(recorder):
        cls = "cms.db.jingluo"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(JingLuo).filter(JingLuo.mingcheng=="足厥阴肝经").first()
    if bool(recorder):
        cls = "cms.db.jingluo"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(JingLuo).filter(JingLuo.mingcheng=="足少阴肾经").first()
    if bool(recorder):
        cls = "cms.db.jingluo"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(JingLuo).filter(JingLuo.mingcheng=="足太阴脾经").first()
    if bool(recorder):
        cls = "cms.db.jingluo"
        id = "%s" % recorder.id
        eventobj = RecorderCreated(id=id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)                                        
    recorder = Session.query(BingRen).filter(BingRen.xingming=="张三").first()
    if bool(recorder):
        cls = "cms.db.bingren"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.xingming)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(YiSheng).filter(YiSheng.xingming=="余浩").first()
    if bool(recorder):
        cls = "cms.db.yisheng"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.xingming)
        if eventobj.available():event.notify(eventobj)
        
    recorder = Session.query(ChuFang).filter(ChuFang.mingcheng=="桂枝汤").first()
    if bool(recorder):
        cls = "cms.db.chufang"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    recorder = Session.query(DanWei).filter(DanWei.mingcheng=="任之堂").first()
    if bool(recorder):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IAutomaticTypesSettings, check=False)
        settings.danweiid = int(recorder.id)
        cls = "cms.db.danwei"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)
    
    recorder = Session.query(DanWei).filter(DanWei.mingcheng=="润生堂").first()
    if bool(recorder):
        cls = "cms.db.danwei"
        eventobj = RecorderCreated(id=recorder.id,cls=cls,ttl=recorder.mingcheng)
        if eventobj.available():event.notify(eventobj)                        
                        
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
    
            
