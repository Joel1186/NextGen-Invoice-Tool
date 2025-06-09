
from flask import Flask, render_template, request, send_file, session, redirect, url_for
from fpdf import FPDF
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = "nextgen_secure_key"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    if request.form['username'] == "admin" and request.form['password'] == "buildfast":
        session['auth'] = True
        return redirect(url_for('form'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('auth', None)
    return redirect(url_for('login'))

@app.route('/form')
def form():
    if not session.get('auth'):
        return redirect(url_for('login'))
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_invoice():
    if not session.get('auth'):
        return redirect(url_for('login'))

    customer = request.form['customer']
    address = request.form['address']
    service = request.form['service']
    rate = float(request.form['rate'])
    quantity = int(request.form['quantity'])
    total = rate * quantity
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    pdf = FPDF()
    pdf.add_page()
    pdf.image("static/logo.png", x=10, y=8, w=50)
    pdf.set_font("Arial", size=12)
    pdf.ln(30)
    pdf.cell(200, 10, txt="NextGenConstructionCorp Invoice", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(100, 10, txt=f"Customer: {customer}", ln=True)
    pdf.cell(100, 10, txt=f"Address: {address}", ln=True)
    pdf.cell(100, 10, txt=f"Service: {service}", ln=True)
    pdf.cell(100, 10, txt=f"Rate: ${rate:.2f}", ln=True)
    pdf.cell(100, 10, txt=f"Quantity: {quantity}", ln=True)
    pdf.cell(100, 10, txt=f"Total: ${total:.2f}", ln=True)
    pdf.cell(100, 10, txt=f"Date: {now}", ln=True)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="invoice.pdf", mimetype='application/pdf')
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

