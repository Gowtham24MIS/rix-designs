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

# 🔥 DEBUG - ADD THESE 3 LINES:
    print(f"🔑 EMAILJS_SERVICE_ID: {os.getenv('EMAILJS_SERVICE_ID', '***MISSING***')[:10]}...")
    print(f"🔑 EMAILJS_TEMPLATE_ID: {os.getenv('EMAILJS_TEMPLATE_ID', '***MISSING***')[:10]}...")
    print(f"🔑 EMAILJS_PUBLIC_KEY: {os.getenv('EMAILJS_PUBLIC_KEY', '***MISSING***')[:10] if os.getenv('EMAILJS_PUBLIC_KEY') else '***MISSING***'}...")

    
    # 🔥 EMAILJS API (ANY sender email WORKS!)
    url = "https://api.emailjs.com/api/v1.0/email/send"
    
    data = {
        "service_id": os.getenv('EMAILJS_SERVICE_ID'),        # service_abc123
        "template_id": os.getenv('EMAILJS_TEMPLATE_ID'),      # template_xyz789
        "public_key": os.getenv('EMAILJS_PUBLIC_KEY'),        # abc123def456
        "template_params": {
            "name": name,
            "user_email": email,     # pmgowtham2007@gmail.com ✓
            "message": message,
            "to_email": "rix.designs02@gmail.com"
        }
    }
    
    try:
        print("🚀 Sending to EmailJS...")
        response = requests.post(url, json=data)
        print(f"✅ EMAILJS RESPONSE: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ EMAIL SENT SUCCESSFULLY!")
            return jsonify({'success': True, 'message': 'Thank you! Your message has been sent.'})
        else:
            print(f"❌ EMAILJS ERROR: {response.text}")
            return jsonify({'success': False, 'error': f'EmailJS error: {response.text}'}), 500
            
    except Exception as e:
        print(f"❌ REQUEST ERROR: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
