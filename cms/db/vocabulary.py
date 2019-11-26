# -*- coding: utf-8 -*-
from zope.interface import provider
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from cms.db.interfaces import IDbapi
from cms.db import _


@provider(IVocabularyFactory)
def xingbie(context):

    values = {1:_(u'nan'),0:_(u'nv')}
    return SimpleVocabulary(
        [SimpleTerm(value=int(i), token=str(i), title=values[i]) for i in values.keys()],
    )


@provider(IVocabularyFactory)
def bingren(context):
  
    locator = queryUtility(IDbapi, name='bingren')

    values = locator.query({'start':0,'size':1000,'SearchableText':'','sort_order':'reverse'})

    return SimpleVocabulary(
        [SimpleTerm(value=int(i[0]), token=str(i[0]), title=i[2]+i[5]) for i in values],
    )

@provider(IVocabularyFactory)
def yao(context):
  
    locator = queryUtility(IDbapi, name='yao')

    values = locator.query({'start':0,'size':300,'SearchableText':'','sort_order':'reverse'})

    return SimpleVocabulary(
        [SimpleTerm(value=int(i[0]), token=str(i[0]), title=i[3]) for i in values],
    )

@provider(IVocabularyFactory)
def danwei(context):
  
    locator = queryUtility(IDbapi, name='danwei')

    values = locator.query({'start':0,'size':100,'SearchableText':'','sort_order':'reverse'})

    return SimpleVocabulary(
        [SimpleTerm(value=int(i[0]), token=str(i[0]), title=i[2]) for i in values],
    )

@provider(IVocabularyFactory)
def yisheng(context):
  
    locator = queryUtility(IDbapi, name='yisheng')

    values = locator.query({'start':0,'size':100,'SearchableText':'','sort_order':'reverse'})

    return SimpleVocabulary(
        [SimpleTerm(value=int(i[0]), token=str(i[0]), title=i[2]) for i in values],
    )

@provider(IVocabularyFactory)
def dizhi(context):
  
    locator = queryUtility(IDbapi, name='dizhi')

    values = locator.query({'start':0,'size':100,'SearchableText':'','sort_order':'reverse'})

    return SimpleVocabulary(
        [SimpleTerm(value=int(i[0]), token=str(i[0]), title=i[3]+i[4]) for i in values],
    )
    
@provider(IVocabularyFactory)
def yao_wei(context):
  
    locator = queryUtility(IDbapi, name='yaowei')

    values = locator.query({'start':0,'size':10,'SearchableText':'','sort_order':'reverse'})

    return SimpleVocabulary(
        [SimpleTerm(value=int(i[0]), token=str(i[0]), title=i[1]) for i in values],
    )

@provider(IVocabularyFactory)
def yao_xing(context):
  
    locator = queryUtility(IDbapi, name='yaoxing')

    values = locator.query({'start':0,'size':15,'SearchableText':'','sort_order':'reverse'})
    return SimpleVocabulary(
        [SimpleTerm(value=int(i[0]), token=str(i[0]), title=i[1]) for i in values],
    )
    
@provider(IVocabularyFactory)
def jingluo_mingcheng(context):
  
    locator = queryUtility(IDbapi, name='jingluo')

    values = locator.query({'start':0,'size':12,'SearchableText':'','sort_order':'reverse'})
    return SimpleVocabulary(
        [SimpleTerm(value=int(i[0]), token=str(i[0]), title=i[1]) for i in values],
    )    
        