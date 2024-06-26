from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)
        


class Customer(BaseModel):
    
    LEVEL = (
        ('basic', 'Basic'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    )
    
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    level = models.CharField(max_length=20, choices=LEVEL, default='basic')
    total_spending = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
        
    def __str__(self) -> str:
        return f'{self.name} ({self.level} Member)'


class WashService(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self) -> str:
        return self.name


class Appointment(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    wash_service = models.ForeignKey(WashService, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_check_in = models.BooleanField(default=False)
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time cannot be before start time")
        
    def __str__(self) -> str:
        return f"{self.customer.name}'s appointment"
