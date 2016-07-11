from django.db.models import Func, Value


class Subpath(Func):
    function = 'SUBPATH'

    def __init__(self, expression, pos, length=None, **extra):
        """
        expression: the name of a field, or an expression returning a string
        pos: an integer > 0, or an expression returning an integer
        length: an optional number of characters to return
        """
        if not hasattr(pos, 'resolve_expression'):
            if pos < -2:
                raise ValueError("'pos' must be greater than -1")
            pos = Value(pos)
        expressions = [expression, pos]
        if length is not None:
            if not hasattr(length, 'resolve_expression'):
                length = Value(length)
            expressions.append(length)
        super(Subpath, self).__init__(*expressions, **extra)


class Nlevel(Func):
    function = 'NLEVEL'
