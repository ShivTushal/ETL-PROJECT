from flask import Flask, render_template, request, redirect
from db_config import get_connection

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])
        gender = request.form["gender"]
        insurance_type = request.form["preferred_insurance_type"]
        interest_level = request.form["interest_level"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO insurance_interest 
            (name, age, gender, preferred_insurance_type, interest_level) 
            VALUES (%s, %s, %s, %s, %s)
        """, (name, age, gender, insurance_type, interest_level))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
