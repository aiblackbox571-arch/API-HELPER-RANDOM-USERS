from flask import Flask, jsonify, request
from flask_cors import CORS
from faker import Faker
import random

app = Flask(__name__)
CORS(app)

faker = Faker('en_IN')

def generate_user():
    gender = random.choice(["Male", "Female"])
    if gender == "Male":
        name = faker.name_male()
        father_name = faker.name_male()
    else:
        name = faker.name_female()
        father_name = faker.name_male()

    job = faker.job()
    salary_ranges = {
        "Software Engineer": (60000, 200000),
        "Teacher": (20000, 80000),
        "Doctor": (80000, 300000),
        "Sales Executive": (15000, 60000),
        "Clerk": (10000, 30000),
    }
    salary_min, salary_max = salary_ranges.get(job, (25000, 120000))
    salary = f"₹{random.randint(salary_min, salary_max):,}"

    return {
        "name": name,
        "father_name": father_name,
        "gender": gender,
        "age": random.randint(18, 60),
        "email": faker.mail(),
        "phone": faker.phone_number(),
        "job": job,
        "salary": salary,
        "country": "India",
        "address": faker.address().replace("\n", ", "),
    }

@app.route('/')
def home():
    return jsonify({
        "message": "✅ Fake User API running successfully!",
        "usage": "/api/users?count=10"
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    count = request.args.get('count', default=1, type=int)
    users = [generate_user() for _ in range(count)]
    return jsonify(users)

# 🔥 Vercel expects a variable called `app`
# So DO NOT rename this to `handler` or wrap it — this works correctly
# Just export `app` directly.
# Remove `app.run()` since Vercel runs it automatically.

