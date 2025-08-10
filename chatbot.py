# chatbot.py
import re
import random
import json
import os

PROFILE_FILE = 'user_profile.json'

# load saved user info (simple "memory")
if os.path.exists(PROFILE_FILE):
    with open(PROFILE_FILE, 'r') as f:
        user_profile = json.load(f)
else:
    user_profile = {}

# small built-in knowledge & word lists
greetings = ['hi', 'hello', 'hey', 'hii']
thanks_words = ['thanks', 'thank you', 'thx']
faqs = {
    'what is your name': "I'm SimpleBot — a small Python chatbot.",
    'how are you': "I'm code, so I'm always ready! How can I help?",
    'what can you do': "I can chat, do simple math, remember your name, and answer a few basic questions."
}

def save_profile():
    with open(PROFILE_FILE, 'w') as f:
        json.dump(user_profile, f)

# math responder: finds expressions like "5 + 3" and calculates
def respond_math(text):
    m = re.search(r'(-?\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(-?\d+(?:\.\d+)?)', text)
    if m:
        a, op, b = m.groups()
        a = float(a); b = float(b)
        try:
            if op == '+': res = a + b
            elif op == '-': res = a - b
            elif op == '*': res = a * b
            elif op == '/': res = a / b
            # make integers pretty
            if res.is_integer():
                res = int(res)
            return f"The answer is {res}."
        except Exception:
            return "I can't compute that (maybe division by zero)."
    return None

# try to capture "my name is ..." or "i am ..."
def get_name_from_text(text):
    m = re.search(r'\b(?:my name is|i am|i\'m|im)\s+([A-Za-z][A-Za-z0-9_-]*)', text, re.I)
    if m:
        return m.group(1).capitalize()
    return None

def get_response(text):
    text = text.strip()
    low = text.lower()

    # set name if user told it
    name = get_name_from_text(text)
    if name:
        user_profile['name'] = name
        save_profile()
        return f"Nice to meet you, {name}!"

    # greetings
    if any(word in low for word in greetings):
        if 'name' in user_profile:
            return f"Hello {user_profile['name']}! What would you like to do?"
        else:
            return "Hello! What's your name?"

    # math
    math_ans = respond_math(low)
    if math_ans:
        return math_ans

    # simple FAQ match
    for q, a in faqs.items():
        if q in low:
            return a

    # thanks
    if any(t in low for t in thanks_words):
        return "You're welcome!"

    # fallback help text
    return random.choice([
        "Sorry, I didn't get that. Try: 'my name is <YourName>' or 'what is 5 + 7'.",
        "I can do simple math and remember your name. Try 'what can you do'.",
        "Try asking: 'what is 12 / 4' or tell me 'my name is ...'."
    ])

def main():
    print("SimpleBot v1 — type 'quit' or 'exit' to leave.")
    if 'name' in user_profile:
        print(f"Welcome back, {user_profile['name']}!")
    while True:
        user = input("You: ").strip()
        if not user:
            continue
        if user.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print("SimpleBot: Bye! 👋")
            break
        resp = get_response(user)
        print("SimpleBot:", resp)

if __name__ == '__main__':
    main()
