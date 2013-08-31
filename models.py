from minimongo import Model, Index, configure

configure(host=u'paulo.mongohq.com', port=10067, user=u"emhs08@gmail.com", pass=u'dea84638ime', database='Exhumator')

class Source(Model):
    class Meta:
        collection="sources"

