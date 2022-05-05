from app import app
from flask import render_template, request, redirect
from flask import session
import users, courses

@app.route("/")
def index():
    return render_template("index.html", courses=courses.get_courses())

@app.route("/course/<int:course_id>")
def course(course_id):
        return render_template("course.html", course=courses.get_course(course_id))

@app.route("/create", methods=["get","post"])
def create_course():
    if request.method == "GET":
        if session["user_role"] == 1:
            return redirect("/")
        users.require_role(2)
        return render_template("create.html")
    if request.method == "POST":
        course_name = request.form["course_name"]
        if courses.create_course(course_name):
            return redirect("/")
        return render_template("error.html", message="Kurssin lisääminen ei onnistunut.")

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", message="Käyttäjätunnus ei ole kelvollinen")
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("error.html", message="Salasanat eivät ole samat")
    if password1 == "":
        return render_template("error.html", message="Aseta salasana")
    role = request.form["role"]
    if role not in ("1", "2"):
        return render_template("error.html", message="Tuntematon käyttäjärooli")
    if users.register(username,password2,role):
        return redirect("/")
    if not users.register(username, password2, role):
        return render_template("error.html", message="Käyttäjätunnus on varattu")
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
