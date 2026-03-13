# Navigation Menu Restriction Feature

## Overview
The navigation menu now only displays full features when a company or employee is logged in. Non-authenticated users see a simplified menu with only Home, Login, and Register Company options.

## Changes Made

### 1. Updated `templates/base.html`
- Modified navigation menu to check for session variables: `request.session.company_id` or `request.session.user_id`
- When logged in: Shows full menu with all features (Dashboard, Materials, Production Orders, Shift Production, Issues, Housekeeping, Job Cards, Mould Runs, Mould Changes, Troubleshooting, Checklists, Master Samples, Comparisons, Defect Types, Logout)
- When not logged in: Shows limited menu (Home, Login, Register Company)

### 2. Updated `moulding/views.py`
- Modified `dashboard()` view to check for both Django authentication and session-based authentication
- Redirects to `login_home` only if user is not authenticated AND no company/user session exists
- Allows access to dashboard for:
  - Django authenticated users (`request.user.is_authenticated`)
  - Company sessions (`request.session.get('company_id')`)
  - Employee sessions (`request.session.get('user_id')`)

### 3. Updated `moulding/views_auth.py`
- Modified `user_login()` view to set `user_id` in session when employee logs in
- Session variables set on employee login:
  - `user_id`: Django user ID
  - `user_role`: Employee role (manager/supervisor/operator)
  - `company_id`: Associated company ID
  - `company_name`: Associated company name

## Session Variables

### Company Login
When a company logs in, the following session variables are set:
- `company_id`: Company database ID
- `company_name`: Company name
- `is_company`: Boolean flag (True)

### Employee Login
When an employee logs in, the following session variables are set:
- `user_id`: Django user ID
- `user_role`: Employee role (manager/supervisor/operator)
- `company_id`: Associated company ID
- `company_name`: Associated company name

## User Experience

### Before Login
1. User visits the application
2. Sees simplified navigation: Home, Login, Register Company
3. Clicking Dashboard redirects to login page
4. Clicking any feature URL redirects to login page

### After Login (Company or Employee)
1. User logs in successfully
2. Full navigation menu appears with all features
3. Can access all application features
4. Logout option available in navigation

## Testing

To test the feature:

1. **Test Non-Authenticated Access:**
   - Open browser in incognito/private mode
   - Visit http://127.0.0.1:8000/
   - Verify only Home, Login, and Register Company links appear
   - Try accessing http://127.0.0.1:8000/dashboard/ - should redirect to login

2. **Test Company Login:**
   - Click "Register Company" or "Login"
   - Login as a company
   - Verify full navigation menu appears
   - Verify all features are accessible

3. **Test Employee Login:**
   - Logout if logged in
   - Click "Login" → "Employee Login"
   - Login as an employee
   - Verify full navigation menu appears
   - Verify all features are accessible

4. **Test Logout:**
   - Click "Logout" in navigation
   - Verify navigation returns to simplified menu
   - Verify dashboard redirects to login page

## Benefits

1. **Security**: Prevents unauthorized access to application features
2. **Clean UI**: Non-authenticated users see a clean, simple interface
3. **Clear Call-to-Action**: Encourages users to register or login
4. **Flexible Authentication**: Supports both company and employee login methods
5. **Session-Based**: Works with custom authentication system (not just Django auth)

## Future Enhancements

Potential improvements:
- Add role-based menu items (show different features based on manager/supervisor/operator role)
- Add company-specific branding in navigation when logged in
- Add user profile dropdown in navigation
- Add notification badges for pending tasks
- Add quick action buttons in navigation
