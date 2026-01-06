#!/usr/bin/env python
"""
Django Secret Key Generator
Run this script to generate a new secure SECRET_KEY for Django
"""
import secrets
import string

def generate_secret_key():
    """Generate a secure Django SECRET_KEY"""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(50))

if __name__ == '__main__':
    secret_key = generate_secret_key()
    print("Generated Django SECRET_KEY:")
    print(f'SECRET_KEY = "{secret_key}"')
    print("\nAdd this to your Django settings.py file.")