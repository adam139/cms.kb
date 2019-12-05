#-*- coding: UTF-8 -*-
from zope import schema
from plone.directives import form, dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives

from collective import dexteritytextindexer
from collective.dexteritytextindexer.behavior import IDexterityTextIndexer

from emc.db import _
    
class IYisheng(form.Schema):
    """
    CMS yisheng content type
    """
#标准名称
    dexteritytextindexer.searchable('title')    
    title = schema.TextLine(title=_(u"yisheng xingming"),
            required=True)

    form.widget(text="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    description = schema.Text(
        title=_(u"yisheng jianjie"),
        required=True)
#     form.widget(sendto=AutocompleteMultiFieldWidget)    
#     sendto = schema.Tuple(
#         title=_(u"send to"),
#         value_type=schema.TextLine(),
#         required=True,
#         missing_value=(), # important!
#     )           
#     directives.widget(
#         'sendto',
#         AjaxSelectFieldWidget,
#         vocabulary='plone.principalsource.Users'
#     )
@form.validator(field=IYisheng['description'])
def maxSize(value):
    if value is not None:
        if len(value)/1024 > 128:
            raise schema.ValidationError(_(u"message text must be smaller than 128KB"))
 
