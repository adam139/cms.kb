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


@implementer(IYaoUI)
class YaoUI(object):
    mingcheng = FieldProperty(IYaoUI['mingcheng'])
    zhuzhi = FieldProperty(IYaoUI['zhuzhi'])        
    yaowei = FieldProperty(IYaoUI['yaowei'])
    yaoxing = FieldProperty(IYaoUI['yaoxing'])
    guijing = FieldProperty(IYaoUI['guijing'])
    # allow getSource to proceed
    _Modify_portal_content_Permission = ('Anonymous', )

    def __init__(self, mingcheng=None, zhuzhi=None, yaowei=None, yaoxing=None, guijing=None):
        self.mingcheng = mingcheng
        self.zhuzhi = zhuzhi
        self.yaowei = yaowei
        self.yaoxing = yaoxing
        self.guijing = guijing


                