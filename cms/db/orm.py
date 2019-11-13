#-*- coding: UTF-8 -*-

import sqlalchemy.schema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import mysql
from sqlalchemy import Column, String, Integer, Date, DateTime, Boolean, Table, func
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from zope import schema
from zope.interface import Interface,implements

from Chinese.medical.science import ORMBase as Base
from Chinese.medical.science import _


###药味
class IYaoWei(Interface):
    """wu wei:
    酸、苦、甘、辛、咸
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    wei = schema.TextLine(
            title=_(u"wu wei qizhong zhi yiwei"),
        ) 
       

class YaoWei(Base):
    
    implements(IYaoWei)
    __tablename__ = 'yaowei'

    id = Column(Integer, primary_key=True)
    wei = Column(String(8))    

    def __init__(self, wei):
        self.wei = wei


###药性
class IYaoXing(Interface):
    """药性:
    大热、热、平、大寒、寒
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    xing = schema.TextLine(
            title=_(u"yao xing"),
        ) 
       

class YaoXing(Base):
    
    implements(IYaoXing)
    __tablename__ = 'yaoxing'

    id = Column(Integer, primary_key=True)
    xing = Column(String((8)))    

    def __init__(self, xing):
        self.xing = xing
 
        
### 经络
class IJingLuo(Interface):
    """经络:
    足太阳膀胱经、足少阳胆经等
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    mingcheng = schema.TextLine(
            title=_(u"ming cheng"),
        ) 
#     yaoes = schema.Object(
#             title=_(u"yao"),
#             schema=IYao,
#         )
    
           

class JingLuo(Base):
    
    implements(IJingLuo)
    __tablename__ = 'jingluo'

    id = Column(Integer, primary_key=True)
    mingcheng = Column(String(14))
#     yaoes = relationship("Yao", secondary=Yao_JingLuo_Asso)    

    def __init__(self, mingcheng):
        self.mingcheng = mingcheng

       
 ###药和经络关联表
Yao_JingLuo_Asso = Table(
    'yao_jingluo', Base.metadata,
    Column('yao_id', Integer, ForeignKey('yao.id')),
    Column('jingluo_id', Integer, ForeignKey('jingluo.id'))
)


###药
class IYao(Interface):
    """中药:
    人参、白术、甘草
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    yaowei_id = schema.Int(
            title=_(u"foreagn key link to wei"),
        ) 
    yaoxing_id = schema.Int(
            title=_(u"foreagn key link to yao xing"),
        )       
    mingcheng = schema.TextLine(
            title=_(u"ming cheng"),
        )
    zhuzhi = schema.TextLine(
            title=_(u"zhu zhi"),
        )
    yaowei = schema.Object(
            title=_(u"gui jing"),
            schema=IJingLuo,
        )
    yaoxing = schema.Object(
            title=_(u"gui jing"),
            schema=IJingLuo,
        )        
    guijing = schema.Object(
            title=_(u"gui jing"),
            schema=IJingLuo,
        )
        
        
class Yao(Base):
    
    implements(IYao)    
    __tablename__ = 'yao'

    id = Column(Integer, primary_key=True)
    yaowei_id = Column(Integer, ForeignKey('yaowei.id'))
    yaoxing_id = Column(Integer, ForeignKey('yaoxing.id'))
    mingcheng = Column(String(4))
    zhuzhi = Column(String(64))
    yaowei = relationship("YaoWei", backref="yaoes")
    yaoxing = relationship("YaoXing", backref="yaoes")
    guijing = relationship("JingLuo", secondary=Yao_JingLuo_Asso)    

    def __init__(self, mingcheng,zhuzhi=None):
        self.mingcheng = mingcheng
        self.zhuzhi = zhuzhi

 
