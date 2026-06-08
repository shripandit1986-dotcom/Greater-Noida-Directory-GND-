from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

# ---------------- APP ----------------
app = Flask(__name__)
app.secret_key = "gnd_super_secret_key"
# ---------------- DATABASE ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gnd.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ADMIN_PASSWORD = "PasswordProMax777"

# ---------------- BUSINESS MODEL ----------------
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    category = db.Column(db.String(100))
    city = db.Column(db.String(100))
    address = db.Column(db.String(200))

    approved = db.Column(db.Boolean, default=False)
# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- ADD BUSINESS ----------------
@app.route("/add-business", methods=["GET", "POST"])
def add_business():

    if request.method == "POST":

        business = Business(
            name=request.form.get("name"),
            owner=request.form.get("owner"),
            phone=request.form.get("phone"),
            email=request.form.get("email"),
            category=request.form.get("category"),
            city=request.form.get("city"),
            address=request.form.get("address")
        )

        db.session.add(business)
        db.session.commit()

        return redirect("/")

    return render_template("add-business.html")

# ---------------- CATEGORY ----------------
@app.route("/category/<cat>")
def category(cat):

    businesses = Business.query.filter_by(
    category=cat,
    approved=True
).all()

    return render_template(
        "category.html",
        businesses=businesses,
        category=cat
    )

# ---------------- CONTACT ----------------
@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- GND ----------------
@app.route("/gnd")
def gnd():
    return "Greater Noida Directory (GND)"

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        password = request.form.get("password")

        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")

        return "Wrong Password"

    return render_template("admin-login.html")

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/admin-login")

    businesses = Business.query.all()

    return render_template(
        "admin.html",
        businesses=businesses
    )

@app.route("/approve/<int:id>")
def approve(id):

    if not session.get("admin"):
        return redirect("/admin-login")

    business = Business.query.get_or_404(id)

    business.approved = True

    db.session.commit()

    return redirect("/admin")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/test")
def test():
    businesses = Business.query.all()

    text = ""

    for b in businesses:
        text += f"{b.id} - {b.name}<br>"

    return text

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=10000)
