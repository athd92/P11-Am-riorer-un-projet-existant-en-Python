from django.test import TestCase
from main.models import Aliment, Favorite
from django.test.client import Client
from django.contrib.auth.models import User

class TestAlimentModel(TestCase):
    '''Calss used to test the aliments model view'''

    def test_valid_Aliment(self):
        
        self.aliment = Aliment.objects.create(
            name='Tomates',
            name_fr='Tomates cerises',
            date='2019/01/09',
            brands='La Conserve',
            nutriscore='a',
            ingredients='Tomates, sel, sure, conservateurs',
            image='https://image-test-p8-url-test.com',
            url='https://test-p8-url-test.com',
            stores='Lidl, Auchan, Franprix',
            quantity='200g',
            packaging='Conserve',
            ingredients_fr='Tomates, sel, sucre',
            manufactured_places='Dijon',
            purchase_places='Bordeaux, Paris',
            categories='Légumes',
            code='654f654651651')

        self.aliment.save()
        self.assertEqual(self.aliment.name, 'Tomates')
        self.assertEqual(self.aliment.code, '654f654651651')
        self.assertNotEqual(self.aliment.code, 'ZZE3232')
