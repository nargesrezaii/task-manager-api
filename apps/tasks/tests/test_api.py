from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.tasks.models import Task


User = get_user_model()


class TaskAPITests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username = "testuser",
            email = "test@example.com",
            password = "TestPassword123!",
        )
        self.client.force_authenticate(
            user=self.user,    
        )
        
    def test_authenticated_user_can_list_tasks(self):
        Task.objects.create(
            title = "First task",
            owner = self.user
        )
        
        Task.objects.create(
            title = "Second task",
            owner = self.user,
        )

        response = self.client.get("/api/tasks/")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        
        self.assertEqual(
            response.data["count"],
            2,
        )
        
    def test_user_only_sees_their_own_tasks(self):
        other_user = User.objects.create_user(
            username = "otheruser",
            email="other@example.com",
            password = "OtherPassword123!",
        )
        
        Task.objects.create(
            title = "My task",
            owner = self.user,
        )
        
        Task.objects.create(
            title = "Other user's task",
            owner = other_user,
        )

        response = self.client.get("/api/tasks/")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        
        self.assertEqual(
            response.data["count"],
            1,
        )
        
        self.assertEqual(
            response.data["results"][0]["title"],
            "My task",
        )
        
    def test_authenticated_user_can_create_task(self):
        data = {
            "title": "Learn French",    
        }
        
        response = self.client.post(
            "/api/tasks/",
            data,
            format = "json",
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Task.objects.count(),
            1,
        )
        
    def test_created_task_belongs_to_authenticateed_user(self):
        data = {
            "title": "My task",    
        }
        
        response = self.client.post(
            "/api/tasks/",
            data,
            format="json",
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        
        task = Task.objects.get()
        
        self.assertEqual(
            task.owner,
            self.user,
        )
        
    def test_unauthenticated_user_cannot_list_tasks(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/tasks/")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_cannot_retrieve_another_users_task(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="OtherPassword123!",
        )

        task = Task.objects.create(
            title="Private task",
            owner=other_user,
        )
        
        response = self.client.get(
            f"/api/tasks/{task.pk}/"    
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        
    def test_user_cannot_update_another_users_task(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="OtherPassword123!",
        )

        task = Task.objects.create(
            title="Original title",
            owner=other_user,
        )
        
        response = self.client.patch(
            f"/api/tasks/{task.pk}/",
            {"title": "Hacked title"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        
        task.refresh_from_db()
        
        self.assertEqual(
            task.title,
            "Original title",
        )
        
    def test_user_cannot_delete_another_users_task(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="OtherPassword123!",
        )

        task = Task.objects.create(
            title="Private task",
            owner=other_user,
        )

        response = self.client.delete(
            f"/api/tasks/{task.pk}/"    
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        
        self.assertTrue(
            Task.objects.filter(pk=task.pk).exists()    
        )

    def test_user_can_complete_their_task(self):
        task = Task.objects.create(
            title = "Complete this",
            owner = self.user,
            status = "TODO",
        )

        response = self.client.post(
            f"/api/tasks/{task.pk}/complete/"    
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        
        task.refresh_from_db()
        
        self.assertEqual(
            task.status,
            "COMPLETED",
        )

    def test_task_list_is_paginated(self):
        for index in range(11):
            Task.objects.create(
                title = f"Task {index}",
                owner = self.user,
            )
            
        response = self.client.get("/api/tasks/")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        
        self.assertEqual(
            response.data["count"],
            11,
        )

        self.assertIsNotNone(
            response.data["next"]   
        )