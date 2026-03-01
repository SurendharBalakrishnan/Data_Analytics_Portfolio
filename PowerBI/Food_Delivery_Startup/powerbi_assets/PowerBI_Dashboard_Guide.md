# QuickBite Express — Power BI Dashboard Build Guide
## Complete Step-by-Step Instructions (6 Pages)

**Version:** 1.0 | **Tool:** Power BI Desktop (Free) | **Canvas:** 1920 x 1080
SurendharPBIAccoiunt@EbookEducate.onmicrosoft.com
---

## TABLE OF CONTENTS

1. [Initial Setup (One-Time)](#1-initial-setup)
2. [Data Loading & Star Schema](#2-data-loading--star-schema)
3. [Calculated Columns & DAX Measures](#3-calculated-columns--dax-measures)
4. [Page 1: Home / Executive Summary](#4-page-1-home--executive-summary)
5. [Page 2: Orders & Revenue Analytics](#5-page-2-orders--revenue-analytics)
6. [Page 3: Delivery & Operations](#6-page-3-delivery--operations)
7. [Page 4: Ratings & Sentiment](#7-page-4-ratings--sentiment)
8. [Page 5: Customer Loyalty & LTV](#8-page-5-customer-loyalty--ltv)
9. [Page 6: Recovery Recommendations](#9-page-6-recovery-recommendations)
10. [Final Checklist](#10-final-checklist)

---

## 1. INITIAL SETUP

### 1.1 Canvas Size
1. Go to **File → Options and settings → Options → Report settings**
2. Set Canvas: **Custom** → Width: `1920` Height: `1080`
3. Click OK

### 1.2 Apply Background Image
1. Go to **Visualizations pane → Format page** (paint roller icon)
2. Expand **Canvas background**
3. Click **Browse** → Select `background_1920x1080.png`
4. Set **Image fit:** `Fit`
5. Set **Transparency:** `0%`
6. **Repeat this on ALL 6 pages** (copy-paste the settings)

### 1.3 Color Theme (Apply Once, Used Everywhere)
Create a custom theme JSON file or manually apply these colors consistently:

| Element | Hex Code | Usage |
|---------|----------|-------|
| **Navy** | `#1A2744` | Headers, titles, primary bars, sidebar text |
| **Teal** | `#0D8A8A` | KPI cards, accents, secondary bars, positive |
| **Orange** | `#E8743B` | Crisis indicators, alerts, CTA buttons |
| **Soft Blue** | `#5B9BD5` | Supporting charts, secondary series |
| **Red** | `#D94F4F` | Decline, negative, cancellations |
| **Green** | `#2ECC71` | Positive, growth, active |
| **Gray** | `#888888` | Labels, axis text, borders |
| **White** | `#FFFFFF` | Card backgrounds |
| **Background** | `#F0F7F7` | Canvas (already in background image) |

### 1.4 Font Standards
- **Titles:** Segoe UI Bold, 18-20pt, color `#1A2744`
- **Subtitles:** Segoe UI, 12-14pt, color `#888888`
- **KPI Numbers:** Segoe UI Bold, 28-36pt
- **Labels/Axis:** Segoe UI, 10-11pt, color `#888888`
- **Data Labels:** Segoe UI, 9-10pt

### 1.5 Create All 6 Pages
1. At the bottom of Power BI, right-click the page tab
2. Create these 6 pages (rename them):
   - `Home`
   - `Orders & Revenue`
   - `Delivery & Ops`
   - `Ratings & Sentiment`
   - `Customer Loyalty`
   - `Recovery Plan`

---

## 2. DATA LOADING & STAR SCHEMA

### 2.1 Load CSV Files
1. **Home → Get Data → Text/CSV**
2. Load these 8 files (use the CLEANED versions from `output/02_cleaned_data/`):

| File | Table Name in Power BI |
|------|----------------------|
| `fact_orders_clean.csv` | `fact_orders` |
| `fact_order_items_clean.csv` | `fact_order_items` |
| `fact_ratings_clean.csv` | `fact_ratings` |
| `fact_delivery_performance_clean.csv` | `fact_delivery_performance` |
| `dim_customer_clean.csv` | `dim_customer` |
| `dim_restaurant_clean.csv` | `dim_restaurant` |
| `dim_delivery_partner_clean.csv` | `dim_delivery_partner` |
| `dim_menu_item_clean.csv` | `dim_menu_item` |

### 2.2 Power Query Transforms (for each table, do in Transform Data)
**Click "Transform Data" to open Power Query Editor.**

**fact_orders:**
1. Select `order_timestamp` → Change Type → **Date/Time**
2. Add Column → Custom Column → Name: `order_month` → Formula: `= Date.StartOfMonth([order_timestamp])`
3. Add Column → Custom Column → Name: `phase` → Formula:
   ```
   = if [order_timestamp] < #datetime(2025, 6, 1, 0, 0, 0) then "Pre-Crisis" else "Crisis"
   ```
4. Add Column → Custom Column → Name: `is_cancelled_flag` → Formula:
   ```
   = if [is_cancelled] = "Y" then 1 else 0
   ```
5. Ensure `subtotal_amount`, `discount_amount`, `delivery_fee`, `total_amount` are **Decimal Number**

**fact_ratings:**
1. Ensure `rating` is **Decimal Number**
2. Ensure `sentiment_score` is **Decimal Number**

**fact_delivery_performance:**
1. Add Column → Custom Column → Name: `sla_breach` → Formula:
   ```
   = if [actual_delivery_time_mins] > [expected_delivery_time_mins] then 1 else 0
   ```
2. Add Column → Custom Column → Name: `delay_mins` → Formula:
   ```
   = [actual_delivery_time_mins] - [expected_delivery_time_mins]
   ```

**dim_customer:**
1. Change `signup_date` type to **Date** (may need to specify format DD-MM-YYYY)

**dim_restaurant:**
1. Rename `cuisine_type` if it shows as `cusini_type`
2. Ensure `avg_prep_time_min` is **Whole Number** -> issue

**Click "Close & Apply"**

### 2.3 Create Date Table (CRITICAL for Time Intelligence)
1. Go to **Modeling → New Table**
2. Enter this DAX:

```dax
DateTable = 
ADDCOLUMNS(
    CALENDAR(DATE(2025, 1, 1), DATE(2025, 9, 30)),
    "Year", YEAR([Date]),
    "MonthNum", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMM"),
    "MonthYear", FORMAT([Date], "MMM YYYY"),
    "Phase", IF([Date] < DATE(2025, 6, 1), "Pre-Crisis", "Crisis"),
    "MonthSort", YEAR([Date]) * 100 + MONTH([Date])
)
```

3. **Mark as Date Table:** Right-click `DateTable` → Mark as date table → Select `Date` column

### 2.4 Create Relationships (Star Schema)
1. Go to **Model view** (left sidebar icon)
2. Create these relationships by dragging columns:

| From Table | From Column | To Table | To Column | Cardinality |
|------------|-------------|----------|-----------|-------------|
| `fact_orders` | `customer_id` | `dim_customer` | `customer_id` | Many to One |
| `fact_orders` | `restaurant_id` | `dim_restaurant` | `restaurant_id` | Many to One |
| `fact_orders` | `delivery_partner_id` | `dim_delivery_partner` | `delivery_partner_id` | Many to One |
| `fact_orders` | `order_id` | `fact_delivery_performance` | `order_id` | One to One |
| `fact_orders` | `order_id` | `fact_ratings` | `order_id` | One to One |
| `fact_order_items` | `order_id` | `fact_orders` | `order_id` | Many to One |
| `fact_order_items` | `menu_item_id` | `dim_menu_item` | `menu_item_id` | Many to One |
| `DateTable` | `Date` | `fact_orders` | `order_month` | One to Many |

> **Note:** For DateTable → fact_orders, this connects if `order_month` is a date. If you stored it as text, create a `Date.StartOfMonth(order_timestamp)` column instead and link to that.

> **Alternative:** Link `DateTable[Date]` to `fact_orders[order_timestamp]` directly. Power BI will handle the date hierarchy.

3. Set **Cross-filter direction** to **Single** for all relationships
4. Verify the star schema looks correct visually

---

## 3. CALCULATED COLUMNS & DAX MEASURES

### 3.1 Create a Measures Table
1. **Modeling → New Table** → Enter: `_Measures = {BLANK()}`
2. This keeps all measures organized in one place

### 3.2 Core DAX Measures
**Right-click `_Measures` table → New Measure** for each:

```dax
-- ORDER METRICS
Total Orders = COUNTROWS(fact_orders)

Cancelled Orders = CALCULATE(COUNTROWS(fact_orders), fact_orders[is_cancelled] = "Y")

Cancellation Rate = DIVIDE([Cancelled Orders], [Total Orders], 0) * 100

Non-Cancelled Orders = CALCULATE(COUNTROWS(fact_orders), fact_orders[is_cancelled] = "N")
```

```dax
-- REVENUE METRICS
Total Revenue = SUM(fact_orders[total_amount])

Total Subtotal = SUM(fact_orders[subtotal_amount])

Total Discounts = SUM(fact_orders[discount_amount])

Total Delivery Fees = SUM(fact_orders[delivery_fee])

Avg Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

```dax
-- PHASE COMPARISON METRICS
Pre-Crisis Orders = 
CALCULATE([Total Orders], fact_orders[phase] = "Pre-Crisis")

Crisis Orders = 
CALCULATE([Total Orders], fact_orders[phase] = "Crisis")

Pre-Crisis Monthly Avg = DIVIDE([Pre-Crisis Orders], 5, 0)

Crisis Monthly Avg = DIVIDE([Crisis Orders], 4, 0)

Order Decline % = 
DIVIDE([Pre-Crisis Monthly Avg] - [Crisis Monthly Avg], [Pre-Crisis Monthly Avg], 0) * 100
```

```dax
-- REVENUE COMPARISON
Pre-Crisis Revenue = 
CALCULATE([Total Revenue], fact_orders[phase] = "Pre-Crisis")

Crisis Revenue = 
CALCULATE([Total Revenue], fact_orders[phase] = "Crisis")

Revenue Decline % = 
DIVIDE(
    DIVIDE([Pre-Crisis Revenue], 5) - DIVIDE([Crisis Revenue], 4),
    DIVIDE([Pre-Crisis Revenue], 5),
    0
) * 100

Estimated Revenue Loss = 
DIVIDE([Pre-Crisis Revenue], 5) * 4 - [Crisis Revenue]
```

```dax
-- DELIVERY METRICS
Avg Delivery Time = AVERAGE(fact_delivery_performance[actual_delivery_time_mins])

Avg Expected Time = AVERAGE(fact_delivery_performance[expected_delivery_time_mins])

SLA Breach Count = SUM(fact_delivery_performance[sla_breach])

SLA Breach Rate = DIVIDE([SLA Breach Count], COUNTROWS(fact_delivery_performance), 0) * 100

Avg Delay = AVERAGE(fact_delivery_performance[delay_mins])
```

```dax
-- RATING METRICS
Avg Rating = AVERAGE(fact_ratings[rating])

Avg Sentiment = AVERAGE(fact_ratings[sentiment_score])

Total Reviews = COUNTROWS(fact_ratings)

Negative Reviews = CALCULATE(COUNTROWS(fact_ratings), fact_ratings[sentiment_score] < 0)

Negative Review % = DIVIDE([Negative Reviews], [Total Reviews], 0) * 100
```

```dax
-- CUSTOMER METRICS
Unique Customers = DISTINCTCOUNT(fact_orders[customer_id])

Pre-Crisis Customers = 
CALCULATE(DISTINCTCOUNT(fact_orders[customer_id]), fact_orders[phase] = "Pre-Crisis")

Crisis Customers = 
CALCULATE(DISTINCTCOUNT(fact_orders[customer_id]), fact_orders[phase] = "Crisis")

Customer Decline % = 
DIVIDE([Pre-Crisis Customers] - [Crisis Customers], [Pre-Crisis Customers], 0) * 100
```

```dax
-- KPI TREND ARROWS (for card subtitles)
Order Trend Arrow = 
IF([Crisis Monthly Avg] < [Pre-Crisis Monthly Avg], "▼ " & FORMAT([Order Decline %], "0.0") & "% decline", "▲ Growing")

Revenue Trend Arrow = 
IF([Crisis Revenue] < [Pre-Crisis Revenue], "▼ " & FORMAT([Revenue Decline %], "0.0") & "% decline", "▲ Growing")
```

---

## 4. PAGE 1: HOME / EXECUTIVE SUMMARY

### Layout Overview
```
┌──────────┬─────────────────────────────────────────────────────────┐
│ SIDEBAR  │  HEADER: Logo + "Crisis Recovery Dashboard"            │
│          ├─────────┬─────────┬─────────┬─────────┬─────────┐      │
│ Logo     │ KPI 1   │ KPI 2   │ KPI 3   │ KPI 4   │ KPI 5   │      │
│          │ Orders  │ Revenue │ Rating  │ Cancel% │ SLA %   │      │
│ Nav      ├─────────┴─────────┴─────────┴─────────┴─────────┘      │
│ Buttons  │                                                         │
│          │  ┌───────────────────────┐  ┌───────────────────────┐   │
│ [Home]   │  │ Monthly Orders Trend  │  │  City Heatmap         │   │
│ [Orders] │  │ Line Chart            │  │  (Order Decline)      │   │
│ [Deliv]  │  │                       │  │                       │   │
│ [Rate]   │  └───────────────────────┘  └───────────────────────┘   │
│ [Loyal]  │                                                         │
│ [Recov]  │  ┌──── NAV CARDS ─────────────────────────────────┐    │
│          │  │ [Orders] [Delivery] [Ratings] [Loyalty] [Plan] │    │
│          │  └────────────────────────────────────────────────┘    │
│          │  Key Insight Box                                       │
└──────────┴─────────────────────────────────────────────────────────┘
```

### Step-by-Step Build

#### 4.1 Sidebar (Left Panel — already in background image)
The background image has a navy sidebar (0-220px). Place elements on top:

1. **Insert → Image** → Select `logo_sidebar.png`
   - Position: X=`10`, Y=`15`, Width=`200`, Height=`80`

2. **Sidebar Navigation Buttons** (6 buttons):
   For each page, create a **Button**:
   - **Insert → Buttons → Blank**
   - Position/size for each:

   | Button | Y Position | Label Text |
   |--------|-----------|------------|
   | Home | 120 | 🏠 Home |
   | Orders | 195 | 📊 Orders |
   | Delivery | 270 | 🚚 Delivery |
   | Ratings | 345 | ⭐ Ratings |
   | Loyalty | 420 | ❤️ Loyalty |
   | Recovery | 495 | 🎯 Recovery |

   For EACH button:
   - Width: `200`, Height: `60`, X: `10`
   - **Format button:**
     - Fill: `#1A2744` (same as sidebar, or slightly lighter `#243555` for contrast)
     - Border: Off
     - Text: **Segoe UI**, 12pt, **White**, Left aligned
     - Hover fill: `#0D8A8A` (teal)
   - **Action:** Type = **Page navigation** → Destination = corresponding page

3. **Active State:** On the Home page, make the Home button fill color `#0D8A8A` (teal) to show it's active. Repeat on each page for its own button.

#### 4.2 Header Area (Top Bar)
1. **Insert → Text box**
   - Text: `Crisis Recovery Dashboard`
   - Font: Segoe UI Bold, 20pt, color `#1A2744`
   - Position: X=`240`, Y=`12`, Width=`600`, Height=`50`

2. **Insert → Text box** (right side)
   - Text: `QuickBite Express | Jan – Sep 2025`
   - Font: Segoe UI, 12pt, color `#888888`
   - Position: X=`1400`, Y=`18`, Width=`500`, Height=`40`
   - Alignment: Right

#### 4.3 KPI Cards Row (5 cards across the top)
Create **5 Card visuals** in a horizontal row:

**Positions (all Y=`85`, Height=`110`):**

| KPI | X | Width | Value Field | Format |
|-----|---|-------|-------------|--------|
| Total Orders | 240 | 310 | `[Total Orders]` | #,0 |
| Total Revenue | 560 | 310 | `[Total Revenue]` | ₹#,0 |
| Avg Rating | 880 | 310 | `[Avg Rating]` | 0.00 |
| Cancel Rate | 1200 | 310 | `[Cancellation Rate]` | 0.0% |
| SLA Breach | 1520 | 310 | `[SLA Breach Rate]` | 0.0% |

**For EACH card visual:**
1. Drag the measure to the **Fields** well
2. **Format → Visual:**
   - Callout value: Segoe UI Bold, 28pt, color `#1A2744`
   - Category label: Segoe UI, 10pt, color `#888888`
3. **Format → General:**
   - Background: `#FFFFFF`, Transparency `10%`
   - Border: On, color `#E0E0E0`, radius `8`
   - Shadow: On (subtle)
4. **Add subtitle** (optional): Use a **Text box** below each card showing:
   - Orders card: Text = `▼ 61.2% from pre-crisis avg`
   - Revenue card: Text = `▼ ₹19.1M estimated loss`
   - Etc.
   - Font: Segoe UI, 9pt, color `#E8743B` (orange for decline)

#### 4.4 Monthly Orders Trend (Left Chart)
1. **Insert → Line chart**
2. Position: X=`240`, Y=`210`, Width=`820`, Height=`350`
3. **Fields:**
   - X-axis: `fact_orders[order_month]` (or `DateTable[MonthName]`)
   - Y-axis: `[Total Orders]`
4. **Format:**
   - Line color: `#1A2744` (navy)
   - Line width: 3
   - Markers: On, size 8
   - Data labels: On, Segoe UI 10pt
   - Title: "Monthly Order Trend (Jan–Sep 2025)", Segoe UI Bold, 14pt, `#1A2744`
   - X-axis label: "Month", Y-axis label: "Orders"
   - Gridlines: Light gray `#E0E0E0`
5. **Add a Constant Line** (Analytics pane):
   - Value: `22761` (pre-crisis monthly avg)
   - Style: Dashed, color `#1A2744`, transparency 60%
   - Label: "Pre-Crisis Avg"

> **Tip:** To shade the crisis zone, add a shape (Rectangle) behind the chart from Jun-Sep area with orange fill, 5% opacity.

#### 4.5 City Heatmap (Right Chart)
1. **Insert → Matrix** visual
2. Position: X=`1080`, Y=`210`, Width=`810`, Height=`350`
3. **Fields:**
   - Rows: `dim_restaurant[city]`
   - Columns: `fact_orders[order_month]`
   - Values: `[Total Orders]`
4. **Format:**
   - Enable **Conditional formatting** on values:
     - Background color → Rules → Gradient:
       - Min color: `#FFEBEE` (light red, for low values)
       - Max color: `#1A2744` (navy, for high values)
   - Title: "Orders by City & Month", Segoe UI Bold, 14pt
   - Row headers: Segoe UI 11pt
   - Values: Segoe UI 10pt

#### 4.6 Navigation Cards (Bottom Row)
Create **5 clickable cards** for navigation to pages 2-6:

1. For each page, **Insert → Image** → Select the corresponding `card_page{N}.png`
2. Positions (all Y=`580`, Height=`90`):

| Card | X | Width | Image | Navigate To |
|------|---|-------|-------|-------------|
| Orders & Revenue | 240 | 310 | `card_page2.png` | Orders & Revenue page |
| Delivery & Ops | 560 | 310 | `card_page3.png` | Delivery & Ops page |
| Ratings & Sentiment | 880 | 310 | `card_page4.png` | Ratings & Sentiment page |
| Customer Loyalty | 1200 | 310 | `card_page5.png` | Customer Loyalty page |
| Recovery Plan | 1520 | 310 | `card_page6.png` | Recovery Plan page |

3. For each image: **Format → Action → Type: Page navigation → Destination: [page]**

#### 4.7 Key Insight Box (Bottom)
1. **Insert → Text box**
2. Position: X=`240`, Y=`690`, Width=`1680`, Height=`80`
3. Text:
   ```
   💡 KEY INSIGHT: QuickBite experienced a 61.2% order decline and ₹19.1M revenue loss 
   over 4 months (Jun-Sep 2025). Delivery SLA breach rate hit 88%, ratings crashed to 2.5 stars, 
   and 84% of loyal customers churned. Recovery requires urgent action on delivery reliability, 
   food safety, and targeted win-back campaigns.
   ```
4. Font: Segoe UI, 11pt, color `#1A2744`
5. Background: `#FFF3E0` (light orange), Border: `#E8743B`, radius 8

#### 4.8 Filters (Optional - Top Right)
1. **Insert → Slicer** for Phase filter
   - Field: `fact_orders[phase]`
   - Style: **Dropdown** or **Tile**
   - Position: X=`1700`, Y=`85`, Width=`200`, Height=`40`
   - This lets users filter between Pre-Crisis / Crisis / All

---

## 5. PAGE 2: ORDERS & REVENUE ANALYTICS
*Answers: Q1, Q2, Q3, Q8*

### Layout
```
┌──────────┬──────────────────────────────────────────────────────────┐
│ SIDEBAR  │  HEADER: "Orders & Revenue Analytics"                    │
│          ├──────────┬──────────┬──────────┬──────────────────────┐  │
│          │ KPI:     │ KPI:     │ KPI:     │ KPI:                 │  │
│          │ Orders   │ Revenue  │ AOV      │ Decline %            │  │
│          ├──────────┴──────────┴──────────┴──────────────────────┘  │
│          │                                                          │
│          │ ┌──────────────────────┐ ┌──────────────────────────┐   │
│          │ │ Monthly Orders Bar   │ │ Top 5 Cities Decline     │   │
│          │ │ (Q1)                 │ │ Horizontal Bar (Q2)      │   │
│          │ └──────────────────────┘ └──────────────────────────┘   │
│          │                                                          │
│          │ ┌──────────────────────┐ ┌──────────────────────────┐   │
│          │ │ Revenue Breakdown    │ │ Top 10 Restaurant Decline│   │
│          │ │ Stacked Bar (Q8)     │ │ Table (Q3)               │   │
│          │ └──────────────────────┘ └──────────────────────────┘   │
└──────────┴──────────────────────────────────────────────────────────┘
```

### Step-by-Step

#### 5.1 Header
- Copy the sidebar + header format from Page 1
- Change header text to: `Orders & Revenue Analytics`
- Update active nav button to "Orders" (teal fill)

#### 5.2 KPI Cards (Same pattern as Page 1)
4 cards in a row at Y=`85`:

| KPI | Measure | Format |
|-----|---------|--------|
| Total Orders | `[Total Orders]` | #,0 |
| Net Revenue | `[Total Revenue]` | ₹#,0 |
| Avg Order Value | `[Avg Order Value]` | ₹0.00 |
| Order Decline | `[Order Decline %]` | 0.0% |

#### 5.3 Q1: Monthly Orders Bar Chart (Top Left)
1. **Insert → Clustered bar chart** (vertical)
2. Position: X=`240`, Y=`210`, Width=`820`, Height=`310`
3. Fields:
   - X-axis: `fact_orders[order_month]`
   - Y-axis: `[Total Orders]`
   - Legend: `fact_orders[phase]`
4. Format:
   - Pre-Crisis bars: `#1A2744` (navy)
   - Crisis bars: `#E8743B` (orange)
   - Data labels: On, 10pt
   - Title: "Q1: Monthly Orders — Pre-Crisis vs Crisis"

**OR (Alternative - single color with conditional):**
- Use **Conditional formatting** on bar colors:
  - Rules → Based on `phase`: Pre-Crisis = `#1A2744`, Crisis = `#E8743B`

#### 5.4 Q2: Top 5 Cities Decline (Top Right)
1. **Insert → Clustered bar chart** (horizontal)
2. Position: X=`1080`, Y=`210`, Width=`810`, Height=`310`
3. **This requires a pre-calculated table.** Create a DAX table:

```dax
CityDecline = 
VAR PreCrisis = 
    SUMMARIZE(
        FILTER(fact_orders, fact_orders[phase] = "Pre-Crisis"),
        dim_restaurant[city],
        "PreOrders", COUNTROWS(fact_orders)
    )
VAR Crisis = 
    SUMMARIZE(
        FILTER(fact_orders, fact_orders[phase] = "Crisis"),
        dim_restaurant[city],
        "CrisisOrders", COUNTROWS(fact_orders)
    )
RETURN
    ADDCOLUMNS(
        PreCrisis,
        "CrisisOrders", 
            VAR CurrentCity = [city]
            RETURN CALCULATE(COUNTROWS(fact_orders), fact_orders[phase] = "Crisis", dim_restaurant[city] = CurrentCity),
        "DeclinePct",
            VAR CurrentCity = [city]
            VAR PreAvg = DIVIDE([PreOrders], 5)
            VAR CrisisAvg = DIVIDE(
                CALCULATE(COUNTROWS(fact_orders), fact_orders[phase] = "Crisis", dim_restaurant[city] = CurrentCity), 4)
            RETURN DIVIDE(PreAvg - CrisisAvg, PreAvg) * 100
    )
```

**Simpler approach:** Use a **Clustered bar chart** with:
- Y-axis: `dim_restaurant[city]`
- X-axis: `[Total Orders]`
- Legend: `fact_orders[phase]`
- Sort by crisis orders ascending
- Title: "Q2: Orders by City (Pre-Crisis vs Crisis)"
- Add a text box below noting: "Top 5 cities by decline: Chennai (62.5%), Kolkata (61.5%), Bengaluru (61.5%), Hyderabad (61.1%), Ahmedabad (61.0%)"

#### 5.5 Q8: Revenue Breakdown (Bottom Left)
1. **Insert → Stacked bar chart** (vertical)
2. Position: X=`240`, Y=`540`, Width=`820`, Height=`310`
3. Fields:
   - X-axis: `fact_orders[order_month]`
   - Y-axis: `[Total Subtotal]`, `[Total Delivery Fees]`
   - Also add a **Line** for `[Total Discounts]`
4. Format:
   - Subtotal color: `#1A2744`
   - Delivery Fees: `#0D8A8A`
   - Discounts line: `#D94F4F` (red)
   - Title: "Q8: Monthly Revenue Composition"
   - Y-axis format: ₹ with millions

**Alternative:** Use a **Waterfall chart** to show revenue flow:
- Category: `[Subtotal, -Discounts, +Delivery Fee, = Net Revenue]`
- For Pre-Crisis vs Crisis periods

#### 5.6 Q3: Top 10 Restaurant Decline Table (Bottom Right)
1. **Insert → Table** visual
2. Position: X=`1080`, Y=`540`, Width=`810`, Height=`310`
3. Fields:
   - `dim_restaurant[restaurant_name]`
   - `dim_restaurant[city]`
   - `dim_restaurant[cuisine_type]`
   - Pre-Crisis Orders (measure filtered to phase)
   - Crisis Orders (measure filtered to phase)
4. Format:
   - Alternating row colors: White / `#F0F7F7`
   - Header: `#1A2744` background, white text
   - Title: "Q3: Top 10 Restaurants — Largest Decline"
   - Sort by decline descending
   - Note: Add a text box clarifying "Min 10+ pre-crisis orders (dataset max ~21/restaurant)"

#### 5.7 Phase Slicer (Top Right Corner)
- Same slicer as Page 1 → Sync across pages:
  **View → Sync slicers** → Check all pages

---

## 6. PAGE 3: DELIVERY & OPERATIONS
*Answers: Q4, Q5*

### Layout
```
┌──────────┬──────────────────────────────────────────────────────────┐
│ SIDEBAR  │  HEADER: "Delivery & Operations Performance"            │
│          ├──────────┬──────────┬──────────┬──────────────────────┐  │
│          │ Avg Del  │ SLA      │ Cancel   │ Avg Delay            │  │
│          │ Time     │ Breach%  │ Rate     │ (mins)               │  │
│          ├──────────┴──────────┴──────────┴──────────────────────┘  │
│          │                                                          │
│          │ ┌──────────────────────────────────────────────────┐    │
│          │ │ Q5: Delivery Time — Actual vs Expected           │    │
│          │ │ Dual-Line Chart with Area Fill                    │    │
│          │ └──────────────────────────────────────────────────┘    │
│          │                                                          │
│          │ ┌──────────────────────┐ ┌──────────────────────────┐   │
│          │ │ Q4: Cancellation     │ │ Q4b: City Cancellation   │   │
│          │ │ Rate Trend Line      │ │ Heatmap (Matrix)         │   │
│          │ └──────────────────────┘ └──────────────────────────┘   │
└──────────┴──────────────────────────────────────────────────────────┘
```

### Step-by-Step

#### 6.1 KPI Cards (4 cards)

| KPI | Measure | Format | Card Accent |
|-----|---------|--------|-------------|
| Avg Delivery Time | `[Avg Delivery Time]` | 0.0 mins | Red if > 45 |
| SLA Breach Rate | `[SLA Breach Rate]` | 0.0% | Red if > 70% |
| Cancellation Rate | `[Cancellation Rate]` | 0.0% | Orange |
| Avg Delay | `[Avg Delay]` | 0.0 mins | Red if > 10 |

#### 6.2 Q5: Delivery Time Dual-Line Chart (Full Width)
1. **Insert → Line chart**
2. Position: X=`240`, Y=`210`, Width=`1680`, Height=`280`
3. Fields:
   - X-axis: `fact_orders[order_month]`
   - Y-axis (Line 1): `[Avg Delivery Time]` (Actual)
   - Y-axis (Line 2): `[Avg Expected Time]`
4. Format:
   - Actual line: `#D94F4F` (red), width 3, markers on
   - Expected line: `#0D8A8A` (teal), width 3, markers on
   - Data labels: On
   - Title: "Q5: Avg Delivery Time — Actual vs Expected (SLA)"
   - Add **Constant line** at 45 mins (reference threshold)
5. **Add Analytics:**
   - Add a **Reference Band** or text annotation showing "Pre-Crisis: 39.5 min → Crisis: 60.1 min"

#### 6.3 Q4: Cancellation Rate Trend (Bottom Left)
1. **Insert → Line chart**
2. Position: X=`240`, Y=`510`, Width=`820`, Height=`280`
3. Fields:
   - X-axis: `fact_orders[order_month]`
   - Y-axis: `[Cancellation Rate]`
4. Format:
   - Line color: `#D94F4F` (red)
   - Width: 3, Markers: On (size 8)
   - Data labels: On, showing percentages
   - Title: "Q4: Monthly Cancellation Rate"
   - Add constant lines for Pre-Crisis avg (6.1%) and Crisis avg (11.9%)

#### 6.4 Q4b: City Cancellation Heatmap (Bottom Right)
1. **Insert → Matrix** visual
2. Position: X=`1080`, Y=`510`, Width=`810`, Height=`280`
3. Fields:
   - Rows: `dim_restaurant[city]`
   - Columns: `fact_orders[order_month]`
   - Values: `[Cancellation Rate]`
4. Format:
   - **Conditional formatting** on values:
     - Background color gradient: Green (low) → Yellow → Red (high)
     - Min: 5%, Max: 14%
   - Title: "Q4b: Cancellation Rate by City & Month"

---

*Continued in Part 2...*

## 7. PAGE 4: RATINGS & SENTIMENT
*Answers: Q6, Q7*

### Layout
```
┌──────────┬──────────────────────────────────────────────────────────┐
│ SIDEBAR  │  HEADER: "Customer Ratings & Sentiment"                  │
│          ├──────────┬──────────┬──────────┬──────────────────────┐  │
│          │ Avg      │ Avg      │ Total    │ Negative             │  │
│          │ Rating   │ Sentiment│ Reviews  │ Review %             │  │
│          ├──────────┴──────────┴──────────┴──────────────────────┘  │
│          │                                                          │
│          │ ┌──────────────────────────────────────────────────┐    │
│          │ │ Q6: Monthly Rating + Sentiment Trend             │    │
│          │ │ Combo Chart (Line + Bar)                          │    │
│          │ └──────────────────────────────────────────────────┘    │
│          │                                                          │
│          │ ┌──────────────────────┐ ┌──────────────────────────┐   │
│          │ │ Q6b: Rating          │ │ Q7: Word Cloud /         │   │
│          │ │ Distribution Grouped │ │ Top Keywords Bar Chart   │   │
│          │ │ Bar Chart            │ │                           │   │
│          │ └──────────────────────┘ └──────────────────────────┘   │
└──────────┴──────────────────────────────────────────────────────────┘
```

### Step-by-Step

#### 7.1 KPI Cards (4 cards)

| KPI | Measure | Format | Color Rule |
|-----|---------|--------|------------|
| Avg Rating | `[Avg Rating]` | 0.00 ★ | Red if < 3.0 |
| Avg Sentiment | `[Avg Sentiment]` | +0.00 | Red if < 0 |
| Total Reviews | `[Total Reviews]` | #,0 | Navy |
| Negative % | `[Negative Review %]` | 0.0% | Red if > 50% |

#### 7.2 Q6: Monthly Rating + Sentiment Combo Chart (Full Width)
1. **Insert → Line and clustered column chart** (Combo chart)
2. Position: X=`240`, Y=`210`, Width=`1680`, Height=`280`
3. Fields:
   - Shared axis: `fact_orders[order_month]`
   - Column series: `[Avg Sentiment]` (bars)
   - Line series: `[Avg Rating]` (line)
4. Format:
   - Column color: Use **Conditional formatting**:
     - Positive sentiment (> 0): `#0D8A8A` (teal)
     - Negative sentiment (< 0): `#D94F4F` (red)
   - Line: `#1A2744` (navy), width 3, markers on (size 8)
   - Data labels: On for both
   - Title: "Q6: Monthly Avg Rating & Sentiment Score"
   - Secondary Y-axis for Sentiment (-0.5 to +1.0)
   - Primary Y-axis for Rating (1.0 to 5.0)

#### 7.3 Q6b: Rating Distribution (Bottom Left)
1. **Insert → Clustered column chart**
2. Position: X=`240`, Y=`510`, Width=`820`, Height=`280`
3. **You'll need a measure for each star bucket.** Create:

```dax
1-Star Reviews = CALCULATE(COUNTROWS(fact_ratings), fact_ratings[rating] >= 0.5, fact_ratings[rating] < 1.5)
2-Star Reviews = CALCULATE(COUNTROWS(fact_ratings), fact_ratings[rating] >= 1.5, fact_ratings[rating] < 2.5)
3-Star Reviews = CALCULATE(COUNTROWS(fact_ratings), fact_ratings[rating] >= 2.5, fact_ratings[rating] < 3.5)
4-Star Reviews = CALCULATE(COUNTROWS(fact_ratings), fact_ratings[rating] >= 3.5, fact_ratings[rating] < 4.5)
5-Star Reviews = CALCULATE(COUNTROWS(fact_ratings), fact_ratings[rating] >= 4.5)
```

**Alternative (Simpler):** Add a calculated column in `fact_ratings`:
```dax
Rating Bucket = ROUND(fact_ratings[rating], 0)
```

Then use:
- X-axis: `fact_ratings[Rating Bucket]`
- Y-axis: Count of reviews
- Legend: `fact_orders[phase]` (requires relationship)
- Colors: Pre-Crisis = `#1A2744`, Crisis = `#D94F4F`
- Title: "Q6b: Rating Distribution — Pre-Crisis vs Crisis"

#### 7.4 Q7: Word Cloud / Keyword Bar Chart (Bottom Right)
**Option A: Word Cloud (Recommended — Power BI has a Word Cloud visual)**

1. **Get the Word Cloud visual:**
   - Click **"..."** in Visualizations pane → **Get more visuals**
   - Search "Word Cloud" → Add the **Microsoft Word Cloud**
2. Position: X=`1080`, Y=`510`, Width=`810`, Height=`280`
3. Fields:
   - Category: `fact_ratings[review_text]`
4. **Important Filter:** Add a page-level filter:
   - `fact_orders[phase]` = "Crisis"
   - `fact_ratings[sentiment_score]` < 0
5. Format:
   - Max words: 80
   - Min font size: 12, Max font size: 60
   - Colors: Use `#D94F4F` (red) for negative impact feel
   - Title: "Q7: Negative Review Keywords (Crisis Period)"
6. **Stop Words:** In the Word Cloud settings, add stop words:
   `the, is, was, a, an, and, or, but, in, on, at, to, for, of, with, it, not, this, that, i, my, me, very, than`

**Option B: Horizontal Bar Chart (if Word Cloud visual unavailable)**
1. **Pre-calculate keywords** — use the `Q7_keywords.csv` from notebook output
2. Load as a separate table: `keyword_freq`
3. **Insert → Clustered bar chart** (horizontal)
4. Fields:
   - Y-axis: `keyword_freq[keyword]`
   - X-axis: `keyword_freq[count]`
5. Sort by count descending, Top N = 15
6. Color: `#D94F4F`
7. Title: "Q7: Top 15 Negative Keywords"

---

## 8. PAGE 5: CUSTOMER LOYALTY & LTV
*Answers: Q9, Q10*

### Layout
```
┌──────────┬──────────────────────────────────────────────────────────┐
│ SIDEBAR  │  HEADER: "Customer Loyalty & Lifetime Value"             │
│          ├──────────┬──────────┬──────────┬──────────────────────┐  │
│          │ Unique   │ Customer │ Loyal    │ High-Value           │  │
│          │ Customers│ Decline% │ Churned  │ Churned              │  │
│          ├──────────┴──────────┴──────────┴──────────────────────┘  │
│          │                                                          │
│          │ ┌──────────────────────┐ ┌──────────────────────────┐   │
│          │ │ Q9: Loyal Customer   │ │ Q9b: High-Rating         │   │
│          │ │ Churn Donut Chart    │ │ Churners Donut           │   │
│          │ └──────────────────────┘ └──────────────────────────┘   │
│          │                                                          │
│          │ ┌──────────────────────┐ ┌──────────────────────────┐   │
│          │ │ Q10: High-Value      │ │ Q10b: Patterns —         │   │
│          │ │ Customer Churn %     │ │ City & Cuisine Bars      │   │
│          │ │ Big Number + Context │ │                           │   │
│          │ └──────────────────────┘ └──────────────────────────┘   │
└──────────┴──────────────────────────────────────────────────────────┘
```

### Step-by-Step

#### 8.1 KPI Cards

| KPI | Value | Format |
|-----|-------|--------|
| Unique Customers | `[Unique Customers]` | #,0 |
| Customer Decline | `[Customer Decline %]` | 0.0% |
| Loyal Churned | `49 of 58` (text card) | — |
| High-Value Churned | `3,648 of 4,342` (text card) | — |

> **Note:** For Q9 and Q10 metrics, you may want to use **Card with text** or **Multi-row Card** since these are specific computed values.

#### 8.2 Creating Q9 Measures

```dax
Loyal Customers = 
VAR LoyalList = 
    CALCULATETABLE(
        VALUES(fact_orders[customer_id]),
        fact_orders[phase] = "Pre-Crisis",
        FILTER(
            SUMMARIZE(fact_orders, fact_orders[customer_id], "OrderCount", COUNTROWS(fact_orders)),
            [OrderCount] >= 5
        )
    )
RETURN COUNTROWS(LoyalList)
```

**Simpler approach — use pre-computed values from our Python analysis:**

Create a **manual table** for Q9/Q10 display:
1. **Modeling → New Table:**

```dax
LoyaltyMetrics = 
DATATABLE(
    "Metric", STRING,
    "Value", INTEGER,
    {
        {"Loyal Customers (5+ orders)", 58},
        {"Churned Loyal", 49},
        {"Still Active Loyal", 9},
        {"High-Rating Churners (>4.5★)", 26},
        {"Top 5% Customers", 4342},
        {"Top 5% Churned", 3648},
        {"Top 5% Still Active", 694}
    }
)
```

#### 8.3 Q9: Loyal Customer Churn Donut (Top Left)
1. **Insert → Donut chart**
2. Position: X=`240`, Y=`210`, Width=`410`, Height=`310`
3. Fields (from LoyaltyMetrics table):
   - Use a filtered version: Legend = Churned / Active
   - Values: 49 / 9

**Alternative approach:**
1. Create another simple table:

```dax
LoyalChurn = 
DATATABLE(
    "Status", STRING,
    "Count", INTEGER,
    {
        {"Churned", 49},
        {"Still Active", 9}
    }
)
```

2. Donut chart: Legend = `Status`, Values = `Count`
3. Format:
   - Churned: `#D94F4F` (red)
   - Active: `#2ECC71` (green)
   - Inner radius: 60%
   - Data labels: Name + Value + %
   - Title: "Q9: Loyal Customer Status (5+ Pre-Crisis Orders)"

#### 8.4 Q9b: High-Rating Churners Donut (Top Right)
1. **Insert → Donut chart**
2. Position: X=`670`, Y=`210`, Width=`410`, Height=`310`
3. Create table:

```dax
ChurnerRatings = 
DATATABLE(
    "Rating Group", STRING,
    "Count", INTEGER,
    {
        {"Avg Rating > 4.5", 26},
        {"Avg Rating ≤ 4.5", 22},
        {"No Rating Data", 1}
    }
)
```

4. Format:
   - Rating > 4.5: `#E8743B` (orange — high priority targets)
   - Rating ≤ 4.5: `#1A2744` (navy)
   - No Rating: `#888888`
   - Title: "Q9b: Churned Loyal — Rating Breakdown"

#### 8.5 Q9 Insight Box (Top Right Area)
1. **Insert → Text box**
2. Position: X=`1100`, Y=`210`, Width=`790`, Height=`310`
3. Text:
   ```
   🔑 LOYALTY FINDINGS

   • 58 customers placed 5+ orders before the crisis
   • 49 of them (84.5%) STOPPED ordering during crisis
   • 26 of those had avg rating > 4.5 — they LOVED the service

   ⚡ ACTION: These 26 high-rating churners are the #1 
   win-back priority. They were satisfied before — a 
   personalized cashback + food safety guarantee could 
   bring them back.

   • Top 5% spenders (4,342 customers, ₹923+ spend)
   • 3,648 (84%) churned completely
   • Rating dropped from 4.51★ to 2.51★
   ```
4. Font: Segoe UI, 11pt, color `#1A2744`
5. Background: `#FFFFFF`, Border: `#0D8A8A`

#### 8.6 Q10: High-Value Churn Chart (Bottom Left)
1. **Insert → Donut chart**
2. Position: X=`240`, Y=`540`, Width=`410`, Height=`310`
3. Table:

```dax
HighValueChurn = 
DATATABLE(
    "Status", STRING,
    "Count", INTEGER,
    {
        {"Churned", 3648},
        {"Still Active", 694}
    }
)
```

4. Format same as Q9 donut (red/green)
5. Title: "Q10: Top 5% Spenders — Churn Status"

#### 8.7 Q10b: Patterns (Bottom Right)
1. **Insert → Clustered bar chart** (horizontal)
2. Position: X=`670`, Y=`540`, Width=`550`, Height=`310`
3. **This shows city distribution of top 5% customers**
4. From the pre-computed analysis, create:

```dax
TopCustCities = 
DATATABLE(
    "City", STRING,
    "Orders", INTEGER,
    {
        {"Bengaluru", 3019},
        {"Mumbai", 1940},
        {"Delhi", 1907},
        {"Chennai", 1279},
        {"Hyderabad", 1253},
        {"Kolkata", 992},
        {"Pune", 751},
        {"Ahmedabad", 640}
    }
)
```

5. Fields: Y-axis = City, X-axis = Orders
6. Color: `#1A2744`, Title: "Q10b: Top 5% — City Distribution"

#### 8.8 Q10 Rating Comparison Cards (Bottom Far Right)
1. Two **Card** visuals stacked:
   - Card 1: "Pre-Crisis Rating: 4.51 ★" — Teal card
   - Card 2: "Crisis Rating: 2.51 ★" — Red card
2. Position: X=`1240`, Y=`540`, Width=`650`, Height=`140` each
3. Add a text box: "2-star drop in satisfaction"

---

## 9. PAGE 6: RECOVERY RECOMMENDATIONS
*Answers: Secondary Research S1-S5, Extra E1-E3*

### Layout
```
┌──────────┬──────────────────────────────────────────────────────────┐
│ SIDEBAR  │  HEADER: "Recovery Recommendations & Action Plan"        │
│          ├──────────────────────────────────────────────────────────┤
│          │                                                          │
│          │ ┌──────────────────────────────────────────────────┐    │
│          │ │ PRIORITY MATRIX                                   │    │
│          │ │ ┌──────────┐ ┌──────────┐ ┌──────────┐          │    │
│          │ │ │ IMMEDIATE │ │ SHORT    │ │ LONG     │          │    │
│          │ │ │ (0-30d)   │ │ (1-3mo)  │ │ (3-6mo)  │          │    │
│          │ │ └──────────┘ └──────────┘ └──────────┘          │    │
│          │ └──────────────────────────────────────────────────┘    │
│          │                                                          │
│          │ ┌──────────────────────┐ ┌──────────────────────────┐   │
│          │ │ Strategy Cards       │ │ Risk Matrix              │   │
│          │ │ (S1-S5 findings)     │ │ City Priority            │   │
│          │ └──────────────────────┘ └──────────────────────────┘   │
│          │                                                          │
│          │ ┌──────────────────────────────────────────────────┐    │
│          │ │ KEY RECOMMENDATIONS SUMMARY                       │    │
│          │ └──────────────────────────────────────────────────┘    │
└──────────┴──────────────────────────────────────────────────────────┘
```

### Step-by-Step

#### 9.1 This page is primarily TEXT + SHAPES (strategic, not data-heavy)

#### 9.2 Priority Matrix (Top Section)
Create **3 rectangular shapes** (Insert → Shapes → Rectangle):

**Card 1: IMMEDIATE (0-30 days)**
- Position: X=`240`, Y=`100`, Width=`540`, Height=`280`
- Fill: `#D94F4F` with 90% opacity
- Text (use text boxes inside):
  ```
  🚨 IMMEDIATE (0-30 Days)
  
  1. Fix Delivery SLA — Target <45 min avg
  2. Launch "Food Safety Verified" badge
  3. Send win-back SMS to 26 high-rating churners
  4. Pause new customer acquisition (CAC is 3x)
  5. Emergency audit of top complaint restaurants
  ```
- Font: Segoe UI, 11pt, White

**Card 2: SHORT-TERM (1-3 months)**
- Position: X=`800`, Y=`100`, Width=`540`, Height=`280`
- Fill: `#E8743B` with 90% opacity
- Text:
  ```
  ⚡ SHORT-TERM (1-3 Months)
  
  1. Cashback campaign (₹100 off next 3 orders)
  2. Restaurant partner retention program
  3. Monsoon delivery infrastructure upgrade
  4. Real-time delivery tracking + SLA guarantee
  5. Weekly food safety report to customers
  ```

**Card 3: LONG-TERM (3-6 months)**
- Position: X=`1360`, Y=`100`, Width=`540`, Height=`280`
- Fill: `#0D8A8A` with 90% opacity
- Text:
  ```
  🎯 LONG-TERM (3-6 Months)
  
  1. AI-powered delivery route optimization
  2. Restaurant quality scoring system
  3. Customer loyalty tier program
  4. Competitive pricing analysis (vs Swiggy/Zomato)
  5. Expand cloud kitchen partnerships
  ```

#### 9.3 Strategy Cards (Bottom Left)
Create text boxes for each secondary research finding:

**S1: Competitor Comparison**
- Text box with key finding from secondary research

**S3: Trust Rebuilding Strategies**
- Food safety certification + transparent packaging

**S4: Restaurant Churn Risk**
- Cloud Kitchen vs Dine-in analysis

**S5: Lapsed Customer Win-back**
- Segmentation-based targeting

#### 9.4 City Priority Risk Matrix (Bottom Right)
1. **Insert → Table** or **Matrix** visual
2. Create a manual table:

```dax
CityRisk = 
DATATABLE(
    "City", STRING,
    "Decline %", DOUBLE,
    "Risk Level", STRING,
    "Priority", STRING,
    {
        {"Chennai", 62.5, "🔴 High", "Immediate"},
        {"Kolkata", 61.5, "🔴 High", "Immediate"},
        {"Bengaluru", 61.5, "🔴 High", "Immediate"},
        {"Hyderabad", 61.1, "🟡 Medium", "Short-term"},
        {"Ahmedabad", 61.0, "🟡 Medium", "Short-term"},
        {"Mumbai", 60.9, "🟡 Medium", "Short-term"},
        {"Delhi", 60.6, "🟢 Monitor", "Long-term"},
        {"Pune", 59.9, "🟢 Monitor", "Long-term"}
    }
)
```

3. Format as a clean table with conditional formatting on Risk Level

#### 9.5 Key Recommendations Summary (Bottom)
1. **Insert → Text box** (full width)
2. Position: X=`240`, Y=`780`, Width=`1660`, Height=`100`
3. Text:
   ```
   📌 EXECUTIVE SUMMARY: QuickBite's crisis requires a 3-phase recovery: (1) IMMEDIATE delivery 
   fixes + food safety audits, (2) SHORT-TERM cashback campaigns targeting 26 high-rating churners 
   and 3,648 high-value lost customers, (3) LONG-TERM infrastructure + competitive positioning. 
   Estimated recoverable revenue: ₹12-15M/year. Priority cities: Chennai, Kolkata, Bengaluru.
   ```
4. Background: `#1A2744` (navy), Text: White, Font: Segoe UI Bold, 12pt

---

## 10. FINAL CHECKLIST

### Before Publishing

- [ ] **All 6 pages** have the same background image
- [ ] **Sidebar navigation** works on every page (test all buttons)
- [ ] **Active page button** is highlighted teal on each page
- [ ] **Color consistency** — Navy/Teal/Orange only, no random colors
- [ ] **Font consistency** — Segoe UI only, sizes as specified
- [ ] **KPI cards** show correct numbers (cross-check with Python output)
- [ ] **All chart titles** are descriptive and include Q# reference
- [ ] **Data labels** are on for all key charts
- [ ] **Phase slicer** works and syncs across pages
- [ ] **Relationships** are correct in Model view (star schema)
- [ ] **No visual overlaps** — check each page at 100% zoom
- [ ] **Mobile layout** — optionally create a mobile view (View → Mobile layout)

### Cross-Check Numbers (from Python analysis)

| Metric | Expected Value |
|--------|---------------|
| Total Orders | 149,166 |
| Pre-Crisis Orders | 113,806 |
| Crisis Orders | 35,360 |
| Order Decline % | 61.2% |
| Pre-Crisis Revenue | ₹37,620,964 |
| Crisis Revenue | ₹10,940,151 |
| Pre-Crisis Avg Rating | ~4.5 |
| Crisis Avg Rating | ~2.5 |
| Pre-Crisis Cancel Rate | ~6.1% |
| Crisis Cancel Rate | ~11.9% |
| Pre-Crisis SLA Breach | ~56.4% |
| Crisis SLA Breach | ~87.8% |
| Loyal Churned | 49 of 58 |
| High-Value Churned | 3,648 of 4,342 |

### File Organization

```
powerbi_assets/
├── background_1920x1080.png    ← Canvas background (all pages)
├── logo_large.png              ← Home page logo
├── logo_sidebar.png            ← Sidebar logo (all pages)
├── card_page2.png              ← Nav card: Orders & Revenue
├── card_page3.png              ← Nav card: Delivery & Ops
├── card_page4.png              ← Nav card: Ratings & Sentiment
├── card_page5.png              ← Nav card: Customer Loyalty
├── card_page6.png              ← Nav card: Recovery Plan
├── icon_home.png               ← Sidebar icon
├── icon_orders.png             ← Sidebar icon
├── icon_delivery.png           ← Sidebar icon
├── icon_ratings.png            ← Sidebar icon
├── icon_loyalty.png            ← Sidebar icon
├── icon_recovery.png           ← Sidebar icon
├── kpi_card_navy.png           ← KPI background option
├── kpi_card_teal.png           ← KPI background option
├── kpi_card_orange.png         ← KPI background option
└── kpi_card_white.png          ← KPI background option
```

### Tips for Standing Out

1. **Bookmarks:** Create bookmarks for "Pre-Crisis View" and "Crisis View" — add buttons to toggle
2. **Tooltips:** Add custom tooltip pages showing mini-charts on hover
3. **Drillthrough:** Enable drillthrough from City → detailed city page
4. **Conditional formatting:** Use data bars and icons in tables
5. **Page transitions:** Set smooth transitions between pages

---

**🎯 You now have EVERYTHING to build a professional 6-page Power BI dashboard.**

**Next step after completing this:** Let me know when you're done and we'll proceed to `05_secondary_research.ipynb`.
