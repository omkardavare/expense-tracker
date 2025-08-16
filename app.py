from flask import Flask, render_template, request, redirect
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    # fetch all users from Supabase
    response = supabase.table("expenses").select("*").execute()
    data = response.data if response.data else []
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
            'mode_of_payment': request.form.get('payment_mode'),
            'app_used': request.form.get('app_used'),
            'notes': request.form.get('notes')
        }

        # Ensure no required fields are missing
        if not all([new_entry['date'], new_entry['category_name'], new_entry['subcategory'], new_entry['amount'], new_entry['type'], new_entry['mode_of_payment'], new_entry['app_used']]):
            return "Bad Request: Missing required fields", 400

        
        data, count = supabase.table("expenses").insert(new_entry).execute()

        if data:
            print("Hello, Saved to Supabase ✅")
            return redirect('/')
        else:
            return "Error saving to Supabase ❌"

        # return redirect('/')
    except Exception as e:
        return f"Error: {e}", 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
