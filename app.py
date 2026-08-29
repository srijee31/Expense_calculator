from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory storage for expenses
expenses = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get-summary', methods=['GET'])
def get_summary():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())

    categories_list = ['Travel', 'Food', 'Groceries', 'Investment', 'Shopping', 'Bills', 'Entertainment']

    summary_data = {
        'totals': {'daily': 0.0, 'weekly': 0.0, 'monthly': 0.0, 'yearly': 0.0},
        'by_period': {
            'daily': {c: 0.0 for c in categories_list},
            'weekly': {c: 0.0 for c in categories_list},
            'monthly': {c: 0.0 for c in categories_list},
            'yearly': {c: 0.0 for c in categories_list}
        }
    }

    for item in expenses:
        exp_date = datetime.strptime(item['date'], '%Y-%m-%d')
        amt = item['amount']
        cat = item['category']

        if cat not in categories_list:
            continue

        if exp_date.date() == today.date():
            summary_data['totals']['daily'] += amt
            summary_data['by_period']['daily'][cat] += amt

        if exp_date.date() >= start_of_week.date():
            summary_data['totals']['weekly'] += amt
            summary_data['by_period']['weekly'][cat] += amt

        if exp_date.year == today.year and exp_date.month == today.month:
            summary_data['totals']['monthly'] += amt
            summary_data['by_period']['monthly'][cat] += amt

        if exp_date.year == today.year:
            summary_data['totals']['yearly'] += amt
            summary_data['by_period']['yearly'][cat] += amt

    return jsonify(summary_data)

@app.route('/api/get-logged-dates', methods=['GET'])
def get_logged_dates():
    # Return unique set of dates that have entries
    logged_dates = list(set(item['date'] for item in expenses if item['amount'] > 0))
    return jsonify({'logged_dates': logged_dates})

@app.route('/api/add-expense', methods=['POST'])
def add_expense():
    data = request.json
    date = data.get('date')
    items = data.get('items', {})

    for cat, amt in items.items():
        try:
            val = float(amt)
            if val > 0:
                expenses.append({'date': date, 'category': cat, 'amount': val})
        except (ValueError, TypeError):
            continue

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)