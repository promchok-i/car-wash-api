from django.urls import path

from . import views


urlpatterns = [
    # booking
    path('appt/', view=views.AppointmentCreateView.as_view(), name='appt-create'),
    # get detail
    path('appt/<str:pk>', view=views.AppointmentDetailView.as_view(), name='appt-detail'),
    # check in
    path('appt/<str:pk>/checkin', view=views.AppointmentCheckInView.as_view(), name='appt-check-in'),
    # cancel
    path('appt/<str:pk>/cancel', view=views.AppointmentCancelView.as_view(), name='appt-cancel'),
]