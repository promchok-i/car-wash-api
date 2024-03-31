import logging
from datetime import timedelta

from django.utils import timezone

from .models import Customer, Appointment
from .exceptions import Invalidtime, AlreadyCheckedIn, AlreadyCancelled


logger = logging.getLogger(__name__)

class AppointmentService:
    appt_manager = Appointment.objects
    
    @classmethod
    def filter_by_id(cls, account_id):
        return cls.appt_manager.filter(id=account_id)
    
    @classmethod
    def get_by_id(cls, account_id):
        return cls.appt_manager.get(id=account_id)
    
    @classmethod
    def create(cls, customer, wash_service, start_time):
        duration = 30
        appt = cls.appt_manager.create(customer=customer,
                                        wash_service=wash_service,
                                        start_time=start_time,
                                        end_time=start_time+timedelta(minutes=duration))
        
        logger.info('Create new Appointment success with wash service %s and start %s.', wash_service, start_time)
        return appt
    
    @classmethod
    def check_in(cls, appt):
        appt = cls.allowed_appt(appt, 'check in')
        appt.is_check_in = True
        CustomerService.update_total_spending(appt.customer, appt.wash_service.price)
        appt.save()
        logger.info('Appointment check in success (Customer : %s, Wash service: %s).', appt.customer.name, appt.wash_service)
    
    @classmethod
    def cancel(cls, appt):
        appt = cls.allowed_appt(appt, 'cancel')
        appt.is_active = False
        appt.save()
        logger.info('Appointment cancel success (Customer : %s, Wash service: %s).', appt.customer.name, appt.wash_service)
        
        
    @classmethod
    def allowed_appt(cls, appt, mode):
        if appt.is_check_in:
            logger.error('Appointment is already checked in (Customer : %s, Wash service: %s).', appt.customer.name, appt.wash_service)
            raise AlreadyCheckedIn
        elif not appt.is_active:
            logger.error('Appointment is already cancelled (Customer : %s, Wash service: %s).', appt.customer.name, appt.wash_service)
            raise AlreadyCancelled
        elif timezone.now() > appt.start_time:
            logger.error('Appointment is late to %s (Customer : %s, Wash service: %s).', mode, appt.customer.name, appt.wash_service)
            raise Invalidtime
        
        return appt


class CustomerService:
    customer_manager = Customer.objects
    
    @classmethod
    def update_total_spending(cls, customer, spending):
        customer.total_spending += spending
        
        # Update the customer level from appointment count
        gold_spending = 1000
        silver_spending = 500
        if customer.total_spending >= gold_spending:
            customer.level = 'gold'
            logger.info('Update customer level to %s success (Customer : %s).', customer.level, customer.name)
        elif customer.total_spending >= silver_spending:
            customer.level = 'silver'
            logger.info('Update customer level to %s success (Customer : %s).', customer.level, customer.name)
            
        customer.save()
        logger.info('Update customer total spending to %s success (Customer : %s).', customer.total_spending, customer.name)