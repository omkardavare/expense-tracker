from flask import Flask, request, render_template, redirect
import requests
import os

app = Flask(__name__)

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            "date": request.form['date'],
            "category": request.form['category'],
            "subcategory": request.form['subcategory'],
            "amount": float(request.form['amount']),
            "payment_mode": request.form['payment_mode'],
            "notes": request.form['notes'],
        }

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }

        # Insert into Supabase
        requests.post(f"{SUPABASE_URL}/rest/v1/expenses", json=data, headers=headers)

        return redirect('/')

    # Get all expenses
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    r = requests.get(f"{SUPABASE_URL}/rest/v1/expenses?select=*", headers=headers)
    expenses = r.json()

    return render_template('index.html', expenses=expenses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
