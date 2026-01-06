from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, Payment, User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q
from .forms import PaymentForm, AddPropertyForm, LoginForm, RegisterForm

def property_detail(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    unlocked = False
    payment = None

    if request.user.is_authenticated and request.user.role == 'tenant':
        payment = Payment.objects.filter(
            tenant=request.user,
            property=prop,
            status='approved'
        ).first()
        if payment and payment.is_active():
            unlocked = True

    context = {
        'property': prop,
        'unlocked': unlocked,
        'payment': payment,
        'agent_fee': prop.rooms * 5  # $5 per room
    }
    return render(request, 'rentals/property_detail.html', context)

# ---------------- AUTHENTICATION VIEWS ----------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'rentals/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'rentals/register.html', {'form': form})

# ---------------- PROPERTY MANAGEMENT ----------------
@login_required
@role_required('landlord')
def add_property(request):
    if request.method == 'POST':
        form = AddPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.landlord = request.user
            prop.status = 'pending'  # admin must approve
            prop.save()
            return redirect('landlord_dashboard')
    else:
        form = AddPropertyForm()

    return render(request, 'rentals/add_property.html', {'form': form})

@login_required
@role_required('landlord')
def edit_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id, landlord=request.user)

    if request.method == 'POST':
        form = AddPropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            return redirect('landlord_dashboard')
    else:
        form = AddPropertyForm(instance=prop)

    return render(request, 'rentals/edit_property.html', {
        'form': form,
        'property': prop
    })

@login_required
@role_required('tenant')
def submit_payment(request, property_id):
    prop = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.tenant = request.user
            payment.property = prop
            payment.amount = prop.rooms * 5
            payment.save()
            return redirect('tenant_dashboard')
    else:
        form = PaymentForm()

    return render(request, 'rentals/submit_payment.html', {
        'form': form,
        'property': prop,
        'amount': prop.rooms * 5
    })

# ---------------- SEARCH AND LISTING ----------------
def property_list(request):
    query = request.GET.get('q', '')
    properties = Property.objects.filter(status='approved')

    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(address__icontains=query) |
            Q(landlord__username__icontains=query)
        )

    return render(request, 'rentals/property_list.html', {
        'properties': properties,
        'query': query
    })

# ---------------- TENANT DASHBOARD ----------------
@login_required
@role_required('tenant')
def tenant_dashboard(request):
    payments = Payment.objects.filter(tenant=request.user).order_by('-approved_at')
    active_unlocks = [p for p in payments if p.is_active()]

    return render(request, 'rentals/tenant_dashboard.html', {
        'payments': payments,
        'active_unlocks': active_unlocks
    })


# ---------------- LANDLORD DASHBOARD ----------------
@login_required
@role_required('landlord')
def landlord_dashboard(request):
    properties = Property.objects.filter(landlord=request.user)

    return render(request, 'rentals/landlord_dashboard.html', {
        'properties': properties
    })


# ---------------- ADMIN DASHBOARD ----------------
@login_required
@role_required('admin')
def admin_dashboard(request):
    pending_properties = Property.objects.filter(status='pending')
    pending_payments = Payment.objects.filter(status='pending')
    landlords = User.objects.filter(role='landlord')
    tenants = User.objects.filter(role='tenant')

    return render(request, 'rentals/admin_dashboard.html', {
        'pending_properties': pending_properties,
        'pending_payments': pending_payments,
        'landlords': landlords,
        'tenants': tenants
    })

# ---------------- APPROVAL VIEWS ----------------
@login_required
@role_required('admin')
def approve_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    prop.status = 'approved'
    prop.save()
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def reject_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)
    prop.status = 'rejected'
    prop.save()
    return redirect('admin_dashboard')

@login_required
@role_required('admin')
def approve_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = 'approved'
    payment.approved_at = timezone.now()
    payment.save()
    return redirect('admin_dashboard')


@login_required
@role_required('admin')
def reject_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.status = 'rejected'
    payment.save()
    return redirect('admin_dashboard')

from django.shortcuts import render
from django.contrib.auth import authenticate

def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'tenant':
            return redirect('property_list')
        elif request.user.role == 'landlord':
            return redirect('landlord_dashboard')
        elif request.user.role == 'admin':
            return redirect('admin_dashboard')
    
    # For non-authenticated users, show welcome page
    return render(request, 'rentals/home.html')

# Create your views here.
