from flask import Flask, render_template, request
import psycopg2


app = Flask(__name__)
POSTGRESQL_URI = "postgres://auhynhue:C0AKJymesUvuIeEn9OeTx5f3SkXn7_Qr@topsy.db.elephantsql.com/auhynhue"

connection = psycopg2.connect(POSTGRESQL_URI)

try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE todolist (task TEXT, deadline DATE);")
except psycopg2.errors.DuplicateTable:
    pass


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print(request.form)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO todolist VALUES (%s, %s);",
                    (
                        request.form.get("task"),
                        request.form.get("deadline")
                    ),
                )
    return render_template("form.html")


@app.route("/tasks", methods=["GET", "POST"])
def all_tasks():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM todolist;"
            )
            task_details = cursor.fetchall()

    return render_template("schedule.html", entries=task_details)


app.run(debug=True)
