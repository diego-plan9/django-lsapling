from django.db.models import Lookup, Transform, IntegerField


class ArrayLookup(Lookup):
    '''
    Utility class for providing array-based versions of the operators.
    '''
    using_values = False
    cast = ''  # used for forcing casting of the arrays

    def __init__(self, lhs, rhs):
        from models import TreeQuerySet
        # retrieve the paths if using a queryset as rhs
        if isinstance(rhs, TreeQuerySet):
            if '_overridden_path' in rhs.query.annotation_select.keys():
                rhs = rhs.values('_overridden_path')
            else:
                rhs = rhs.values('_path')
            self.using_values = True
        super(ArrayLookup, self).__init__(lhs, rhs)

    def as_postgresql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        # force the subquery to array() if needed
        if not self.using_values:
            params = lhs_params + rhs_params
            return '%s %s %s' % (lhs, self.sql_operator, rhs), params
        else:
            params = lhs_params + list(rhs_params)
            return '%s %s array(%s)%s' % \
                (lhs, self.sql_operator, rhs, self.cast), params


class LtreeAscendant(ArrayLookup):
    '''
    ltree @> ltree
    boolean    is left argument an ancestor of right (or equal)?
    ltree @> ltree[]
    boolean    does array contain a descendant of ltree?
    '''
    lookup_name = 'ascendant'
    sql_operator = '@>'


class LtreeDescendant(ArrayLookup):
    '''
    ltree <@ ltree
    boolean    is left argument a descendant of right (or equal)?
    ltree <@ ltree[]
    boolean    does array contain an ancestor of ltree?
    '''
    lookup_name = 'descendant'
    sql_operator = '<@'


class LtreePathLike(Lookup):
    '''
    ltree ~ lquery
    boolean    does ltree match lquery?
    '''
    lookup_name = 'path_like'

    def as_postgresql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s ~ %s' % (lhs, rhs), params


class LtreePathLikeTxt(Lookup):
    '''
    ltree @ ltxtquery
    boolean    does ltree match ltxtquery?
    '''
    lookup_name = 'path_like_txt'

    def as_postgresql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s @ %s' % (lhs, rhs), params


class LtreePathLikeExact(ArrayLookup):
    lookup_name = 'path_like_exact'
    sql_operator = '?'
    cast = '::lquery[]'


class LtreeNlevel(Transform):
    '''
    nlevel(ltree)
    integer    number of labels in path     nlevel('Top.Child1.Child2')     3
    '''
    lookup_name = 'nlevel'
    # bilateral = True

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return 'nlevel(%s)' % lhs, params

    def relabeled_clone(self, relabels):
        '''
        Try to fix:
        https://code.djangoproject.com/ticket/23548
        '''
        return self.__class__(self.lhs.relabeled_clone(relabels),
                              self.init_lookups)

    @property
    def output_field(self):
        return IntegerField()
