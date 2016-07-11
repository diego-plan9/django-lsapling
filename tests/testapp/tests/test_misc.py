# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from testapp.models import NoCustomFieldsTree

PRETTY_UPSTREAM = u'''[%s] Top
├───[%s] Top.Science
│   └───[%s] Top.Science.Astronomy
│       ├───[%s] Top.Science.Astronomy.Astrophysics
│       └───[%s] Top.Science.Astronomy.Cosmology
├───[%s] Top.Hobbies
│   └───[%s] Top.Hobbies.Amateurs_Astronomy
└───[%s] Top.Collections
    └───[%s] Top.Collections.Pictures
        └───[%s] Top.Collections.Pictures.Astronomy
            ├───[%s] Top.Collections.Pictures.Astronomy.Stars
            ├───[%s] Top.Collections.Pictures.Astronomy.Galaxies
            └───[%s] Top.Collections.Pictures.Astronomy.Astronauts'''


class MiscTestCase(TestCase):
    '''
    Miscelaneous test cases.
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

    def test_001_pretty_print(self):
        '''
        Test the pretty_print() function.
        '''
        root = NoCustomFieldsTree.objects.get(_path='Top')
        # ids are filled dynamically, due to db reuse and autoincrement
        ids = range(root.pk, root.pk+13)
        pretty = root.pretty_print()
        self.assertEqual(pretty, PRETTY_UPSTREAM % tuple(ids))
