from flask import Flask, request, render_template, redirect
import requests
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    if request.method == 'POST':
        data = {
            "date": request.form['date'],
            "category": request.form['category'],
            "subcategory": request.form['subcategory'],
            "amount": float(request.form['amount']),
            "payment_mode": request.form['payment_mode'],
            "notes": request.form['notes'],
        }

        try:
            res = requests.post(f"{SUPABASE_URL}/rest/v1/expenses", json=data, headers=headers)
            res.raise_for_status()
        except Exception as e:
            print("Error adding expense:", e)

        return redirect('/')

    # Get all expenses
    try:
        r = requests.get(f"{SUPABASE_URL}/rest/v1/expenses?select=*", headers=headers)
        r.raise_for_status()
        expenses = r.json()
    except Exception as e:
        print("Error fetching expenses:", e)
        expenses = []

    return render_template('index.html', expenses=expenses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

