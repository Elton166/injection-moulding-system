from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import models
from .models import (
    Mould, MouldChange, TroubleshootingIssue, TroubleshootingLog,
    HourlyChecklist, MasterSample, ProductComparison, DefectType, MouldRun, ProductionOrder,
    Issue, MaintenanceJobCard, IssueCategory, HousekeepingTask
)
from .forms import (
    MouldChangeForm, TroubleshootingLogForm, HourlyChecklistForm,
    MasterSampleForm, ProductComparisonForm, MouldRunForm, ProductionOrderForm,
    IssueForm, IssueResolveForm, MaintenanceJobCardForm, IssueCommentForm,
    HousekeepingTaskForm, HousekeepingCompleteForm
)
from .utils import compare_images, analyze_defects
import os


def dashboard(request):
    """Main dashboard view.

    If the user is not authenticated and no company session exists,
    redirect to the login/registration landing page.
    """
    # Check if user is logged in (either Django user or company session)
    company_id = request.session.get('company_id')
    user_id = request.session.get('user_id')
    
    if not request.user.is_authenticated and not company_id and not user_id:
        return redirect('login_home')

    context = {
        'active_moulds': Mould.objects.filter(is_active=True).count(),
        'pending_changes': MouldChange.objects.filter(status='planned').count(),
        'open_issues': Issue.objects.filter(status__in=['open', 'in_progress']).count(),
        'recent_checklists': HourlyChecklist.objects.order_by('-check_time')[:5],
        'active_runs': MouldRun.objects.filter(is_active=True).order_by('-start_time'),
        'pending_orders': ProductionOrder.objects.filter(status='pending').order_by('priority', 'due_date'),
        'urgent_orders': ProductionOrder.objects.filter(status='pending', priority='urgent').count(),
        'critical_issues': Issue.objects.filter(status__in=['open', 'in_progress'], priority='critical').count(),
        'open_issues_list': Issue.objects.filter(status__in=['open', 'in_progress']).order_by('-priority', '-reported_date')[:5],
        'pending_housekeeping': HousekeepingTask.objects.filter(status='pending').count(),
        'active_housekeeping': HousekeepingTask.objects.filter(status='in_progress').count(),
    }
    return render(request, 'moulding/dashboard.html', context)


# Mould Change Views
def mould_change_list(request):
    """List all mould changes"""
    changes = MouldChange.objects.all().order_by('-scheduled_time')
    return render(request, 'moulding/mould_change_list.html', {'changes': changes})


def mould_change_create(request):
    """Create new mould change"""
    if request.method == 'POST':
        form = MouldChangeForm(request.POST)
        if form.is_valid():
            change = form.save(commit=False)
            if request.user.is_authenticated:
                change.operator = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                change.operator = default_user
            change.save()
            messages.success(request, 'Mould change scheduled successfully!')
            return redirect('mould_change_list')
    else:
        form = MouldChangeForm()
    return render(request, 'moulding/mould_change_form.html', {'form': form})


def mould_change_update_status(request, pk, status):
    """Update mould change status"""
    change = get_object_or_404(MouldChange, pk=pk)
    change.status = status
    if status == 'in_progress' and not change.start_time:
        change.start_time = timezone.now()
    elif status == 'completed' and not change.end_time:
        change.end_time = timezone.now()
    change.save()
    messages.success(request, f'Mould change status updated to {status}')
    return redirect('mould_change_list')


# Troubleshooting Views
def troubleshooting_list(request):
    """List troubleshooting issues and logs"""
    issues = TroubleshootingIssue.objects.all()
    logs = TroubleshootingLog.objects.all().order_by('-created_at')
    return render(request, 'moulding/troubleshooting_list.html', {
        'issues': issues,
        'logs': logs
    })


def troubleshooting_detail(request, pk):
    """View troubleshooting issue detail"""
    issue = get_object_or_404(TroubleshootingIssue, pk=pk)
    return render(request, 'moulding/troubleshooting_detail.html', {'issue': issue})


def troubleshooting_log_create(request):
    """Create troubleshooting log"""
    if request.method == 'POST':
        form = TroubleshootingLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            if request.user.is_authenticated:
                log.operator = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                log.operator = default_user
            if log.resolved:
                log.resolved_at = timezone.now()
            log.save()
            messages.success(request, 'Troubleshooting log created successfully!')
            return redirect('troubleshooting_list')
    else:
        form = TroubleshootingLogForm()
    return render(request, 'moulding/troubleshooting_log_form.html', {'form': form})


