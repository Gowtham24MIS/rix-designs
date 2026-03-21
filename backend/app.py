from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route('/api/contact', methods=['POST'])
def contact():
    print("🔍 RAW FORM DATA:", dict(request.form))  # Shows ALL data
    
    # ✅ SIMPLIEST - Direct access to form fields
    name = request.form.get('name') or ''
    email = request.form.get('email') or ''
    message = request.form.get('message') or ''
    
    print(f"📨 name='{name}' | email='{email}' | message='{message}'")
    
    # Clean data
    name = name.strip()
    email = email.strip()
    message = message.strip()
    
    if not name or not email or not message:
        print("❌ MISSING FIELDS")
        return jsonify({
            'success': False, 
            'error': f"name='{name}', email='{email}', message='{message}'"
        }), 400
    
    print("✅ ALL FIELDS VALID!")
    
    # Email sending...
    recipient = os.getenv('RECIPIENT_EMAIL', 'gowtham.developer07@gmail.com')
    msg = Message(
        subject=f'Rix Contact: {name}',
        sender=app.config['MAIL_USERNAME'],
        recipients=[recipient],
        body=f'Name: {name}\nEmail: {email}\n\n{message}'
    )
    
    try:
        mail.send(msg)
        print("✅ EMAIL SENT SUCCESSFULLY!")
        return jsonify({'success': True})
    except Exception as e:
        print("❌ EMAIL ERROR:", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
