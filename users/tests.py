from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


CREATE_USER_URL = reverse("users:create")
TOKEN_PAIR_URL = reverse("users:token_obtain_pair")
USER_MANAGE_URL = reverse("users:manage")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_forbid_unauthorized(self):
        response = self.client.get(USER_MANAGE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create(self):
        payload = {
            "email": "test@test.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        }

        response = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload["password"]))

    def test_user_create_token(self):
        payload = {
            "email": "test@test.com",
            "password": "testpassword",
        }
        create_user(**payload)
        response = self.client.post(TOKEN_PAIR_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_token_create_wo_pass_fail(self):
        response = self.client.post(
            TOKEN_PAIR_URL, {"email": "test@test.com", "password": ""}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)


class PrivateUserApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="test@test.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_profile_retrieve_success(self):
        res = self.client.get(USER_MANAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_me_post_not_allowed(self):
        response = self.client.post(USER_MANAGE_URL, {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_update_own_profile(self):
        payload = {
            "email": "test@test.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.patch(USER_MANAGE_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(self.user.last_name, payload["last_name"])
