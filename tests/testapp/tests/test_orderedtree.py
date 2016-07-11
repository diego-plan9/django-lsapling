from django.test.testcases import TestCase
from lsapling.ordering.generic import POSITIONS

from testapp.models import NoCustomFieldsOrderedTree


class OrderedTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_001_order_upstream(self):
        '''
        Build the example tree out of order, using the model add_child() and
        add_sibling() methods to represent the original order.
                                Top
                             /   |  \
                     Science Hobbies Collections
                         /       |              \
                Astronomy   Amateurs_Astronomy Pictures
                   /  \                            |
        Astrophysics  Cosmology                Astronomy
                                                /  |    \
                                         Galaxies Stars Astronauts
        '''
        # order by default is: nlevel, _path, _position
        expected = []
        # level 0
        top = NoCustomFieldsOrderedTree.objects.add_root()
        expected += [top]
        # level 1
        hobbies = top.add_child()
        collections = top.add_child(position=POSITIONS.LAST)
        science = top.add_child(position=POSITIONS.FIRST)
        expected += [science, hobbies, collections]
        # level 2
        pictures = collections.add_child()
        amateurs_astronomy = hobbies.add_child()
        astronomy = science.add_child()
        expected += [astronomy, amateurs_astronomy, pictures]
        # level 3
        astrophysics = astronomy.add_child()
        cosmology = astronomy.add_child(position=POSITIONS.LAST)
        astronomy2 = pictures.add_child()
        expected += [astrophysics, cosmology, astronomy2]
        # level 4
        astronauts = astronomy2.add_child()
        galaxies = astronauts.add_sibling(position=POSITIONS.LEFT)
        stars = galaxies.add_sibling(position=POSITIONS.RIGHT)
        expected += [galaxies, stars, astronauts]

        self.assertSequenceEqual(expected,
                                 NoCustomFieldsOrderedTree.objects.all())

    def test_002_random_siblings(self):
        '''
        Append a bunch of siblings randomly.
        '''
        from random import seed
        from random import choice

        root = NoCustomFieldsOrderedTree.objects.add_root()
        expected = [root.add_child()]

        # populate tree, keep track on expected
        seed(123321)
        for _ in range(100):
            position = choice([POSITIONS.FIRST,
                               POSITIONS.LAST,
                               POSITIONS.LEFT,
                               POSITIONS.RIGHT])
            sibling = choice(expected)
            new_node = sibling.add_sibling(position=position)
            if position == POSITIONS.FIRST:
                expected = [new_node] + expected
            elif position == POSITIONS.LAST:
                expected = expected + [new_node]
            elif position == POSITIONS.LEFT:
                expected.insert(expected.index(sibling), new_node)
            elif position == POSITIONS.RIGHT:
                expected.insert(expected.index(sibling)+1, new_node)

        # check both lists
        self.assertSequenceEqual(expected, root.get_children())
        # check positions individually
        for a, b in zip(root.get_children(), root.get_children()[1:]):
            self.assertLess(a._position, b._position)
