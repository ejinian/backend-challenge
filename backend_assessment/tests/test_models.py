from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Label, Task

class LabelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        self.label = Label.objects.create(name='Test Label', owner=self.user)

    def test_label_name(self):
        label = Label.objects.get(id=self.label.id)
        self.assertEqual(label.name, 'Test Label')

    def test_label_owner(self):
        label = Label.objects.get(id=self.label.id)
        self.assertEqual(label.owner, self.user)

    def test_label_unique_together_constraint(self):
        with self.assertRaises(Exception):
            Label.objects.create(name='Test Label', owner=self.user)

class TaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            is_completed=False,
            owner=self.user
        )

    def test_task_title(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.title, 'Test Task')

    def test_task_description(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.description, 'This is a test task')

    def test_task_owner(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.owner, self.user)

    def test_task_is_completed_default(self):
        task = Task.objects.get(id=self.task.id)
        self.assertFalse(task.is_completed)

    def test_task_labels_relationship(self):
        label = Label.objects.create(name='Test Label', owner=self.user)
        self.task.labels.add(label)
        task = Task.objects.get(id=self.task.id)
        self.assertIn(label, task.labels.all())

class LabelTaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.tasks = []
        cls.labels = []

        for i in range(5):
            task = Task.objects.create(
                title=f'Test Task {i+1}',
                description=f'This is test task {i+1}',
                is_completed=False,
                owner=cls.user
            )
            cls.tasks.append(task)

        # 10 unique labels
        for i in range(10):
            label_name = f'Test Label {i+1}'
            label = Label.objects.get_or_create(name=label_name, owner=cls.user)
            cls.labels.append(label)

    def test_task_label_relationship(self):
        # 5 labels are assigned per task
        for task in self.tasks:
            for label in self.labels[:5]:
                task.labels.add(label[0].id)

        # each task should have at least 5 labels
        for task in self.tasks:
            self.assertGreaterEqual(task.labels.count(), 5)

    def test_unique_label_constraint(self):
        with self.assertRaises(Exception):
            Label.objects.create(name='Test Label 10', owner=self.user)