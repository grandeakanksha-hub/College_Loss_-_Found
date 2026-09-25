from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "secret"

# -----------------------------------
# UPLOAD SETTINGS
# -----------------------------------

UPLOAD_FOLDER = "static/uploads"

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create upload folder automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------------
# CHECK FILE EXTENSION
# -----------------------------------

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

def db():

    conn = sqlite3.connect("lost_found.db")

    conn.row_factory = sqlite3.Row

    return conn


# -----------------------------------
# HOME
# -----------------------------------

@app.route("/")
def home():

    return redirect("/login")


# -----------------------------------
# REGISTER
# -----------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    msg = ""

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        con = db()

        try:

            con.execute(
                """
                INSERT INTO users(name, email, password)
                VALUES(?,?,?)
                """,
                (name, email, password)
            )

            con.commit()
            con.close()

            return redirect("/login")

        except sqlite3.IntegrityError:

            con.close()

            msg = "Email already registered!"

    return render_template(
        "register.html",
        msg=msg
    )


# -----------------------------------
# LOGIN
# -----------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    msg = ""

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        con = db()

        user = con.execute(
            """
            SELECT * FROM users
            WHERE email=? AND password=?
            """,
            (email, password)
        ).fetchone()

        con.close()

        if user:

            session["user"] = user["name"]

            return redirect("/dashboard")

        else:

            msg = "Please register before login!"

    return render_template(
        "login.html",
        msg=msg
    )


# -----------------------------------
# LOGOUT
# -----------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# -----------------------------------
# DASHBOARD
# -----------------------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect("/login")

    con = db()

    total = con.execute(
        "SELECT COUNT(*) FROM items"
    ).fetchone()[0]

    lost = con.execute(
        "SELECT COUNT(*) FROM items WHERE type='Lost'"
    ).fetchone()[0]

    found = con.execute(
        "SELECT COUNT(*) FROM items WHERE type='Found'"
    ).fetchone()[0]

    claims = con.execute(
        "SELECT COUNT(*) FROM items WHERE status='Claimed'"
    ).fetchone()[0]

    con.close()

    return render_template(
        "dashboard.html",
        total=total,
        lost=lost,
        found=found,
        claims=claims
    )


# -----------------------------------
# REPORT LOST / FOUND
# -----------------------------------

@app.route("/report/<kind>", methods=["GET", "POST"])
def report(kind):

    # --------------------------------
    # CHECK TYPE
    # --------------------------------

    if kind not in ["lost", "found"]:

        return redirect("/dashboard")


    # --------------------------------
    # SAVE ITEM
    # --------------------------------

    if request.method == "POST":

        title = request.form["title"]

        category = request.form["category"]

        description = request.form["description"]

        location = request.form["location"]

        date = request.form["date"]


        # --------------------------------
        # IMAGE UPLOAD
        # --------------------------------

        image_file = request.files.get("image")

        image_filename = ""


        if image_file and image_file.filename:

            if allowed_file(image_file.filename):

                filename = secure_filename(
                    image_file.filename
                )

                # Prevent duplicate filename problems
                base, extension = os.path.splitext(filename)

                counter = 1

                original_filename = filename

                while os.path.exists(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )
                ):

                    filename = (
                        f"{base}_{counter}{extension}"
                    )

                    counter += 1

                image_file.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )

                image_filename = filename

            else:

                return "Invalid image format. Please upload JPG, JPEG, PNG, GIF or WEBP."


        # --------------------------------
        # INSERT INTO DATABASE
        # --------------------------------

        data = (
            title,
            category,
            description,
            location,
            date,
            kind.capitalize(),
            "Open",
            image_filename,
            ""
        )

        con = db()

        con.execute(
            """
            INSERT INTO items
            (
                title,
                category,
                description,
                location,
                date,
                type,
                status,
                image,
                claimer
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            data
        )

        con.commit()

        con.close()

        return redirect("/items")


    # --------------------------------
    # SHOW CORRECT PAGE
    # --------------------------------

    if kind == "lost":

        return render_template(
            "report_lost.html"
        )

    else:

        return render_template(
            "report_found.html"
        )


# -----------------------------------
# VIEW ITEMS
# -----------------------------------

@app.route("/items")
def items():

    if "user" not in session:

        return redirect("/login")

    q = request.args.get("q", "")

    con = db()

    items = con.execute(
        """
        SELECT * FROM items
        WHERE title LIKE ?
        ORDER BY id DESC
        """,
        ("%" + q + "%",)
    ).fetchall()

    con.close()

    return render_template(
        "items.html",
        items=items
    )


# -----------------------------------
# CLAIM ITEM
# -----------------------------------

@app.route("/claim/<int:id>")
def claim(id):

    if "user" not in session:

        return redirect("/login")

    con = db()

    con.execute(
        """
        UPDATE items
        SET status='Claimed',
            claimer=?
        WHERE id=?
        """,
        (
            session["user"],
            id
        )
    )

    con.commit()

    con.close()

    return redirect("/items")


# -----------------------------------
# EDIT ITEM
# -----------------------------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    if "user" not in session:

        return redirect("/login")

    con = db()

    if request.method == "POST":

        con.execute(
            """
            UPDATE items
            SET title=?,
                category=?,
                status=?
            WHERE id=?
            """,
            (
                request.form["title"],
                request.form["category"],
                request.form["status"],
                id
            )
        )

        con.commit()

        con.close()

        return redirect("/items")


    item = con.execute(
        """
        SELECT * FROM items
        WHERE id=?
        """,
        (id,)
    ).fetchone()

    con.close()

    return render_template(
        "edit_item.html",
        item=item
    )


# -----------------------------------
# DELETE ITEM
# -----------------------------------

@app.route("/delete/<int:id>")
def delete(id):

    if "user" not in session:

        return redirect("/login")

    con = db()

    con.execute(
        "DELETE FROM items WHERE id=?",
        (id,)
    )

    con.commit()

    con.close()

    return redirect("/items")


# -----------------------------------
# RUN APPLICATION
# -----------------------------------

if __name__ == "__main__":

    app.run(debug=True)