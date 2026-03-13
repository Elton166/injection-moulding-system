from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Mould


class MaterialType(models.Model):
    """Model for material types (Virgin, Regrind, etc.)"""
    CATEGORY_CHOICES = [
        ('virgin', 'Virgin Material'),
        ('regrind', 'Regrind Material'),
        ('mixed', 'Mixed (Virgin + Regrind)'),
    ]
    
    code = models.CharField(max_length=50, unique=True, help_text="e.g., PP-V-001, ABS-R-002")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    material_grade = models.CharField(max_length=100, help_text="e.g., PP, ABS, PE, PVC, Nylon")
    supplier = models.CharField(max_length=200, blank=True)
    
    # Material properties
    density = models.FloatField(help_text="g/cm³", null=True, blank=True)
    melt_flow_index = models.FloatField(help_text="MFI g/10min", null=True, blank=True)
    moisture_content = models.FloatField(help_text="% max", null=True, blank=True)
    
    # Regrind specific
    regrind_percentage = models.IntegerField(default=0, help_text="% if mixed with virgin")
    source = models.CharField(max_length=200, blank=True, help_text="Source of regrind")
    
    # Stock management
    current_stock = models.FloatField(default=0, help_text="kg")
    minimum_stock = models.FloatField(default=0, help_text="kg")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Processing parameters
    drying_temperature = models.IntegerField(null=True, blank=True, help_text="°C")
    drying_time = models.IntegerField(null=True, blank=True, help_text="hours")
    
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.name} ({self.get_category_display()})"
    
    def stock_status(self):
        """Return stock status"""
        if self.current_stock <= self.minimum_stock:
            return 'low'
        elif self.current_stock <= self.minimum_stock * 1.5:
            return 'medium'
        return 'good'


class Masterbatch(models.Model):
    """Model for masterbatch colors and additives"""
    TYPE_CHOICES = [
        ('color', 'Color Masterbatch'),
        ('additive', 'Additive Masterbatch'),
        ('filler', 'Filler Masterbatch'),
        ('uv', 'UV Stabilizer'),
        ('flame', 'Flame Retardant'),
    ]
    
    code = models.CharField(max_length=50, unique=True, help_text="e.g., MB-RED-001, MB-BLK-002")
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='color')
    
    # Color specific
    color_name = models.CharField(max_length=100, blank=True, help_text="e.g., Red, Blue, Black")
    color_code = models.CharField(max_length=50, blank=True, help_text="Pantone or RAL code")
    hex_color = models.CharField(max_length=7, blank=True, help_text="#RRGGBB")
    
    # Supplier info
    supplier = models.CharField(max_length=200)
    supplier_code = models.CharField(max_length=100, blank=True)
    
    # Usage parameters
    recommended_dosage = models.FloatField(help_text="% in final product")
    min_dosage = models.FloatField(help_text="% minimum", null=True, blank=True)
    max_dosage = models.FloatField(help_text="% maximum", null=True, blank=True)
    
    # Compatibility
    compatible_materials = models.TextField(help_text="e.g., PP, PE, ABS", blank=True)
    
    # Stock management
    current_stock = models.FloatField(default=0, help_text="kg")
    minimum_stock = models.FloatField(default=0, help_text="kg")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Properties
    carrier_resin = models.CharField(max_length=100, blank=True, help_text="e.g., PP, PE")
    pigment_content = models.FloatField(null=True, blank=True, help_text="% pigment")
    
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['type', 'color_name', 'code']
    
    def __str__(self):
        if self.color_name:
            return f"{self.code} - {self.color_name} ({self.name})"
        return f"{self.code} - {self.name}"
    
    def stock_status(self):
        """Return stock status"""
        if self.current_stock <= self.minimum_stock:
            return 'low'
        elif self.current_stock <= self.minimum_stock * 1.5:
            return 'medium'
        return 'good'


