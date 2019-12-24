#-*- coding: UTF-8 -*-

import sqlalchemy.schema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import mysql
from sqlalchemy import Column, String, Integer, Date, DateTime, Boolean, Table, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
from datetime import datetime
from zope import schema
from zope.interface import Interface,implements

from cms.db import ORMBase as Base
from cms.db import engine
from cms.db import _


# automap
metadata = MetaData()
metadata.reflect(engine, only=['nianganzhi'])
AutoBase = automap_base(metadata=metadata)
AutoBase.prepare()
NianGanZhi = AutoBase.classes.nianganzhi

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

    def __init__(self, wei=None):
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

    def __init__(self, xing=None):
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

    def __init__(self, mingcheng=None):
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
            required = False,
        )
    yongliang = schema.Int(
            title=_(u"tongchang yongliang"),
            required = False,
        )    
    yaowei = schema.Object(
            title=_(u"yao wei"),
            schema=IYaoWei,
        )
    yaoxing = schema.Object(
            title=_(u"yao xing"),
            schema=IYaoXing,
        )        
    guijing = schema.List(
            title=_(u"gui jing"),
            value_type=schema.Choice(vocabulary='cms.db.jingluo'),
        )
        
        
class Yao(Base):
    
    implements(IYao)    
    __tablename__ = 'yao'

    id = Column(Integer, primary_key=True)
    yaowei_id = Column(Integer, ForeignKey('yaowei.id'))
    yaoxing_id = Column(Integer, ForeignKey('yaoxing.id'))
    mingcheng = Column(String(4))
    zhuzhi = Column(String(64))
    yongliang = Column(Integer)
    yaowei = relationship("YaoWei", backref="yaoes")
    yaoxing = relationship("YaoXing", backref="yaoes")
    guijing = relationship("JingLuo",secondary=Yao_JingLuo_Asso)    
#     guijing = relationship("JingLuo",lazy='subquery', secondary=Yao_JingLuo_Asso,
#                            backref=backref("yaoes",lazy='subquery'))    

    def __init__(self, mingcheng=None,zhuzhi=None,yongliang=None):
        self.mingcheng = mingcheng
        self.zhuzhi = zhuzhi
        self.yongliang = yongliang

 
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
       
    def __init__(self, mingcheng=None,yizhu=None,jiliang=5):
        self.mingcheng = mingcheng
        self.jiliang = jiliang
        self.yizhu = yizhu
        

 ###药和处方关联表
class IYao_ChuFang_Asso(Interface):
    """
    """
    yao_id = schema.Int(
            title=_(u"foreagn key link to yao"),
        )    
    chufang_id = schema.Int(
            title=_(u"foreagn key link to chufang"),
        )
    yaoliang = schema.Int(
            title=_(u"foreagn key link to yisheng"),
        )    
    paozhi = schema.TextLine(
            title=_(u"ming cheng"),
        )
    
         
class Yao_ChuFang_Asso(Base):
    __tablename__ = 'yao_chufang'
    
    yao_id = Column(Integer, ForeignKey('yao.id'), primary_key=True)
    chufang_id = Column(Integer, ForeignKey('chufang.id'), primary_key=True)
    yaoliang = Column(Integer)
    paozhi = Column(String(64))
     
    # bidirectional attribute/collection of "chufang"/"yao_chufang"
    chufang = relationship(ChuFang,lazy='subquery',
                backref=backref("yao_chufang",lazy='subquery',
                                cascade="all, delete-orphan")
            )

    # reference to the "Yao" object
    yao = relationship("Yao",lazy='subquery')
#     yao = relationship("Yao")

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
    jiedao = schema.TextLine(
            title=_(u"jie dao"),
            required=True,            
        )
    

class DiZhi(Base):
    
    implements(IDiZhi)    
    __tablename__ = 'dizhi'

    id = Column(Integer, primary_key=True)
    guojia = Column(String(24))
    sheng = Column(String(12))
    shi = Column(String(12))
    jiedao = Column(String(64))
    type = Column(String(12))
    
    __mapper_args__ = {
        'polymorphic_identity':'dizhi',
        'polymorphic_on':type
    }
    
#     def __init__(self, guojia=None, sheng=None, shi=None, jiedao=None):
#         self.guojia = guojia
#         self.sheng = sheng
#         self.shi = shi
#         self.jiedao = jiedao

class IDanWeiDiZhi(IDiZhi):
    """interface for add DanWeiDiZhi"""
    
    wangzhi = schema.TextLine(
            title=_(u"wang zhi"),           
        )
    gongzhonghao = schema.TextLine(
            title=_(u"gong zhong hao"),           
        )    
    
    
###单位地址
class DanWeiDiZhi(DiZhi):
    
    implements(IDanWeiDiZhi)    
    __tablename__ = 'danweidizhi'

    id = Column(Integer, ForeignKey('dizhi.id'), primary_key=True)
    wangzhi = Column(String(36))
    gongzhonghao = Column(String(24))
    __mapper_args__ = {
        'polymorphic_identity':'danweidizhi'
    }
    

