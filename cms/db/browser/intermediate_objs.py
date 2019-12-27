# -*- coding: utf-8 -*-
"""
   为跨表访问的编辑表单提供临时的中间对象,完成字段值到widget的转换,为getcontent() 
   提供对象数据.
"""
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import NO_VALUE
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zope.component import adapter
from zope.schema import getFieldsInOrder
from zope.schema.fieldproperty import FieldProperty

from cms.db.browser.interfaces import IYaoUI
from cms.db.browser.interfaces import IDanWeiUI
from cms.db.browser.interfaces import IChuFangUI
from cms.db.browser.interfaces import IBingRenUI
from cms.db.browser.interfaces import IYiShengUI
from cms.db.browser.interfaces import IChuFang_BingRen_AssoUI
from cms.db.browser.interfaces import IYao_ChuFang_AssoUI

@implementer(IBingRenUI)
class BingRenUI(object):
    xingming = FieldProperty(IBingRenUI['xingming'])
    xingbie = FieldProperty(IBingRenUI['xingbie'])
    shengri = FieldProperty(IBingRenUI['shengri'])
    dianhua = FieldProperty(IBingRenUI['dianhua']) 
    dizhi = FieldProperty(IBingRenUI['dizhi'])                
    # allow getSource to proceed
    _Modify_portal_content_Permission = ('Anonymous', )

    def __init__(self, xingming=None, xingbie=None, shengri=None, dianhua=None, dizhi=None):
        self.xingming = xingming
        self.xingbie = xingbie
        self.shengri = shengri
        self.dianhua = dianhua
        self.dizhi = dizhi

@implementer(IYiShengUI)
class YiShengUI(object):
    xingming = FieldProperty(IYiShengUI['xingming'])
    xingbie = FieldProperty(IYiShengUI['xingbie'])
    shengri = FieldProperty(IYiShengUI['shengri'])
    dianhua = FieldProperty(IYiShengUI['dianhua']) 
    danwei = FieldProperty(IYiShengUI['danwei'])                
    # allow getSource to proceed
    _Modify_portal_content_Permission = ('Anonymous', )

    def __init__(self, xingming=None, xingbie=None, shengri=None, dianhua=None, danwei=None):
        self.xingming = xingming
        self.xingbie = xingbie
        self.shengri = shengri
        self.dianhua = dianhua
        self.danwei = danwei                

@implementer(IDanWeiUI)
class DanWeiUI(object):
    mingcheng = FieldProperty(IDanWeiUI['mingcheng'])
    dizhi = FieldProperty(IDanWeiUI['dizhi'])        
    # allow getSource to proceed
    _Modify_portal_content_Permission = ('Anonymous', )

    def __init__(self, mingcheng=None, dizhi=None):
        self.mingcheng = mingcheng
        self.dizhi = dizhi


@implementer(IYaoUI)
class YaoUI(object):
    mingcheng = FieldProperty(IYaoUI['mingcheng'])
    zhuzhi = FieldProperty(IYaoUI['zhuzhi'])
    yongliang = FieldProperty(IYaoUI['yongliang'])
    danjia = FieldProperty(IYaoUI['danjia'])
    kucun = FieldProperty(IYaoUI['kucun'])        
    yaowei = FieldProperty(IYaoUI['yaowei'])
    yaoxing = FieldProperty(IYaoUI['yaoxing'])
    guijing = FieldProperty(IYaoUI['guijing'])
    # allow getSource to proceed
    _Modify_portal_content_Permission = ('Anonymous', )

    def __init__(self, mingcheng=None, zhuzhi=None, yongliang=None,
                 danjia=None, kucun=None, yaowei=None,
                  yaoxing=None, guijing=None):
        self.mingcheng = mingcheng
        self.zhuzhi = zhuzhi
        self.kucun = kucun
        self.danjia = danjia
        self.yongliang = yongliang
        self.yaowei = yaowei
        self.yaoxing = yaoxing
        self.guijing = guijing


@implementer(IChuFangUI)
class ChuFangUI(object):
    """temp edit obj"""
    
    mingcheng = FieldProperty(IChuFangUI['mingcheng'])
    yizhu = FieldProperty(IChuFangUI['yizhu'])
    jiliang = FieldProperty(IChuFangUI['jiliang'])        
    yisheng = FieldProperty(IChuFangUI['yisheng'])
    yaoes = FieldProperty(IChuFangUI['yaoes'])
    bingrens = FieldProperty(IChuFangUI['bingrens'])
    # allow getSource to proceed
    _Modify_portal_content_Permission = ('Anonymous', )

    def __init__(self, mingcheng=None, yizhu=None, jiliang=None, yisheng=None, yaoes=None, bingrens=None):
        self.mingcheng = mingcheng
        self.yizhu = yizhu
        self.jiliang = jiliang
        self.yisheng = yisheng
        self.yaoes = yaoes
        self.bingrens = bingrens


@implementer(IChuFang_BingRen_AssoUI)
class ChuFang_BingRen_AssoUI(object):

    bingren_id = FieldProperty(IChuFang_BingRen_AssoUI['bingren_id'])
    shijian = FieldProperty(IChuFang_BingRen_AssoUI['shijian'])
    maixiang = FieldProperty(IChuFang_BingRen_AssoUI['maixiang'])
    shexiang = FieldProperty(IChuFang_BingRen_AssoUI['shexiang'])
    zhusu = FieldProperty(IChuFang_BingRen_AssoUI['zhusu']) 


@implementer(IChuFang_BingRen_AssoUI)
class EditChuFang_BingRen_AssoUI(object):


    bingren_id = FieldProperty(IChuFang_BingRen_AssoUI['bingren_id'])
    shijian = FieldProperty(IChuFang_BingRen_AssoUI['shijian'])
    maixiang = FieldProperty(IChuFang_BingRen_AssoUI['maixiang'])
    shexiang = FieldProperty(IChuFang_BingRen_AssoUI['shexiang'])
    zhusu = FieldProperty(IChuFang_BingRen_AssoUI['zhusu'])    

    def __init__(self, bingren_id=None, shijian=None, maixiang=None,
                  shexiang=None, zhusu=None):
        self.bingren_id = bingren_id
        self.shijian = shijian
        self.maixiang = maixiang
        self.shexiang = shexiang
        self.zhusu = zhusu                        


@implementer(IYao_ChuFang_AssoUI)
class Yao_ChuFang_AssoUI(object):


    yao_id = FieldProperty(IYao_ChuFang_AssoUI['yao_id'])
    yaoliang = FieldProperty(IYao_ChuFang_AssoUI['yaoliang'])
    paozhi = FieldProperty(IYao_ChuFang_AssoUI['paozhi'])
    
@implementer(IYao_ChuFang_AssoUI)
class EditYao_ChuFang_AssoUI(object):


    yao_id = FieldProperty(IYao_ChuFang_AssoUI['yao_id'])
    yaoliang = FieldProperty(IYao_ChuFang_AssoUI['yaoliang'])
    paozhi = FieldProperty(IYao_ChuFang_AssoUI['paozhi'])
    
    def __init__(self, yao_id=None, yaoliang=None, paozhi=None):
        self.yao_id = yao_id
        self.yaoliang = yaoliang
        self.paozhi = paozhi



                                 