from django.test.testcases import TestCase
from testapp.models import NoCustomFieldsTree


class ManagerTestCase(TestCase):
    '''
    Tests that use the Manager and QuerySet methods.
    Testing tree:

                                Top
                             /   |  \
                     Science Hobbies Collections
                         /       |              \
                Astronomy   Amateurs_Astronomy Pictures
                   /  \                            |
        Astrophysics  Cosmology                Astronomy
                                                /  |    \
                                         Galaxies Stars Astronauts

    http://www.postgresql.org/docs/9.4/static/ltree.html
    '''
    @classmethod
    def setUpTestData(cls):
        paths = ['Top',
                 'Top.Science',
                 'Top.Science.Astronomy',
                 'Top.Science.Astronomy.Astrophysics',
                 'Top.Science.Astronomy.Cosmology',
                 'Top.Hobbies',
                 'Top.Hobbies.Amateurs_Astronomy',
                 'Top.Collections',
                 'Top.Collections.Pictures',
                 'Top.Collections.Pictures.Astronomy',
                 'Top.Collections.Pictures.Astronomy.Stars',
                 'Top.Collections.Pictures.Astronomy.Galaxies',
                 'Top.Collections.Pictures.Astronomy.Astronauts']
        for path in paths:
            NoCustomFieldsTree.objects.create(_path=path)

    def test_001_get_children(self):
        '''
        Manager get_children().
        '''
        # only one node
        src = NoCustomFieldsTree.objects.get(_path='Top')
        qs = src.get_children()

        self.assertEqual(set([src._path]),
                         set(['Top']))
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Science',
                              'Top.Hobbies',
                              'Top.Collections']))

        # several nodes
        src = NoCustomFieldsTree.objects.filter(_path__nlevel=3)
        qs = src.get_children()

        self.assertEqual(set(src.values_list('_path', flat=True)),
                         set(['Top.Science.Astronomy',
                              'Top.Hobbies.Amateurs_Astronomy',
                              'Top.Collections.Pictures']))
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Science.Astronomy.Astrophysics',
                              'Top.Science.Astronomy.Cosmology',
                              'Top.Collections.Pictures.Astronomy']))

    def test_002_get_descendants(self):
        '''
        Manager get_descendants().
        '''
        # only one node
        src = NoCustomFieldsTree.objects.get(_path='Top.Science')
        qs = src.get_descendants()

        self.assertEqual(set([src._path]),
                         set(['Top.Science']))
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Science.Astronomy',
                              'Top.Science.Astronomy.Astrophysics',
                              'Top.Science.Astronomy.Cosmology']))

        # several nodes
        src = NoCustomFieldsTree.objects.filter(_path__path_like='*.Astronomy')
        qs = src.get_descendants()

        self.assertEqual(set(src.values_list('_path', flat=True)),
                         set(['Top.Science.Astronomy',
                              'Top.Collections.Pictures.Astronomy']))
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Science.Astronomy.Astrophysics',
                              'Top.Science.Astronomy.Cosmology',
                              'Top.Collections.Pictures.Astronomy.Stars',
                              'Top.Collections.Pictures.Astronomy.Galaxies',
                              'Top.Collections.Pictures.Astronomy.Astronauts'])
                         )

    def test_003_get_ascendants(self):
        '''
        Manager get_ascendant().
        '''
        # only one node
        src = NoCustomFieldsTree.objects.get(
            _path='Top.Collections.Pictures.Astronomy.Astronauts')
        qs = src.get_ascendants()

        self.assertEqual(set([src._path]),
                         set(['Top.Collections.Pictures.Astronomy.Astronauts'])
                         )
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top',
                              'Top.Collections',
                              'Top.Collections.Pictures',
                              'Top.Collections.Pictures.Astronomy']))

        # several nodes
        src = NoCustomFieldsTree.objects.filter(_path__nlevel=2)
        qs = src.get_ascendants()

        self.assertEqual(set(src.values_list('_path', flat=True)),
                         set(['Top.Science',
                              'Top.Hobbies',
                              'Top.Collections']))
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top']))

    def test_004_get_siblings(self):
        '''
        Manager get_siblings().
        '''
        # only one node
        src = NoCustomFieldsTree.objects.get(_path='Top.Collections')
        qs = src.get_siblings()

        self.assertEqual(set([src._path]),
                         set(['Top.Collections']))
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Science',
                              'Top.Hobbies']))

        # several nodes
        src = NoCustomFieldsTree.objects.filter(_path__path_like='*.Stars')
        qs = src.get_siblings()

        self.assertEqual(set(src.values_list('_path', flat=True)),
                         set(['Top.Collections.Pictures.Astronomy.Stars']))
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Collections.Pictures.Astronomy.Galaxies',
                              'Top.Collections.Pictures.Astronomy.Astronauts'])
                         )
