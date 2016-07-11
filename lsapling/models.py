from django.db import models
from django.db.models.expressions import F
from django.db.models.functions import Concat, Value

from fields import NodePathField
from functions import Subpath, Nlevel
from ordering.generic import POSITIONS
from settings import LSAPLING_ORDERER_ADAPTER

# ascii-art constants
DT_CORNER, DT_LINE_VER, DT_LINE_HOR, DT_LINE_VER_CONT = (u'\u2514',
                                                         u'\u2502',
                                                         u'\u2500',
                                                         u'\u251c')


class TreeQuerySet(models.QuerySet):
    def get_ascendants(self):
        '''
        Return all the node's ascendants. The node is excluded.
        '''
        return self.model.objects.filter(_path__ascendant=self.all()).\
            exclude(pk__in=self.all())
    # get_ascendants.queryset_only = True

    def get_children(self):
        '''
        Return the node's immediate children.
        '''
        parent_paths = self.annotate(_overridden_path=Concat('_path',
                                                             Value('.*{1}')))
        return self.model.objects.filter(_path__path_like_exact=parent_paths)
    # get_children.queryset_only = True

    def get_descendants(self):
        '''
        Return all the node's descendants (children and descendants of their
        children). The node is excluded.
        '''
        return self.model.objects.filter(_path__descendant=self.all()).\
            exclude(pk__in=self.all())
    # get_descendants.queryset_only = True

    def get_siblings(self):
        '''
        Return all the node's siblings. The node is excluded.
        '''
        parent_paths = self.annotate(_overridden_path=Concat(
                                     Subpath(F('_path'),
                                             0,
                                             Nlevel(F('_path'))-1),
                                     Value('.*{1}'))
                                     )
        return self.model.objects.filter(_path__path_like_exact=parent_paths).\
            exclude(pk__in=self.all())
    # get_sibling.queryset_only = True


class Tree(models.Model):
    _path = NodePathField()
    objects = TreeQuerySet.as_manager()

    def get_ascendants(self):
        return self.__class__.objects.filter(pk=self.pk).get_ascendants()

    def get_children(self):
        return self.__class__.objects.filter(pk=self.pk).get_children()

    def get_descendants(self):
        return self.__class__.objects.filter(pk=self.pk).get_descendants()

    def get_siblings(self):
        return self.__class__.objects.filter(pk=self.pk).get_siblings()

    def pretty_print(self, last=False, pre=[]):
        '''
        Pretty print the node and its descendants.
        '''
        ret = ''
        label = unicode(self)

        # calculate pres
        if len(pre) == 0:
            ret += label
        else:
            pres = [(DT_LINE_VER if x else u' ') + u' '*3 for x in pre]
            pres_str = u''.join(pres[:-1])
            ret += pres_str + (DT_CORNER if last else DT_LINE_VER_CONT) +\
                DT_LINE_HOR*3 + label

        children = list(self.get_children())
        for child in children:
            last = child == children[-1]

            ret += '\n' + child.pretty_print(last, pre + [not last])

        return ret

    def __unicode__(self):
        return '[%s] %s' % (self.pk, self._path)

    class Meta:
        abstract = True


class OrderedTreeQuerySet(TreeQuerySet):
    '''
    Ordered SaplingTree.
    '''
    def __init__(self, *args, **kwargs):
        from importlib import import_module
        # load the ordering adapter based on configuration
        package, klass = str(LSAPLING_ORDERER_ADAPTER).rsplit('.', 1)
        module = import_module(package)
        self.orderer = getattr(module, klass)()

        super(OrderedTreeQuerySet, self).__init__(*args, **kwargs)

    def add_root(self, *args, **kwargs):
        '''
        Add a root node.
        '''
        # TODO: check alternatives for UNION support in django
        right = self.model.objects.filter(_path__nlevel=1).\
            order_by('-_position').first()
        new_position = self.orderer.get_position_sibling([None, right, None])
        new_node = self.create(_path=new_position,
                               _position=new_position,
                               *args,
                               **kwargs)
        return new_node

    def add_sibling(self, current, position=POSITIONS.RIGHT, *args, **kwargs):
        '''
        Add a sibling.
        '''
        # TODO: check alternatives for UNION support in django
        left = current.get_siblings().filter(_position__lt=current._position).\
            order_by('-_position')
        right = current.get_siblings().filter(_position__gt=current._position).\
            order_by('_position')
        # automatically correct FIRST and LAST cases
        if position == POSITIONS.FIRST:
            left = current.get_siblings().order_by('_position')
        elif position == POSITIONS.LAST:
            right = current.get_siblings().order_by('-_position')

        new_position = self.orderer.get_position_sibling([left.first(),
                                                          current,
                                                          right.first()],
                                                         position)
        new_node = self.create(_path=current._path.rsplit('.', 1)[0]
                               + '.' + new_position,
                               _position=new_position)
        return new_node

    def add_child(self, parent, position=POSITIONS.RIGHT, *args, **kwargs):
        '''
        Add a child.
        '''
        # TODO: check alternatives for UNION support in django
        left = parent.get_children().order_by('_position')
        right = parent.get_children().order_by('-_position')
        new_position = self.orderer.get_position_sibling([left.first(),
                                                          None,
                                                          right.first()],
                                                         position)
        new_node = self.create(_path=parent._path + '.' + new_position,
                               _position=new_position,
                               *args,
                               **kwargs)
        return new_node


class OrderedTree(Tree):
    '''
    Ordered SaplingTree:
    - _path is automatically populated based on the pk.
    - _position is automatically populated.
    '''
    _position = models.CharField(max_length=64,
                                 db_index=True)
    objects = OrderedTreeQuerySet.as_manager()

    def add_child(self, position=POSITIONS.LAST, *args, **kwargs):
        # TODO: raise exception on RIGHT, LEFT - here or on manager?
        return self.__class__.objects.add_child(parent=self,
                                                position=position,
                                                *args,
                                                **kwargs)

    def add_sibling(self, position=POSITIONS.RIGHT, *args, **kwargs):
        return self.__class__.objects.add_sibling(current=self,
                                                  position=position,
                                                  *args,
                                                  **kwargs)

    def __unicode__(self):
        return '[%s] %s %s' % (self.pk, self._path, self._position)

    class Meta:
        abstract = True
        # TODO: provide method that keeps the nlevel ordering at least
        ordering = [Nlevel('_path'), '_path', '_position']

#     class Meta:
#         unique_together = ('_path', '_position',)
#         TODO: unique between (path[-1], position)
