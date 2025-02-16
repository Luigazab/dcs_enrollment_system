from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from admin_dashboard.models import Program, enrollment_dates, student

class AdminDashboardTests(TestCase):
    def setUp(self):
        # Create sample enrollment dates
        enrollment_dates.objects.create(
            enrollment_period="starting_enrollment_date",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day - 1
        )
        enrollment_dates.objects.create(
            enrollment_period="ending_enrollment_date",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day + 1
        )

        # Create sample program
        self.program = Program.objects.create(name="CS", full="Computer Science")

        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="password123",
            email="admin@example.com"
        )

        self.client = Client()

    def test_enroll_new_student(self):
        # Login as admin
        self.client.login(username="admin", password="password123")

        # Define POST data for a new student
        response = self.client.post(reverse('enroll_student', args=['new']), {
            'first_name': 'John',
            'last_name': 'Doe',
            'middle_name': 'A',
            'dob': '2000-01-01',
            'gender': 'Male',
            'contactNumber': '1234567890',
            'email': 'johndoe@example.com',
            'Address': '123 Main St',
            'year_standing': '1',
            'section': 'A',
            'program': self.program.id,
            'suffix': '',
            'status': 'Enrolled',
        })

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertTrue(student.objects.filter(email="johndoe@example.com").exists())

        # Validate created user
        new_user = User.objects.get(username="doejohn")
        self.assertEqual(new_user.email, "johndoe@example.com")
        self.assertFalse(new_user.is_staff)
