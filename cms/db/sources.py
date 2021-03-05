from z3c.formwidget.query.interfaces import IQuerySource
from zope.interface import Interface, implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import queryUtility
from cms.db.interfaces import IDbapi

from cms.db.browser.utility import getDanWeiId
from cms.db.orm import Yao_DanWei_Asso
from cms.db.orm import Yao


@implementer(IQuerySource)
class Source(object):
    def __init__(self, context):
        self.context = context
        values = {1:_(u'nan'),0:_(u'nv')}
        self.vocab =  SimpleVocabulary(
        [SimpleTerm(value=int(i), token=str(i), title=values[i]) for i in values.keys()],)
        self.items = [(int(i),values[i],) for i in values.keys()]
        
    def __contains__(self, term):
        return self.vocab.__contains__(term)

    def __iter__(self):
        return self.vocab.__iter__()

    def __len__(self):
        return self.vocab.__len__()

    def getTerm(self, value):
        return self.vocab.getTerm(value)

    def getTermByToken(self, value):
        return self.vocab.getTermByToken(value)

    def search(self, query_string):
        q = query_string.lower()
        return [self.getTerm(kw[0]) for kw in self.items if q in kw[1].lower()]


@implementer(IQuerySource)
class YaoSource(Source):
    def __init__(self, context):
        self.context = context
        locator = queryUtility(IDbapi, name='yao')
        daiweiid = getDanWeiId()
        # all_a_except_b(self,a_cls,b_cls,b_a_fk,b_id,pk)
        values = locator.all_a_except_b(Yao,Yao_DanWei_Asso,"yao_id","danwei_id",daiweiid)
        self.vocab = SimpleVocabulary(
            [SimpleTerm(value=int(i.id), token=str(i.id), title=i.mingcheng) for i in values],
        )
        self.items = [(i.id,i.mingcheng,) for i in values]
        
        
@implementer(IContextSourceBinder)
class YaoSourceBinder(object):

    def __call__(self, context):
        return YaoSource(context)


@implementer(IQuerySource)
class WoyaoSource(Source):
    def __init__(self, context):
        self.context = context
        locator = queryUtility(IDbapi, name='yao')
        query = {'start':0,'size':0,'SearchableText':'','sort_order':'reverse'}
        values = locator.multi_query(query,Yao_DanWei_Asso,'yao_danwei','danwei_id',getDanWeiId(),'id','yao_id')
        self.vocab = SimpleVocabulary(
            [SimpleTerm(value=int(i[0]), token=str(i[0]), title=i[3]) for i in values],
        )
        self.items = [(i[0],i[3],) for i in values]
        
        
@implementer(IContextSourceBinder)
class WoyaoSourceBinder(object):

    def __call__(self, context):
        return WoyaoSource(context)


@implementer(IQuerySource)
class BingrenSource(Source):
    def __init__(self, context):
        self.context = context
        locator = queryUtility(IDbapi, name='bingren')
        values = locator.query({'start':0,'size':0,
                            'SearchableText':'',
                            'sort_order':'reverse',
                            'with_entities':0})
        self.vocab = SimpleVocabulary(
            [SimpleTerm(value=int(i.id), token=str(i.id), title=i.xingming) for i in values],
        )
        self.items = [(i.id,i.xingming,) for i in values]


@implementer(IContextSourceBinder)
class BingrenSourceBinder(object):

    def __call__(self, context):
        return BingrenSource(context)