# Hourly Checklist Views
def checklist_list(request):
    """List hourly checklists"""
    checklists = HourlyChecklist.objects.all().order_by('-check_time')
    return render(request, 'moulding/checklist_list.html', {'checklists': checklists})


def checklist_create(request):
    """Create hourly checklist"""
    if request.method == 'POST':
        form = HourlyChecklistForm(request.POST)
        if form.is_valid():
            checklist = form.save(commit=False)
            if request.user.is_authenticated:
                checklist.operator = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                checklist.operator = default_user
            checklist.save()
            messages.success(request, 'Hourly checklist submitted successfully!')
            return redirect('checklist_list')
    else:
        form = HourlyChecklistForm(initial={'check_time': timezone.now()})
    return render(request, 'moulding/checklist_form.html', {'form': form})


# Master Sample and Comparison Views
def master_sample_list(request):
    """List master samples"""
    samples = MasterSample.objects.filter(is_active=True)
    return render(request, 'moulding/master_sample_list.html', {'samples': samples})


def master_sample_create(request):
    """Upload master sample"""
    if request.method == 'POST':
        form = MasterSampleForm(request.POST, request.FILES)
        if form.is_valid():
            sample = form.save(commit=False)
            if request.user.is_authenticated:
                sample.created_by = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                sample.created_by = default_user
            sample.save()
            messages.success(request, 'Master sample uploaded successfully!')
            return redirect('master_sample_list')
    else:
        form = MasterSampleForm()
    return render(request, 'moulding/master_sample_form.html', {'form': form})


def product_comparison_create(request):
    """Compare product with master sample"""
    if request.method == 'POST':
        form = ProductComparisonForm(request.POST, request.FILES)
        if form.is_valid():
            comparison = form.save(commit=False)
            if request.user.is_authenticated:
                comparison.operator = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                comparison.operator = default_user
            comparison.save()
            
            # Perform image comparison
            master_path = comparison.master_sample.image.path
            product_path = comparison.product_image.path
            
            try:
                result = compare_images(master_path, product_path)
                if result:
                    comparison.similarity_score = result['similarity_score']
                    comparison.defects_found = result['defect_count'] > 0
                    
                    # Generate defect description and fix instructions
                    defect_desc, fix_inst = analyze_defects(
                        result['defects'],
                        result['similarity_score']
                    )
                    comparison.defect_description = defect_desc
                    comparison.fix_instructions = fix_inst
                    
                    comparison.save()
                    messages.success(request, f'Comparison complete! Similarity: {result["similarity_score"]}%')
                else:
                    messages.error(request, 'Error comparing images')
            except Exception as e:
                messages.error(request, f'Error during comparison: {str(e)}')
            
            return redirect('comparison_detail', pk=comparison.pk)
    else:
        form = ProductComparisonForm()
    return render(request, 'moulding/product_comparison_form.html', {'form': form})


def comparison_detail(request, pk):
    """View comparison results"""
    comparison = get_object_or_404(ProductComparison, pk=pk)
    return render(request, 'moulding/comparison_detail.html', {'comparison': comparison})


def comparison_list(request):
    """List all comparisons"""
    comparisons = ProductComparison.objects.all().order_by('-created_at')
    return render(request, 'moulding/comparison_list.html', {'comparisons': comparisons})


# Defect Type Views
def defect_types_list(request):
    """List all defect types"""
    defects = DefectType.objects.all()
    return render(request, 'moulding/defect_types_list.html', {'defects': defects})


def defect_type_detail(request, pk):
    """View defect type detail"""
    defect = get_object_or_404(DefectType, pk=pk)
    return render(request, 'moulding/defect_type_detail.html', {'defect': defect})


# Mould Run Views
def mould_run_list(request):
    """List all mould runs"""
    runs = MouldRun.objects.all().order_by('-start_time')
    return render(request, 'moulding/mould_run_list.html', {'runs': runs})


def mould_run_create(request):
    """Create new mould run"""
    if request.method == 'POST':
        form = MouldRunForm(request.POST)
        if form.is_valid():
            run = form.save(commit=False)
            # Use logged in user or create a default user
            if request.user.is_authenticated:
                run.created_by = request.user
            else:
                # Get or create a default user for anonymous submissions
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                run.created_by = default_user
            run.save()
            messages.success(request, 'Mould run started successfully!')
            return redirect('dashboard')
    else:
        form = MouldRunForm(initial={
            'start_time': timezone.now(),
            'setter_completion_time': timezone.now()
        })
    return render(request, 'moulding/mould_run_form.html', {'form': form})


