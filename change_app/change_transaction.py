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
    cursor.execute("SELECT transaction_id,date, name, category, subcategory, amount  FROM staging__transactions order by date desc")
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return transactions


def update_transaction_true_value(transaction_id, date,name,category,subcategory, updated_price):
    insert_date = datetime.datetime.now()
    # Convert the updated price to a Decimal with two decimal places
    updated_price_decimal = Decimal(updated_price).quantize(Decimal('0.00'))

    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO true_transaction (transaction_id, date, name, category, subcategory, actual_amount, insert_date) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (transaction_id, date, name, category, subcategory, updated_price_decimal,insert_date))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    transactions = get_transactions()
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        date = request.form['date']
        name = request.form['name']
        category = request.form['category']
        subcategory = request.form['subcategory']
        updated_price = request.form['updated_price']
        update_transaction_true_value(transaction_id,date, name, category, subcategory, updated_price)
        return redirect('/')
    return render_template('index.html', transactions=transactions)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)