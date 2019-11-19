#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema
from plone.autoform import directives as form

from z3c.form.browser.checkbox import CheckBoxFieldWidget
from cms.db.orm import IYao
from cms.db.orm import IDanWei
from cms.db.orm import IYiSheng
from cms.db.orm import IBingRen
from cms.db.orm import IYaoXing
from cms.db.orm import IJingLuo
from cms.db.orm import IChuFang
from cms.db import _
         

class InputError(Exception):
    """Exception raised if there is an error making a data input
    """

# db table add,modify interfaces

class IChuFangUI (IChuFang):
    """chufang table editing ui """

    yisheng = schema.Choice(
            title=_(u"yi sheng"),
            vocabulary='cms.db.yisheng',
            required=True,
        )


class IBingRenUI (IBingRen):
    """yisheng table editing ui """

    dizhi = schema.Choice(
            title=_(u"di zhi"),
            vocabulary='cms.db.dizhi',
            required=True,
        )
    
    
class IYiShengUI (IYiSheng):
    """yisheng table editing ui """

    danwei = schema.Choice(
            title=_(u"dan wei"),
            vocabulary='cms.db.danwei',
            required=True,
        )
    
    
class IDanWeiUI (IDanWei):
    """danwei table editing ui """

    dizhi = schema.Choice(
            title=_(u"di zhi"),
            vocabulary='cms.db.dizhi',
            required=True,
        )
    
class IYaoUI (IYao):
    """yao table ui """

    yaowei = schema.Choice(
            title=_(u"yao wei"),
            vocabulary='cms.db.yaowei',
            required=True,
        )
    yaoxing = schema.Choice(
            title=_(u"yao xing"),
            vocabulary='cms.db.yaoxing',
            required=True,
        )        

#     form.widget(guijing=CheckBoxFieldWidget)
    guijing = schema.List(title=_(u"gui jing"),
                               description=_(u"gui jing"),
                               required=True,
                               value_type=schema.Choice(vocabulary='cms.db.jingluo'),
                               )        
