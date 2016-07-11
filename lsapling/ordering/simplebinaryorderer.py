from generic import BaseOrdererAdapter, POSITIONS


class SimpleBinaryOrdererAdapter(BaseOrdererAdapter):
    def get_backend(self):
        return SimpleBinaryOrderer()

    def get_position_sibling(self, siblings, position=POSITIONS.RIGHT):
        return self.backend.get_position_sibling(siblings, position)


class SimpleBinaryOrderer(object):
    '''
    Orderer implementing a simple binary partition of the available space. When
    a new node is to be inserted, the position is set to the middle of the
    available space delimited by their left and right siblings.
    '''
    NUM_SLOTS = 16
    CHAR_SIZE = 16  # 0..f
    MAX_POS = CHAR_SIZE ** NUM_SLOTS
    NODE_MAPPER = {POSITIONS.FIRST: ([],        [0, 1, 2]),
                   POSITIONS.LAST:  ([2, 1, 0], []),
                   POSITIONS.LEFT:  ([0],       [1, 2]),
                   POSITIONS.RIGHT: ([1, 0],    [2])}

    def __init__(self):
        pass

    def get_position_sibling(self, siblings, position):
        min_indexes, max_indexes = self.NODE_MAPPER[position]

        # iterate over the nodes to find the min and max positions
        min_position = 0
        max_position = self.MAX_POS
        for node in [siblings[x] for x in min_indexes]:
            if node:
                min_position = int(node._position, self.CHAR_SIZE)
                break
        for node in [siblings[x] for x in max_indexes]:
            if node:
                max_position = int(node._position, self.CHAR_SIZE)
                break

        # calculate the new position
        new_position = min_position + (max_position - min_position) / 2
        return '%%0%sx' % self.NUM_SLOTS % new_position
