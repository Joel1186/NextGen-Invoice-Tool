@app.route('/generate', methods=['POST'])
def generate_invoice():
    if not session.get('auth'):
        return redirect(url_for('login'))

    try:
        customer = request.form['customer']
        address = request.form['address']
        service = request.form['service']
        rate = float(request.form['rate'])
        quantity = int(request.form['quantity'])
        total = rate * quantity
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        pdf = FPDF()
        pdf.add_page()
        try:
            pdf.image("static/logo.png", x=10, y=8, w=50)
        except:
            pass
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

        # FIX: Correct BytesIO usage for FPDF and Flask
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        buffer = io.BytesIO(pdf_bytes)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="invoice.pdf", mimetype='application/pdf')

    except Exception as e:
        return f"An error occurred while generating the PDF: {str(e)}", 500
