from flask import Flask, request, render_template, redirect
import requests
import os

app = Flask(__name__)

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# Headers for Supabase API
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.route('/')
def index():
    # Fetch all expenses
    r_exp = requests.get(f"{SUPABASE_URL}/rest/v1/expenses?select=*", headers=headers)
    expenses = r_exp.json()

    # Fetch all categories
    r_cat = requests.get(f"{SUPABASE_URL}/rest/v1/categories?select=*", headers=headers)
    categories = r_cat.json()

    return render_template('index.html', expenses=expenses, categories=categories)


@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = {
        "date": request.form['date'],
        "category_name": request.form['category_name'],
        "category_id": int(request.form['category_id']),
        "type": request.form['type'],
        "description": request.form['description'],
        "amount": float(request.form['amount']),
        "mode_of_payment": request.form['mode_of_payment'],
        "app_used": request.form['app_used'],
    }

    requests.post(f"{SUPABASE_URL}/rest/v1/expenses", json=data, headers=headers)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
