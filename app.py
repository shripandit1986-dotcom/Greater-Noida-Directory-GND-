from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# ---------------- APP ----------------
app = Flask(__name__)

# ---------------- DATABASE ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gnd.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

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

    paid = db.Column(db.Boolean, default=False)
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

        return redirect("/payment")

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

# ---------------- PAYMENT ----------------
@app.route("/payment")
def payment():
    return render_template("payment.html")


@app.route("/payment-success", methods=["POST"])
def payment_success():
    return "Payment Successful! Your listing is pending approval."

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=10000)
