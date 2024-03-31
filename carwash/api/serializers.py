from rest_framework import serializers

from .models import Customer, WashService, Appointment

class CustomerDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'level']

class WashServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashService
        fields = ['name', 'description', 'price']
        
class AppointmentDetailSerializer(serializers.ModelSerializer):
    customer = CustomerDetailSerializer()
    wash_service = WashServiceDetailSerializer()
    
    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'wash_service', 'start_time', 'end_time', 'is_check_in']
        
class AppointmentBookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'wash_service', 'start_time']

class AppointmentCheckInSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Appointment
        fields = ['is_check_in']