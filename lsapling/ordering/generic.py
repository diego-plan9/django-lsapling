# valid positions for insertion of a node
FIRST = 'first'
LAST = 'last'
LEFT = 'left'
RIGHT = 'right'


class POSITIONS(object):
    FIRST = FIRST
    LAST = LAST
    LEFT = LEFT
    RIGHT = RIGHT


class BaseOrdererAdapter(object):
    '''
    Base adapter for an Orderer.
    '''
    def __init__(self):
        self.backend = self.get_backend()

    def get_position_sibling(self, siblings, position=RIGHT):
        '''
        Get the positional value where a sibling would be inserted.

        @param siblings: iterator of the existing siblings (left, current,
            right), ordered by position.
        @param position: position where the sibling should be inserted,
            relative to the current node.
        '''
        raise NotImplementedError
