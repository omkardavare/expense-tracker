from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
CSV_FILE = 'expenses.csv'

@app.route('/')
def index():
    data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    return render_template('index.html', data=data)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        new_entry = {
            'date': request.form.get('date'),
            'category_name': request.form.get('category_name'),
            'subcategory': request.form.get('subcategory'),
            'amount': request.form.get('amount'),
            'type': request.form.get('type'),
            'payment_mode': request.form.get('payment_mode'),
            'app_used': request.form.get('app_used'),
            'notes': request.form.get('notes')
        }

        # Ensure no required fields are missing
        if not all([new_entry['date'], new_entry['category_name'], new_entry['subcategory'], new_entry['amount'], new_entry['type'], new_entry['payment_mode'], new_entry['app_used']]):
            return "Bad Request: Missing required fields", 400

        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=new_entry.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(new_entry)

        return redirect('/')
    except Exception as e:
        return f"Error: {e}", 500
