# 🧮 Automatic Material Calculation for Production Orders

## Overview
Production orders now automatically calculate material requirements based on material recipes and order quantities.

---

## ✨ New Features

### 1. **Material Recipe Assignment**
- Link production orders to material recipes
- Specify weight per part (in grams)
- Automatic calculation on save

### 2. **Automatic Calculations**
When you create or update a production order with a recipe and weight per part, the system automatically calculates:

- **Base Material Required** (kg)
- **Masterbatch Required** (kg)
- **Regrind Required** (kg)
- **Total Material Required** (kg)
- **Estimated Material Cost** ($)

### 3. **Stock Availability Check**
- Real-time check if sufficient materials are in stock
- Shows material shortages with exact quantities needed
- Color-coded alerts (green = sufficient, red = shortage)

### 4. **Waste Factor**
- Automatically adds 5% waste factor to calculations
- Accounts for production scrap and setup waste
- More accurate material planning

---

## 📊 How It Works

### Calculation Formula:

```
1. Total Weight = (Weight per Part × Quantity Ordered) / 1000
   (converts grams to kg)

2. Total with Waste = Total Weight × 1.05
   (adds 5% waste factor)

3. Base Material = Total with Waste × (Base Percentage / 100)

4. Masterbatch = Total with Waste × (Masterbatch Percentage / 100)

5. Regrind = Total with Waste × (Regrind Percentage / 100)

6. Total Material = Base + Masterbatch + Regrind

7. Estimated Cost = (Base × Base Price) + (MB × MB Price) + (Regrind × Regrind Price)
```

---

## 🎯 Usage Example

### Scenario:
**Order:** 10,000 bottle caps
**Recipe:** RCP-001 (90% PP-V-001, 2% MB-RED-001, 8% PP-R-001)
**Weight per Part:** 5 grams

### Automatic Calculations:

```
Total Weight = (5g × 10,000) / 1000 = 50 kg
With Waste (5%) = 50 × 1.05 = 52.5 kg

Base Material (PP-V-001):
  52.5 kg × 90% = 47.25 kg

Masterbatch (MB-RED-001):
  52.5 kg × 2% = 1.05 kg

Regrind (PP-R-001):
  52.5 kg × 8% = 4.2 kg

Total Material = 52.5 kg

Estimated Cost:
  (47.25 × $2.50) + (1.05 × $15.00) + (4.2 × $0.50)
  = $118.13 + $15.75 + $2.10
  = $135.98
```

---

## 📱 User Interface Updates

### Production Order Form
**New Fields:**
- **Material Recipe** (dropdown) - Select from available recipes
- **Weight per Part** (number) - Enter weight in grams

**Help Text:**
- "Select recipe to auto-calculate material requirements"
- "Weight in grams (used with recipe for calculations)"

### Production Order Detail Page
**New Section: Material Requirements**

Shows:
- Recipe code and name
- Weight per part
- Calculated requirements breakdown:
  - Base material (kg and %)
  - Masterbatch (kg and %)
  - Regrind (kg and %)
  - Total material (kg)
  - Estimated cost ($)
- Stock availability status:
  - ✅ Green box: "Sufficient materials in stock"
  - ⚠️ Red box: "Material Shortages" with details

### Production Order List
**Updated Display:**
- Shows total material required (kg)
- Shows estimated material cost ($)
- Quick visibility of material needs

---

## 🔔 Stock Availability Alerts

### Sufficient Stock
```
✅ Sufficient materials in stock
```
All required materials are available.

### Material Shortage
```
⚠️ Material Shortages:

PP-V-001: Need 10.50 kg more
(Required: 47.25 kg, Available: 36.75 kg)

MB-RED-001: Need 0.30 kg more
(Required: 1.05 kg, Available: 0.75 kg)
```

Shows exactly how much more material is needed for each component.

---

## 💡 Benefits

### 1. **Accurate Planning**
- Know exact material requirements before starting production
- No guesswork or manual calculations
- Consistent calculations every time

### 2. **Cost Estimation**
- Instant material cost calculation
- Better pricing and quoting
- Profit margin visibility

### 3. **Inventory Management**
- Check stock availability before starting
- Prevent production delays due to material shortages
- Proactive ordering of materials

### 4. **Waste Tracking**
- 5% waste factor built in
- More realistic material planning
- Better inventory accuracy

### 5. **Efficiency**
- Automatic calculations save time
- Reduce errors from manual calculations
- Standardized process

---

## 🔄 Workflow

