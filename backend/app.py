from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/contact', methods=['POST'])
def contact():
    print("🔍 RAW FORM DATA:", dict(request.form))
    
    # Get form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()
    
    print(f"📨 name='{name}' | email='{email}' | message='{message}'")
    
    # Validate
    if not all([name, email, message]):
        print("❌ MISSING FIELDS")
        return jsonify({
            'success': False, 
            'error': f"name='{name}', email='{email}', message='{message}'"
        }), 400
    
    print("✅ ALL FIELDS VALID!")
    
    # RESEND API CALL (FREE 3k emails/month)
        # BREVO API CALL (300 emails/DAY FREE)
    url = "https://api.brevo.com/v3/smtp/email"
    api_key = os.getenv('BREVO_API_KEY')
    
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    
    data = {
        "sender": {
            "name": f"{name} via Rix Designs",
            "email": email  # User's Gmail OK!
        },
        "to": [{"email": "rix.designs02@gmail.com", "name": "Gowtham"}],  # No yellow!
        "subject": f"New Contact Form: {name}",
        "htmlContent": f"""
        <h2>🎉 New Contact Form Submission</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Message:</strong></p>
        <p>{message}</p>
        <hr>
        <small>Submitted via rix-designs.onrender.com</small>
        """
    }

    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"✅ RESEND RESPONSE: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ EMAIL SENT SUCCESSFULLY!")
            return jsonify({'success': True, 'message': 'Thank you! Your message has been sent.'})
        else:
            print(f"❌ RESEND ERROR: {response.text}")
            return jsonify({'success': False, 'error': f'Resend error: {response.text}'}), 500
            
    except Exception as e:
        print(f"❌ REQUEST ERROR: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