###处方
class IChuFang(Interface):
    """中药:
    人参、白术、甘草
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    yisheng_id = schema.Int(
            title=_(u"foreagn key link to yisheng"),
        ) 
    mingcheng = schema.TextLine(
            title=_(u"ming cheng"),
        )
    yizhu = schema.TextLine(
            title=_(u"zhu zhi"),
        )
    jiliang = schema.Int(
            title=_(u"ji liang"),
        )    
#     yisheng = schema.Object(
#             title=_(u"dan wei"),
#             schema=IYiSheng,
#         )
            
        
class ChuFang(Base):
    
    implements(IChuFang)    
    __tablename__ = 'chufang'

    id = Column(Integer, primary_key=True)
    yisheng_id = Column(Integer, ForeignKey('yisheng.id'))
    mingcheng = Column(String(24))
    jiliang = Column(Integer)
    yizhu = Column(String(64))
    
    # association proxy of "yaoes" collection
    # to "yao" attribute
    yaoes = association_proxy('yao_chufang', 'yao')    

    # association proxy of "bingrens" collection
    # to "bingren" attribute of ChuFang_BingRen_Asso's object
    bingrens = association_proxy('chufang_bingrens', 'bingren')
    # chufang - yisheng: many to one relation
    yisheng = relationship("YiSheng", backref="chufangs")
    
    # association proxy of "yishengxm" through "yisheng" relation object
    # to "xingming" attribute of YiSheng CLASS's object
    yishengxm = association_proxy('yisheng', 'xingming')
       
    def __init__(self, mingcheng,yizhu=None,jiliang=5):
        self.mingcheng = mingcheng
        self.jiliang = jiliang
        self.yizhu = yizhu
        

 ###药和处方关联表
class Yao_ChuFang_Asso(Base):
    __tablename__ = 'yao_chufang'
    
    yao_id = Column(Integer, ForeignKey('yao.id'), primary_key=True)
    chufang_id = Column(Integer, ForeignKey('chufang.id'), primary_key=True)
    yaoliang = Column(Integer)
    paozhi = Column(String(64))
     
    # bidirectional attribute/collection of "chufang"/"yao_chufang"
    chufang = relationship(ChuFang,
                backref=backref("yao_chufang",
                                cascade="all, delete-orphan")
            )

    # reference to the "Yao" object
    yao = relationship("Yao")

    def __init__(self, yao=None, chufang=None, yaoliang=None, paozhi=None):
        self.yao = yao
        self.chufang = chufang
        self.yaoliang = yaoliang
        self.paozhi = paozhi



        
###联系地址
class IDiZhi(Interface):
    """地址:
    中国 湖南 湘潭市 湘潭县云湖桥镇北岸村道林组83号
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )   
    guojia = schema.TextLine(
            title=_(u"guo jia"),
            required=True,
            default=u"中国",
        )
    sheng = schema.TextLine(
            title=_(u"sheng(state)"),
            required=True,            
        )    
    shi = schema.TextLine(
            title=_(u"shi (city)"),
            required=True,             
        )        
    jiadao = schema.TextLine(
            title=_(u"jie dao"),
        )
    

class DiZhi(Base):
    
    implements(IDiZhi)    
    __tablename__ = 'dizhi'

    id = Column(Integer, primary_key=True)
    guojia = Column(String(24))
    sheng = Column(String(12))
    shi = Column(String(12))
    jiedao = Column(String(64))
    
    def __init__(self, guojia=None, sheng=None, shi=None, jiedao=None):
        self.guojia = guojia
        self.sheng = sheng
        self.shi = shi
        self.jiedao = jiedao


###医生单位
class IDanWei(Interface):
    """单位:
    任之堂
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    dizhi_id = schema.Int(
            title=_(u"foreagn key link to wei"),
        ) 
    mingcheng = schema.TextLine(
            title=_(u"ming cheng"),
            required=True,
        )
    dizhi = schema.Object(
            title=_(u"di zhi"),
            schema=IDiZhi,
        )    


class DanWei(Base):
    
    implements(IDanWei)    
    __tablename__ = 'danwei'

    id = Column(Integer, primary_key=True)
    dizhi_id = Column(Integer, ForeignKey('dizhi.id'))
    mingcheng = Column(String(32))
    dizhi = relationship("DiZhi", uselist=False)

    
    def __init__(self, mingcheng=None, dizhi=None):
        self.mingcheng = mingcheng
        self.dizhi = dizhi
        
                    
###医生
class IYiSheng(Interface):
    """余浩:
    
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    danwei_id = schema.Int(
            title=_(u"foreagn key link to danwei"),
        ) 
    xingming = schema.TextLine(
            title=_(u"xing ming"),
            required=True,
        )
    xingbie = schema.Choice(
            title=_(u"xing bie"),
            vocabulary='Chinese.medical.science.vocabulary.xiebie',
            required=True,            
        )    
    shengri = schema.Date(
            title=_(u"xing ming"),
        )        
    dianhua = schema.TextLine(
            title=_(u"dian hua"),
        )
    danwei = schema.Object(
            title=_(u"dan wei"),
            schema=IDanWei,
        )    


