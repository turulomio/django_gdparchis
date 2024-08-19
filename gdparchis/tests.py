from django.contrib.auth.models import User
from gdparchis.reusing import tests_helpers
from json import loads
from pydicts import lod,  dod
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

lod,  dod

class API(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        """
            Only instantiated once
        """
        super().setUpClass()
        
        # User to test api
        cls.user_authorized_1 = User(
            email='testing@testing.com',
            first_name='Testing',
            last_name='Testing',
            username='testing',
        )
        cls.user_authorized_1.set_password('testing123')
        cls.user_authorized_1.save()
            # User to confront security
        cls.user_authorized_2 = User(
            email='other@other.com',
            first_name='Other',
            last_name='Other',
            username='other',
        )
        cls.user_authorized_2.set_password('other123')
        cls.user_authorized_2.save()
        
        
        client = APIClient()
        response = client.post('/login/', {'username': cls.user_authorized_1.username, 'password': 'testing123',},format='json')
        result = loads(response.content)
        cls.token_user_authorized_1 = result
        
        response = client.post('/login/', {'username': cls.user_authorized_2.username, 'password': 'other123',},format='json')
        result = loads(response.content)
        cls.token_user_authorized_2 = result

        
        cls.client_authorized_1=APIClient()
        cls.client_authorized_1.credentials(HTTP_AUTHORIZATION='Token ' + cls.token_user_authorized_1)
        cls.client_authorized_1.user=cls.user_authorized_1

        cls.client_authorized_2=APIClient()
        cls.client_authorized_2.credentials(HTTP_AUTHORIZATION='Token ' + cls.token_user_authorized_2)
        cls.client_authorized_2.user=cls.user_authorized_2
        
        cls.client_anonymous=APIClient()
        cls.client_anonymous.user=None

    def test_Game(self):
        game=tests_helpers.client_post(self, self.client_authorized_1, "/api/game/",  {"max_players":4},  status.HTTP_201_CREATED)
        print(game)
        state=tests_helpers.client_get(self, self.client_authorized_1, game["url"]+"state/",   status.HTTP_200_OK)
        
        state=tests_helpers.client_post(self, self.client_authorized_1, game["url"]+"dice_click/",   {"player": 1,  "value":5},  status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Incorrect player clicked dice",  state)
                
        state=tests_helpers.client_post(self, self.client_authorized_1, game["url"]+"dice_click/",   {"player": 0,  "value":5},  status.HTTP_200_OK)
        
        state=tests_helpers.client_post(self, self.client_authorized_1, game["url"]+"piece_click/",   {"player": 0,  "piece":0},  status.HTTP_200_OK)
        dod.dod_print(state)
        
