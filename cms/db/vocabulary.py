# -*- coding: utf-8 -*-
from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtility
from Chinese.medical.science import _


@provider(IVocabularyFactory)
def xingbie(context):

    values = {1:_(u'nan'),0:_(u'nv')}
    return SimpleVocabulary(
        [SimpleTerm(value=int(i), token=str(i), title=values[i]) for i in values.keys()],
    )
    
# @provider(IVocabularyFactory)
# def donateId(context):
#  
#     locator = getUtility(IDonateLocator)
# #     values = locator.query(start=0,size=100,multi=1,did=18,sortchildid=3)
#     values = locator.query(start=0,size=100,multi=1)
#     return SimpleVocabulary(
#         [SimpleTerm(value=int(i.did), token=str(i.did), title=i.aname) for i in values],
#     )