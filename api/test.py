import unittest
import requests
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Todo

class TestTodoViews(TestCase):

    def test_fetch_data(self):
        # Fetch 'data' from endpoint
        response = requests.get('https://jsonplaceholder.typicode.com/todos')
        # Assuming the response is a list of dictionaries
        todos_data = response.json()

        # Call the function to fetch and save todos
        Todo.objects.all().delete()  # Clear the todos before testing
        Todo.fetch_data(None)

        # Check if the todos are saved in the database
        self.assertEqual(Todo.objects.count(), len(todos_data))

        # Check if the todos' attributes are the same as the ones in the response
        for todo_db, todo_data in zip(Todo.objects.all(), todos_data):
            self.assertEqual(todo_db.userId, todo_data['userId'])
            self.assertEqual(todo_db.id, todo_data['id'])
            self.assertEqual(todo_db.title, todo_data['title'])
            self.assertEqual(todo_db.completed, todo_data['completed'])

    def test_login_view(self):
        # Test the login view
        response = self.client.post('/api/login/', {'username': 'sbrito', 'password': 'a'})
        self.assertEqual(response.status_code, 200)
        # Assuming the login view returns the index page
        self.assertTemplateUsed(response, 'api/index.html')