#-*- coding: UTF-8 -*-
from zope.interface import Interface,implementer
import zope.interface
from zope.schema.fieldproperty import FieldProperty
from zope import schema
from plone.directives import form
# from plone.autoform import directives
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.autoform import directives as adirectives

from z3c.form.browser.checkbox import CheckBoxFieldWidget
from cms.db.orm import IYao
from cms.db.orm import IDanWei
from cms.db.orm import IYiSheng
from cms.db.orm import IBingRen
from cms.db.orm import IYaoXing
from cms.db.orm import IJingLuo
from cms.db.orm import IChuFang
from cms.db.orm import IYao_ChuFang_Asso
from cms.db.orm import IYao_DanWei_Asso
from cms.db import _


class YaoListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass


class BingRenListField(schema.List):
    """We need to have a unique class for the field list so that we
    can apply a custom adapter."""
    pass


class InputError(Exception):
    """Exception raised if there is an error making a data input
    """


## db table add,modify interfaces
class IYao_DanWei_AssoUI (IYao_DanWei_Asso):
    """yao_danwei association table editing ui """
    
    adirectives.widget(yao_id=AutocompleteFieldWidget)
    yao_id = schema.Choice(
            title=_(u"ming cheng"),
            vocabulary='cms.db.yao',
            required=True,
        )


class IChuFang_BingRen_AssoUI (Interface):
    """chufang_bingren association table editing ui """

    bingren_id = schema.Choice(
            title=_(u"bing ren"),
            vocabulary='cms.db.bingren',
            required=True,
        )          
    shijian = schema.Datetime(
            title=_(u"chu fang shi jian"),
            required=False,
        )    
    maixiang = schema.TextLine(
            title=_(u"mai xiang"),
        )
    shexiang = schema.TextLine(
            title=_(u"she xiang"),
            required=False,
        )
    zhusu = schema.TextLine(
            title=_(u"zhu su"),
        )        


class IYao_ChuFang_AssoUI (Interface):
    """yao chufang association table editing ui """

    yao_id = schema.Choice(
            title=_(u"ming cheng"),
            vocabulary='cms.db.wo_yao',
            required=True,
        )          
    yaoliang = schema.Int(
            title=_(u"yao liang"),
        )    
    paozhi = schema.TextLine(
            title=_(u"pao zhi"),
            required=False,
        )
 

class IChuFangUI (IChuFang):
    """chufang table editing ui """

    yisheng = schema.Choice(
            title=_(u"yi sheng"),
            vocabulary='cms.db.yisheng',
            required=True,
        )

    yaoes = YaoListField(title=_(u"yao qingdan"),
        value_type=schema.Object(title=_(u"yao qingdan data row"), schema=IYao_ChuFang_AssoUI),
        required=False,
        )   

    bingrens = BingRenListField(title=_(u"bing ren qingdan"),
        value_type=schema.Object(title=_(u"bing ren qing dan"), schema=IChuFang_BingRen_AssoUI),
        required=False,
        )
   


class IBingRenUI (IBingRen):
    """bingren table editing ui """

    dizhi = schema.Choice(
            title=_(u"di zhi"),
            vocabulary='cms.db.gerendizhi',
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

    form.widget(guijing=CheckBoxFieldWidget)
    guijing = schema.List(title=_(u"gui jing"),
                               description=_(u"gui jing"),
                               required=False,
                               value_type=schema.Choice(vocabulary='cms.db.jingluo'),
                               ) 
    
    
class IAutomaticTypesSettings(Interface):
    """A utility used to set CMSAI system 's automatic create content types list
    """
    
    types = schema.List(
            title=_(u"types"),
            description=_(u"automatic create content types list"),
            value_type=schema.Choice(vocabulary='plone.app.vocabularies.UserFriendlyTypes'),
            required=False,
        )
    danweiid = schema.Int(
            title=_(u"danwei id"),
            description=_(u"danwei id"),
            default=1,
            required=False,
        )


