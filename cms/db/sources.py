from z3c.formwidget.query.interfaces import IQuerySource
from zope.interface import Interface, implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import queryUtility
from cms.db.interfaces import IDbapi
from cms.db.browser.utility import getYaoShuliang


@implementer(IQuerySource)
class YaoSource(object):
    def __init__(self, context):
        self.context = context
        locator = queryUtility(IDbapi, name='yao')
        size = getYaoShuliang()
        values = locator.query({'start':0,'size':size,'SearchableText':'','sort_order':'reverse'})
        self.vocab = SimpleVocabulary(
            [SimpleTerm(value=int(i[0]), token=str(i[0]), title=i[3]) for i in values],
        )
        self.items = [(i[0],i[3],) for i in values]
        
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
#         import pdb
#         pdb.set_trace()
        return [self.getTerm(kw[0]) for kw in self.items if q in kw[1].lower()]

    
@implementer(IContextSourceBinder)
class YaoSourceBinder(object):

    def __call__(self, context):
        return YaoSource(context)