class MaterialUsage(models.Model):
    """Model for tracking material usage per production run"""
    usage_number = models.CharField(max_length=50, unique=True, blank=True)
    
    # Production details
    mould = models.ForeignKey(Mould, on_delete=models.CASCADE)
    machine_number = models.CharField(max_length=50)
    product_name = models.CharField(max_length=200)
    
    # Material composition
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE, related_name='usages')
    material_quantity = models.FloatField(help_text="kg used")
    
    # Masterbatch usage
    masterbatch = models.ForeignKey(Masterbatch, on_delete=models.SET_NULL, null=True, blank=True, related_name='usages')
    masterbatch_quantity = models.FloatField(default=0, help_text="kg used")
    masterbatch_percentage = models.FloatField(default=0, help_text="% in mix")
    
    # Additional materials
    additional_regrind = models.FloatField(default=0, help_text="kg additional regrind")
    regrind_percentage = models.FloatField(default=0, help_text="% regrind in total mix")
    
    # Production output
    parts_produced = models.IntegerField(default=0)
    good_parts = models.IntegerField(default=0)
    rejected_parts = models.IntegerField(default=0)
    
    # Efficiency
    material_per_part = models.FloatField(default=0, help_text="kg per part")
    scrap_rate = models.FloatField(default=0, help_text="% scrap")
    
    # Tracking
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    shift = models.CharField(max_length=20, blank=True, help_text="e.g., Day, Night, Morning")
    production_date = models.DateField(default=timezone.now)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-production_date', '-start_time']
    
    def save(self, *args, **kwargs):
        if not self.usage_number:
            # Generate usage number
            last_usage = MaterialUsage.objects.order_by('-id').first()
            if last_usage and last_usage.usage_number:
                try:
                    last_num = int(last_usage.usage_number.split('-')[1])
                    self.usage_number = f'MU-{last_num + 1:05d}'
                except:
                    self.usage_number = f'MU-{self.id or 1:05d}'
            else:
                self.usage_number = 'MU-00001'
        
        # Calculate material per part
        if self.good_parts > 0:
            total_material = self.material_quantity + self.masterbatch_quantity + self.additional_regrind
            self.material_per_part = total_material / self.good_parts
        
        # Calculate scrap rate
        if self.parts_produced > 0:
            self.scrap_rate = (self.rejected_parts / self.parts_produced) * 100
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.usage_number} - {self.product_name} ({self.production_date})"
    
    def total_material_used(self):
        """Calculate total material used"""
        return self.material_quantity + self.masterbatch_quantity + self.additional_regrind
    
    def material_cost(self):
        """Calculate material cost"""
        cost = float(self.material_type.unit_price) * self.material_quantity
        if self.masterbatch:
            cost += float(self.masterbatch.unit_price) * self.masterbatch_quantity
        return cost


class MaterialRecipe(models.Model):
    """Model for standard material recipes/formulations"""
    recipe_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    mould = models.ForeignKey(Mould, on_delete=models.CASCADE, null=True, blank=True)
    
    # Base material
    base_material = models.ForeignKey(MaterialType, on_delete=models.CASCADE, related_name='recipes')
    base_percentage = models.FloatField(help_text="% of base material")
    
    # Masterbatch
    masterbatch = models.ForeignKey(Masterbatch, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipes')
    masterbatch_percentage = models.FloatField(default=0, help_text="% of masterbatch")
    
    # Regrind
    regrind_material = models.ForeignKey(MaterialType, on_delete=models.SET_NULL, null=True, blank=True, 
                                         related_name='regrind_recipes', limit_choices_to={'category': 'regrind'})
    regrind_percentage = models.FloatField(default=0, help_text="% of regrind")
    
    # Additional info
    total_weight_per_part = models.FloatField(help_text="grams per part", null=True, blank=True)
    color_specification = models.CharField(max_length=200, blank=True)
    
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['recipe_code']
    
    def __str__(self):
        return f"{self.recipe_code} - {self.name}"
    
    def validate_percentages(self):
        """Check if percentages add up to 100"""
        total = self.base_percentage + self.masterbatch_percentage + self.regrind_percentage
        return abs(total - 100) < 0.1  # Allow small rounding errors