### Creating an Order with Material Calculation:

1. **Go to Production Orders**
   - Click "New Order"

2. **Fill Basic Information**
   - Order number
   - Product name
   - Customer details
   - Mould selection
   - Quantity ordered

3. **Add Material Information**
   - Select Material Recipe (e.g., RCP-001)
   - Enter Weight per Part (e.g., 5 grams)

4. **Set Priority and Dates**
   - Priority level
   - Due date

5. **Save Order**
   - System automatically calculates:
     - Base material required
     - Masterbatch required
     - Regrind required
     - Total material
     - Estimated cost

6. **View Calculations**
   - Click on order to see detailed breakdown
   - Check stock availability
   - See material shortages if any

7. **Plan Production**
   - Order materials if needed
   - Start production when materials available

---

## 📊 Integration

### Integrated With:

1. **Material Recipes**
   - Uses recipe percentages
   - Links to material types
   - Accesses material pricing

2. **Material Types**
   - Checks current stock levels
   - Uses unit prices for cost calculation
   - Tracks material codes

3. **Masterbatches**
   - Includes in calculations
   - Checks stock availability
   - Calculates costs

4. **Production Dashboard**
   - Shows material requirements
   - Displays cost estimates
   - Highlights shortages

---

## 🎨 Visual Indicators

### Stock Status Colors:
- 🟢 **Green Box** - All materials available
- 🔴 **Red Box** - Material shortages detected

### Priority Colors:
- 🔴 **Red** - Urgent orders
- 🟠 **Orange** - High priority
- 🟢 **Green** - Normal priority
- ⚫ **Gray** - Low priority

---

## 📈 Reporting Capabilities

### Available Data:
- Total material required per order
- Material cost per order
- Material availability status
- Shortage quantities
- Cost estimates for quoting

### Future Enhancements:
- Material consumption reports
- Cost analysis by product
- Material usage trends
- Inventory forecasting

---

## ⚙️ Configuration

### Prerequisites:
1. ✅ Material types must be created
2. ✅ Masterbatches must be created
3. ✅ Material recipes must be defined
4. ✅ Stock levels must be maintained
5. ✅ Unit prices must be set

### Optional:
- Weight per part can be stored in recipe
- Recipes can be product-specific
- Multiple recipes per product possible

---

## 🚀 Quick Start

### Step 1: Create Material Recipe
```
Recipe Code: RCP-001
Product: Bottle Cap
Base Material: PP-V-001 (90%)
Masterbatch: MB-RED-001 (2%)
Regrind: PP-R-001 (8%)
Weight per Part: 5g
```

### Step 2: Create Production Order
```
Order Number: PO-001
Product: Bottle Cap
Quantity: 10,000 pieces
Material Recipe: RCP-001
Weight per Part: 5g
```

### Step 3: View Calculations
```
✅ Automatically calculated:
- Base Material: 47.25 kg
- Masterbatch: 1.05 kg
- Regrind: 4.2 kg
- Total: 52.5 kg
- Cost: $135.98
```

### Step 4: Check Stock
```
✅ Stock availability checked automatically
⚠️ Alerts shown if materials insufficient
```

---

## 📝 Notes

### Waste Factor:
- Default: 5% added to all calculations
- Accounts for setup waste, scrap, and rejects
- Can be adjusted in model if needed

### Calculation Timing:
- Calculations run automatically on save
- Updates when quantity or recipe changes
- Recalculates when weight per part changes

### Stock Deduction:
- Stock is NOT automatically deducted on order creation
- Stock deducted when material usage is recorded
- Allows for planning without affecting inventory

---

## ✅ Status

**Fully Implemented:**
- ✅ Material recipe field in orders
- ✅ Weight per part field
- ✅ Automatic calculations on save
- ✅ Stock availability checking
- ✅ Cost estimation
- ✅ Shortage detection
- ✅ Visual indicators
- ✅ Detailed breakdown display
- ✅ Admin panel integration
- ✅ Database migrations

**Ready to Use:**
- Server running at http://127.0.0.1:8000/
- Create orders at: http://127.0.0.1:8000/production-orders/create/
- View calculations in order details

---

## 🎉 Summary

Production orders now automatically calculate:
- ✅ Exact material requirements (kg)
- ✅ Material costs ($)
- ✅ Stock availability
- ✅ Material shortages
- ✅ Waste factor included (5%)

All based on:
- Material recipes
- Order quantity
- Weight per part

**No manual calculations needed!** 🎯
