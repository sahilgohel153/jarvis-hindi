from flask import Flask, render_template, request, jsonify
import requests
import json
import re

app = Flask(__name__)

# === OpenRouter API Configuration ===
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://example.com",
    "X-Title": "Jarvis Assistant"
}

# === Clean up AI's response text
def clean_response(text):
    text = re.sub(r'\\n|\n|\r', ' ', text)
    text = re.sub(r'[*_#>\[\]{}|]', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

# === Handle Jarvis response logic
def ask_jarvis(prompt):
    prompt_lower = prompt.lower().strip()

    # ✅ Custom response for Sahil Gohel
    if any(phrase in prompt_lower for phrase in [
        "who is your developer", "who made you", "who created you", "who is your maker",
        "तुम्हें किसने बनाया", "तुम्हारे निर्माता कौन हैं"
    ]):
        return (
            "मेरे निर्माता साहिल गोहेल हैं — एक इंजीनियरिंग छात्र जिनमें टेक्नोलॉजी, क्रिएटिविटी और इनोवेशन के प्रति गहरी रुचि है। "
            "वो न केवल प्रोग्रामिंग और AI में माहिर हैं, बल्कि यूजर एक्सपीरियंस डिज़ाइन में भी उनकी खास समझ है। "
            "मुझे गर्व है कि उन्होंने मुझे बनाया।"
        )

    # ✅ Custom response for Manoj Gohel
    if any(phrase in prompt_lower for phrase in [
        "who is sahil's father", "who is my dad", "who manoj gohel", "manoj gohel kon chhe",
        "साहिल के पापा कौन हैं", "मनोज गोहेल कौन हैं"
    ]):
        return (
            "साहिल गोहेल के पिता का नाम मनोज गोहेल है। वे एक सरकारी कर्मचारी हैं और अपने काम में बहुत ही निपुण हैं। "
            "वे एक अच्छे पिता और एक नेक इंसान हैं। और हाँ, वह विमल बहुत पसंद करते हैं!"
        )
    if any(phrase in prompt_lower for phrase in [
        "who is sahil's mother", "who is my mom", "who bhavana gohel", "bhavana gohel kon chhe",
        "साहिल के माता  कौन हैं", "भावना गोहेल कौन हैं"
    ]):
        return (
            "मेरी मम्मी एक full-time housewife हैं।"
             " बहुत sweet हैं, दिल की भी kind हैं… लेकिन सोने में तो world record तोड़ दें! दिन हो या रात, बस सोती रहती हैं"
             "और वो भी बिना snoring के तो नींद पूरी ही नहीं होती! कभी-कभी लगता है उनकी snoring को Dolby Atmos में सुना जाए  लेकिन फिर भी,"
              " उनकी ममता और प्यार का कोई मुकाबला नहीं है!"
            
        )

    # 🧠 Default AI response in Hindi
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
        return f"⚠️ त्रुटि: {str(e)}"

# === Flask routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt")
    reply = ask_jarvis(prompt)
    return jsonify({"reply": reply})

# === Run on local IP for phone access
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)
