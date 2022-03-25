import jwt
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .factories import GymFactory, UserFactory
from .models import Gym


class GymTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(password="password123")
        payload = {"username": self.user.username, "password": "password123"}
        self.client.post(
            reverse("ldn_central_app:session-create"), payload, format="json"
        )

    def test_create_gym(self):
        url = reverse("ldn_central_app:gym-list-create")
        payload = {
            "name": "Your FRAME",
            "gym_details": "WHY YOUR FRAME",
            "gym_link": "https://moveyourframe.com/",
            "description": "FRAME was born in 2009 with the simple mantra that getting fit should never feel like a chore and we’ve been putting the FUN back into fitness ever since. We believe in the power of sweet endorphins and the magical effects it can.",
            "quality": "Who said getting fit needs to be a chore? Not us! We’ve been putting the FUN back into fitness since 2009. It’s easy to stay motivated when you actually enjoy the class. Variety is the spice of life and Frame is your spice rack. We’ve got a class to suit.",
            "access": "Workout from anywhere (with 4G or WIFI) at any time. Whether you need a quickie 10-minute workout or to move for a full hour we’ve got what you need.",
            "network": "Our team of high-energy instructors make working out from home FUN. They’ll challenge you to smash your class and make sure you have a good time doing it!",
            "contract": "Remember your mum's 90s VHS workouts? We’ve taken inspiration from Cindy Crawford, Tracy Anderson, Cher and co. to bring you a full body workout using ankle weights, resistance bands and your own body weight. High reps, high vibes makes for a workout that",
        }
        res = self.client.post(url, payload, format="json")
        json_resp = res.json()
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(payload["name"], json_resp["name"])
        self.assertEqual(payload["gym_details"], json_resp["gym_details"])
        self.assertEqual(payload["gym_link"], json_resp["gym_link"])
        self.assertEqual(payload["description"], json_resp["description"])
        self.assertEqual(payload["quality"], json_resp["quality"])
        self.assertEqual(payload["access"], json_resp["access"])
        self.assertEqual(payload["network"], json_resp["network"])
        self.assertEqual(payload["contract"], json_resp["contract"])
        self.assertIsInstance(json_resp["id"], int)

    def test_list_gyms(self):
        gym = GymFactory()
        url = reverse("ldn_central_app:gym-list-create")
        res = self.client.get(url, format="json")
        json_resp = res.json()
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(gym.name, json_resp[0]["name"])
        self.assertEqual(gym.gym_details, json_resp[0]["gym_details"])
        self.assertEqual(gym.gym_link, json_resp[0]["gym_link"])
        self.assertEqual(gym.description, json_resp[0]["description"])
        self.assertEqual(gym.quality, json_resp[0]["quality"])
        self.assertEqual(gym.access, json_resp[0]["access"])
        self.assertEqual(gym.network, json_resp[0]["network"])
        self.assertEqual(gym.contract, json_resp[0]["contract"])

    def test_retrieve_gyms(self):
        gym = GymFactory()
        url = reverse("ldn_central_app:gym-retrieve-update-destroy", args=[gym.id])
        res = self.client.get(url, format="json")
        json_resp = res.json()
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(gym.name, json_resp["name"])
        self.assertEqual(gym.gym_details, json_resp["gym_details"])
        self.assertEqual(gym.gym_link, json_resp["gym_link"])
        self.assertEqual(gym.description, json_resp["description"])
        self.assertEqual(gym.quality, json_resp["quality"])
        self.assertEqual(gym.access, json_resp["access"])
        self.assertEqual(gym.network, json_resp["network"])
        self.assertEqual(gym.contract, json_resp["contract"])

    def test_delete_expense(self):
        gym = GymFactory()
        url = reverse("ldn_central_app:gym-retrieve-update-destroy", args=[gym.id])
        res = self.client.delete(url, format="json")
        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)
        self.assertFalse(Gym.objects.filter(id=gym.id))

    def test_update_expense(self):
        gym = GymFactory()
        url = reverse("ldn_central_app:gym-retrieve-update-destroy", args=[gym.id])
        payload = {
            "name": "Your FRAME",
            "gym_details": "WHY YOUR FRAME",
            "gym_link": "https://moveyourframe.com/",
            "description": "FRAME was born in 2009 with the simple mantra that getting fit should never feel like a chore and we’ve been putting the FUN back into fitness ever since. We believe in the power of sweet endorphins and the magical effects it can.",
            "quality": "Who said getting fit needs to be a chore? Not us! We’ve been putting the FUN back into fitness since 2009. It’s easy to stay motivated when you actually enjoy the class. Variety is the spice of life and Frame is your spice rack. We’ve got a class to suit.",
            "access": "Workout from anywhere (with 4G or WIFI) at any time. Whether you need a quickie 10-minute workout or to move for a full hour we’ve got what you need.",
            "network": "Our team of high-energy instructors make working out from home FUN. They’ll challenge you to smash your class and make sure you have a good time doing it!",
            "contract": "Remember your mum's 90s VHS workouts? We’ve taken inspiration from Cindy Crawford, Tracy Anderson, Cher and co. to bring you a full body workout using ankle weights, resistance bands and your own body weight. High reps, high vibes makes for a workout that",
        }
        res = self.client.put(url, payload, format="json")
        updated_gym = Gym.objects.get(id=gym.id)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(updated_gym.name, payload["name"])
        self.assertEqual(updated_gym.gym_details, payload["gym_details"])
        self.assertEqual(updated_gym.gym_link, payload["gym_link"])
        self.assertEqual(updated_gym.description, payload["description"])
        self.assertEqual(updated_gym.quality, payload["quality"])
        self.assertEqual(updated_gym.access, payload["access"])
        self.assertEqual(updated_gym.network, payload["network"])
        self.assertEqual(updated_gym.contract, payload["contract"])

    def test_unsuccessful_update_expense(self):
        gym = GymFactory()
        url = reverse("ldn_central_app:gym-retrieve-update-destroy", args=[gym.id])
        payload = {}
        res = self.client.put(url, payload, format="json")
        json_resp = res.json()
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual(json_resp["name"], ["This field is required."])
        self.assertEqual(json_resp["gym_link"], ["This field is required."])


class RegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("ldn_central_app:registration-create")

    def test_registration(self):
        payload = {
            "first_name": "Obi",
            "last_name": "Ade",
            "email": "obi@email.com",
            "password": "pass123",
            "username": "obi123",
        }
        res = self.client.post(self.url, payload, format="json")
        json_resp = res.json()

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        self.assertEqual(json_resp["first_name"], payload["first_name"])
        self.assertEqual(json_resp["last_name"], payload["last_name"])
        self.assertEqual(json_resp["email"], payload["email"])
        self.assertEqual(json_resp["username"], payload["username"])
        # password is not sent back with response
        with self.assertRaises(KeyError):
            json_resp["password"]


class SessionCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("ldn_central_app:session-create")
        self.user = UserFactory(password="password123")

    def test_create_session(self):
        # we have to use a non-hashed version of passord
        payload = {"username": self.user.username, "password": "password123"}
        res = self.client.post(self.url, payload, format="json")
        decoded_token = jwt.decode(
            res.data["jwt"], settings.SECRET_KEY, algorithms=["HS256"]
        )
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertTrue("jwt" in res.data)
        self.assertEqual(self.user.id, decoded_token["user_id"])


class SessionRetrieveDestroyTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(password="password123")

    def test_retrieve_session(self):
        # we have to use a non-hashed version of passord
        payload = {"username": self.user.username, "password": "password123"}
        # create a session
        self.client.post(
            reverse("ldn_central_app:session-create"), payload, format="json"
        )

        res = self.client.get(
            reverse("ldn_central_app:session-retrieve-destroy"), format="json"
        )

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(res.data["data"]["id"], self.user.id)
        self.assertEqual(res.data["data"]["first_name"], self.user.first_name)
        self.assertEqual(res.data["data"]["last_name"], self.user.last_name)
        self.assertEqual(res.data["data"]["email"], self.user.email)

    def test_delete_session(self):
        # we have to use a non-hashed version of passord
        payload = {"username": self.user.username, "password": "password123"}
        # create a session
        self.client.post(
            reverse("ldn_central_app:session-create"), payload, format="json"
        )
        # delete a session
        self.client.delete(
            reverse("ldn_central_app:session-retrieve-destroy"), format="json"
        )
        # attempt retrieving a session
        res = self.client.get(
            reverse("ldn_central_app:session-retrieve-destroy"), format="json"
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, res.status_code)
