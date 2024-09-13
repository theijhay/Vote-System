from django.test import TestCase
from .models import StudentVoter

# Create your tests here.
class StudentVoterTestCase(TestCase):
    def setUp(self):
        StudentVoter.objects.create(
            student_id="123", first_name="John", last_name="Doe", email="john@example.com", department="CS", year=3
        )

    def test_student_creation(self):
        """Test if a StudentVoter instance is created successfully."""
        john = StudentVoter.objects.get(student_id="123")
        self.assertEqual(john.first_name, "John")
