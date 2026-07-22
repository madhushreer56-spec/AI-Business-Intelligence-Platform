def local_sql(question):

    q = question.lower().strip()

    # ======================================================
    # TOTAL SALES
    # ======================================================

    if any(x in q for x in [
        "total sales",
        "overall sales",
        "total revenue"
    ]):

        return (

            """
            SELECT
                SUM(Sales) AS Total_Sales
            FROM sales;
            """,

            "Table",

            """
The business has generated the displayed total sales revenue.

This KPI helps understand the company's overall business performance.

Recommendation:
Monitor total revenue regularly to measure growth.
            """
        )

    # ======================================================
    # TOTAL ORDERS
    # ======================================================

    elif any(x in q for x in [

        "total orders",

        "number of orders",

        "orders count"

    ]):

        return (

            """
            SELECT
                COUNT(*) AS Total_Orders
            FROM sales;
            """,

            "Table",

            """
The dataset contains the total number of completed orders.

Recommendation:
Compare order count with previous months to identify demand trends.
            """
        )

    # ======================================================
    # TOTAL QUANTITY
    # ======================================================

    elif any(x in q for x in [

        "total quantity",

        "quantity sold"

    ]):

        return (

            """
            SELECT
                SUM(Quantity) AS Total_Quantity
            FROM sales;
            """,

            "Table",

            """
Shows the total number of products sold.

Recommendation:
Track quantity sold to improve inventory planning.
            """
        )

    # ======================================================
    # AVERAGE SALES
    # ======================================================

    elif "average sales" in q:

        return (

            """
            SELECT
                AVG(Sales) AS Average_Sales
            FROM sales;
            """,

            "Table",

            """
Displays the average sales value per transaction.

Recommendation:
Compare average sales over time to identify purchasing behavior.
            """
        )

    # ======================================================
    # MAXIMUM SALE
    # ======================================================

    elif any(x in q for x in [

        "highest sale",

        "maximum sale",

        "largest sale"

    ]):

        return (

            """
            SELECT
                MAX(Sales) AS Highest_Sale
            FROM sales;
            """,

            "Table",

            """
Shows the highest single sales transaction.

Recommendation:
Investigate high-value transactions to understand successful sales.
            """
        )

    # ======================================================
    # MINIMUM SALE
    # ======================================================

    elif any(x in q for x in [

        "lowest sale",

        "minimum sale"

    ]):

        return (

            """
            SELECT
                MIN(Sales) AS Lowest_Sale
            FROM sales;
            """,

            "Table",

            """
Displays the smallest sales transaction.

Recommendation:
Identify products with consistently low sales and improve marketing.
            """
        )

    # ======================================================
    # TOP PRODUCT
    # ======================================================

    elif any(x in q for x in [

        "highest selling product",

        "top product",

        "best selling product"

    ]):

        return (

            """
            SELECT
                Product,
                SUM(Sales) AS TotalSales
            FROM sales
            GROUP BY Product
            ORDER BY TotalSales DESC
            LIMIT 1;
            """,

            "Bar Chart",

            """
This product contributes the highest revenue.

Recommendation:
Increase inventory and marketing for this product.
            """
        )

    # ======================================================
    # LOWEST PRODUCT
    # ======================================================

    elif any(x in q for x in [

        "lowest selling product",

        "least selling product"

    ]):

        return (

            """
            SELECT
                Product,
                SUM(Sales) AS TotalSales
            FROM sales
            GROUP BY Product
            ORDER BY TotalSales ASC
            LIMIT 1;
            """,

            "Bar Chart",

            """
This product generates the lowest revenue.

Recommendation:
Review pricing, demand and marketing strategy.
            """
        )

    # ======================================================
    # SALES BY REGION
    # ======================================================

    elif "region" in q:

        return (

            """
            SELECT
                Region,
                SUM(Sales) AS TotalSales
            FROM sales
            GROUP BY Region;
            """,

            "Pie Chart",

            """
Compares revenue across all regions.

Recommendation:
Focus investments on high-performing regions.
            """
        )

    # ======================================================
    # SALES BY CATEGORY
    # ======================================================

    elif "category" in q:

        return (

            """
            SELECT
                Category,
                SUM(Sales) AS TotalSales
            FROM sales
            GROUP BY Category;
            """,

            "Pie Chart",

            """
Shows revenue generated by each product category.

Recommendation:
Expand categories with strong performance.
            """
        )    # ======================================================
    # SALES BY PRODUCT
    # ======================================================

    elif any(x in q for x in [

        "sales by product",

        "product sales"

    ]):

        return (

            """
            SELECT
                Product,
                SUM(Sales) AS TotalSales
            FROM sales
            GROUP BY Product
            ORDER BY TotalSales DESC;
            """,

            "Bar Chart",

            """
Shows total revenue generated by each product.

Recommendation:
Focus inventory on products with consistently high sales.
            """
        )

    # ======================================================
    # QUANTITY BY PRODUCT
    # ======================================================

    elif any(x in q for x in [

        "quantity by product",

        "product quantity",

        "quantity sold"

    ]):

        return (

            """
            SELECT
                Product,
                SUM(Quantity) AS TotalQuantity
            FROM sales
            GROUP BY Product
            ORDER BY TotalQuantity DESC;
            """,

            "Bar Chart",

            """
Displays total quantity sold for every product.

Recommendation:
Use this information for inventory planning.
            """
        )

    # ======================================================
    # TOP 10 SALES
    # ======================================================

    elif any(x in q for x in [

        "top 10",

        "highest transactions"

    ]):

        return (

            """
            SELECT *
            FROM sales
            ORDER BY Sales DESC
            LIMIT 10;
            """,

            "Bar Chart",

            """
Displays the ten highest sales transactions.

Recommendation:
Study these transactions to understand successful sales patterns.
            """
        )

    # ======================================================
    # TOP 5 PRODUCTS
    # ======================================================

    elif "top 5 products" in q:

        return (

            """
            SELECT
                Product,
                SUM(Sales) AS TotalSales
            FROM sales
            GROUP BY Product
            ORDER BY TotalSales DESC
            LIMIT 5;
            """,

            "Bar Chart",

            """
Shows the five best-performing products.

Recommendation:
Promote these products further to increase revenue.
            """
        )

    # ======================================================
    # MONTHLY SALES
    # ======================================================

    elif any(x in q for x in [

        "monthly sales",

        "sales by month"

    ]):

        return (

            """
            SELECT
                strftime('%Y-%m', Date) AS Month,
                SUM(Sales) AS TotalSales
            FROM sales
            GROUP BY Month
            ORDER BY Month;
            """,

            "Line Chart",

            """
Displays monthly revenue trend.

Recommendation:
Identify seasonal demand and plan marketing campaigns.
            """
        )

    # ======================================================
    # YEARLY SALES
    # ======================================================

    elif any(x in q for x in [

        "yearly sales",

        "annual sales"

    ]):

        return (

            """
            SELECT
                strftime('%Y', Date) AS Year,
                SUM(Sales) AS TotalSales
            FROM sales
            GROUP BY Year;
            """,

            "Line Chart",

            """
Displays yearly revenue.

Recommendation:
Compare annual performance to measure business growth.
            """
        )

    # ======================================================
    # SALES TREND
    # ======================================================

    elif "trend" in q:

        return (

            """
            SELECT
                Date,
                Sales
            FROM sales
            ORDER BY Date;
            """,

            "Line Chart",

            """
Shows how sales change over time.

Recommendation:
Observe increasing or decreasing trends for forecasting.
            """
        )

    # ======================================================
    # REGION WITH HIGHEST SALES
    # ======================================================

    elif any(x in q for x in [

        "highest region",

        "best region",

        "highest revenue region"

    ]):

        return (

            """
            SELECT
                Region,
                SUM(Sales) AS Revenue
            FROM sales
            GROUP BY Region
            ORDER BY Revenue DESC
            LIMIT 1;
            """,

            "Bar Chart",

            """
Shows the highest revenue generating region.

Recommendation:
Increase investment in this region.
            """
        )

    # ======================================================
    # CATEGORY WITH HIGHEST SALES
    # ======================================================

    elif any(x in q for x in [

        "best category",

        "highest category",

        "highest revenue category"

    ]):

        return (

            """
            SELECT
                Category,
                SUM(Sales) AS Revenue
            FROM sales
            GROUP BY Category
            ORDER BY Revenue DESC
            LIMIT 1;
            """,

            "Bar Chart",

            """
Displays the highest revenue generating category.

Recommendation:
Expand the product range in this category.
            """
        )

    # ======================================================
    # SHOW ALL DATA
    # ======================================================

    elif any(x in q for x in [

        "show data",

        "show dataset",

        "show all",

        "all records"

    ]):

        return (

            """
            SELECT *
            FROM sales
            LIMIT 100;
            """,

            "Table",

            """
Displaying the available records.

Recommendation:
Use filters or ask more specific business questions.
            """
        )    # ======================================================
    # SCATTER PLOT
    # ======================================================

    elif any(x in q for x in [

        "scatter",

        "correlation",

        "relationship"

    ]):

        return (

            """
            SELECT
                Sales,
                Quantity
            FROM sales;
            """,

            "Scatter Plot",

            """
Displays the relationship between Sales and Quantity.

Recommendation:
Identify whether higher quantities lead to increased revenue.
            """
        )

    # ======================================================
    # HISTOGRAM
    # ======================================================

    elif any(x in q for x in [

        "distribution",

        "histogram"

    ]):

        return (

            """
            SELECT
                Sales
            FROM sales;
            """,

            "Histogram",

            """
Displays the distribution of sales values.

Recommendation:
Use this to identify common sales ranges and unusual values.
            """
        )

    # ======================================================
    # PIE CHART
    # ======================================================

    elif "pie chart" in q:

        return (

            """
            SELECT
                Category,
                SUM(Sales) AS TotalSales
            FROM sales
            GROUP BY Category;
            """,

            "Pie Chart",

            """
Shows the contribution of each category to total sales.

Recommendation:
Increase investment in categories with larger market share.
            """
        )

    # ======================================================
    # BAR CHART
    # ======================================================

    elif "bar chart" in q:

        return (

            """
            SELECT
                Product,
                SUM(Sales) AS TotalSales
            FROM sales
            GROUP BY Product
            ORDER BY TotalSales DESC;
            """,

            "Bar Chart",

            """
Displays product-wise revenue comparison.

Recommendation:
Focus on products generating maximum revenue.
            """
        )

    # ======================================================
    # LINE CHART
    # ======================================================

    elif "line chart" in q:

        return (

            """
            SELECT
                Date,
                Sales
            FROM sales
            ORDER BY Date;
            """,

            "Line Chart",

            """
Shows sales trend over time.

Recommendation:
Monitor long-term business growth using this trend.
            """
        )

    # ======================================================
    # DEFAULT FALLBACK
    # ======================================================

    else:

        return (

            """
            SELECT *
            FROM sales
            LIMIT 20;
            """,

            "Table",

            """
Gemini AI is currently unavailable.

The application has automatically switched to Offline Business Intelligence Mode.

Recommendation:

Try asking one of the following:

• Total Sales
• Average Sales
• Highest Selling Product
• Sales by Region
• Sales by Category
• Monthly Sales
• Yearly Sales
• Top 10 Sales
• Quantity by Product
            """
        )