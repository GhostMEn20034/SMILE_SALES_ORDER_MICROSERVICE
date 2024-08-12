from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from testing_utils.auth.auth_setup import AuthSetupInitializer


Account = get_user_model()


class TestAuthSetup(APITestCase):
    def setUp(self):
        self.password = "test1234"

        self.test_user = Account.objects.create_user(
            email="testing44@gmail.com",
            password=self.password,
            first_name="Hello",
            original_id=69,
        )
        self.access_token = AuthSetupInitializer.get_auth_token(self.test_user)

    def test_access_tokens_user_id_equals_to_users_original_id_value(self):
        """
        Checks whether user_id in the token's payload equals to the original_id value of the user
        """
        token = AccessToken(self.access_token)
        payload = token.payload

        user_id = payload['user_id']
        self.assertEqual(user_id, self.test_user.original_id)
