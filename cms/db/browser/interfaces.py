#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema
from cms.db.orm import IYao
from cms.db.orm import IYaoXing
from cms.db.orm import IJingLuo
from cms.db import _

 
         

class InputError(Exception):
    """Exception raised if there is an error making a data input
    """

# db table add,modify interfaces
class IYaoUI (IYao):
    """yao table ui """

    yaowei = schema.Choice(
            title=_(u"gui jing"),
            vocabulary='cms.db.vocabulary.yao_wei',
            required=True,
        )
    yaoxing = schema.Choice(
            title=_(u"gui jing"),
            vocabulary='cms.db.vocabulary.yao_xing',
            required=True,
        )        
    guijing = schema.Choice(
            title=_(u"gui jing"),
            vocabulary='cms.db.vocabulary.jingluo_mingcheng',
            required=True,
        )
        
