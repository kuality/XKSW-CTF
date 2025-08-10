from flask import Flask, request, render_template_string

app = Flask(__name__)
FLAG = open("flag.txt").read().strip()

@app.route("/")
def index():
    return render_template_string("""
    <html>
    <head>
        <title>easy-login</title>
        <style>
            body {
                background-color: #111;
                color: #eee;
                font-family: monospace;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background: #222;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 15px #0ff5;
                text-align: center;
            }
            input {
                margin: 10px;
                padding: 10px;
                width: 200px;
                background: #333;
                border: 1px solid #555;
                color: white;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                background: #00bcd4;
                border: none;
                color: white;
                border-radius: 5px;
                cursor: pointer;
            }
            h2 {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔐 easy-login</h2>
            <form action="/login" method="POST">
                <input name="id" placeholder="ID"><br>
                <input type="password" name="pw" placeholder="Password"><br>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """)

@app.route("/login", methods=["POST"])
def login():
    user = request.form["id"]
    pw = request.form["pw"]

    if user == "guest" and pw == "guest123":
        return "Welcome guest. No flag for you."

    try:
        result = eval(f"{user} == {pw}")
        if result:
            return f"FLAG: {FLAG}"
    except:
        pass

    return "Login failed."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

