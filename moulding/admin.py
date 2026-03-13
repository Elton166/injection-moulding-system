from django.contrib import admin
from .models import (
    Mould, MouldChange, TroubleshootingIssue, TroubleshootingLog,
    HourlyChecklist, MasterSample, ProductComparison, DefectType, MouldRun
)


@admin.register(Mould)
class MouldAdmin(admin.ModelAdmin):
    list_display = ['mould_number', 'name', 'material_type', 'cavity_count', 'is_active']
    list_filter = ['is_active', 'material_type']
    search_fields = ['mould_number', 'name']


@admin.register(MouldChange)
class MouldChangeAdmin(admin.ModelAdmin):
    list_display = ['mould_to', 'machine_number', 'operator', 'status', 'scheduled_time']
    list_filter = ['status', 'scheduled_time']
    search_fields = ['machine_number', 'mould_to__name']


@admin.register(TroubleshootingIssue)
class TroubleshootingIssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['title', 'description']


@admin.register(TroubleshootingLog)
class TroubleshootingLogAdmin(admin.ModelAdmin):
    list_display = ['issue', 'mould', 'machine_number', 'operator', 'resolved', 'created_at']
    list_filter = ['resolved', 'created_at']
    search_fields = ['machine_number', 'description']


@admin.register(HourlyChecklist)
class HourlyChecklistAdmin(admin.ModelAdmin):
    list_display = ['machine_number', 'mould', 'operator', 'check_time', 'issues_found']
    list_filter = ['check_time', 'issues_found']
    search_fields = ['machine_number']


@admin.register(MasterSample)
class MasterSampleAdmin(admin.ModelAdmin):
    list_display = ['sample_number', 'mould', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['sample_number', 'mould__name']


@admin.register(ProductComparison)
class ProductComparisonAdmin(admin.ModelAdmin):
    list_display = ['master_sample', 'operator', 'machine_number', 'similarity_score', 'defects_found', 'approved', 'created_at']
    list_filter = ['defects_found', 'approved', 'created_at']
    search_fields = ['machine_number']


@admin.register(DefectType)
class DefectTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']


@admin.register(MouldRun)
class MouldRunAdmin(admin.ModelAdmin):
    list_display = ['mould', 'machine_number', 'setter_name', 'start_time', 'setter_completion_time', 'is_active', 'created_by']
    list_filter = ['is_active', 'start_time']
    search_fields = ['mould__name', 'machine_number', 'setter_name']


from .models_auth import Company, UserProfile

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'username', 'email']
    exclude = ['password_hash']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'role', 'employee_id', 'department', 'is_active']
    list_filter = ['role', 'is_active', 'company']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id']


from .models_orders import ProductionOrder

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'product_name', 'customer_name', 'mould', 'quantity_ordered', 'quantity_produced', 
                    'material_recipe', 'total_material_required', 'estimated_material_cost', 'priority', 'status', 'due_date']
    list_filter = ['status', 'priority', 'due_date', 'created_at']
    search_fields = ['order_number', 'product_name', 'customer_name']
    date_hierarchy = 'due_date'
    readonly_fields = ['base_material_required', 'masterbatch_required', 'regrind_required', 
                      'total_material_required', 'estimated_material_cost']


from .models_issues import IssueCategory, Issue, MaintenanceJobCard, IssueComment

@admin.register(IssueCategory)
class IssueCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'color']
    list_filter = ['category_type']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['issue_number', 'title', 'category', 'priority', 'status', 'reported_by', 'reported_date']
    list_filter = ['status', 'priority', 'category__category_type', 'reported_date']
    search_fields = ['issue_number', 'title', 'customer_name', 'product_name']
    date_hierarchy = 'reported_date'


@admin.register(MaintenanceJobCard)
class MaintenanceJobCardAdmin(admin.ModelAdmin):
    list_display = ['job_card_number', 'title', 'status', 'priority', 'assigned_to', 'scheduled_date']
    list_filter = ['status', 'priority', 'scheduled_date']
    search_fields = ['job_card_number', 'title', 'machine_number']


@admin.register(IssueComment)
class IssueCommentAdmin(admin.ModelAdmin):
    list_display = ['issue', 'user', 'created_at']
    list_filter = ['created_at']



from .models_housekeeping import HousekeepingTask

@admin.register(HousekeepingTask)
class HousekeepingTaskAdmin(admin.ModelAdmin):
    list_display = ['task_number', 'area_type', 'area_description', 'status', 'assigned_to', 'started_at', 'completed_at']
    list_filter = ['status', 'area_type', 'started_at', 'completed_at']
    search_fields = ['task_number', 'area_description']
    date_hierarchy = 'created_at'



from .models_materials import MaterialType, Masterbatch, MaterialUsage, MaterialRecipe

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'material_grade', 'current_stock', 'minimum_stock', 'is_active']
    list_filter = ['category', 'material_grade', 'is_active']
    search_fields = ['code', 'name', 'material_grade', 'supplier']


@admin.register(Masterbatch)
class MasterbatchAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'type', 'color_name', 'recommended_dosage', 'current_stock', 'is_active']
    list_filter = ['type', 'is_active']
    search_fields = ['code', 'name', 'color_name', 'supplier']


@admin.register(MaterialUsage)
class MaterialUsageAdmin(admin.ModelAdmin):
    list_display = ['usage_number', 'product_name', 'material_type', 'masterbatch', 'parts_produced', 'production_date']
    list_filter = ['production_date', 'shift']
    search_fields = ['usage_number', 'product_name', 'machine_number']
    date_hierarchy = 'production_date'


@admin.register(MaterialRecipe)
class MaterialRecipeAdmin(admin.ModelAdmin):
    list_display = ['recipe_code', 'name', 'product_name', 'base_material', 'masterbatch', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['recipe_code', 'name', 'product_name']



from .models_production import ShiftProduction

@admin.register(ShiftProduction)
class ShiftProductionAdmin(admin.ModelAdmin):
    list_display = ['production_number', 'production_order', 'shift', 'shift_date', 'quantity_produced', 
                    'quantity_rejected', 'scrap_rate', 'production_rate', 'operator', 'approved']
    list_filter = ['shift', 'shift_date', 'approved']
    search_fields = ['production_number', 'production_order__order_number', 'machine_number']
    date_hierarchy = 'shift_date'
    readonly_fields = ['production_number', 'total_quantity', 'scrap_rate', 'production_rate']
