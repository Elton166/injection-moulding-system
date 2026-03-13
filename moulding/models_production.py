from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models_orders import ProductionOrder


class ShiftProduction(models.Model):
    """Model for tracking production per shift"""
    SHIFT_CHOICES = [
        ('day', 'Day Shift'),
        ('night', 'Night Shift'),
        ('morning', 'Morning Shift'),
        ('afternoon', 'Afternoon Shift'),
        ('evening', 'Evening Shift'),
    ]
    
    production_number = models.CharField(max_length=50, unique=True, blank=True)
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE, related_name='shift_productions')
    
    # Shift details
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    shift_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(help_text="Shift start time")
    end_time = models.TimeField(help_text="Shift end time")
    
    # Production quantities
    quantity_produced = models.IntegerField(help_text="Good parts produced this shift")
    quantity_rejected = models.IntegerField(default=0, help_text="Rejected parts this shift")
    total_quantity = models.IntegerField(default=0, help_text="Total parts attempted")
    
    # Efficiency metrics
    scrap_rate = models.FloatField(default=0, help_text="% scrap rate")
    production_rate = models.FloatField(default=0, help_text="Parts per hour")
    
    # Machine and personnel
    machine_number = models.CharField(max_length=50)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shift_productions')
    supervisor = models.CharField(max_length=200, blank=True, help_text="Supervisor name")
    
    # Downtime tracking
    downtime_minutes = models.IntegerField(default=0, help_text="Minutes of downtime")
    downtime_reason = models.TextField(blank=True, help_text="Reason for downtime")
    
    # Material usage (optional - can link to MaterialUsage)
    material_used = models.FloatField(default=0, help_text="kg of material used", blank=True)
    
    # Notes
    notes = models.TextField(blank=True, help_text="Shift notes, issues, observations")
    quality_issues = models.TextField(blank=True, help_text="Any quality issues encountered")
    
    # Approval
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='approved_shift_productions')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-shift_date', '-start_time']
        unique_together = ['production_order', 'shift', 'shift_date']
    
    def save(self, *args, **kwargs):
        # Generate production number
        if not self.production_number:
            last_prod = ShiftProduction.objects.order_by('-id').first()
            if last_prod and last_prod.production_number:
                try:
                    last_num = int(last_prod.production_number.split('-')[1])
                    self.production_number = f'SP-{last_num + 1:05d}'
                except:
                    self.production_number = f'SP-{self.id or 1:05d}'
            else:
                self.production_number = 'SP-00001'
        
        # Calculate total quantity
        self.total_quantity = self.quantity_produced + self.quantity_rejected
        
        # Calculate scrap rate
        if self.total_quantity > 0:
            self.scrap_rate = (self.quantity_rejected / self.total_quantity) * 100
        
        # Calculate production rate (parts per hour)
        if self.start_time and self.end_time:
            # Calculate shift duration in hours
            start_minutes = self.start_time.hour * 60 + self.start_time.minute
            end_minutes = self.end_time.hour * 60 + self.end_time.minute
            
            # Handle overnight shifts
            if end_minutes < start_minutes:
                end_minutes += 24 * 60
            
            duration_minutes = end_minutes - start_minutes - self.downtime_minutes
            
            if duration_minutes > 0:
                duration_hours = duration_minutes / 60
                self.production_rate = self.quantity_produced / duration_hours
        
        super().save(*args, **kwargs)
        
        # Update production order quantity
        self.update_order_quantity()
    
    def update_order_quantity(self):
        """Update the production order's total quantity produced"""
        order = self.production_order
        total_produced = ShiftProduction.objects.filter(
            production_order=order,
            approved=True
        ).aggregate(total=models.Sum('quantity_produced'))['total'] or 0
        
        order.quantity_produced = total_produced
        order.save()
    
    def __str__(self):
        return f"{self.production_number} - {self.production_order.order_number} - {self.shift} ({self.shift_date})"
    
    def shift_duration_hours(self):
        """Calculate shift duration in hours"""
        if not self.start_time or not self.end_time:
            return 0
        
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        
        if end_minutes < start_minutes:
            end_minutes += 24 * 60
        
        duration_minutes = end_minutes - start_minutes
        return round(duration_minutes / 60, 2)
    
    def effective_hours(self):
        """Calculate effective production hours (excluding downtime)"""
        total_hours = self.shift_duration_hours()
        downtime_hours = self.downtime_minutes / 60
        return round(total_hours - downtime_hours, 2)
    
    def efficiency_percentage(self):
        """Calculate shift efficiency (production time vs total time)"""
        total_hours = self.shift_duration_hours()
        if total_hours == 0:
            return 0
        effective = self.effective_hours()
        return round((effective / total_hours) * 100, 1)
