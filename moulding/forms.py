from django import forms
from .models import (
    MouldChange, TroubleshootingLog, HourlyChecklist,
    MasterSample, ProductComparison, MouldRun, HousekeepingTask
)


class MouldChangeForm(forms.ModelForm):
    class Meta:
        model = MouldChange
        fields = ['mould_from', 'mould_to', 'machine_number', 'scheduled_time', 'notes']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class TroubleshootingLogForm(forms.ModelForm):
    class Meta:
        model = TroubleshootingLog
        fields = ['issue', 'mould', 'machine_number', 'description', 'resolution', 'resolved']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'resolution': forms.Textarea(attrs={'rows': 4}),
        }


class HourlyChecklistForm(forms.ModelForm):
    class Meta:
        model = HourlyChecklist
        fields = [
            'mould', 'machine_number', 'check_time',
            'visual_inspection', 'dimensional_check', 'color_consistency', 'surface_finish',
            'temperature_ok', 'pressure_ok', 'cycle_time_ok',
            'material_level_ok', 'material_drying_ok',
            'notes', 'issues_found'
        ]
        widgets = {
            'check_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MasterSampleForm(forms.ModelForm):
    class Meta:
        model = MasterSample
        fields = ['mould', 'sample_number', 'image', 'description', 'specifications']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'specifications': forms.Textarea(attrs={'rows': 4}),
        }


class ProductComparisonForm(forms.ModelForm):
    class Meta:
        model = ProductComparison
        fields = ['master_sample', 'product_image', 'machine_number', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MouldRunForm(forms.ModelForm):
    class Meta:
        model = MouldRun
        fields = ['mould', 'machine_number', 'setter_name', 'start_time', 'setter_completion_time', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'setter_completion_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


from .models_orders import ProductionOrder

class ProductionOrderForm(forms.ModelForm):
    class Meta:
        model = ProductionOrder
        fields = [
            'order_number', 'mould', 'product_name', 'customer_name', 'customer_contact',
            'quantity_ordered', 'unit', 'material_recipe', 'weight_per_part',
            'priority', 'order_date', 'due_date',
            'notes', 'special_requirements'
        ]
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'special_requirements': forms.Textarea(attrs={'rows': 3}),
            'weight_per_part': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'grams per part'}),
        }
        help_texts = {
            'material_recipe': 'Select recipe to auto-calculate material requirements',
            'weight_per_part': 'Weight in grams (used with recipe for calculations)',
        }



from .models_issues import Issue, MaintenanceJobCard, IssueComment

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'issue_number', 'title', 'category', 'description', 'mould', 'machine_number',
            'customer_name', 'product_name', 'priority', 'assigned_to', 'notes'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class IssueResolveForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['resolution', 'root_cause', 'corrective_action', 'preventive_action']
        widgets = {
            'resolution': forms.Textarea(attrs={'rows': 3}),
            'root_cause': forms.Textarea(attrs={'rows': 3}),
            'corrective_action': forms.Textarea(attrs={'rows': 3}),
            'preventive_action': forms.Textarea(attrs={'rows': 3}),
        }


class MaintenanceJobCardForm(forms.ModelForm):
    class Meta:
        model = MaintenanceJobCard
        fields = [
            'job_card_number', 'title', 'description', 'issue', 'machine_number', 'mould',
            'priority', 'assigned_to', 'scheduled_date', 'notes'
        ]
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class IssueCommentForm(forms.ModelForm):
    class Meta:
        model = IssueComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }



class HousekeepingTaskForm(forms.ModelForm):
    class Meta:
        model = HousekeepingTask
        fields = ['area_type', 'area_description', 'before_image', 'before_notes']
        widgets = {
            'before_notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the condition before cleaning...'}),
            'area_description': forms.TextInput(attrs={'placeholder': 'e.g., Machine #5, Mould Storage, Production Floor'}),
        }


class HousekeepingCompleteForm(forms.ModelForm):
    class Meta:
        model = HousekeepingTask
        fields = ['after_image', 'after_notes', 'cleaning_products_used', 'issues_found']
        widgets = {
            'after_notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the condition after cleaning...'}),
            'cleaning_products_used': forms.Textarea(attrs={'rows': 2, 'placeholder': 'List cleaning products used...'}),
            'issues_found': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any issues discovered during cleaning...'}),
        }



from .models_materials import MaterialType, Masterbatch, MaterialUsage, MaterialRecipe


class MaterialTypeForm(forms.ModelForm):
    class Meta:
        model = MaterialType
        fields = ['code', 'name', 'category', 'material_grade', 'supplier', 
                  'density', 'melt_flow_index', 'moisture_content',
                  'regrind_percentage', 'source', 'current_stock', 'minimum_stock', 
                  'unit_price', 'drying_temperature', 'drying_time', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'code': forms.TextInput(attrs={'placeholder': 'e.g., PP-V-001, ABS-R-002'}),
            'material_grade': forms.TextInput(attrs={'placeholder': 'e.g., PP, ABS, PE'}),
        }


class MasterbatchForm(forms.ModelForm):
    class Meta:
        model = Masterbatch
        fields = ['code', 'name', 'type', 'color_name', 'color_code', 'hex_color',
                  'supplier', 'supplier_code', 'recommended_dosage', 'min_dosage', 'max_dosage',
                  'compatible_materials', 'current_stock', 'minimum_stock', 'unit_price',
                  'carrier_resin', 'pigment_content', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'compatible_materials': forms.Textarea(attrs={'rows': 2, 'placeholder': 'e.g., PP, PE, ABS'}),
            'code': forms.TextInput(attrs={'placeholder': 'e.g., MB-RED-001'}),
            'hex_color': forms.TextInput(attrs={'type': 'color'}),
        }


class MaterialUsageForm(forms.ModelForm):
    class Meta:
        model = MaterialUsage
        fields = ['mould', 'machine_number', 'product_name', 'material_type', 'material_quantity',
                  'masterbatch', 'masterbatch_quantity', 'masterbatch_percentage',
                  'additional_regrind', 'regrind_percentage', 'parts_produced', 'good_parts',
                  'rejected_parts', 'shift', 'production_date', 'start_time', 'end_time', 'notes']
        widgets = {
            'production_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class MaterialRecipeForm(forms.ModelForm):
    class Meta:
        model = MaterialRecipe
        fields = ['recipe_code', 'name', 'product_name', 'mould', 'base_material', 'base_percentage',
                  'masterbatch', 'masterbatch_percentage', 'regrind_material', 'regrind_percentage',
                  'total_weight_per_part', 'color_specification', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'recipe_code': forms.TextInput(attrs={'placeholder': 'e.g., RCP-001'}),
        }



from .models_production import ShiftProduction


class ShiftProductionForm(forms.ModelForm):
    class Meta:
        model = ShiftProduction
        fields = ['production_order', 'shift', 'shift_date', 'start_time', 'end_time',
                  'quantity_produced', 'quantity_rejected', 'machine_number', 'supervisor',
                  'downtime_minutes', 'downtime_reason', 'material_used',
                  'notes', 'quality_issues']
        widgets = {
            'shift_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'downtime_reason': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Reason for downtime...'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Shift notes, observations...'}),
            'quality_issues': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any quality issues...'}),
        }
        help_texts = {
            'quantity_produced': 'Number of good parts produced',
            'quantity_rejected': 'Number of rejected/scrap parts',
            'downtime_minutes': 'Total minutes of machine downtime',
            'material_used': 'Total kg of material used (optional)',
        }


class ShiftProductionApprovalForm(forms.ModelForm):
    class Meta:
        model = ShiftProduction
        fields = ['approved']