def mould_run_stop(request, pk):
    """Stop a mould run"""
    run = get_object_or_404(MouldRun, pk=pk)
    run.is_active = False
    run.end_time = timezone.now()
    run.save()
    messages.success(request, f'Mould run stopped for {run.mould}')
    return redirect('dashboard')


# Production Order Views
def production_order_list(request):
    """List all production orders"""
    orders = ProductionOrder.objects.all()
    context = {
        'orders': orders,
        'pending': orders.filter(status='pending'),
        'in_progress': orders.filter(status='in_progress'),
        'completed': orders.filter(status='completed'),
    }
    return render(request, 'moulding/production_order_list.html', context)


def production_order_create(request):
    """Create new production order"""
    if request.method == 'POST':
        form = ProductionOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.created_by = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                order.created_by = default_user
            order.save()
            messages.success(request, f'Production order {order.order_number} created successfully!')
            return redirect('dashboard')
    else:
        form = ProductionOrderForm(initial={'order_date': timezone.now().date()})
    return render(request, 'moulding/production_order_form.html', {'form': form})


def production_order_detail(request, pk):
    """View production order details"""
    order = get_object_or_404(ProductionOrder, pk=pk)
    return render(request, 'moulding/production_order_detail.html', {'order': order})


def production_order_update_status(request, pk, status):
    """Update production order status"""
    order = get_object_or_404(ProductionOrder, pk=pk)
    order.status = status
    if status == 'in_progress' and not order.start_date:
        order.start_date = timezone.now().date()
    elif status == 'completed' and not order.completion_date:
        order.completion_date = timezone.now().date()
    order.save()
    messages.success(request, f'Order {order.order_number} status updated to {status}')
    return redirect('production_order_list')


# Issue Management Views
def issue_list(request):
    """List all issues"""
    issues = Issue.objects.all()
    categories = IssueCategory.objects.all()
    
    # Filter by category if provided
    category_filter = request.GET.get('category')
    if category_filter:
        issues = issues.filter(category__category_type=category_filter)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        issues = issues.filter(status=status_filter)
    
    context = {
        'issues': issues,
        'categories': categories,
        'open_issues': issues.filter(status__in=['open', 'in_progress']),
        'resolved_issues': issues.filter(status='resolved'),
        'customer_complaints': issues.filter(category__category_type='customer_complaint'),
        'mould_issues': issues.filter(category__category_type='mould_issue'),
        'product_defects': issues.filter(category__category_type='product_defect'),
        'machine_issues': issues.filter(category__category_type='machine_issue'),
        'maintenance_issues': issues.filter(category__category_type='maintenance'),
    }
    return render(request, 'moulding/issue_list.html', context)


def issue_create(request):
    """Create new issue"""
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            if request.user.is_authenticated:
                issue.reported_by = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                issue.reported_by = default_user
            issue.save()
            messages.success(request, f'Issue {issue.issue_number} created successfully!')
            return redirect('issue_detail', pk=issue.pk)
    else:
        form = IssueForm()
    return render(request, 'moulding/issue_form.html', {'form': form})


def issue_detail(request, pk):
    """View issue details"""
    issue = get_object_or_404(Issue, pk=pk)
    comments = issue.comments.all()
    job_cards = issue.job_cards.all()
    
    if request.method == 'POST':
        comment_form = IssueCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.issue = issue
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                comment.user = default_user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('issue_detail', pk=pk)
    else:
        comment_form = IssueCommentForm()
    
    context = {
        'issue': issue,
        'comments': comments,
        'job_cards': job_cards,
        'comment_form': comment_form,
    }
    return render(request, 'moulding/issue_detail.html', context)


def issue_update_status(request, pk, status):
    """Update issue status"""
    issue = get_object_or_404(Issue, pk=pk)
    issue.status = status
    
    if status == 'in_progress' and not issue.started_date:
        issue.started_date = timezone.now()
    elif status == 'resolved' and not issue.resolved_date:
        issue.resolved_date = timezone.now()
    elif status == 'closed' and not issue.closed_date:
        issue.closed_date = timezone.now()
    
    issue.save()
    messages.success(request, f'Issue {issue.issue_number} status updated to {status}')
    return redirect('issue_detail', pk=pk)


