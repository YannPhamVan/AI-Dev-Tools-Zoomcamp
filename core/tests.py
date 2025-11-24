from django.test import TestCase
from django.urls import reverse
from .models import Todo


class TodoModelTests(TestCase):
    def test_create_todo(self):
        t = Todo.objects.create(title='Test', description='Desc')
        self.assertEqual(str(t), 'Test')
        self.assertFalse(t.completed)
        self.assertIsNone(t.due_date)


class TodoViewTests(TestCase):
    def setUp(self):
        self.list_url = reverse('core:list')
        self.create_url = reverse('core:create')

    def test_list_view_empty(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'No TODOs')

    def test_create_view(self):
        data = {'title': 'New', 'description': 'x', 'completed': False}
        resp = self.client.post(self.create_url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Todo.objects.filter(title='New').exists())

    def test_update_view(self):
        todo = Todo.objects.create(title='Old')
        url = reverse('core:edit', args=[todo.pk])
        resp = self.client.post(url, {'title': 'Updated', 'description': '', 'completed': False}, follow=True)
        self.assertEqual(resp.status_code, 200)
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated')

    def test_delete_view(self):
        todo = Todo.objects.create(title='ToDelete')
        url = reverse('core:delete', args=[todo.pk])
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Todo.objects.filter(pk=todo.pk).exists())

    def test_toggle_view(self):
        todo = Todo.objects.create(title='T')
        url = reverse('core:toggle', args=[todo.pk])
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        todo.refresh_from_db()
        self.assertTrue(todo.completed)
