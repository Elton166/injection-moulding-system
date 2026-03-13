# 🎨 Material Management System

## Overview
Complete material management system for tracking virgin materials, regrind, masterbatch colors, material usage, and recipes.

---

## ✨ Features Implemented

### 1. **Material Types** 📦
Track all raw materials used in production:

**Categories:**
- ✨ **Virgin Material** - New, unused plastic resin
- ♻️ **Regrind Material** - Recycled/reprocessed material
- 🔀 **Mixed Material** - Combination of virgin and regrind

**Information Tracked:**
- Material code (e.g., PP-V-001, ABS-R-002)
- Material name and grade (PP, ABS, PE, PVC, Nylon)
- Supplier information
- Material properties (density, MFI, moisture content)
- Regrind percentage and source
- Stock levels (current and minimum)
- Unit pricing
- Drying parameters (temperature and time)

### 2. **Masterbatch Management** 🎨
Track color masterbatches and additives:

**Types:**
- 🎨 Color Masterbatch
- ➕ Additive Masterbatch
- 📦 Filler Masterbatch
- ☀️ UV Stabilizer
- 🔥 Flame Retardant

**Information Tracked:**
- Masterbatch code (e.g., MB-RED-001, MB-BLK-002)
- Color name and code (Pantone/RAL)
- Hex color code (#RRGGBB) with color picker
- Supplier and supplier code
- Recommended dosage (min/max percentages)
- Compatible materials
- Stock levels and pricing
- Carrier resin and pigment content

### 3. **Material Usage Tracking** 📊
Record material consumption per production run:

**Tracks:**
- Usage number (auto-generated: MU-00001)
- Mould, machine, and product details
- Material type and quantity used
- Masterbatch and quantity used
- Masterbatch percentage in mix
- Additional regrind usage
- Total regrind percentage
- Parts produced (good/rejected)
- Material per part calculation
- Scrap rate calculation
- Operator, shift, and date
- Production time tracking
- Material cost calculation

### 4. **Material Recipes** 📋
Standard formulations for products:

**Defines:**
- Recipe code and name
- Product and mould association
- Base material and percentage
- Masterbatch and percentage
- Regrind material and percentage
- Total weight per part
- Color specifications
- Percentage validation (must total 100%)

---

## 🎯 Key Capabilities

### Stock Management
- ✅ Track current stock levels
- ✅ Set minimum stock thresholds
- ✅ Low stock alerts (color-coded)
- ✅ Automatic stock deduction on usage
- ✅ Stock status indicators (Good/Medium/Low)

### Material Tracking
- ✅ Virgin vs Regrind tracking
- ✅ Regrind percentage monitoring
- ✅ Material source documentation
- ✅ Supplier management
- ✅ Unit pricing and cost calculation

### Color Management
- ✅ Visual color display (hex codes)
- ✅ Color picker for easy selection
- ✅ Pantone/RAL code tracking
- ✅ Dosage recommendations
- ✅ Compatibility tracking

### Production Efficiency
- ✅ Material per part calculation
- ✅ Scrap rate monitoring
- ✅ Good vs rejected parts tracking
- ✅ Material cost per run
- ✅ Usage history and trends

### Recipe Management
- ✅ Standard formulations
- ✅ Percentage validation
- ✅ Product-specific recipes
- ✅ Mould association
- ✅ Easy recipe lookup

---

## 📱 User Interface

### Material Dashboard
**URL:** `/materials/`

**Shows:**
- Total materials count (Virgin/Regrind breakdown)
- Total masterbatches count
- Low stock alerts
- Recent material usage
- Active recipes
- Quick action buttons

### Material Types
**URLs:**
- List: `/materials/types/`
- Create: `/materials/types/create/`
- Detail: `/materials/types/<id>/`

**Features:**
- Category filtering (Virgin/Regrind/Mixed)
- Stock status indicators
- Detailed material properties
- Usage history per material

### Masterbatches
**URLs:**
- List: `/materials/masterbatch/`
- Create: `/materials/masterbatch/create/`
- Detail: `/materials/masterbatch/<id>/`

**Features:**
- Visual color display
- Type filtering
- Dosage information
- Usage history per masterbatch

### Material Usage
**URLs:**
- List: `/materials/usage/`
- Create: `/materials/usage/create/`
- Detail: `/materials/usage/<id>/`

**Features:**
- Production tracking
- Automatic calculations
- Stock deduction
- Cost tracking

### Material Recipes
**URLs:**
- List: `/materials/recipes/`
- Create: `/materials/recipes/create/`
- Detail: `/materials/recipes/<id>/`

**Features:**
- Standard formulations
- Percentage breakdown
- Product association
- Recipe validation

---

## 💡 Usage Examples

### Example 1: Adding Virgin Material
```
Code: PP-V-001
Name: Polypropylene Virgin Grade A
Category: Virgin Material
Grade: PP
Supplier: ABC Plastics
Current Stock: 500 kg
Minimum Stock: 100 kg
Unit Price: $2.50/kg
Drying Temp: 80°C
Drying Time: 4 hours
```

### Example 2: Adding Regrind Material
```
Code: PP-R-001
Name: Polypropylene Regrind
Category: Regrind Material
Grade: PP
Source: In-house production scrap
Regrind %: 100%
Current Stock: 200 kg
Minimum Stock: 50 kg
Unit Price: $0.50/kg
```

### Example 3: Adding Color Masterbatch
```
Code: MB-RED-001
Name: Red Masterbatch
Type: Color Masterbatch
Color Name: Bright Red
Color Code: RAL 3020
Hex Color: #CC0605
Supplier: ColorTech Inc
Recommended Dosage: 2%
Min Dosage: 1.5%
Max Dosage: 3%
Compatible Materials: PP, PE
Current Stock: 50 kg
```

### Example 4: Recording Material Usage
```
Product: Bottle Cap
Material: PP-V-001 (45 kg)
Masterbatch: MB-RED-001 (1 kg, 2%)
Additional Regrind: 4 kg (8%)
Total Material: 50 kg
Parts Produced: 10,000
Good Parts: 9,800
Rejected Parts: 200
Scrap Rate: 2%
Material per Part: 5.1g
```

### Example 5: Creating Recipe
```
Recipe Code: RCP-001
Name: Red Bottle Cap Formula
Product: Bottle Cap
Base Material: PP-V-001 (90%)
Masterbatch: MB-RED-001 (2%)
Regrind: PP-R-001 (8%)
Total: 100% ✓
Weight per Part: 5g
```

---

## 🎨 Color Coding

### Stock Status
- 🟢 **Green** - Good stock (above 1.5x minimum)
- 🟡 **Yellow** - Medium stock (between minimum and 1.5x)
- 🔴 **Red** - Low stock (at or below minimum)

### Material Categories
- ✨ **Purple Gradient** - Virgin materials
- ♻️ **Pink Gradient** - Regrind materials
- 🔀 **Blue Gradient** - Mixed materials

### Masterbatch Types
- 🎨 **Color** - Color masterbatches
- ➕ **Additive** - Functional additives
- 📦 **Filler** - Filler masterbatches
- ☀️ **UV** - UV stabilizers
- 🔥 **Flame** - Flame retardants

---

## 📊 Calculations

### Automatic Calculations:

1. **Material per Part**
   ```
   Material per Part = Total Material Used / Good Parts
   ```

2. **Scrap Rate**
   ```
   Scrap Rate = (Rejected Parts / Total Parts) × 100%
   ```

3. **Material Cost**
   ```
   Material Cost = (Material Qty × Material Price) + (MB Qty × MB Price)
   ```

4. **Stock Status**
   ```
   Low: Current ≤ Minimum
   Medium: Minimum < Current ≤ 1.5 × Minimum
   Good: Current > 1.5 × Minimum
   ```

5. **Recipe Validation**
   ```
   Base % + Masterbatch % + Regrind % = 100%
   ```

---

## 🔔 Alerts & Notifications

### Low Stock Alerts
- Displayed on material dashboard
- Color-coded cards for each low stock item
- Shows current vs minimum stock
- Separate alerts for materials and masterbatches

### Stock Deduction
- Automatic when recording usage
- Updates material stock levels
- Updates masterbatch stock levels
- Triggers low stock alerts if needed

---

## 📈 Benefits

### Cost Tracking
- ✅ Track material costs per run
- ✅ Monitor regrind usage for cost savings
- ✅ Optimize material mix ratios
- ✅ Identify cost reduction opportunities

### Quality Control
- ✅ Consistent material formulations
- ✅ Standard recipes for products
- ✅ Dosage control for masterbatches
- ✅ Traceability of materials used

### Inventory Management
- ✅ Real-time stock levels
- ✅ Low stock alerts
- ✅ Prevent stockouts
- ✅ Optimize ordering

### Production Efficiency
- ✅ Track material consumption
- ✅ Monitor scrap rates
- ✅ Identify waste reduction opportunities
- ✅ Optimize material usage

### Compliance & Documentation
- ✅ Complete material traceability
- ✅ Usage records for audits
- ✅ Supplier documentation
- ✅ Material specifications

---

## 🎯 Integration

### Integrated With:
- ✅ Mould management
- ✅ Production orders
- ✅ User authentication
- ✅ Admin panel
- ✅ Dashboard

### Data Flow:
```
Material Recipe → Material Usage → Stock Deduction → Low Stock Alert
```

---

## 🚀 Quick Start

### 1. Add Materials
1. Go to Materials → Material Types
2. Click "Add New Material"
3. Enter material details
4. Set stock levels
5. Save

### 2. Add Masterbatches
1. Go to Materials → Masterbatches
2. Click "Add Masterbatch"
3. Enter color/additive details
4. Use color picker for hex code
5. Set dosage recommendations
6. Save

### 3. Create Recipes
1. Go to Materials → Recipes
2. Click "Create Recipe"
3. Select base material
4. Add masterbatch (optional)
5. Add regrind (optional)
6. Ensure percentages total 100%
7. Save

### 4. Record Usage
1. Go to Materials → Usage
2. Click "Record Usage"
3. Select mould and material
4. Enter quantities
5. Add masterbatch if used
6. Enter production numbers
7. Save (stock auto-updates)

---

## 📱 Navigation

Added to main menu: **Materials**

Submenu structure:
- Material Dashboard
- Material Types
- Masterbatches
- Material Usage
- Material Recipes

---

## ✅ Status

**Fully Implemented:**
- ✅ Database models
- ✅ Forms and validation
- ✅ Views and URLs
- ✅ Templates and UI
- ✅ Admin panel integration
- ✅ Navigation menu
- ✅ Stock management
- ✅ Automatic calculations
- ✅ Low stock alerts
- ✅ Color management
- ✅ Recipe validation

**Ready to Use:**
- Server running at http://127.0.0.1:8000/
- Access via: http://127.0.0.1:8000/materials/

---

## 🎉 Summary

Your injection moulding app now has a complete material management system that tracks:
- Virgin and regrind materials with codes
- Masterbatch colors with visual display
- Material usage per production run
- Standard recipes with percentage validation
- Stock levels with automatic alerts
- Material costs and efficiency metrics

All integrated seamlessly with your existing production management system!
