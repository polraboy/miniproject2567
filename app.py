from flask import Flask, render_template, redirect, url_for, request, flash
import qrcode
import re
import pymysql
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/coffee_images"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}
app.secret_key = os.urandom(24)  # สร้าง secret key แบบสุ่ม


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="miniproject",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM customer WHERE cus_username = %s AND cus_password = %s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()

                if result:
                    flash("เข้าสู่ระบบสำเร็จ!", "success")
                    return redirect(url_for("index"))
                else:
                    flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง", "error")
        finally:
            conn.close()

    return render_template("login.html")

@app.route("/logout")
def logout():
    
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        phone = request.form["phone"]

        if password != confirm_password:
            flash("รหัสผ่านไม่ตรงกัน", "error")
            return render_template("register.html")

        if not re.match(r"^\d{10}$", phone):
            flash("เบอร์โทรศัพท์ไม่ถูกต้อง", "error")
            return render_template("register.html")

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM customer WHERE cus_username = %s"
                cursor.execute(sql, (username,))
                if cursor.fetchone():
                    flash("ชื่อผู้ใช้นี้มีอยู่แล้ว", "error")
                    return render_template("register.html")

                sql = "INSERT INTO customer (cus_name, cus_username, cus_password, cus_phone) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, username, password, phone))
                conn.commit()

                flash("สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ", "success")
                return redirect(url_for("login"))
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/customer")
def customer():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT cus_id, cus_name, cus_username, cus_phone FROM customer"
            )
            customer = cursor.fetchall()
    finally:
        conn.close()
    return render_template("customer.html", customer=customer)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/edit_customer/<int:cus_id>", methods=["GET", "POST"])
def edit_customer(cus_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == "POST":
                cus_name = request.form["cus_name"]
                cus_username = request.form["cus_username"]
                cus_phone = request.form["cus_phone"]
                cus_password = request.form["cus_password"]

                # ตรวจสอบว่ามีการเปลี่ยนรหัสผ่านหรือไม่
                if cus_password:
                    sql = "UPDATE customer SET cus_name = %s, cus_username = %s, cus_phone = %s, cus_password = %s WHERE cus_id = %s"
                    cursor.execute(
                        sql, (cus_name, cus_username, cus_phone, cus_password, cus_id)
                    )
                else:
                    sql = "UPDATE customer SET cus_name = %s, cus_username = %s, cus_phone = %s WHERE cus_id = %s"
                    cursor.execute(sql, (cus_name, cus_username, cus_phone, cus_id))

                conn.commit()
                flash("แก้ไขข้อมูลพนักงานสำเร็จ", "success")
                return redirect(url_for("customer"))
            else:
                cursor.execute("SELECT * FROM customer WHERE cus_id = %s", (cus_id,))
                customer = cursor.fetchone()
                if customer is None:
                    flash("ไม่พบข้อมูลพนักงาน", "error")
                    return redirect(url_for("customer"))
                return render_template("edit_customer.html", customer=customer)
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดในการแก้ไขข้อมูลพนักงาน: {str(e)}", "error")
    finally:
        conn.close()
    return redirect(url_for("customer"))


@app.route("/tables")
def tables():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tables")
            tables = cursor.fetchall()
    finally:
        conn.close()
    return render_template("tables.html", tables=tables)


@app.route("/add_table", methods=["POST"])
def add_table():
    table_id = request.form["table_id"]
    table_capacity = request.form["table_capacity"]
    qr_code = generate_qr_code(table_id)

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO tables (table_id, table_qrcode, capacity) VALUES (%s, %s, %s)"
            cursor.execute(sql, (table_id, qr_code, table_capacity))
        conn.commit()
        flash("เพิ่มโต๊ะสำเร็จ", "success")
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดในการเพิ่มโต๊ะ: {str(e)}", "error")
    finally:
        conn.close()
    return redirect(url_for("tables"))


@app.route("/edit_table/<string:table_id>", methods=["GET", "POST"])
def edit_table(table_id):
    if request.method == "POST":
        new_table_id = request.form["table_id"]
        table_capacity = request.form["table_capacity"]

        qr_code = generate_qr_code(new_table_id)

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE tables SET table_id = %s, table_qrcode = %s, table_capacity = %s  WHERE table_id = %s"
                cursor.execute(sql, (new_table_id, qr_code, table_capacity, table_id))
            conn.commit()
            flash("แก้ไขโต๊ะสำเร็จ", "success")
        except Exception as e:
            flash(f"เกิดข้อผิดพลาดในการแก้ไขโต๊ะ: {str(e)}", "error")
        finally:
            conn.close()
        return redirect(url_for("tables"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tables WHERE table_id = %s", (table_id,))
            table = cursor.fetchone()
    finally:
        conn.close()
    return render_template("edit_table.html", table=table)


@app.route("/delete_table/<string:table_id>")
def delete_table(table_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM tables WHERE table_id = %s", (table_id,))
        conn.commit()
        flash("ลบโต๊ะสำเร็จ", "success")
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดในการลบโต๊ะ: {str(e)}", "error")
    finally:
        conn.close()
    return redirect(url_for("tables"))


@app.route("/coffee_menu")
def coffee_menu():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM coffee_menu")
            menu_items = cursor.fetchall()
    finally:
        conn.close()
    return render_template("coffee_menu.html", menu_items=menu_items)


@app.route("/add_coffee", methods=["POST"])
def add_coffee():
    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]

    # Handle image upload
    if "image" in request.files:
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            image_path = f"coffee_images/{filename}"
        else:
            image_path = None
    else:
        image_path = None

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO coffee_menu (name, price, description, image_path) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, price, description, image_path))
        conn.commit()
        flash("เพิ่มเมนูกาแฟสำเร็จ", "success")
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดในการเพิ่มเมนูกาแฟ: {str(e)}", "error")
    finally:
        conn.close()
    return redirect(url_for("coffee_menu"))


@app.route("/edit_coffee/<int:id>", methods=["GET", "POST"])
def edit_coffee(id):
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]

        # Handle image upload
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                image_path = f"coffee_images/{filename}"
            else:
                image_path = request.form["current_image"]
        else:
            image_path = request.form["current_image"]

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE coffee_menu SET name = %s, price = %s, description = %s, image_path = %s WHERE id = %s"
                cursor.execute(sql, (name, price, description, image_path, id))
            conn.commit()
            flash("แก้ไขเมนูกาแฟสำเร็จ", "success")
        except Exception as e:
            flash(f"เกิดข้อผิดพลาดในการแก้ไขเมนูกาแฟ: {str(e)}", "error")
        finally:
            conn.close()
        return redirect(url_for("coffee_menu"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM coffee_menu WHERE id = %s", (id,))
            coffee = cursor.fetchone()
    finally:
        conn.close()
    return render_template("edit_coffee.html", coffee=coffee)


@app.route("/delete_coffee/<int:id>")
def delete_coffee(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM coffee_menu WHERE id = %s", (id,))
        conn.commit()
        flash("ลบเมนูกาแฟสำเร็จ", "success")
    except Exception as e:
        flash(f"เกิดข้อผิดพลาดในการลบเมนูกาแฟ: {str(e)}", "error")
    finally:
        conn.close()
    return redirect(url_for("coffee_menu"))


def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qr_folder = os.path.join("static", "qr_codes")
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)

    img_path = os.path.join(qr_folder, f"{data}.png")
    img.save(img_path)
    return img_path


if __name__ == "__main__":
    app.run(debug=True)
