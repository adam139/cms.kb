# -*- coding: utf-8 -*-
from zope.interface import provider
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from cms.db import _


@provider(IVocabularyFactory)
def xingbie(context):

    values = {1:_(u'nan'),0:_(u'nv')}
    return SimpleVocabulary(
        [SimpleTerm(value=int(i), token=str(i), title=values[i]) for i in values.keys()],
    )
    
@provider(IVocabularyFactory)
def yao_wei(context):
  
    locator = queryUtility(IDbapi, name='yaowei')

    values = locator.query({'start':0,'size':0,'SearchableText':'','sort_order':'reverse'})
    return SimpleVocabulary(
        [SimpleTerm(value=int(i.id), token=str(i.id), title=i.wei) for i in values],
    )

@provider(IVocabularyFactory)
def yao_xing(context):
  
    locator = queryUtility(IDbapi, name='yaoxing')

    values = locator.query({'start':0,'size':0,'SearchableText':'','sort_order':'reverse'})
    return SimpleVocabulary(
        [SimpleTerm(value=int(i.id), token=str(i.id), title=i.xing) for i in values],
    )
    
@provider(IVocabularyFactory)
def jingluo_mingcheng(context):
  
    locator = queryUtility(IDbapi, name='jingluo')

    values = locator.query({'start':0,'size':0,'SearchableText':'','sort_order':'reverse'})
    return SimpleVocabulary(
        [SimpleTerm(value=int(i.id), token=str(i.id), title=i.mingcheng) for i in values],
    )    
        