import os
import json
import re
from flask import Flask, request, jsonify, render_template, session
import google.generativeai as genai
from orders import get_order_by_id, get_orders_by_email, get_all_products

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="""You are a smart customer service assistant for TrendShop, an online retailer. Your name is "Trend Assistant".

## Your Responsibilities
- Order status lookups (by order number or email address)
- Product information and stock availability
- Explaining return and exchange processes
- Providing shipping tracking details
- Handling complaints with empathy and offering solutions

## Order Database
When the user provides an order number or email address, you will receive order details as JSON. Use this information to give a detailed, helpful response.

## Tone & Style
- Friendly but professional
- Always respond in English
- Keep answers concise and clear
- You may use emojis sparingly
- Address the customer by name if you know it

## Return Policy
- Unconditional returns within 30 days
- Free return shipping for damaged items
- Return approval within 1-3 business days
- Refund processed within 5-7 business days

## What You Must Not Do
- Process actual payments
- Ask for passwords or card numbers
- Make promises with uncertain timelines

Always be polite and helpful. For issues you cannot resolve, direct the customer to a human representative."""
)


def build_context_message(user_message: str) -> str:
    context_parts = []

    order_ids = re.findall(r'TS-\d+', user_message.upper())
    for order_id in order_ids:
        order = get_order_by_id(order_id)
        if order:
            context_parts.append(f"Order Info ({order_id}):\n{json.dumps(order, indent=2)}")

    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', user_message)
    for email in emails:
        orders = get_orders_by_email(email)
        if orders:
            context_parts.append(f"Customer Orders ({email}):\n{json.dumps(orders, indent=2)}")

    product_keywords = ['product', 'stock', 'price', 'how much', 'available', 'in stock', 'do you have']
    if any(kw in user_message.lower() for kw in product_keywords):
        products = get_all_products()
        context_parts.append(f"Product Catalog:\n{json.dumps(products, indent=2)}")

    if context_parts:
        return "[SYSTEM INFO - Do not show to customer]\n" + "\n\n".join(context_parts) + "\n\n---\nCustomer message: " + user_message
    return user_message


def history_to_gemini(history):
    """Flask session geçmişini Gemini formatına çevir."""
    gemini_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})
    return gemini_history


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    if 'history' not in session:
        session['history'] = []

    enriched_message = build_context_message(user_message)

    try:
        # Gemini chat oturumu oluştur
        chat_session = model.start_chat(history=history_to_gemini(session['history']))
        response = chat_session.send_message(enriched_message)
        assistant_message = response.text

        # Geçmişe ekle
        session['history'].append({"role": "user", "content": enriched_message})
        session['history'].append({"role": "assistant", "content": assistant_message})

        if len(session['history']) > 20:
            session['history'] = session['history'][-20:]

        session.modified = True
        return jsonify({'response': assistant_message, 'message_count': len(session['history'])})

    except Exception as e:
        return jsonify({'error': f'API error: {str(e)}'}), 500


@app.route('/reset', methods=['POST'])
def reset():
    session.pop('history', None)
    return jsonify({'status': 'ok', 'message': 'Conversation reset'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
