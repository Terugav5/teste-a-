from flask import Flask, render_template, request, jsonify
from gemini_agent import call_gemini_api

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main chat page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles chat messages from the user."""
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    # Call the Gemini API
    ai_response = call_gemini_api(user_message)

    return jsonify({'response': ai_response})

if __name__ == '__main__':
    # Note: This is a development server. For production, use a proper WSGI server.
    app.run(debug=True, port=5001)