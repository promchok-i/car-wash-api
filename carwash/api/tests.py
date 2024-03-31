import datetime
import pytz
from freezegun import freeze_time

from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Customer, Appointment, WashService


class BaseAPITest(APITestCase):
    
    def setUp(self):
        self.start_time_1 = datetime.datetime(2024, 1, 1, 11, 00, tzinfo=pytz.UTC)
        self.end_time_1 = datetime.datetime(2024, 1, 1, 11, 30, tzinfo=pytz.UTC)
        self.start_time_2 = datetime.datetime(2024, 2, 2, 12, 30, tzinfo=pytz.UTC)
        self.end_time_2 = datetime.datetime(2024, 2, 2, 13, 00, tzinfo=pytz.UTC)
        
        self.customer_1 = Customer.objects.create(name='Customer 1')
        self.customer_2 = Customer.objects.create(name='Customer 2')
        
        self.wash_service_1 = WashService.objects.create(name='Wash Service 1', price=500)
        self.wash_service_2 = WashService.objects.create(name='Wash Service 2', price=1000)
        
        self.appointment_1 = Appointment.objects.create(customer=self.customer_1, 
                                                    wash_service=self.wash_service_1, 
                                                    start_time=self.start_time_1,
                                                    end_time=self.end_time_1)
        self.appointment_2 = Appointment.objects.create(customer=self.customer_2, 
                                                    wash_service=self.wash_service_2, 
                                                    start_time=self.start_time_2,
                                                    end_time=self.end_time_2)
        

class AppointmentTest(BaseAPITest):
    
    def test_create_appt(self):
        url = reverse('appt-create')
        data = {"customer": 1, "wash_service": 1, "start_time": self.start_time_1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 3)
    
    @freeze_time("2024-01-01 10:00:00")
    def test_check_in_appt_success(self):
        url = reverse('appt-check-in', kwargs={'pk': 1})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Appointment checked in successfully.'})
        
        # test update customer total spending and level
        customer = Customer.objects.get(id=1)
        self.assertEqual(customer.total_spending, 500)
        self.assertEqual(customer.level, 'silver')
    
    @freeze_time("2024-01-01 10:00:00")
    def test_check_in_same_appt(self):
        self.appointment_1.is_check_in = True
        self.appointment_1.save()
        
        url = reverse('appt-check-in', kwargs={'pk': 1})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'Already Checked In'})
    
    @freeze_time("2024-01-01 10:00:00")
    def test_check_in_cancelled_appt(self):
        self.appointment_1.is_active = False
        self.appointment_1.save()
        
        url = reverse('appt-check-in', kwargs={'pk': 1})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'Already Cancelled'})
    
    @freeze_time("2024-01-02 10:00:00")
    def test_late_check_in_appt(self):
        url = reverse('appt-check-in', kwargs={'pk': 1})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'Invalid Time'})
    
    @freeze_time("2024-01-01 10:00:00")
    def test_cancel_appt_success(self):
        url = reverse('appt-cancel', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Appointment cancel successfully.'})
    
    @freeze_time("2024-01-01 10:00:00")
    def test_cancel_checked_in_appt(self):
        self.appointment_1.is_check_in = True
        self.appointment_1.save()
        
        url = reverse('appt-cancel', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'Already Checked In'})
    
    @freeze_time("2024-01-01 10:00:00")
    def test_cancel_cancelled_appt(self):
        self.appointment_1.is_active = False
        self.appointment_1.save()
        
        url = reverse('appt-cancel', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'Already Cancelled'})
    
    @freeze_time("2024-01-02 10:00:00")
    def test_late_cancel_appt(self):
        url = reverse('appt-cancel', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'Invalid Time'})