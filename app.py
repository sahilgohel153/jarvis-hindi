from flask import Flask, render_template, request, jsonify
import requests
import json
import re
import os

app = Flask(__name__)

# ✅ API key from environment variable (set in Render)
API_KEY = os.getenv("API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://example.com",
    "X-Title": "Jarvis Assistant"
}

# ✅ Clean the AI response
def clean_response(text):
    text = re.sub(r'\\n|\n|\r', ' ', text)
    text = re.sub(r'[*_#>\[\]{}|]', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

# ✅ Ask Jarvis logic
def ask_jarvis(prompt):
    prompt_lower = prompt.lower().strip()

    # Custom replies
    if any(phrase in prompt_lower for phrase in ["who is your developer", "who made you", "तुम्हें किसने बनाया"]):
        return (
            "मेरे निर्माता साहिल गोहेल हैं — एक इंजीनियरिंग छात्र जिनमें टेक्नोलॉजी, क्रिएटिविटी और इनोवेशन के प्रति गहरी रुचि है।"
        )

    # AI Response
    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "तुम जार्विस हो — एक बुद्धिमान और मददगार हिंदी बोलने वाला सहायक। हमेशा उपयोगकर्ता की भाषा में जवाब दो, यदि संभव हो तो हिंदी में जवाब दो।"
            },
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(API_URL, headers=HEADERS, data=json.dumps(data))
        result = res.json()
        reply = result["choices"][0]["message"]["content"]
        return clean_response(reply)
    except Exception as e:
        return f"⚠️ एरर: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt")
    reply = ask_jarvis(prompt)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
