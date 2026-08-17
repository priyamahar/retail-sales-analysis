from flask import Flask, jsonify,render_template
import mysql.connector

app = Flask(__name__)

# MYSQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="priya@123",
    database="retail_sales"
)

@app.route("/")
def home():
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sales")
    total_sales = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total_amount)FROM sales")
    total_amount = cursor.fetchone()[0] or 0
    cursor.close()

    return render_template(
        "index.html",
        total_customers=total_customers,
        total_products=total_products,
        total_sales=total_sales
    )

@app.route("/customers")
def customers():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()

    cursor.execute("DESCRIBE customers")
    column_data = cursor.fetchall()
    columns = [column["Field"] for column in column_data]

    cursor.close()

    return render_template(
        "customers.html",
        customers=data,
        columns=columns
    )

@app.route("/products")
def products():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()

    cursor.execute("DESCRIBE products")
    column_data = cursor.fetchall()
    columns = [column["Field"] for column in column_data]

    cursor.close()

    return render_template(
        "products.html",
        products=data,
        columns=columns
    )

@app.route("/sales")
def sales():
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sales")
    data = cursor.fetchall()

    cursor.execute("DESCRIBE sales")
    column_data = cursor.fetchall()
    columns = [column["Field"] for column in column_data]

    cursor.close()

    return render_template(
        "sales.html",
        sales=data,
        columns=columns
    )
@app.route("/reports")
def reports():
    cursor = db.cursor(dictionary=True)

    # Sales Report
    cursor.execute("""
        SELECT *
        FROM sales_report
    """)
    sales_report = cursor.fetchall()

    # Product Sales Report
    cursor.execute("""
        SELECT *
        FROM product_sales_report
    """)
    product_report = cursor.fetchall()

    # Get column names
    sales_columns = list(sales_report[0].keys()) if sales_report else []
    product_columns = list(product_report[0].keys()) if product_report else []

    cursor.close()

    return render_template(
        "reports.html",
        sales_report=sales_report,
        sales_columns=sales_columns,
        product_report=product_report,
        product_columns=product_columns
    )

if __name__ == "__main__":
    app.run(debug=True)