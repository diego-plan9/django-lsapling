from django.db import models
import lookups


class NodePathField(models.Field):
    def db_type(self, connection):
        return 'ltree'

    def __init__(self, *args, **kwargs):
        super(NodePathField, self).__init__(*args, **kwargs)

NodePathField.register_lookup(lookups.LtreeAscendant)
NodePathField.register_lookup(lookups.LtreeDescendant)
NodePathField.register_lookup(lookups.LtreePathLike)
NodePathField.register_lookup(lookups.LtreePathLikeTxt)
NodePathField.register_lookup(lookups.LtreePathLikeExact)

NodePathField.register_lookup(lookups.LtreeNlevel)
