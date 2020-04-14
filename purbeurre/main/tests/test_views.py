from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth
from main.models import Aliment, Favorite
from django.contrib.auth.models import User
import json


class TestHomePage(TestCase):
    '''Test of the homepage view'''

    def setUp(self):
        self.client = Client()
        self.homepage = reverse('main:homepage')

    def test_homepage_GET(self):
        ''' Testing index / homepage view method '''

        response = self.client.get(self.homepage)
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/1')
        self.assertEquals(response.status_code, 404)


class TestRegister(TestCase):
    '''Clas to test the register view'''
    def setUp(self):

        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')

    def test_get_register_page(self):

        response = self.client.get(reverse('main:register'))
        self.assertEqual(response.status_code, 200)

    def test_registration_invalid_infos(self):

        response = self.client.post(reverse('main:register'),
                                    data={'username': 'antoine',
                                          'email': 'antoine@email.com',
                                          'password1': 'pasword121331+',
                                          'password2': 'wrongpassword121331+'})
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)


class TestLogout(TestCase):
    '''Calss used to test the logout view'''

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')

    def test_logout_redirect_visitor(self):
        '''test redirect function after logout'''
        self.client.login()
        self.client.logout()
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_logout_view_user_status(self):
        '''test redirects for visitor logout url'''
        self.client.login(username="antoine", password="Password3216854+")
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)


class TestLogin(TestCase):
    '''Calss used to test the login view'''

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')

    def test_access_login_page(self):

        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):

        self.client.login(username='antoine', password='Password3216854+')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)

    def test_login_fail(self):

        self.client.login(username='antoine', password='wrongpassword1234')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)

    def test_redirect_after_login(self):

        self.client.login(username='antoine', password='Password3216854+')
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 302)


class TestAliments(TestCase):
    '''Test the aliments view'''

    def setUp(self):

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

    def test_aliments_get_view(self):

        response = self.client.get('/aliments/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/aliments/pain')
        self.assertEqual(response.status_code, 404)

    def test_aliment_display(self):

        self.aliment.save()
        product = self.aliment.name
        response = self.client.post('/aliments/', args=(product))
        self.assertEqual(response.status_code, 302)


class TestAccount(TestCase):
    '''Test of the account view'''

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')

    def test_account_is_logged_in(self):
        '''test access account page if logged in '''

        self.client.login(username="antoine", password="Password3216854+")
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)

    def test_account_visitor(self):
        '''test access account page if not logged in'''

        self.client = Client()
        self.client.login(username="antoine", password="password1234")
        self.client.logout()
        response = self.client.get('/account/')
        self.assertRedirects(response, '/')


class TestInfos(TestCase):
    '''Calss used to test the infos view'''

    def setUp(self):

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

    def test_infos_valid_page(self):

        product = self.aliment.id
        response = self.client.get(reverse('main:infos', args=(product,)))
        self.assertEqual(response.status_code, 200)

    def test_infos_empty_args(self):

        response = self.client.get('/infos/')
        self.assertEqual(response.status_code, 404)

    def test_infos_wrong_args(self):

        response = self.client.get('/infos/tests')
        self.assertEqual(response.status_code, 404)


class TestSaveAliment(TestCase):
    '''Calss used to test the aliment view'''

    def setUp(self):

        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
        self.client = Client()
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

    def test_save_aliment_view(self):

        product = self.aliment.id
        self.client.login(username='antoine', password='Password3216854+')
        aliment_saved = Favorite.objects.create(saved_by=self.user,
                                                saved_aliment=self.aliment)
        aliments_saved = Favorite.objects.filter(saved_by=self.user,
                                                 saved_aliment=self.aliment)
        self.assertTrue(aliments_saved.exists())


class TestAlternative(TestCase):
    '''Calss used to test the alternative view'''

    def setUp(self):

        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
        self.client = Client()
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

    def test_alternative_view_get(self):

        product = self.aliment.id
        response = self.client.get(reverse('main:alternative',
                                   args=(product, )))
        self.assertEqual(response.status_code, 200)

    def test_alternative_view_get_with_extra(self):

        product = self.aliment.id + 1
        response = self.client.get(reverse('main:alternative',
                                           args=(product, )))
        self.assertEqual(response.status_code, 302)


class TestDelete(TestCase):
    '''Calss used to test the delete view'''

    def setUp(self):

        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
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

    def test_delete_logged_user(self):

        self.client.login(username='antoine', password='Password3216854+')
        response = self.client.get(reverse('main:delete', args=("1")))
        self.assertEqual(response.status_code, 302)
    
    def test_delete_not_logged_user(self):

        self.client.login(username='antoine', password='Password3216854+')
        self.client.logout()
        response = self.client.get(reverse('main:delete', args=('1')))
        self.assertEqual(response.status_code, 302)

    def test_delete_aliment(self):

        self.client.login(username='antoine', password='Password3216854+')
        product = self.aliment.id
        response = self.client.get(reverse('main:delete', args=(str(product))))
        self.assertEqual(response.status_code, 302)


class TestSaved(TestCase):
    '''Calss used to test the saved view'''

    def setUp(self):

        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
    
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

    def test_saved_view_get_logged_in(self):

        self.client.login(username='antoine', password='Password3216854+')
        response = self.client.get(reverse('main:saved'))
        self.assertEqual(response.status_code, 200)

    def test_saved_view_get_not_logged(self):

        self.client.login(username='antoine', password='Password3216854+')
        self.client.logout()
        response = self.client.get(reverse('main:saved'))
        self.assertRedirects(response, '/login/')


