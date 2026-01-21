import logging
import re  # NEW: Regular Expressions for smart matching
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import pooling

# -----------------------------------------------------------
# 1. LOGGING SETUP
# -----------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# -----------------------------------------------------------
# 2. DATABASE CONNECTION POOLING
# -----------------------------------------------------------
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'fyp_chatbot_db',
    'pool_name': "chatbot_pool",
    'pool_size': 5
}

try:
    db_pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)
    logger.info("✅ Database Connection Pool Created Successfully!")
except Exception as e:
    logger.error(f"❌ Error creating DB Pool: {e}")

# -----------------------------------------------------------
# 3. HELPER FUNCTIONS
# -----------------------------------------------------------
def execute_read_query(query, params=None):
    conn = None
    cursor = None
    result = None
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchone()
    except Exception as e:
        logger.error(f"DB Read Error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    return result

def execute_read_all(query, params=None):
    conn = None
    cursor = None
    result = []
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchall()
    except Exception as e:
        logger.error(f"DB Read All Error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    return result

def execute_write_query(query, params):
    conn = None
    cursor = None
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"DB Write Error: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# -----------------------------------------------------------
# SMALL TALK DATA
# -----------------------------------------------------------
SMALL_TALK_RESPONSES = {
    "thank you": "You’re welcome! If you need anything else, feel free to ask. 🌟",
    "thanks": "You’re welcome! If you need anything else, feel free to ask. 🌟",
    "take care": "Take care! If you need more help, just send me a message. 👋",
    "good evening": "Good evening! 🌙 How can I assist you today?",
    "good afternoon": "Good Afternoon! How can I assist you today?",
    "good morning": "Good morning! ☀️ Hope you're doing well. How can I help you today?",
    "how are you": "I’m doing great, thank you for asking! 🤖 How can I help you today?",
    "hello": "Hello! 👋 How can I assist you today?",
    "hi": "Hi there! 👋 How can I assist you today?",
    "hey": "Hey! 👋 How can I assist you today?"
}

def get_small_talk_reply(user_message: str):
    if not user_message: return None
    msg = user_message.lower().strip()
    
    # 1. Exact Match
    if msg in SMALL_TALK_RESPONSES: return SMALL_TALK_RESPONSES[msg]
    
    # 2. Smart Word Match (Fixes 'Graphic' containing 'hi')
    # Hum Regex use kar rahe hain taake wo sirf ALAG se likhay hue "hi" ko pakray.
    # Grap-hi-c ko ignore karega.
    for key in SMALL_TALK_RESPONSES:
        # \b ka matlab hai "Word Boundary" (Lafz ka kinara)
        pattern = r'\b' + re.escape(key) + r'\b'
        if re.search(pattern, msg):
            return SMALL_TALK_RESPONSES[key]
            
    return None

# -----------------------------------------------------------
# MAIN WEBHOOK ROUTE
# -----------------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    return "🚀 ZTTI Chatbot Backend is Running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    user_message = req.get('queryResult', {}).get('queryText', '') or ''
    intent = req.get('queryResult', {}).get('intent', {}).get('displayName', '')
    output_contexts = req.get('queryResult', {}).get('outputContexts', [])

    # --- INTERCEPT CORRECTION LOGIC ---
    correction_context = next((ctx for ctx in output_contexts if 'awaiting_course_correction' in ctx.get('name', '')), None)
    if correction_context:
        saved_params = correction_context.get('parameters', {})
        req['queryResult']['parameters'] = saved_params
        req['queryResult']['parameters']['course'] = user_message 
        return register_student(req)

    # Small Talk (Now Smarter!)
    small_talk = get_small_talk_reply(user_message)
    if small_talk: return jsonify({'fulfillmentText': small_talk})

    # Intent Routing
    intent_map = {
        "Default Welcome Intent": welcome_response,
        "GetCourseInfo": get_course_info,
        "GetSchedule": get_schedule,
        "RegisterStudent": register_student,
        "CertificateStatus": get_certificate_status,
        "ListActiveCourses": list_active_courses,
        "ContactInfo": get_contact_info,
        "CourseRecommendation": get_course_recommendation
    }

    if intent in intent_map:
        return intent_map[intent](req)
    else:
        return jsonify({'fulfillmentText': f"No handler for intent: {intent}"})

# -----------------------------------------------------------
# DEFAULT RESPONSE/WELCOME MESSAGE
# -----------------------------------------------------------
def welcome_response(req):
    return jsonify({
        "fulfillmentMessages": [
            {
                "payload": {
                    "richContent": [
                        [
                            {
                                "type": "description",
                                "title": "Hi there! I'm your virtual assistant. 🤖",
                                "text": [
                                    "You can ask me about:",
                                    "🔹 Available training courses & fees",
                                    "🔹 Class schedules & timings",
                                    "🔹 Student registration",
                                    "🔹 Certificate status",
                                    "🔹 Course recommendations"
                                ]
                            },
                            {
                                "type": "chips",
                                "options": [
                                    {"text": "Show Courses"},
                                    {"text": "Register Now"},
                                    {"text": "Contact Info"}
                                ]
                            }
                        ]
                    ]
                }
            }
        ]
    })

def get_contact_info(req):
    return jsonify({'fulfillmentText': (
        "📞 You can contact us at: +92345398200 or arslanakhtar868@gmail.com \n\n"
        "📍 Our training center is located at: Saddar Rawalpindi."
    )})

# -----------------------------------------------------------
# GET COURSE INFO (SMART FALLBACK ADDED)
# -----------------------------------------------------------
def get_course_info(req):
    # Dialogflow se parameter nikalo
    course = req['queryResult']['parameters'].get('course')
    
    # --- SMART FALLBACK ---
    # Agar Dialogflow ne course nahi pakra (e.g. "Python Programming" likha aur param khali aaya)
    # To hum khud Database check karenge ke user ke sentence mein koi course hai ya nahi.
    if not course:
        user_text = req.get('queryResult', {}).get('queryText', '')
        all_courses = execute_read_all("SELECT course_name FROM courses")
        
        if all_courses:
            for r in all_courses:
                db_course_name = r[0]
                # Check karo agar DB ka course user ke message mein mojood hai
                if db_course_name.lower() in user_text.lower():
                    course = db_course_name
                    break

    # Agar ab bhi course nahi mila, tab poocho
    if not course:
        return jsonify({'fulfillmentText': "Could you please specify which course you want to know about?"})

    sql = "SELECT course_name, fee, duration, mode FROM courses WHERE course_name LIKE %s"
    row = execute_read_query(sql, (f"%{course}%",))

    if row:
        name, fee, duration, mode = row
        reply = (
            f"🎓 Here are the details for **{name}**:\n\n"
            f"⏳ Duration: {duration}\n"
            f"💰 Fee: {fee}\n"
            f"📍 Mode: {mode}"
        )
    else:
        reply = f"Sorry, I couldn't find detailed information for the course '{course}' in our database."
    
    return jsonify({'fulfillmentText': reply})

def get_schedule(req):
    course = req['queryResult']['parameters'].get('course')
    
    # Same smart fallback here
    if not course:
        user_text = req.get('queryResult', {}).get('queryText', '')
        all_courses = execute_read_all("SELECT course_name FROM courses")
        if all_courses:
            for r in all_courses:
                if r[0].lower() in user_text.lower():
                    course = r[0]
                    break

    if not course:
        return jsonify({'fulfillmentText': "Which course schedule do you need?"})

    sql = "SELECT days, timing FROM schedules WHERE course_name LIKE %s"
    row = execute_read_query(sql, (f"%{course}%",))

    if row:
        days, timing = row
        reply = (
            f"📅 **Schedule for {course}**:\n\n"
            f"🗓 Days: {days}\n"
            f"⏰ Timing: {timing}"
        )
    else:
        reply = f"Sorry, I do not have schedule information for '{course}'."

    return jsonify({'fulfillmentText': reply})

def register_student(req):
    params = req['queryResult']['parameters']
    name = params.get('name')
    phone = params.get('phone')
    email = params.get('email')
    course_input = params.get('course')
    session_id = req['session']

    if course_input == "RETRY":
        rows = execute_read_all("SELECT course_name FROM courses")
        course_list = " | ".join([r[0] for r in rows]) if rows else "No courses found"
        return jsonify({
            "fulfillmentText": (
                f"🚫 Sorry, we don't have a course named that.\n"
                f"Available Courses:\n🔹 {course_list}\n\n"
                f"Please type the course name again:"
            ),
            "outputContexts": [{
                "name": f"{session_id}/contexts/awaiting_course_correction",
                "lifespanCount": 1,
                "parameters": {"name": name, "phone": phone, "email": email, "course": None}
            }]
        })

    check_sql = "SELECT course_name FROM courses WHERE course_name LIKE %s"
    row = execute_read_query(check_sql, (f"%{course_input}%",))

    if not row:
        return jsonify({
            "followupEventInput": {
                "name": "RETRY_COURSE",
                "languageCode": "en-US",
                "parameters": {"name": name, "phone": phone, "email": email, "course": "RETRY"}
            }
        })

    official_course = row[0]
    insert_sql = "INSERT INTO registrations (student_name, phone, email, course_selected) VALUES (%s, %s, %s, %s)"
    success = execute_write_query(insert_sql, (name, phone, email, official_course))

    if success:
        return jsonify({
            'fulfillmentText': (
                f"✅ Thank you **{name}**!\n\n"
                f"You have been successfully registered for the **{official_course}** course.\n"
                "Our team will contact you soon with further details."
            ),
            "outputContexts": [{"name": f"{session_id}/contexts/awaiting_course_correction", "lifespanCount": 0}]
        })
    else:
        return jsonify({'fulfillmentText': "❌ System Error: Could not save registration."})

def get_certificate_status(req):
    email = req['queryResult']['parameters'].get('email')
    rows = execute_read_all("SELECT course_name, status FROM certificates WHERE email LIKE %s", (f"%{email}%",))

    if not rows:
        return jsonify({'fulfillmentText': f"🚫 I could not find any certificate record for {email}.\nPlease make sure you are using your registered email. or Contact us on: 03345398200 or arslanakhtar868@gmail.com "})
    
    lines = [f"• {r[0]}: {r[1]}" for r in rows]
    return jsonify({'fulfillmentText': f"📜 **Certificate Status for {email}**:\n\n" + "\n".join(lines)})

def list_active_courses(req):
    rows = execute_read_all("SELECT course_name FROM courses")
    if not rows:
        return jsonify({"fulfillmentText": "No active courses found."})
    
    course_names = [r[0] for r in rows]
    text = "📚 **Our Active Courses:**\n\n🔹 " + "\n🔹 ".join(course_names)
    chips = [{"text": name} for name in course_names]
    
    return jsonify({
        "fulfillmentText": text,
        "fulfillmentMessages": [
            {"text": {"text": [text]}},
            {"payload": {"richContent": [[{"type": "chips", "options": chips}]]}}
        ]
    })

def get_course_recommendation(req):
    params = req.get('queryResult', {}).get('parameters', {})
    interest = str(params.get('interest', '') or req.get('queryResult', {}).get('queryText', '')).lower()
    
    reply = (
        "Based on your interest, I would recommend starting with either:\n\n"
        "🐍 Python Programming (for IT/Coding)\n"
        "📄 MS Office Professional (for Office skills)\n\n"
        "You can also ask about any specific course for more details."
    )

    if "ms_office" in interest or "office" in interest or "excel" in interest:
        reply = "👉 I recommend the **MS Office Professional** course for office skills."
    elif "programming" in interest or "it" in interest or "developer" in interest or "python" in interest:
        reply = "👉 You should start with our **Python Programming** course for IT career."
    elif "design" in interest or "graphic" in interest:
        reply = "👉 I recommend our **Graphic Designing** course for creative skills."
    elif "data" in interest or "analysis" in interest:
        reply = "👉 You can plan to move towards our **Data Science** course."
    
    return jsonify({'fulfillmentText': reply})

if __name__ == '__main__':
    app.run(port=5000, debug=True)