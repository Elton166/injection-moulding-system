# 🏭 Injection Moulding Management System

A comprehensive Django-based web application for managing injection moulding production operations, quality control, and maintenance.

![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 🔐 Multi-Level Authentication
- **Company Registration & Login**: Companies can register and manage their operations
- **Employee Management**: Create and manage Manager, Supervisor, and Operator accounts
- **Role-Based Access**: Different permission levels for different roles
- **Session-Based Authentication**: Secure login system with session management

### 🏭 Production Management
- **Mould Run Tracking**: Track active mould operations with setter information and duration
- **Production Orders**: Manage orders with priority levels, due dates, and customer information
- **Shift Production Tracking**: Record production per shift with approval workflow
- **Mould Change Scheduling**: Plan and track mould changes with status updates

### 📊 Material Management
- **Material Types**: Track virgin, regrind, and mixed materials with stock levels
- **Masterbatch Management**: Color and additive tracking with hex color codes
- **Material Recipes**: Standard formulations for consistent production
- **Automatic Calculations**: Auto-calculate material requirements for orders with 5% waste factor
- **Stock Alerts**: Low stock warnings for materials and masterbatches

### ✅ Quality Control
- **Master Sample Management**: Upload and maintain reference samples
- **Product Comparison**: AI-powered image comparison using OpenCV
- **Defect Detection**: Automated defect identification and analysis
- **Hourly Checklists**: Regular quality checks with issue tracking

### 🔧 Issue & Maintenance Management
- **Comprehensive Issue Tracking**: Customer complaints, mould issues, product defects, machine issues
- **Priority Levels**: Critical, High, Medium, Low priority classification
- **Time Tracking**: Track time open, time to resolve, and resolution time
- **Maintenance Job Cards**: Detailed maintenance task management
- **Issue Comments**: Collaborative problem-solving with comment threads

### 🧹 Housekeeping
- **Task Management**: Track cleaning tasks for machines, moulds, and factory areas
- **Before/After Photos**: Document cleaning with image uploads
- **Cleaning Products Tracking**: Record products used and issues found
- **Status Tracking**: Pending, In Progress, Completed status workflow

### 🔍 Troubleshooting Database
- **17 Detailed Issues**: Comprehensive troubleshooting guides based on industry standards
- **10 Defect Types**: Common injection moulding defects with solutions
- **Step-by-Step Solutions**: 10-step resolution guides for each issue
- **Parameter Adjustments**: Specific machine parameter recommendations
- **Prevention Strategies**: Tips to prevent future occurrences

### 📱 Progressive Web App (PWA)
- **Installable**: Add to home screen on mobile devices
- **Offline Capable**: Service worker for offline functionality
- **Unique Icons**: Custom-designed app icons with gradient backgrounds
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Elton166/injection-moulding-system.git
cd injection-moulding-system
```

Or download the ZIP file from the repository.

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Load sample data (optional)**
```bash
python setup_troubleshooting.py
python setup_issues.py
```

8. **Run the development server**
```bash
python manage.py runserver
```

9. **Access the application**
Open your browser and navigate to: `http://127.0.0.1:8000/`

## 📖 Usage Guide

### First Time Setup

1. **Register a Company**
   - Click "Register Company" on the home page
   - Fill in company details and create login credentials
   - Login with your company account

2. **Create Employees**
   - From the company dashboard, click "Register Employee"
   - Create Manager, Supervisor, and Operator accounts
   - Employees can then login with their credentials

3. **Set Up Materials**
   - Navigate to "Materials" in the menu
   - Add material types (virgin, regrind, mixed)
   - Add masterbatches with color codes
   - Create material recipes for standard formulations

4. **Create Production Orders**
   - Go to "Production Orders"
   - Create orders with customer details, quantities, and due dates
   - Assign material recipes to orders
   - System automatically calculates material requirements

5. **Track Production**
   - Start mould runs from the dashboard
   - Record shift production with quantities produced and rejected
   - Supervisors approve shift productions
   - Track order completion progress

### Daily Operations

- **Submit Hourly Checklists**: Regular quality checks
- **Report Issues**: Log problems as they occur
- **Create Job Cards**: Schedule maintenance tasks
- **Record Housekeeping**: Document cleaning activities
- **Compare Products**: Use image comparison for quality control
- **Check Troubleshooting**: Reference guides for common issues

## 🎨 Design Features

- **Funky Modern UI**: Gradient backgrounds and vibrant colors
- **Animated Cards**: Hover effects and smooth transitions
- **Emoji Icons**: Visual indicators throughout the interface
- **Color-Coded Priorities**: Easy identification of urgent items
- **Responsive Layout**: Grid-based design adapts to screen size

## 📁 Project Structure

```
injection-moulding-system/
├── injection_moulding/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── moulding/                    # Main application
│   ├── models.py               # Core models
│   ├── models_auth.py          # Authentication models
│   ├── models_issues.py        # Issue tracking models
│   ├── models_materials.py     # Material management models
│   ├── models_orders.py        # Production order models
│   ├── models_production.py    # Shift production models
│   ├── models_housekeeping.py  # Housekeeping models
│   ├── views.py                # Main views
│   ├── views_auth.py           # Authentication views
│   ├── forms.py                # All forms
│   ├── forms_auth.py           # Authentication forms
│   ├── urls.py                 # URL routing
│   ├── admin.py                # Admin configuration
│   └── utils.py                # Image comparison utilities
├── templates/                   # HTML templates
│   ├── base.html
│   └── moulding/
├── static/                      # Static files (CSS, JS, images)
│   ├── manifest.json
│   ├── service-worker.js
│   └── icons/
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
└── README.md                    # This file
```

## 🛠️ Technologies Used

- **Backend**: Django 5.2.6
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Image Processing**: OpenCV, Pillow
- **Frontend**: HTML5, CSS3, JavaScript
- **PWA**: Service Workers, Web App Manifest
- **Authentication**: Django Auth + Custom Session-Based Auth

## 📊 Database Models

- **Company**: Company registration and management
- **UserProfile**: Employee profiles with roles
- **Mould**: Mould information and specifications
- **MouldRun**: Active mould operation tracking
- **ProductionOrder**: Customer orders and requirements
- **ShiftProduction**: Per-shift production records
- **MaterialType**: Material inventory management
- **Masterbatch**: Color and additive tracking
- **MaterialRecipe**: Standard material formulations
- **Issue**: Comprehensive issue tracking
- **MaintenanceJobCard**: Maintenance task management
- **HousekeepingTask**: Cleaning and housekeeping records
- **TroubleshootingIssue**: Knowledge base for problem-solving
- **HourlyChecklist**: Quality control checklists
- **MasterSample**: Reference samples for comparison
- **ProductComparison**: Quality comparison results

## 🔒 Security Features

- Password hashing for all user accounts
- Session-based authentication
- CSRF protection
- SQL injection prevention (Django ORM)
- XSS protection
- Secure file upload handling

## 📱 Mobile App Conversion

The application is PWA-ready and can be:
- Installed on mobile devices
- Converted to native Android app using tools like:
  - PWA Builder
  - Trusted Web Activity (TWA)
  - Apache Cordova
  - Capacitor

See `ANDROID_APP_GUIDE.md` for detailed instructions.

## 📝 Documentation

- `AUTHENTICATION_GUIDE.md` - Authentication system details
- `MATERIAL_MANAGEMENT_FEATURE.md` - Material management guide
- `MATERIAL_CALCULATION_FEATURE.md` - Automatic calculation details
- `SHIFT_PRODUCTION_TRACKING.md` - Shift production guide
- `HOUSEKEEPING_FEATURE.md` - Housekeeping feature guide
- `TROUBLESHOOTING_DATABASE.md` - Troubleshooting system details
- `NAVIGATION_RESTRICTION.md` - Navigation menu security
- `ICON_DESIGN.md` - App icon design details
- `ANDROID_APP_GUIDE.md` - Mobile app conversion guide

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Elton**
- GitHub: [@Elton166](https://github.com/Elton166)

## 🙏 Acknowledgments

- Industry-standard injection moulding troubleshooting charts
- Django community for excellent documentation
- OpenCV for image processing capabilities

## 📞 Support

For support, please open an issue in the GitHub repository or contact the author.

---

Made with ❤️ for the injection moulding industry
