# Django Blog Authentication System

## Overview

This Django blog implements a comprehensive user authentication system with registration, login, logout, and profile management features.

## Features

- User Registration with email validation
- User Login/Logout
- Profile Management
- Password Reset functionality
- CSRF Protection
- Secure password hashing

## Authentication System Components

### 1. User Registration

- **URL**: `/register/`
- **View**: `users.views.register`
- **Template**: `users/templates/users/register.html`
- **Form**: `UserRegisterForm` (extends Django's `UserCreationForm`)
- **Fields**: username, email, first_name, last_name, password1, password2

The registration form includes:

- Email uniqueness validation
- Automatic login after successful registration
- CSRF token protection
- Password strength validation

### 2. User Login

- **URL**: `/login/`
- **View**: Django's built-in `LoginView`
- **Template**: `users/templates/users/login.html`
- Uses Django's authentication backend
- Redirects to home page after successful login

### 3. User Logout

- **URL**: `/logout/`
- **View**: Django's built-in `LogoutView`
- **Template**: `users/templates/users/logout.html`
- Redirects to home page after logout

### 4. Profile Management

- **URL**: `/profile/`
- **View**: `users.views.profile`
- **Template**: `users/templates/users/profile.html`
- **Form**: `UserUpdateForm`
- Requires login (`@login_required` decorator)
- Allows users to update username, email, first_name, and last_name

### 5. Password Reset

- **URLs**: `/password-reset/`, `/password-reset/done/`, etc.
- Uses Django's built-in password reset views
- Sends reset email via console backend (for development)

## Static Files

- **CSS**: `blog/static/blog/css/style.css`
- **JavaScript**: `blog/static/blog/js/main.js`

All authentication templates load these static files using Django's `{% static %}` template tag.

## Security Features

- CSRF tokens on all forms
- Password hashing using Django's built-in algorithms
- Email uniqueness validation
- Login required decorator for protected views
- Secure session management

## Setup Instructions

1. Install dependencies:

```bash
   pip install django
```

Run migrations:

bash python manage.py makemigrations
python manage.py migrate

Collect static files:

bash python manage.py collectstatic

Create superuser (optional):

bash python manage.py createsuperuser

Run development server:

bash python manage.py runserver
