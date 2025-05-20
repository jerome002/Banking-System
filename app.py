from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, login_required
from auth import auth, login_manager
from models.database import db, cursor
from fpdf import FPDF
import csv, os


app = Flask(__name__, template_folder='frontend/templates')
print(f"Template folder is: {app.template_folder}")


app.secret_key = 'supersecretkey'
app.register_blueprint(auth)
login_manager.init_app(app)

@app.route('/')
@login_required
def index():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users)

@app.route('/frontendtemplates/account/<int:user_id>')
@login_required
def account(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    return render_template('account.html', user=user)

@app.route('/frontend/templates/transaction/<int:user_id>', methods=['GET', 'POST'])
@login_required
def transaction(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        amount = float(request.form['amount'])
        txn_type = request.form['type']
        cursor.execute("INSERT INTO transactions (user_id, amount, type) VALUES (%s, %s, %s)",
                       (user_id, amount, txn_type))
        new_balance = user['balance'] + amount if txn_type == 'credit' else user['balance'] - amount
        cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (new_balance, user_id))
        db.commit()
        return redirect(url_for('account', user_id=user_id))

    cursor.execute("SELECT * FROM transactions WHERE user_id = %s ORDER BY timestamp DESC", (user_id,))
    transactions = cursor.fetchall()
    return render_template('transaction.html', user=user, transactions=transactions)

@app.route('/frontend/templates/add-user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        balance = float(request.form['balance'])
        cursor.execute("INSERT INTO users (name, email, balance) VALUES (%s, %s, %s)",
                       (name, email, balance))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.route('/frontend/templates/edit-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        balance = float(request.form['balance'])
        cursor.execute("UPDATE users SET name=%s, email=%s, balance=%s WHERE id=%s",
                       (name, email, balance, user_id))
        db.commit()
        return redirect(url_for('index'))
    return render_template('edit_user.html', user=user)

@app.route('/export/<int:user_id>/csv')
@login_required
def export_csv(user_id):
    cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
    transactions = cursor.fetchall()
    path = f"exports/transactions_{user_id}.csv"
    os.makedirs("exports", exist_ok=True)
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Amount", "Type", "Timestamp"])
        for txn in transactions:
            writer.writerow([txn['id'], txn['amount'], txn['type'], txn['timestamp']])
    return send_file(path, as_attachment=True)

@app.route('/export/<int:user_id>/pdf')
@login_required
def export_pdf(user_id):
    cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
    transactions = cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for txn in transactions:
        pdf.cell(200, 10, txt=f"{txn['timestamp']} - {txn['type']} ${txn['amount']}", ln=True)
    os.makedirs("exports", exist_ok=True)
    path = f"exports/transactions_{user_id}.pdf"
    pdf.output(path)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
