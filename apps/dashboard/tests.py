from urllib import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.tasks.models import Task


User = get_user_model()


class DashboardTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email = "test@example.com",
            password="testpassword123",
        )

        self.other_user = User.objects.create_user(
            username="othertestuser",
            email = "other@example.com",
            password = "testpassword123",
        )
        
        self.task = Task.objects.create(
            owner = self.user,
            title = "My task",
        )
    

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("login"),    
            {
                "email": self.user.email,
                "password": "testpassword123",
            },
        )
    
        self.assertRedirects(
            response,
            reverse("dashboard"),
        )
        

    def test_dashboard_requires_login(self):
        response = self.client.get(
            reverse("dashboard")    
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
        )
        
        
    def test_authenticated_user_can_access_dashboard(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("dashboard")    
        )

        self.assertEqual(
            response.status_code,
            200,
        )


    def test_profile_requires_login(self):
        response = self.client.get(
            reverse("profile")    
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",    
        )


    def test_authenticated_user_can_access_profile(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("profile")    
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        

    def test_user_can_update_profile(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("profile"),
            {
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        
        self.assertRedirects(
            response,
            reverse("profile"),
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.first_name,
            "John",
        )
        
        self.assertEqual(
            self.user.last_name,
            "Doe",
        )


    def test_user_can_change_password(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("change-password"),
            {
                "current_password": "testpassword123",
                "new_password": "NewStrongPassword123!",
                "confirm_password": "NewStrongPassword123!",
            },
        )

        self.assertRedirects(
            response,
            reverse("profile"),
        )

        self.user.refresh_from_db()
        
        self.assertTrue(
            self.user.check_password(
                "NewStrongPassword123!"    
            )    
        )


    def test_user_cannot_access_another_users_task(self):
        self.client.force_login(self.other_user)
        
        response = self.client.get(
            reverse(
                "task-detail",
                args=[self.task.pk],
            )
        )
        
        self.assertEqual(
            response.status_code,
            404,
        )