import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# export API_KEY=pk_b8ac2e08bd5b4905ab03016a1943a002

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
    stocks = db.execute("SELECT symbol, name, SUM(shares) as totalShares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    total = user_cash

    for stock in stocks:
        total += stock["price"] * stock["totalShares"]

    return render_template("index.html", stocks=stocks, user_cash=user_cash, total=total, usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Please type the stock symbol!")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Please type an integer!")

        if not shares:
            return apology("Please type the number of shares")
        if shares <= 0:
            return apology("You need to buy at least one share")

        # Check how much cash I have right now.
        user_id = session["user_id"]
        # cash will look like [{cash:10000}] without [0]["cash"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # Take the name and price of this stock by looking up the symbol typed in.
        item = lookup(symbol)
        item_price = item["price"]
        item_name = item["name"]
        total_price = item_price * shares

        # Check you have enough capital to buy the shares.
        if cash < total_price:
            return apology("You need more capital to buy the shares")
        else:
            # Update my cash after purchasing shares.
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_price, user_id)
            # Append a transaction of purchasing shares.
            db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES(?, ?, ?, ?, ?, ?)", user_id, item_name, shares, item_price, "buy", symbol)

        return redirect("/")


    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, type, shares, price, time FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", usd=usd, transactions=transactions)


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
            return apology("Please fill the symbol field")
        # look through 'name','price','symbol' which returns a dict looks
        # {
        #     "name": quote["companyName"],
        #
        #     "price": float(quote["latestPrice"]),
        #     "symbol": quote["symbol"]
        # }
        item = lookup(symbol)

        if not item:
            return apology("The symbol isn't exist")




        return render_template("quoted.html", item=item, usd=usd)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Make hash using your password.
        hash = generate_password_hash(password)

        # Check if the user didn't type something
        if  not username:
            return apology("Please fill your username")
        if  not password:
            return apology("Please fill your password")
        if  not confirmation:
            return apology("Please fill your confirmation")
        if password != confirmation:
            return apology("Please check that your password is same as confirmation")

        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        except:
            return apology("The user is already exists!")

        return redirect("/login")

    else:
        return render_template("register.html")


    return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        user_id  = session["user_id"]
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Please select a symbol to sell")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Please type an integer")

        if shares <= 0:
            return apology("You need to sell at least one share")

        # Check if I have enough shares to sell.
        item_price = int(lookup(symbol)["price"])
        item_name = lookup(symbol)["name"]
        total = item_price * shares
        own_shares = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)[0]["shares"]



        if own_shares < shares:
            return apology("You have insufficient shares to sell")


        db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES(?, ?, ?, ?, ?, ?)", user_id, item_name, -shares, item_price, "sell", symbol)
        # Update the user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + total, user_id)
        return redirect("/")
    else:
        user_id = session["user_id"]
        stocks = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        return render_template("sell.html", stocks=stocks)
    return apology("asfd")