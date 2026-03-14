#!/usr/bin/env python3
"""
Security Key Generator for CampusNav API
Generates cryptographically secure random keys for your .env file
"""

import secrets
import string
import sys

def generate_secret_key(length=64):
    """Generate a cryptographically secure random key"""
    return secrets.token_urlsafe(length)

def generate_hex_key(length=32):
    """Generate a hex-encoded secret key"""
    return secrets.token_hex(length)

def generate_api_key(prefix=""):
    """Generate an API key with optional prefix"""
    key = secrets.token_urlsafe(32)
    return f"{prefix}_{key}" if prefix else key

def generate_password(length=24):
    """Generate a strong random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def main():
    print("=" * 60)
    print("🔐 CAMPUSNAV API - SECURITY KEY GENERATOR")
    print("=" * 60)
    print("\nCopy these values to your .env file:\n")
    print("-" * 60)
    
    # Flask Secret Key
    print(f"FLASK_SECRET_KEY={generate_hex_key(32)}")
    
    # JWT Secret Key
    print(f"JWT_SECRET_KEY={generate_secret_key(48)}")
    
    # API Keys
    print(f"\nDEVELOPER_API_KEY={generate_api_key('dev')}")
    print(f"WEBSITE_API_KEY={generate_api_key('web')}")
    
    # Database Password Suggestion
    print(f"\n# Suggested strong database password:")
    print(f"# DB_PASSWORD={generate_password(24)}")
    
    print("\n" + "-" * 60)
    print("\n⚠️  IMPORTANT SECURITY REMINDERS:")
    print("   1. Never commit .env file to git")
    print("   2. Use different keys for dev/staging/production")
    print("   3. Rotate keys regularly (every 90 days)")
    print("   4. Store production keys in secure vault (not .env)")
    print("   5. Never share these keys via email/chat")
    print("\n" + "=" * 60)
    
    # Verify .gitignore
    try:
        with open('.gitignore', 'r') as f:
            if '.env' not in f.read():
                print("\n⚠️  WARNING: .env is not in .gitignore!")
                print("   Add it now to prevent accidental commits")
    except FileNotFoundError:
        print("\n⚠️  WARNING: No .gitignore found!")
        print("   Create one and add .env to it")

if __name__ == "__main__":
    main()