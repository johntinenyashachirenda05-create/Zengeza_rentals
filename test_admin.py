#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zengeza_rentals.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    admin_user = User.objects.get(username='admin')
    print(f'Admin user found: {admin_user.username}')
    print(f'Role: {admin_user.role}')
    print(f'Superuser: {admin_user.is_superuser}')
    print(f'Staff: {admin_user.is_staff}')
    print(f'Active: {admin_user.is_active}')
except User.DoesNotExist:
    print('Admin user does not exist')
    print('Creating admin user...')
    try:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@zengeza.com',
            password='admin123'
        )
        print('Admin user created successfully')
    except Exception as e:
        print(f'Error creating admin user: {e}')
except Exception as e:
    print(f'Error: {e}')

# Check total users
print(f'Total users: {User.objects.count()}')