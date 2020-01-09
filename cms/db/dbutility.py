#-*- coding: UTF-8 -*-
from cms.db import  Session
from cms.db.ORMdbAPI import Dbapi
from cms.db.orm import YaoWei,YaoXing,JingLuo,Yao,DiZhi,YiSheng,DanWei,DanWeiDiZhi,GeRenDiZhi
from cms.db.orm import ChuFang,YiSheng,BingRen,Yao_ChuFang_Asso,ChuFang_BingRen_Asso
from cms.db.orm import NianGanZhi

yaoxing = Dbapi(Session,'cms.db.orm','yaoxing',YaoXing)
# yaowei table       
yaowei = Dbapi(Session,'cms.db.orm','yaowei',YaoWei)
# jingluo table       
jingluo = Dbapi(Session,'cms.db.orm','jingluo',JingLuo)
dizhi = Dbapi(Session,'cms.db.orm','dizhi',DiZhi)
search_clmns = ['jiedao','shi']
gerendizhi = Dbapi(Session,'cms.db.orm','gerendizhi',GeRenDiZhi,fullsearch_clmns=search_clmns)
danweidizhi = Dbapi(Session,'cms.db.orm','danweidizhi',DanWeiDiZhi)
yao =  Dbapi(Session,'cms.db.orm','yao',Yao)
chufang = Dbapi(Session,'cms.db.orm','chufang',ChuFang)
bingren = Dbapi(Session,'cms.db.orm','bingren',BingRen)
danwei =  Dbapi(Session,'cms.db.orm','danwei',DanWei)
yisheng =  Dbapi(Session,'cms.db.orm','yisheng',YiSheng)
chufang_bingren =  Dbapi(Session,'cms.db.orm','chufang_bingren',ChuFang_BingRen_Asso)
yao_chufang =  Dbapi(Session,'cms.db.orm','yao_chufang',Yao_ChuFang_Asso)
#automap class start
search_clmns = ['ganzhi']
nianganzhi =  Dbapi(Session,'cms.db.orm','nianganzhi',NianGanZhi,fullsearch_clmns=search_clmns)


def map_yao_chufang_list(recorder):
    "chufang_listings view map function,"
    "provide a specify output format"
    "parameter:recorder is a association table object recorder"

    yao_id = recorder.yao_id
    yao = Session.query(Yao).filter(Yao.id ==yao_id).one()
    mingcheng = getattr(yao,'mingcheng',"")
    yaoliang = u"%s克" % recorder.yaoliang
    paozhi = recorder.paozhi
    if bool(paozhi):
        paozhi = "(%s)" % recorder.paozhi
        return ",".join([mingcheng,yaoliang,paozhi])
    else:                
        return ",".join([mingcheng,yaoliang])

def map_yao_chufang_total(recorder):
    "chufang's base_view map function,"
    "provide a total output format"
    "parameter:recorder is a association table object recorder"

    yao_id = recorder.yao_id
    yao = Session.query(Yao).filter(Yao.id ==yao_id).one()
    danjia = getattr(yao,'danjia',0)

    yaoliang = recorder.yaoliang
    if bool(danjia):
        xiaoji = str(yaoliang * danjia)
        return xiaoji
    return str(0.00)

def map_yao_chufang_table(recorder):
    "chufang's base_view map function,"
    "provide a specify output format"
    "parameter:recorder is a yao_chufang association table object recorder"

    yao_id = recorder.yao_id
    yao = Session.query(Yao).filter(Yao.id ==yao_id).one()
    mingcheng = getattr(yao,'mingcheng',"")
    yaoliang = u"%s克" % recorder.yaoliang
    paozhi = recorder.paozhi
    
    if bool(paozhi):
#         paozhi = "(%s)" % recorder.paozhi
        return "<td>%s</td><td>%s</td><td>%s</td>" % (mingcheng,yaoliang,paozhi)
    else:                
        paozhi = u"无"
        return "<td>%s</td><td>%s</td><td>%s</td>" % (mingcheng,yaoliang,paozhi)
    
def map_chufang_bingren_table(recorder):
    "chufang's base_view map function,"
    "provide a specify output format"
    "parameter:recorder is a association table object recorder"

    _id = recorder.bingren_id
    bingren = Session.query(BingRen).filter(BingRen.id ==_id).one()
    xingming = getattr(bingren,'xingming',"")    
    dianhua = getattr(bingren,'dianhua',"") 
    shijian = recorder.shijian   

    return "<td>%s</td><td>%s</td><td>%s</td>" % (xingming,dianhua,shijian)
    