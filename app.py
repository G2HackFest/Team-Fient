from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
CORS(app)

# Simple in-memory storage for demo purposes
plans_db = {}
chats_db = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    try:
        data = request.json
        username = data.get('username')
        condition = data.get('condition')
        weight = data.get('weight')
        
        if not all([username, condition, weight]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Simple plan generation
        plan = {
            'diet_plan': f"{condition} diet plan for {weight}kg",
            'meals': ["Breakfast: Scrambled eggs + spinach + avocado + whole-grain toast", "Lunch: Lentil soup + mixed greens + olive oil dressing", "Dinner: Stir-fried tofu + broccoli + mushrooms + sesame oil"],
            'shopping_list': ["Oats", "Chicken", "Fish", "Vegetables"]
        }
        
        plans_db[username] = plan
        return jsonify({'success': True, **plan})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message required'}), 400
        
        # Simple chatbot responses
        responses = {
            'hi': "Hello! How can I help with your diet?",
            'hello': "Hi there! Ask me about nutrition.",
            'diet': "Focus on whole foods and vegetables.",
            'default': "I can help with diet advice. Ask me anything!",
            'how to avoid diabetes': "Maintain a healthy weight, exercise regularly,quit smoking",
            'how to loss weight':"Exercise regularly,Balanced diet"
        }
        
        response = responses.get(message.lower(), responses['default'])
        chats_db.append({'message': message, 'response': response})
        
        return jsonify({'success': True, 'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)