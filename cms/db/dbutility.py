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

