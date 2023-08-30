from flask import Flask, render_template, request, redirect
import psycopg2
import os
from decimal import Decimal
import datetime

app = Flask(__name__)

# PostgreSQL connection details
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')




def get_transactions():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute("SELECT transaction_id,date, name, category, subcategory, amount  FROM v_true_staging_transactions order by date desc")
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return transactions

def get_categories():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT transaction_id,date, name, category, subcategory FROM v_true_staging_transactions order by date desc")
    category = cursor.fetchall()
    cursor.close()
    conn.close()
    return category

def update_transaction_true_value(transaction_id, date, name, updated_category, updated_subcategory, updated_price):
    insert_date = datetime.datetime.now()
    # Convert the updated price to a Decimal with two decimal places
    updated_price_decimal = Decimal(updated_price).quantize(Decimal('0.00'))

    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO true_transaction (transaction_id, date, name, category, subcategory, actual_amount, insert_date) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (transaction_id, date, name, updated_category, updated_subcategory, updated_price_decimal, insert_date))
    conn.commit()
    cursor.close()
    conn.close()


def update_category_true_value(transaction_id, name, category, subcategory, updatedCategory, updatedSubcategory):
    insert_date = datetime.datetime.now()

    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

    # Check if the record with the same name, category, and subcategory combination already exists
    
        # Perform INSERT if record with the same name, category, and subcategory combination does not exist
    cursor.execute("INSERT INTO true_category (transaction_id, name, category, subcategory, updatedCategory, updatedSubcategory, insert_date) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (transaction_id,name, category, subcategory, updatedCategory, updatedSubcategory, insert_date))

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/changeTransactions', methods=['GET', 'POST'])
def changeTransactions():
    transactions = get_transactions()
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        date = request.form['date']
        name = request.form['name']
        updated_price = request.form['updated_price']
        updated_category = request.form['updated_category']
        updated_subcategory = request.form['updated_subcategory']
        
        # Update the transaction and category details
        update_transaction_true_value(transaction_id, date, name, updated_category, updated_subcategory, updated_price)
        
        return redirect('/changeTransactions')
    return render_template('change_transactions.html', transactions=transactions)


@app.route('/changeCategory', methods=['GET', 'POST'])
def change_category():
    category = get_categories()
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        date = request.form['date']
        name = request.form['name']
        category = request.form['category']
        subcategory = request.form['subcategory']
        updatedCategory = request.form['updatedCategory']
        updatedSubcategory = request.form['updatedSubcategory']
        update_category_true_value(transaction_id,name, category, subcategory, updatedCategory, updatedSubcategory)
        return redirect('/changeCategory')
    return render_template('change_category.html', categories=category)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)