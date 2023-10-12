import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
#db = SQL("sqlite:///finance.db")
db = SQL("sqlite:///myshop.db")

def usd(value):
    """Format value as USD."""
    value = int(value)
    return f"${value:,.2f}"


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#@login_required
@app.route("/<int:prod_id>", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
@app.route("/home/<int:prod_id>", methods=["GET", "POST"])
@login_required
def home():

    prodId = request.args.get("prod_id")
    if prodId:
        theproduct = db.execute("select prod_id, name, img, description, price from products where prod_id = ?",int(prodId))[0]
        rate = db.execute("select avg(rate) as rate from products_rate where product_id = ?",int(prodId))[0]
        if not rate:
            rate = "not rates"
        #return render_template("prod.html", theproduct=theproduct, rate=rate,usd=usd)
    else:
        theproduct = None
        rate = None
    if request.method == "POST":
        if request.form.get("rate") and request.form.get("prod_id"):
            rate = int(request.form.get("rate"))
            prodId = int(request.form.get("prod_id"))
            if rate>=1 and rate<=5 and prodId:
                row = db.execute("select * from products_rate where user_id = ? and product_id = ?",session["user_id"],prodId)
                if len(row)>0:
                    db.execute("update products_rate set rate = ? where user_id = ? and product_id = ?",rate,session["user_id"],prodId)
                else:
                    db.execute("insert into products_rate(user_id,product_id,rate) values(?,?,?)",session["user_id"],prodId,rate)
        if request.form.get("cart_prod_id"):
            if "cart" in session:
                session["cart"].append(int( request.form.get("cart_prod_id") ) )
            else:
                session["cart"] = []
                session["cart"].append(int( request.form.get("cart_prod_id") ) )


    else:
        pass
    """
    if prodId:
        theproduct = db.execute("select prod_id, name, img, description from products where prod_id = ?",int(prodId))[0]
        rate  = db.execute("select avg(rate) as rate from products_rate where product_id = ?",int(prodId))[0]
        return render_template("prod.html", theproduct=theproduct, rate=rate)
    else:
        if not request.args.get("sreach"):
            sreach = "%"+"%"
        else:
            sreach = "%"+request.args.get("sreach")+"%"
        if not request.args.get("filter"):
            products = db.execute("select prod_id, name, img, description from products where name like ?",sreach)
        else:
            filter = int(request.args.get("filter"))
            products = db.execute("select prod_id, name, img, description from products where name like ? ans category = ?",sreach,filter)
        return render_template("home.html",products=products)
    """
    if not request.args.get("search"):
        search = "%"+"%"
    else:
        search = "%"+str(request.args.get("search"))+"%"
    if not request.args.get("filter") or int(request.args.get("filter")) == 1:
        products = db.execute("select prod_id, name, img, description from products where name like ?",search)
    else:
        filter = int(request.args.get("filter"))
        products = db.execute("select prod_id, name, img, description from products where name like ? and category_id = ?",search,filter)
    categories = db.execute("select * from categories")
    return render_template("home.html",products=products,theproduct=theproduct,categories=categories,rate=rate,usd=usd)





@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    prodId = request.args.get("prod_id")
    if prodId:
        theproduct = db.execute("select prod_id, name, img, description, price from products where prod_id = ?",int(prodId))[0]
        rate = db.execute("select avg(rate) as rate from products_rate where product_id = ?",int(prodId))[0]
        if not rate:
            rate = "not rates";
        #return render_template("prod.html", theproduct=theproduct, rate=rate,usd=usd)
    else:
        theproduct = None
        rate = None
    if request.method == "POST":
        if request.form.get("rate") and request.form.get("prod_id"):
            rate = int(request.form.get("rate"))
            prodId = int(request.form.get("prod_id"))
            if rate>=1 and rate<=5 and prodId:
                row = db.execute("select * from products_rate where user_id = ? and product_id = ?",session["user_id"],prodId)
                if len(row)>0:
                    db.execute("update products_rate set rate = ? where user_id = ? and product_id = ?",rate,session["user_id"],prodId)
                else:
                    db.execute("insert into products_rate(user_id,product_id,rate) values(?,?,?)",session["user_id"],prodId,rate)
        if request.form.get("cart_prod_id"):
            if "cart" in session and int( request.form.get("cart_prod_id") ) in session["cart"]:
                session["cart"].remove(int( request.form.get("cart_prod_id") ) )
            else:
                pass
        if request.form.get("buy"):
            date = datetime.now()
            for x in session["cart"]:
                db.execute("insert into operations_details(usre_id,product_id,oper_date,price) values(?,?,?,(select price from products where prod_id = ?))",session["user_id"],x,date,x)
            session["cart"].clear()
    else:
        pass


    if "cart" in session:
        products = []
        totalprice = 0
        for x in session["cart"]:
            onerow = db.execute("select prod_id, name, img,price, description from products where prod_id = ?",int(x))[0]
            products.append(onerow)
            totalprice += onerow["price"]
            #products = db.execute("select prod_id, name, img, description from products where prod_id in [?]",session["cart"])
    else:
        products = []
        totalprice = None

    return render_template("cart.html",products=products,theproduct=theproduct,rate=rate,usd=usd,totalprice=totalprice)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        if request.form.get("email"):
            db.execute("update users set email = ? where id = ?",request.form.get("email"),session["user_id"])
        if request.form.get("phone"):
            db.execute("update users set phone = ? where id = ?",request.form.get("phone"),session["user_id"])
    else:
        pass
    info = db.execute("select * from users where id = ?",session["user_id"])[0]
    return render_template("profile.html",info=info)


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    msg = ""
    if request.method == "POST":
        if request.form.get("del-prod_id"):
            db.execute("delete from products where prod_id = ? and owner_id = ?",int(request.form.get("del-prod_id")),session["user_id"])
        elif request.form.get("prod_name") and request.form.get("price") and request.form.get("quantity") and request.form.get("category"):
            name = request.form.get("prod_name")
            price = int(request.form.get("price"))
            owner = session["user_id"]
            desc = request.form.get("description")
            quant = int(request.form.get("quantity"))
            categ = int(request.form.get("category"))
            db.execute("insert into products(name,price,owner_id,description,quantity,category_id) values(?,?,?,?,?,?)",name,price,owner,desc,quant,categ)
        else:
            msg = "There is problem in some of the product information!"
    else:
        pass
    products = db.execute("select prod_id, name, img, description from products where owner_id = ?",session["user_id"])
    categories = db.execute("select * from categories")
    return render_template("admin.html",products=products,categories=categories,message=msg)


@app.route("/operations", methods=["GET", "POST"])
@login_required
def operations():
    tables = db.execute("select Products.name as name, Operations_details.oper_date as op_date,sum(Operations_details.price) as price,count(Operations_details.product_id) as quant from Products join Operations_details on Products.prod_id = Operations_details.product_id where Operations_details.usre_id = ? group by Operations_details.product_id,Operations_details.oper_date order by Operations_details.oper_date desc",session["user_id"])
    return render_template("operation.html",tables=tables,usd=usd)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html",the_message="user name is invaled")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html",the_message="password is invaled")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE user_name = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return render_template("login.html",the_message="user name and password are invaled")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("register.html",the_message="user name is invaled")
        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return render_template("register.html",the_message="password and or confirmation password is invaled")
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html",the_message="password and confirmation are not same")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE user_name = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 0:
            return render_template("register.html",the_message="user name is invaled, choose another user name")

        # add this user into database
        db.execute(
            "INSERT INTO users (user_name,password) values(?,?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )
        rows = db.execute(
            "SELECT * FROM users WHERE user_name = ?", request.form.get("username")
        )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")