def issue_resolve(request, pk):
    """Resolve an issue"""
    issue = get_object_or_404(Issue, pk=pk)
    
    if request.method == 'POST':
        form = IssueResolveForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.status = 'resolved'
            issue.resolved_date = timezone.now()
            issue.save()
            messages.success(request, f'Issue {issue.issue_number} resolved!')
            return redirect('issue_detail', pk=pk)
    else:
        form = IssueResolveForm(instance=issue)
    
    return render(request, 'moulding/issue_resolve.html', {'form': form, 'issue': issue})


# Maintenance Job Card Views
def job_card_list(request):
    """List all maintenance job cards"""
    job_cards = MaintenanceJobCard.objects.all()
    context = {
        'job_cards': job_cards,
        'pending': job_cards.filter(status='pending'),
        'in_progress': job_cards.filter(status='in_progress'),
        'completed': job_cards.filter(status='completed'),
    }
    return render(request, 'moulding/job_card_list.html', context)


def job_card_create(request):
    """Create new job card"""
    if request.method == 'POST':
        form = MaintenanceJobCardForm(request.POST)
        if form.is_valid():
            job_card = form.save(commit=False)
            if request.user.is_authenticated:
                job_card.created_by = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                job_card.created_by = default_user
            job_card.save()
            messages.success(request, f'Job card {job_card.job_card_number} created!')
            return redirect('job_card_list')
    else:
        form = MaintenanceJobCardForm()
    return render(request, 'moulding/job_card_form.html', {'form': form})


def job_card_update_status(request, pk, status):
    """Update job card status"""
    job_card = get_object_or_404(MaintenanceJobCard, pk=pk)
    job_card.status = status
    
    if status == 'in_progress' and not job_card.started_date:
        job_card.started_date = timezone.now()
    elif status == 'completed' and not job_card.completed_date:
        job_card.completed_date = timezone.now()
    
    job_card.save()
    messages.success(request, f'Job card {job_card.job_card_number} status updated')
    return redirect('job_card_list')


def troubleshooting_chart(request):
    """Comprehensive troubleshooting chart view"""
    issues = TroubleshootingIssue.objects.all()
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        issues = issues.filter(category=category)
    
    return render(request, 'moulding/troubleshooting_chart.html', {'issues': issues})



# Housekeeping Views
def housekeeping_list(request):
    """List all housekeeping tasks"""
    tasks = HousekeepingTask.objects.all()
    context = {
        'tasks': tasks,
        'pending': tasks.filter(status='pending'),
        'in_progress': tasks.filter(status='in_progress'),
        'completed': tasks.filter(status='completed'),
    }
    return render(request, 'moulding/housekeeping_list.html', context)


def housekeeping_create(request):
    """Create new housekeeping task"""
    if request.method == 'POST':
        form = HousekeepingTaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            if request.user.is_authenticated:
                task.assigned_to = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                task.assigned_to = default_user
            task.status = 'in_progress'
            task.started_at = timezone.now()
            task.save()
            messages.success(request, f'Housekeeping task {task.task_number} started!')
            return redirect('housekeeping_detail', pk=task.pk)
    else:
        form = HousekeepingTaskForm()
    return render(request, 'moulding/housekeeping_form.html', {'form': form})


def housekeeping_detail(request, pk):
    """View housekeeping task details"""
    task = get_object_or_404(HousekeepingTask, pk=pk)
    return render(request, 'moulding/housekeeping_detail.html', {'task': task})


def housekeeping_complete(request, pk):
    """Complete housekeeping task with after picture"""
    task = get_object_or_404(HousekeepingTask, pk=pk)
    
    if request.method == 'POST':
        form = HousekeepingCompleteForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.status = 'completed'
            task.completed_at = timezone.now()
            task.save()
            messages.success(request, f'Housekeeping task {task.task_number} completed!')
            return redirect('housekeeping_detail', pk=pk)
    else:
        form = HousekeepingCompleteForm(instance=task)
    
    return render(request, 'moulding/housekeeping_complete.html', {'form': form, 'task': task})



# Material Management Views
from .models_materials import MaterialType, Masterbatch, MaterialUsage, MaterialRecipe
from .forms import MaterialTypeForm, MasterbatchForm, MaterialUsageForm, MaterialRecipeForm


