import csv

# -----------------------------------------
# SALES PERFORMANCE ANALYSIS
# -----------------------------------------

data = []

# Read CSV file
try:
    with open("sales_data.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data.append({
                "date": row["date"],
                "Product": row["Product"],
                "Region": row["Region"],
                "Quantity": int(row["Quantity"]),
                "Price": float(row["Price"]),
                "Discount": float(row["Discount"]),
                "Returns": int(row["Returns"]),
                "StockLoss": float(row["StockLoss"])
            })

except FileNotFoundError:
    print("ERROR: sales_data.csv not found!")
    print("Make sure sales_data.csv is in the same folder as sale.py")
    exit()

# -----------------------------------------
# VARIABLES
# -----------------------------------------

total_revenue = 0
total_profit = 0

discount_loss = 0
return_loss = 0
stock_loss = 0

regional_sales = {}
product_sales = {}
monthly_sales = {}

# -----------------------------------------
# ANALYSIS
# -----------------------------------------

for row in data:

    quantity = row["Quantity"]
    price = row["Price"]
    discount = row["Discount"]

    # Gross Sales
    gross_sales = quantity * price

    # Actual Revenue after discount
    revenue = gross_sales * (1 - discount)

    # Assume 20% profit margin
    profit = revenue * 0.20

    total_revenue += revenue
    total_profit += profit

    # -------------------------------------
    # DISCOUNT LEAKAGE
    # -------------------------------------

    if discount > 0.15:

        leakage = gross_sales * (discount - 0.15)

        discount_loss += leakage

    # -------------------------------------
    # RETURN LEAKAGE
    # -------------------------------------

    return_leakage = (
        row["Returns"] *
        price *
        (1 - discount)
    )

    return_loss += return_leakage

    # -------------------------------------
    # STOCK LEAKAGE
    # -------------------------------------

    stock_loss += row["StockLoss"]

    # -------------------------------------
    # REGIONAL SALES
    # -------------------------------------

    region = row["Region"]

    if region not in regional_sales:
        regional_sales[region] = 0

    regional_sales[region] += revenue

    # -------------------------------------
    # PRODUCT SALES
    # -------------------------------------

    product = row["Product"]

    if product not in product_sales:
        product_sales[product] = 0

    product_sales[product] += revenue

    # -------------------------------------
    # MONTHLY SALES
    # -------------------------------------

    month = row["date"][:7]

    if month not in monthly_sales:
        monthly_sales[month] = 0

    monthly_sales[month] += revenue


# -----------------------------------------
# TOTAL REVENUE LEAKAGE
# -----------------------------------------

total_leakage = (
    discount_loss +
    return_loss +
    stock_loss
)


# -----------------------------------------
# DISPLAY MAIN RESULTS
# -----------------------------------------

print()
print("=" * 55)
print("       SALES PERFORMANCE ANALYSIS SYSTEM")
print("=" * 55)

print("Total Orders        :", len(data))
print("Total Revenue       : ₹", round(total_revenue, 2))
print("Total Profit        : ₹", round(total_profit, 2))


# -----------------------------------------
# REVENUE LEAKAGE
# -----------------------------------------

print()
print("=" * 55)
print("             REVENUE LEAKAGE")
print("=" * 55)

print("Discount Leakage    : ₹", round(discount_loss, 2))
print("Return Leakage      : ₹", round(return_loss, 2))
print("Stock Leakage       : ₹", round(stock_loss, 2))
print("Total Leakage       : ₹", round(total_leakage, 2))


# -----------------------------------------
# REGIONAL PERFORMANCE
# -----------------------------------------

print()
print("=" * 55)
print("             REGIONAL PERFORMANCE")
print("=" * 55)

sorted_regions = sorted(
    regional_sales.items(),
    key=lambda x: x[1],
    reverse=True
)

for region, revenue in sorted_regions:

    print(
        f"{region:<15} : ₹{revenue:,.2f}"
    )


# -----------------------------------------
# PRODUCT PERFORMANCE
# -----------------------------------------

print()
print("=" * 55)
print("             PRODUCT PERFORMANCE")
print("=" * 55)

sorted_products = sorted(
    product_sales.items(),
    key=lambda x: x[1],
    reverse=True
)

for product, revenue in sorted_products:

    print(
        f"{product:<15} : ₹{revenue:,.2f}"
    )


# -----------------------------------------
# MONTHLY PERFORMANCE
# -----------------------------------------

print()
print("=" * 55)
print("             MONTHLY PERFORMANCE")
print("=" * 55)

sorted_months = sorted(monthly_sales.items())

for month, revenue in sorted_months:

    print(
        f"{month:<15} : ₹{revenue:,.2f}"
    )


# -----------------------------------------
# LEAKAGE PRIORITY
# -----------------------------------------

leakage_data = {
    "Excessive Discounts": discount_loss,
    "Product Returns": return_loss,
    "Stock Unavailability": stock_loss
}

sorted_leakage = sorted(
    leakage_data.items(),
    key=lambda x: x[1],
    reverse=True
)

print()
print("=" * 55)
print("             LEAKAGE PRIORITY")
print("=" * 55)

print(
    f"{'Leakage Source':<25} {'Loss':>15}"
)

print("-" * 55)

for source, loss in sorted_leakage:

    print(
        f"{source:<25} ₹{loss:>13,.2f}"
    )


# -----------------------------------------
# RECOMMENDATIONS
# -----------------------------------------

print()
print("=" * 55)
print("             RECOMMENDATIONS")
print("=" * 55)

if discount_loss > 0:
    print("1. Review products with excessive discounts.")

if return_loss > 0:
    print("2. Investigate products with frequent returns.")

if stock_loss > 0:
    print("3. Improve inventory and stock forecasting.")

print("4. Monitor low-performing regions.")
print("5. Review major sources of revenue leakage.")


# -----------------------------------------
# FINAL RESULT
# -----------------------------------------

print()
print("=" * 55)
print("              ANALYSIS COMPLETE")
print("=" * 55)

print()
print("Total Revenue Leakage = ₹", round(total_leakage, 2))
print()