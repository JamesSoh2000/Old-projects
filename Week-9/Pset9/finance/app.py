import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# export API_KEY=pk_b8ac2e08bd5b4905ab03016a1943a002  이게 API_KEY임


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # 아래 stocks는 outpout이 [{symbol: ~, name: ~, ...},{~},{~}] 이런식으로 줌
    stocks = db.execute("SELECT symbol, name, SUM(shares) as totalShares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    total = user_cash

    for stock in stocks:
        total += stock["price"] * stock["totalShares"]



    return render_template("index.html", stocks = stocks, total = total, cash = user_cash, usd = usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        item = lookup(symbol)

        if not symbol:
            return apology("Please type the symbol")
        elif not item:
            return apology("The symbol doesn't exist!")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Please type an integer!")

        if shares <= 0:
            return apology("Type at least 1 share please!")

        # 현재 내가 접속해있는 유저 아이디
        user_id = session["user_id"]

        # 현재 이 유저가 가지고있는 cash(현금)의 양
        # Watch 18:59 on HarvardX CS50: Finance - Part 3
        # [0]["cash"]없이는 [{cash:10000}] 이렇게줌
        cash = db.execute("SELECT cash FROM users WHERE id = ?" , user_id)[0]["cash"]

        name = item["name"]
        price = item["price"]
        total_price = price * shares

        if cash < total_price:
            return apology("You need more capital(money)")
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_price, user_id)
            db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)", user_id, name, shares, price, "buy", symbol)
        return redirect("/")

    else:
        return render_template("buy.html")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, type, shares, price, time FROM transactions WHERE user_id = ?", user_id)

    return render_template("history.html", transactions = transactions, usd = usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Please enter a symbol!")
        item = lookup(symbol)

        if not item:
            return apology("This symbol doesn't exist!")
        return render_template("quoted.html", item=item, usd=usd)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Type username")
        elif not password:
            return apology("Type password")
        elif not confirmation:
            return apology("Type password confirmation")

        if confirmation != password:
            return apology("Password and confirmation are different")

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
            # then finally we login to the page by redirect to "/"
            return redirect("/")
        except:
            return apology("This username already exists!")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        user_id = session["user_id"]
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if shares <= 0:
            return apology("You need to give positive shares")

        item_price = int(lookup(symbol)["price"])
        item_name = lookup(symbol)["name"]
        total = item_price * shares
        own_shares = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)[0]["shares"]

        if own_shares < shares:
            return apology("You need more shares to sell!")

        # Check how much the user have right now 판 돈과 합치기위해
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # Update the total cash that the user has after selling.
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + total, user_id)

        # Now add this "sell" transaction to our portfolio.
        # 여기서 shares를 -shares로 하면 위에 route("/")에서 SUM(shares)를 만든것으로 모든 shares를 합칠때 자연스럽게 + (-) 되어 마이너스가 된다.
        db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES(?, ?, ?, ?, ?, ?)", user_id, item_name, -shares, item_price, "sell", symbol)
        return redirect("/")
    else:
        user_id = session["user_id"]
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol",  user_id)
        return render_template("sell.html", symbols=symbols)
    return redirect("/")