class IGeRenDiZhi(IDiZhi):
    """interface for add GeRenDiZhi"""
    pass


###个人地址
class GeRenDiZhi(DiZhi):
    
    implements(IGeRenDiZhi)    
    __tablename__ = 'gerendizhi'

    id = Column(Integer, ForeignKey('dizhi.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'gerendizhi'
    }


###医生单位
class IDanWei(Interface):
    """单位:
    任之堂
    """
    id = schema.Int(
            title=_(u"table primary key"),
        )    
    dizhi_id = schema.Int(
            title=_(u"foreagn key link to dizhi"),
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
    dizhi_id = Column(Integer, ForeignKey('danweidizhi.id'))
    mingcheng = Column(String(32))
    dizhi = relationship("DanWeiDiZhi", uselist=False)

    
    def __init__(self, mingcheng=None, dizhi=None):
        self.mingcheng = mingcheng
        self.dizhi = dizhi
        
                    
###person
class IPerson(Interface):
    """余浩:
    
    """
    id = schema.Int(
            title=_(u"table primary key"),
        ) 
    xingming = schema.TextLine(
            title=_(u"xing ming"),
            required=True,
        )
    xingbie = schema.Choice(
            title=_(u"xing bie"),
            vocabulary='cms.db.xingbie',
            required=True,            
        )    
    shengri = schema.Date(
            title=_(u"xing ming"),
        )        
    dianhua = schema.TextLine(
            title=_(u"dian hua"),
        )
    type = schema.TextLine(
            title=_(u"lei xing"),
        )    


class Person(Base):
    """many to one:
    多端放外键及关系
    """
     
    implements(IPerson)    
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    xingming = Column(String(16))
    xingbie = Column(Boolean)
    shengri = Column(Date)
    dianhua = Column(String(16))
    type = Column(String(16))
     
    __mapper_args__ = {
        'polymorphic_identity':'person',
        'polymorphic_on':type
    }


###医生
class IYiSheng(IPerson):
    """余浩:
    
    """
  
    danwei_id = schema.Int(
            title=_(u"foreagn key link to danwei"),
        ) 
    danwei = schema.Object(
            title=_(u"dan wei"),
            schema=IDanWei,
        )
    

class YiSheng(Person):
    """many to one:
    多端放外键及关系
    """
    
    implements(IYiSheng)    
    __tablename__ = 'yisheng'

    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    danwei_id = Column(Integer, ForeignKey('danwei.id'))
    danwei = relationship("DanWei", backref="yishengs")
    __mapper_args__ = {
        'polymorphic_identity':'yisheng',
    }    
       
        
###病人
class IBingRen(IPerson):
    """病人:
    
    """
   
    dizhi_id = schema.Int(
            title=_(u"foreagn key link to wei"),
        )
    dizhi = schema.Object(
            title=_(u"di zhi"),
            schema=IDiZhi,
        )
    
    

class BingRen(Person):
    
    implements(IBingRen)    
    __tablename__ = 'bingren'

    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    dizhi_id = Column(Integer, ForeignKey('gerendizhi.id'))
    dizhi = relationship("GeRenDiZhi", uselist=False)
    
    # association proxy of "chufangs" collection
    # to "chufang" attribute of ChuFang_BingRen CLASS's object
    chufangs = association_proxy('chufangs_bingren', 'chufang')    
    
    __mapper_args__ = {
        'polymorphic_identity':'bingren',
    }             
        
        
 ###处方和病人关联表
class ChuFang_BingRen_Asso(Base):
    __tablename__ = 'chufang_bingren'
    
    bingren_id = Column(Integer, ForeignKey('bingren.id'), primary_key=True)
    chufang_id = Column(Integer, ForeignKey('chufang.id'), primary_key=True)
    shijian = Column(DateTime, default=func.now())
    #脉象
    maixiang = Column(String(64))
    #舌相
    shexiang = Column(String(64))
    #主诉
    zhusu = Column(String(64))
     
    # bidirectional attribute/collection of "bingren"/"chufang_bingren"
    bingren = relationship(BingRen,lazy='subquery',
                backref=backref("chufangs_bingren",lazy='subquery',
                                cascade="all, delete-orphan")
            )
    # bidirectional attribute/collection of "chufang"/"chufang_bingren"
    chufang = relationship(ChuFang,lazy='subquery',
                backref=backref("chufang_bingrens",lazy='subquery',
                                cascade="all, delete-orphan")
            )    
#     # reference to the "ChuFang" object
#     chufang = relationship("ChuFang")

    def __init__(self, bingren=None, chufang=None, shijian=None,
                  maixiang=None, shexiang=None, zhusu=None):
        self.bingren = bingren
        self.chufang = chufang
        self.shijian = shijian
        self.maixiang = maixiang
        self.shexiang = shexiang
        self.zhusu = zhusu

                
                   