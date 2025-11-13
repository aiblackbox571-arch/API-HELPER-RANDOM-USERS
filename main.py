from flask import Flask, jsonify, request
from flask_cors import CORS
from faker import Faker
import random

app = Flask(__name__)
CORS(app)

faker = Faker('en_IN')

def generate_user():
    job = faker.job()

    job_age_map = {
        "Student": (18, 25),
        "Software Engineer": (22, 40),
        "Teacher": (25, 55),
        "Doctor": (28, 60),
        "Businessperson": (25, 65),
        "Police Officer": (23, 50),
        "Driver": (21, 55),
        "Retired": (60, 85),
        "Engineer": (23, 45),
        "Laborer": (20, 55),
    }

    job_salary_map = {
        "Student": (0, 15000),
        "Software Engineer": (35000, 200000),
        "Teacher": (20000, 80000),
        "Doctor": (50000, 300000),
        "Businessperson": (40000, 500000),
        "Police Officer": (30000, 100000),
        "Driver": (15000, 60000),
        "Retired": (0, 40000),
        "Engineer": (25000, 150000),
        "Laborer": (10000, 40000),
    }

    matched_job = next((k for k in job_age_map if k.lower() in job.lower()), "Engineer")
    age_min, age_max = job_age_map.get(matched_job, (21, 60))
    salary_min, salary_max = job_salary_map.get(matched_job, (20000, 100000))

    age = random.randint(age_min, age_max)
    salary = f"₹{random.randint(salary_min, salary_max):,}"

    gender = faker.random_element(elements=("Male", "Female"))
    if gender == "Male":
        first_name = faker.first_name_male()
        father_name = faker.first_name_male()
    else:
        first_name = faker.first_name_female()
        father_name = faker.first_name_male()

    last_name = faker.last_name()
    full_name = f"{first_name} {last_name}"
    email = f"{first_name.lower()}.{last_name.lower()}@{faker.free_email_domain()}"
    phone = f"+91{random.randint(6000000000, 9999999999)}"

    return {
        "name": full_name,
        "gender": gender,
        "father_name": f"{father_name} {last_name}",
        "email": email,
        "phone": phone,
        "age": age,
        "job": job,
        "salary": salary,
        "country": "India",
        "state": faker.state(),
        "city": faker.city(),
        "address": faker.address().replace("\n", ", "),
        "postal_code": faker.postcode(),
    }


@app.route('/')
def home():
    return jsonify({
        "message": "✅ Welcome to the Indian User Data API on Vercel!",
        "usage": "/api/users?count=10"
    })


@app.route('/api/users', methods=['GET'])
def get_users():
    count = request.args.get('count', default=1, type=int)
    users = [generate_user() for _ in range(count)]
    return jsonify(users)


# ✅ Required for Vercel
def handler(event, context):
    return app(event, context)


if __name__ == '__main__':
    app.run(debug=True)
