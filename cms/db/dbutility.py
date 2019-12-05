#-*- coding: UTF-8 -*-
from cms.db import  Session
from cms.db.ORMdbAPI import Dbapi
from cms.db.orm import YaoWei,YaoXing,JingLuo,Yao,DiZhi,YiSheng,DanWei
from cms.db.orm import ChuFang,YiSheng,BingRen,Yao_ChuFang_Asso,ChuFang_BingRen_Asso

yaoxing = Dbapi(Session,'cms.db.orm','yaoxing',YaoXing)
# yaowei table       
yaowei = Dbapi(Session,'cms.db.orm','yaowei',YaoWei)
# jingluo table       
jingluo = Dbapi(Session,'cms.db.orm','jingluo',JingLuo)
dizhi = Dbapi(Session,'cms.db.orm','dizhi',DiZhi)
yao =  Dbapi(Session,'cms.db.orm','yao',Yao)
chufang = Dbapi(Session,'cms.db.orm','chufang',ChuFang)
bingren = Dbapi(Session,'cms.db.orm','bingren',BingRen)
danwei =  Dbapi(Session,'cms.db.orm','danwei',DanWei)
yisheng =  Dbapi(Session,'cms.db.orm','yisheng',YiSheng)
chufang_bingren =  Dbapi(Session,'cms.db.orm','chufang_bingren',ChuFang_BingRen_Asso)
yao_chufang =  Dbapi(Session,'cms.db.orm','yao_chufang',Yao_ChuFang_Asso)


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

def map_yao_chufang_table(recorder):
    "chufang's base_view map function,"
    "provide a specify output format"
    "parameter:recorder is a association table object recorder"

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
    