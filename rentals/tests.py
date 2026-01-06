from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Property, Payment

User = get_user_model()

class RejectFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='pass', role='admin')
        self.tenant = User.objects.create_user(username='tenant', password='pass', role='tenant')
        self.landlord = User.objects.create_user(username='landlord', password='pass', role='landlord')
        self.property = Property.objects.create(
            title='Test Property',
            rooms=2,
            rent=1000,
            deposit=500,
            landlord=self.landlord,
            photos='test.jpg',
            address='Test Address',
            status='pending'
        )
        self.payment = Payment.objects.create(
            tenant=self.tenant,
            property=self.property,
            amount=500,
            method='EcoCash',
            proof_image='test.jpg',
            status='pending'
        )

    def test_reject_property(self):
        from rentals.views import reject_property
        
        factory = RequestFactory()
        request = factory.post(f'/admin/reject-property/{self.property.id}/')
        request.user = self.admin
        
        response = reject_property(request, self.property.id)
        self.property.refresh_from_db()
        self.assertEqual(self.property.status, 'rejected')
        self.assertEqual(response.status_code, 302)  # Redirect

    def test_reject_payment(self):
        from rentals.views import reject_payment
        
        factory = RequestFactory()
        request = factory.post(f'/admin/reject-payment/{self.payment.id}/')
        request.user = self.admin
        
        response = reject_payment(request, self.payment.id)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'rejected')
        self.assertEqual(response.status_code, 302)  # Redirect
