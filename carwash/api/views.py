import logging

from rest_framework import generics, response, status, views

from . import serializers, services



logger = logging.getLogger(__name__)


class AppointmentCreateView(generics.CreateAPIView):
    def get_serializer_class(self):
        return serializers.AppointmentBookingSerializer
    
    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        customer = data.get('customer')
        wash_service = data.get('wash_service')
        start_time = data.get('start_time')
        
        appt = services.AppointmentService.create(customer, wash_service, start_time)
        appt_serializer = serializers.AppointmentDetailSerializer(appt)
        return response.Response(appt_serializer.data, status=status.HTTP_201_CREATED)
    

class AppointmentDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.AppointmentDetailSerializer
    
    def get_queryset(self):
        appt_id = self.kwargs.get('pk')
        return services.AppointmentService.filter_by_id(appt_id)
    
    
class AppointmentCheckInView(views.APIView):
    def patch(self, request, *args, **kwargs):
        appt_id = self.kwargs.get('pk')
        appt = services.AppointmentService.get_by_id(appt_id)
        services.AppointmentService.check_in(appt)
        return response.Response({'message': 'Appointment checked in successfully.'}, status=status.HTTP_200_OK)


class AppointmentCancelView(views.APIView):
    
    def delete(self, request, *args, **kwargs):
        appt_id = self.kwargs.get('pk')
        appt = services.AppointmentService.get_by_id(appt_id)
        services.AppointmentService.cancel(appt)
        return response.Response({'message': 'Appointment cancel successfully.'}, status=status.HTTP_200_OK)