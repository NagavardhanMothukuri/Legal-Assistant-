from application import app, db
from flask import render_template, request, redirect, flash, url_for, jsonify
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegisterForm, LoginForm, QueryForm, ReplyForm, ContactForm, NewsletterForm
from PyPDF2 import PdfReader
import requests
import json

# API Keys
NEWS_API_KEY = "ebde2f3c54a9426abb4bb84becd4c61d"
OPENROUTER_API_KEY = "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"

# Global variable to store uploaded PDF text
uploaded_text = ""

# Routes

@app.route("/")
def index():
    return render_template("index.html", contact_form=ContactForm(), newsletter_form=NewsletterForm())

@app.route("/subscribe_newsletter", methods=['POST'])
def subscribe_newsletter():
    form = NewsletterForm()
    if form.validate_on_submit():
        db.newsletter_subscribers.insert_one({
            "email": form.email.data,
            "date_subscribed": datetime.utcnow()
        })
        flash("Thank you for subscribing to our newsletter!", "success")
    else:
        flash("There was an error with your subscription. Please try again.", "danger")
    return redirect(url_for('index'))

@app.route("/submit_contact", methods=['POST'])
def submit_contact():
    form = ContactForm()
    if form.validate_on_submit():
        db.contacts.insert_one({
            "name": form.name.data,
            "email": form.email.data,
            "subject": form.subject.data,
            "message": form.message.data,
            "date_submitted": datetime.utcnow()
        })
        flash("Thank you for your message! We'll get back to you soon.", "success")
    else:
        flash("There was an error with your submission. Please try again.", "danger")
    return redirect(url_for('index'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate():
        hashed_password = generate_password_hash(form.password.data)
        result = db.users.insert_one({
            "username": form.username.data,
            "email": form.email.data,
            "password": hashed_password,
            "date_registered": datetime.utcnow()
        })
        flash("Registration successful", "success")
        return redirect(url_for("home", id=str(result.inserted_id)))
    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.users.find_one({"email": form.email.data})
        if user and check_password_hash(user["password"], form.password.data):
            flash("Login successful", "success")
            return redirect(url_for("home", id=str(user["_id"])))
        flash("Invalid email or password", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    flash("Logged out successfully", "success")
    return redirect(url_for("index"))

@app.route("/profile/<id>")
def profile(id):
    user_details = db.users.find_one({"_id": ObjectId(id)})
    return render_template("profile.html", user=user_details)

@app.route("/home/<id>")
def home(id):
    user_details = db.users.find_one({"_id": ObjectId(id)})
    articles = []

    try:
        response = requests.get(f"https://newsapi.org/v2/everything?q=legal+india&apiKey={NEWS_API_KEY}")
        if response.status_code == 200:
            articles = response.json().get("articles", [])
    except Exception as e:
        print(f"Error fetching news: {e}")

    return render_template("home.html", news=articles, user=user_details)

@app.route("/community/<id>")
def community(id):
    user = db.users.find_one({"_id": ObjectId(id)})
    user_queries = list(db.queries.find({"questioner_id": id}))
    other_queries = list(db.queries.find({"questioner_id": {"$ne": id}}))
    return render_template("community.html", user=user, user_queries=user_queries, other_queries=other_queries)

@app.route("/nearby_lawyer/<id>")
def nearby_lawyer(id):
    user = db.users.find_one({"_id": ObjectId(id)})
    lawyers_detail = list(db.lawyers.find({}))
    domains = sorted(set(l.get("domain") for l in lawyers_detail))
    cities = sorted(set(l.get("city_of_practice") for l in lawyers_detail))
    return render_template("nearby_lawyer.html", user=user, lawyers=json.dumps(lawyers_detail, default=str), domains=domains, cities=cities)

@app.route("/post_query/<id>", methods=['GET', 'POST'])
def post_query(id):
    form = QueryForm()
    if request.method == "POST" and form.validate_on_submit():
        db.queries.insert_one({
            "questioner_id": id,
            "title": form.title.data,
            "description": form.description.data,
            "domain": form.domain.data,
            "date_posted": datetime.utcnow(),
            "replies": []
        })
        flash("Query posted successfully", "success")
        return redirect(url_for("community", id=id))
    return render_template("post_query.html", form=form)

@app.route("/reply/<query_id>/<id>", methods=['GET', 'POST'])
def reply(query_id, id):
    query = db.queries.find_one({"_id": ObjectId(query_id)})
    if not query:
        flash("Query not found!", "danger")
        return redirect(url_for('community', id=id))

    form = ReplyForm()
    replyer = db.users.find_one({"_id": ObjectId(id)})
    username = replyer.get("username", "Unknown User")

    if form.validate_on_submit():
        db.queries.update_one(
            {"_id": ObjectId(query_id)},
            {"$push": {
                "replies": {
                    "replyer": username,
                    "text": form.reply_text.data,
                    "timestamp": datetime.utcnow()
                }
            }}
        )
        flash("Reply posted successfully!", "success")
        return redirect(url_for('community', id=id))

    return render_template("reply.html", form=form, query=query)

@app.route('/AI_assistance/<id>')
def AI_assistance(id):
    user = db.users.find_one({"_id": ObjectId(id)})
    return render_template('AI_assistance.html', user=user)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [{"role": "user", "content": [{"type": "text", "text": user_message}]}]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Flask Chat App"
            },
            data=json.dumps(payload)
        )
        if response.status_code == 200:
            return jsonify({'response': response.json()['choices'][0]['message']['content']})
        return jsonify({'error': f"API Error: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/document_assistance/<id>')
def document_assistance(id):
    user = db.users.find_one({"_id": ObjectId(id)})
    return render_template('document_assistance.html', user=user)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global uploaded_text
    file = request.files.get('pdf')
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

    reader = PdfReader(file)
    uploaded_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return jsonify({'message': 'PDF uploaded successfully'}), 200

@app.route('/chat_with_document', methods=['POST'])
def document_chat():
    global uploaded_text
    if not uploaded_text:
        return jsonify({'error': 'No PDF uploaded. Please upload a PDF first.'}), 400

    user_message = request.json['message']
    prompt = f"The following text is extracted from a PDF:\n\n{uploaded_text}\n\nQuestion: {user_message}\nAnswer:"

    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Chat with PDF"
            },
            data=json.dumps(payload)
        )
        if response.status_code == 200:
            return jsonify({'response': response.json()['choices'][0]['message']['content']})
        return jsonify({'error': f"API Error: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