def material_dashboard(request):
    """Material management dashboard"""
    context = {
        'total_materials': MaterialType.objects.filter(is_active=True).count(),
        'virgin_materials': MaterialType.objects.filter(category='virgin', is_active=True).count(),
        'regrind_materials': MaterialType.objects.filter(category='regrind', is_active=True).count(),
        'total_masterbatches': Masterbatch.objects.filter(is_active=True).count(),
        'low_stock_materials': MaterialType.objects.filter(current_stock__lte=models.F('minimum_stock'), is_active=True),
        'low_stock_masterbatches': Masterbatch.objects.filter(current_stock__lte=models.F('minimum_stock'), is_active=True),
        'recent_usages': MaterialUsage.objects.all()[:10],
        'active_recipes': MaterialRecipe.objects.filter(is_active=True)[:10],
    }
    return render(request, 'moulding/material_dashboard.html', context)


# Material Type Views
def material_type_list(request):
    """List all material types"""
    materials = MaterialType.objects.filter(is_active=True)
    context = {
        'materials': materials,
        'virgin': materials.filter(category='virgin'),
        'regrind': materials.filter(category='regrind'),
        'mixed': materials.filter(category='mixed'),
    }
    return render(request, 'moulding/material_type_list.html', context)


def material_type_create(request):
    """Create new material type"""
    if request.method == 'POST':
        form = MaterialTypeForm(request.POST)
        if form.is_valid():
            material = form.save()
            messages.success(request, f'Material {material.code} created successfully!')
            return redirect('material_type_list')
    else:
        form = MaterialTypeForm()
    return render(request, 'moulding/material_type_form.html', {'form': form})


def material_type_detail(request, pk):
    """View material type details"""
    material = get_object_or_404(MaterialType, pk=pk)
    usages = MaterialUsage.objects.filter(material_type=material)[:20]
    recipes = MaterialRecipe.objects.filter(base_material=material)
    
    context = {
        'material': material,
        'usages': usages,
        'recipes': recipes,
    }
    return render(request, 'moulding/material_type_detail.html', context)


# Masterbatch Views
def masterbatch_list(request):
    """List all masterbatches"""
    masterbatches = Masterbatch.objects.filter(is_active=True)
    context = {
        'masterbatches': masterbatches,
        'colors': masterbatches.filter(type='color'),
        'additives': masterbatches.filter(type='additive'),
    }
    return render(request, 'moulding/masterbatch_list.html', context)


def masterbatch_create(request):
    """Create new masterbatch"""
    if request.method == 'POST':
        form = MasterbatchForm(request.POST)
        if form.is_valid():
            masterbatch = form.save()
            messages.success(request, f'Masterbatch {masterbatch.code} created successfully!')
            return redirect('masterbatch_list')
    else:
        form = MasterbatchForm()
    return render(request, 'moulding/masterbatch_form.html', {'form': form})


def masterbatch_detail(request, pk):
    """View masterbatch details"""
    masterbatch = get_object_or_404(Masterbatch, pk=pk)
    usages = MaterialUsage.objects.filter(masterbatch=masterbatch)[:20]
    recipes = MaterialRecipe.objects.filter(masterbatch=masterbatch)
    
    context = {
        'masterbatch': masterbatch,
        'usages': usages,
        'recipes': recipes,
    }
    return render(request, 'moulding/masterbatch_detail.html', context)


# Material Usage Views
def material_usage_list(request):
    """List all material usages"""
    usages = MaterialUsage.objects.all()
    return render(request, 'moulding/material_usage_list.html', {'usages': usages})


def material_usage_create(request):
    """Create new material usage record"""
    if request.method == 'POST':
        form = MaterialUsageForm(request.POST)
        if form.is_valid():
            usage = form.save(commit=False)
            if request.user.is_authenticated:
                usage.operator = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                usage.operator = default_user
            usage.save()
            
            # Update stock levels
            usage.material_type.current_stock -= usage.material_quantity
            usage.material_type.save()
            
            if usage.masterbatch:
                usage.masterbatch.current_stock -= usage.masterbatch_quantity
                usage.masterbatch.save()
            
            messages.success(request, f'Material usage {usage.usage_number} recorded!')
            return redirect('material_usage_list')
    else:
        form = MaterialUsageForm(initial={
            'production_date': timezone.now().date(),
            'start_time': timezone.now()
        })
    return render(request, 'moulding/material_usage_form.html', {'form': form})


