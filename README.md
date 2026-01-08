# Phone Zilla 📱

A modern, robust Django-based Phone Inventory Management System designed for retail shops. Recently modernized to support the latest industry standards.

## 🚀 Project Snapshot (v0.1.0)

This project has undergone a significant modernization effort:
- **Language:** Python 3.12+ (Tested on 3.13.5)
- **Framework:** Django 6.0.1
- **Package Management:** [uv](https://github.com/astral-sh/uv) (Migrated from legacy `requirements.txt`)
- **Admin Interface:** Django JET (via `django-jet-reboot` for modern compatibility)
- **API Support:** Django REST Framework 3.16+
- **Database:** SQLite (Default)

## ✨ Core Features

### 📦 Inventory & Purchase
- **Supplier Management:** Track distributors and contact details.
- **Product Registry:** Catalog mobile brands, models, specifications, and images.
- **Stock Tracking:** Automatic stock updates on purchase and sale.
- **Cost Management:** Track effective costs after discounts.

### 💰 Sales & Invoicing
- **Customer Database:** Manage customer history and contact information.
- **Sales Logging:** Record sales with IMEI tracking and discount calculations.
- **Invoice Generation:** PDF invoice generation for printing (using ReportLab).
- **GST Support:** Built-in GST/Tax calculation (CGST/SGST and IGST).

### 📊 Reports & Filters
- **Smart Filtering:** Filter by mobile brand, IMEI, or product launch date.
- **Search:** Find customers by name, number, address, or device IMEI.
- **Financial Status:** Track payment status (Paid, Pending, Dispute).

## 🛠️ Setup & Development

### Fast Setup with UV:
```bash
# Install uv if you haven't (https://docs.astral-sh.dev/uv/getting-started/installation/)
# Synchronize environment and install all dependencies
uv sync

# Run database migrations
uv run python manage.py migrate

# Create a superuser for admin access
uv run python manage.py createsuperuser

# Start the development server
uv run python manage.py runserver
```

### Management Commands:
We've integrated a shortcut script. You can run management commands as:
- `uv run phonezilla runserver`
- `uv run phonezilla migrate`

## 📂 Project Structure
- `core_settings/`: Main project configuration and URLs.
- `inventory_management/`: Core logic for products, suppliers, and purchases.
- `sale_record/`: Logic for customers, sales, and invoicing.
- `accounts/`: User authentication and profile management.
- `main/`: Base abstract models, serializers, and shared utilities.
- `templates/`: Global UI templates.
- `static/`: CSS, JavaScript, and assets.

## 📝 Recent Modernization Notes (Jan 2026)
- Upgraded from Django 2.0 to **Django 6.0**.
- Replaced legacy `ugettext` with modern `gettext`.
- Migrated from `distutils` to `setuptools` for compilation scripts.
- Removed legacy and broken dependencies (`coreapi`, `easy-select2`).
- Switched to `django-jet-reboot` for stable dashboard support on Python 3.13.
- Cleaned up codebase to remove star imports and implement explicit member importing.

---
*Maintained by Gahan Saraiya*
