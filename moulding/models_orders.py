from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Mould


class ProductionOrder(models.Model):
    """Model for production orders"""
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=100, unique=True)
    mould = models.ForeignKey(Mould, on_delete=models.CASCADE, related_name='production_orders')
    product_name = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=200)
    customer_contact = models.CharField(max_length=100, blank=True)
    
    # Order details
    quantity_ordered = models.IntegerField(help_text="Total quantity to produce")
    quantity_produced = models.IntegerField(default=0, help_text="Quantity already produced")
    unit = models.CharField(max_length=50, default='pieces', help_text="Unit of measurement")
    
    # Material calculation
    material_recipe = models.ForeignKey('MaterialRecipe', on_delete=models.SET_NULL, null=True, blank=True, 
                                       related_name='production_orders',
                                       help_text="Material recipe for this product")
    weight_per_part = models.FloatField(null=True, blank=True, help_text="grams per part")
    
    # Calculated material requirements (in kg)
    base_material_required = models.FloatField(default=0, help_text="kg of base material needed")
    masterbatch_required = models.FloatField(default=0, help_text="kg of masterbatch needed")
    regrind_required = models.FloatField(default=0, help_text="kg of regrind needed")
    total_material_required = models.FloatField(default=0, help_text="Total kg needed")
    estimated_material_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Priority and status
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Dates
    order_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    
    # Additional info
    notes = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'due_date', '-created_at']
    
    def save(self, *args, **kwargs):
        """Calculate material requirements on save"""
        self.calculate_material_requirements()
        super().save(*args, **kwargs)
    
    def calculate_material_requirements(self):
        """Calculate material requirements based on recipe and quantity"""
        if not self.material_recipe or not self.weight_per_part:
            return
        
        # Total weight needed in kg (weight_per_part is in grams)
        total_weight_kg = (self.weight_per_part * self.quantity_ordered) / 1000
        
        # Add 5% waste factor
        total_weight_with_waste = total_weight_kg * 1.05
        
        # Calculate each material component
        recipe = self.material_recipe
        self.base_material_required = (total_weight_with_waste * recipe.base_percentage) / 100
        self.masterbatch_required = (total_weight_with_waste * recipe.masterbatch_percentage) / 100
        self.regrind_required = (total_weight_with_waste * recipe.regrind_percentage) / 100
        self.total_material_required = total_weight_with_waste
        
        # Calculate estimated cost
        cost = 0
        if recipe.base_material:
            cost += float(recipe.base_material.unit_price) * self.base_material_required
        if recipe.masterbatch:
            cost += float(recipe.masterbatch.unit_price) * self.masterbatch_required
        if recipe.regrind_material:
            cost += float(recipe.regrind_material.unit_price) * self.regrind_required
        
        self.estimated_material_cost = round(cost, 2)
    
    def __str__(self):
        return f"{self.order_number} - {self.product_name} for {self.customer_name}"
    
    def quantity_remaining(self):
        """Calculate remaining quantity to produce"""
        return self.quantity_ordered - self.quantity_produced
    
    def progress_percentage(self):
        """Calculate production progress percentage"""
        if self.quantity_ordered == 0:
            return 0
        return round((self.quantity_produced / self.quantity_ordered) * 100, 1)
    
    def is_overdue(self):
        """Check if order is overdue"""
        if self.status in ['completed', 'cancelled']:
            return False
        return timezone.now().date() > self.due_date
    
    def days_until_due(self):
        """Calculate days until due date"""
        delta = self.due_date - timezone.now().date()
        return delta.days
    
    def priority_display_color(self):
        """Return color for priority badge"""
        colors = {
            'urgent': '#dc3545',
            'high': '#fd7e14',
            'normal': '#28a745',
            'low': '#6c757d',
        }
        return colors.get(self.priority, '#6c757d')
    
    def has_sufficient_materials(self):
        """Check if there are sufficient materials in stock"""
        if not self.material_recipe:
            return None
        
        sufficient = True
        shortages = []
        
        recipe = self.material_recipe
        
        # Check base material
        if recipe.base_material and recipe.base_material.current_stock < self.base_material_required:
            sufficient = False
            shortages.append({
                'material': recipe.base_material.code,
                'required': self.base_material_required,
                'available': recipe.base_material.current_stock,
                'shortage': self.base_material_required - recipe.base_material.current_stock
            })
        
        # Check masterbatch
        if recipe.masterbatch and recipe.masterbatch.current_stock < self.masterbatch_required:
            sufficient = False
            shortages.append({
                'material': recipe.masterbatch.code,
                'required': self.masterbatch_required,
                'available': recipe.masterbatch.current_stock,
                'shortage': self.masterbatch_required - recipe.masterbatch.current_stock
            })
        
        # Check regrind
        if recipe.regrind_material and recipe.regrind_material.current_stock < self.regrind_required:
            sufficient = False
            shortages.append({
                'material': recipe.regrind_material.code,
                'required': self.regrind_required,
                'available': recipe.regrind_material.current_stock,
                'shortage': self.regrind_required - recipe.regrind_material.current_stock
            })
        
        return {
            'sufficient': sufficient,
            'shortages': shortages
        }