def material_usage_detail(request, pk):
    """View material usage details"""
    usage = get_object_or_404(MaterialUsage, pk=pk)
    return render(request, 'moulding/material_usage_detail.html', {'usage': usage})


# Material Recipe Views
def material_recipe_list(request):
    """List all material recipes"""
    recipes = MaterialRecipe.objects.filter(is_active=True)
    return render(request, 'moulding/material_recipe_list.html', {'recipes': recipes})


def material_recipe_create(request):
    """Create new material recipe"""
    if request.method == 'POST':
        form = MaterialRecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            if request.user.is_authenticated:
                recipe.created_by = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                recipe.created_by = default_user
            recipe.save()
            messages.success(request, f'Recipe {recipe.recipe_code} created successfully!')
            return redirect('material_recipe_list')
    else:
        form = MaterialRecipeForm()
    return render(request, 'moulding/material_recipe_form.html', {'form': form})


def material_recipe_detail(request, pk):
    """View material recipe details"""
    recipe = get_object_or_404(MaterialRecipe, pk=pk)
    return render(request, 'moulding/material_recipe_detail.html', {'recipe': recipe})



# Shift Production Tracking Views
from .models_production import ShiftProduction
from .forms import ShiftProductionForm, ShiftProductionApprovalForm


def shift_production_list(request):
    """List all shift productions"""
    productions = ShiftProduction.objects.all()
    
    # Filter by order if provided
    order_id = request.GET.get('order')
    if order_id:
        productions = productions.filter(production_order_id=order_id)
    
    context = {
        'productions': productions,
        'pending_approval': productions.filter(approved=False),
        'approved': productions.filter(approved=True),
    }
    return render(request, 'moulding/shift_production_list.html', context)


def shift_production_create(request):
    """Create new shift production record"""
    if request.method == 'POST':
        form = ShiftProductionForm(request.POST)
        if form.is_valid():
            production = form.save(commit=False)
            if request.user.is_authenticated:
                production.operator = request.user
            else:
                from django.contrib.auth.models import User
                default_user, _ = User.objects.get_or_create(
                    username='operator',
                    defaults={'first_name': 'Default', 'last_name': 'Operator'}
                )
                production.operator = default_user
            production.save()
            messages.success(request, f'Shift production {production.production_number} recorded!')
            return redirect('shift_production_detail', pk=production.pk)
    else:
        # Pre-fill order if provided in URL
        order_id = request.GET.get('order')
        initial = {
            'shift_date': timezone.now().date(),
            'start_time': '08:00',
            'end_time': '16:00',
        }
        if order_id:
            initial['production_order'] = order_id
        form = ShiftProductionForm(initial=initial)
    
    return render(request, 'moulding/shift_production_form.html', {'form': form})


def shift_production_detail(request, pk):
    """View shift production details"""
    production = get_object_or_404(ShiftProduction, pk=pk)
    return render(request, 'moulding/shift_production_detail.html', {'production': production})


def shift_production_approve(request, pk):
    """Approve shift production"""
    production = get_object_or_404(ShiftProduction, pk=pk)
    
    if request.method == 'POST':
        production.approved = True
        if request.user.is_authenticated:
            production.approved_by = request.user
        production.approved_at = timezone.now()
        production.save()
        messages.success(request, f'Shift production {production.production_number} approved!')
        return redirect('shift_production_detail', pk=pk)
    
    return render(request, 'moulding/shift_production_approve.html', {'production': production})


def order_production_summary(request, order_pk):
    """View production summary for an order"""
    order = get_object_or_404(ProductionOrder, pk=order_pk)
    shift_productions = ShiftProduction.objects.filter(production_order=order)
    
    # Calculate totals
    total_produced = shift_productions.filter(approved=True).aggregate(
        total=models.Sum('quantity_produced'))['total'] or 0
    total_rejected = shift_productions.filter(approved=True).aggregate(
        total=models.Sum('quantity_rejected'))['total'] or 0
    
    context = {
        'order': order,
        'shift_productions': shift_productions,
        'total_produced': total_produced,
        'total_rejected': total_rejected,
        'pending_approval': shift_productions.filter(approved=False).count(),
    }
    return render(request, 'moulding/order_production_summary.html', context)


def tutorial(request):
    """Tutorial page with video guides and documentation"""
    return render(request, 'moulding/tutorial.html')
