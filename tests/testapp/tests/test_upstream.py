from django.test.testcases import TestCase
from testapp.models import NoCustomFieldsTree


class UpstreamTestCase(TestCase):
    '''
    Tests that mimic the "Example" section on the official ltree documentation.
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

    def test_001_inheritance(self):
        '''
        Test descendants using the '@>' (is_descendant_of) operator.
        '''
        qs = NoCustomFieldsTree.objects.filter(_path__descendant='Top.Science')
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Science',
                              'Top.Science.Astronomy',
                              'Top.Science.Astronomy.Astrophysics',
                              'Top.Science.Astronomy.Cosmology']))

    def test_002_path_matching(self):
        '''
        Test path matching using the '~' (path_like) operator.
        '''
        qs = NoCustomFieldsTree.objects.filter(
            _path__path_like='*.Astronomy.*')
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Science.Astronomy',
                              'Top.Science.Astronomy.Astrophysics',
                              'Top.Science.Astronomy.Cosmology',
                              'Top.Collections.Pictures.Astronomy',
                              'Top.Collections.Pictures.Astronomy.Stars',
                              'Top.Collections.Pictures.Astronomy.Galaxies',
                              'Top.Collections.Pictures.Astronomy.Astronauts'])
                         )

        qs = NoCustomFieldsTree.objects.\
            filter(_path__path_like='*.!pictures@.*.Astronomy.*')
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Science.Astronomy',
                              'Top.Science.Astronomy.Astrophysics',
                              'Top.Science.Astronomy.Cosmology']))

    def test_003_path_matching_txt(self):
        '''
        Test path matching using the '@' (path_like_txt) operator.
        '''
        qs = NoCustomFieldsTree.objects.\
            filter(_path__path_like_txt='Astro*% & !pictures@')
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Science.Astronomy',
                              'Top.Science.Astronomy.Astrophysics',
                              'Top.Science.Astronomy.Cosmology',
                              'Top.Hobbies.Amateurs_Astronomy']))

        qs = NoCustomFieldsTree.objects.\
            filter(_path__path_like_txt='Astro* & !pictures@')
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Science.Astronomy',
                              'Top.Science.Astronomy.Astrophysics',
                              'Top.Science.Astronomy.Cosmology']))

    def test_004_chains(self):
        '''
        Test the chaining of some filters that were problematic
        '''
        # use queryset as ascendant query
        src = NoCustomFieldsTree.objects.filter(_path__nlevel=2)
        qs = NoCustomFieldsTree.objects.filter(_path__ascendant=src)

        self.assertEqual(set(src.values_list('_path', flat=True)),
                         set(['Top.Science',
                              'Top.Hobbies',
                              'Top.Collections']))
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top',
                              'Top.Science',
                              'Top.Hobbies',
                              'Top.Collections']))

        # chain some filters
        src = NoCustomFieldsTree.objects.filter(_path__nlevel=4,
                                                _path__path_like='*.Astronomy')
        qs = NoCustomFieldsTree.objects.filter(_path__descendant=src)
        self.assertEqual(set(src.values_list('_path', flat=True)),
                         set(['Top.Collections.Pictures.Astronomy']))
        self.assertEqual(set(qs.values_list('_path', flat=True)),
                         set(['Top.Collections.Pictures.Astronomy',
                              'Top.Collections.Pictures.Astronomy.Stars',
                              'Top.Collections.Pictures.Astronomy.Galaxies',
                              'Top.Collections.Pictures.Astronomy.Astronauts'])
                         )