class YiSheng(Base):
    """many to one:
    多端放外键及关系
    """
    
    implements(IYiSheng)    
    __tablename__ = 'yisheng'

    id = Column(Integer, primary_key=True)
    danwei_id = Column(Integer, ForeignKey('danwei.id'))
    xingming = Column(String(16))
    xingbie = Column(Boolean)
    shengri = Column(Date)
    dianhua = Column(String(16))
    danwei = relationship("DanWei", backref="yishengs")
    
    def __init__(self, xingming=None, xingbie=None, shengri=None, dianhua=None):
        self.xingming = xingming
        self.xingbie = xingbie
        self.shengri = shengri
        self.dianhua = dianhua
        
        
###病人
class IBingRen(Interface):
    """病人:
    
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    dizhi_id = schema.Int(
            title=_(u"foreagn key link to wei"),
        ) 
    xingming = schema.TextLine(
            title=_(u"xing ming"),
            required=True,
        )
    xingbie = schema.Choice(
            title=_(u"xing bie"),
            vocabulary='Chinese.medical.science.vocabulary.xiebie',
            required=True,            
        )    
    shengri = schema.Date(
            title=_(u"xing ming"),
        )        
    dianhua = schema.TextLine(
            title=_(u"dian hua"),
        )
    dizhi = schema.Object(
            title=_(u"di zhi"),
            schema=IDiZhi,
        )
# all chufangs of bingren
    chufangs = schema.Object(
            title=_(u"chu fang"),
            schema=IChuFang,
        )    
    

class BingRen(Base):
    
    implements(IBingRen)    
    __tablename__ = 'bingren'

    id = Column(Integer, primary_key=True)
    dizhi_id = Column(Integer, ForeignKey('dizhi.id'))
    xingming = Column(String(16))
    xingbie = Column(Boolean)
    shengri = Column(Date)
    dianhua = Column(String(16))
    dizhi = relationship("DiZhi", uselist=False)
    
    # association proxy of "chufangs" collection
    # to "chufang" attribute of ChuFang_BingRen CLASS's object
    chufangs = association_proxy('chufangs_bingren', 'chufang')    
    
    def __init__(self, xingming=None, xingbie=None, shengri=None, dianhua=None, dizhi=None):
        self.xingming = xingming
        self.xingbie = xingbie
        self.shengri = shengri
        self.dianhua = dianhua
        self.dizhi = dizhi              
        
        
 ###处方和病人关联表
class ChuFang_BingRen_Asso(Base):
    __tablename__ = 'chufang_bingren'
    
    bingren_id = Column(Integer, ForeignKey('bingren.id'), primary_key=True)
    chufang_id = Column(Integer, ForeignKey('chufang.id'), primary_key=True)
    shijian = Column(DateTime, default=func.now())
     
    # bidirectional attribute/collection of "bingren"/"chufang_bingren"
    bingren = relationship(BingRen,
                backref=backref("chufangs_bingren",
                                cascade="all, delete-orphan")
            )
    # bidirectional attribute/collection of "chufang"/"chufang_bingren"
    chufang = relationship(ChuFang,
                backref=backref("chufang_bingrens",
                                cascade="all, delete-orphan")
            )    
#     # reference to the "ChuFang" object
#     chufang = relationship("ChuFang")

    def __init__(self, bingren=None, chufang=None, shijian=None):
        self.bingren = bingren
        self.chufang = chufang
        self.shijian = shijian

                
                   