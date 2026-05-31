from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import requests



app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    "mysql+pymysql://root:335027@localhost/mydb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about-me', methods=['GET', 'POST'])
def about_me():
    user_input = ''
    if request.method   == 'POST':
        user_input = request.form.get('xss_input','')
    return render_template('aboutme.html', user_input=user_input)


@app.route('/login', methods=['GET','POST'])
def login():
    message=""
    if request.method=="POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        query_stmt = text(f"SELECT username FROM users WHERE username='{username}' AND password='{password}'")

        result = db.engine.connect().execute(query_stmt)


        user = result.fetchone()
        
        if user:
            message=f"Welcome! {username}"
        else:
            message="Incorrect username or password"
    return render_template('login.html', message=message)


    # user_input=""
    # if request.method == 'POST':
    #     user_input = request.form.get('username','')
    # return render_template('login.html', user_input=user_input)
bad_chars=["'", ":", ";","--", "#"]
def black_list(uName):
    for char in bad_chars:
        if char in uName.lower():
            return True
    return False




# below code is secured
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if black_list(username):
            message="No Hacker allowed"
            return render_template('/register.html', message=message)
        with db.engine.connect() as conn:

            # Check if username already exists
            check_query = text(
                "SELECT username FROM users WHERE username = :username"
            )

            user_exists = conn.execute(
                check_query,
                {"username": username}
            ).fetchone()

            if user_exists:
                message = "Username Already Exists!"

            else:
                # Insert new user
                insert_query = text(
                    """
                    INSERT INTO users (username, password)
                    VALUES (:username, :password)
                    """
                )

                conn.execute(
                    insert_query,
                    {
                        "username": username,
                        "password": password
                    }
                )

                conn.commit()

                message = "Registration Successful!"

    return render_template('register.html', message=message)




# for open redirect vulnerability

@app.route('/redirect', methods=['GET'])
def redirect_page():
    return render_template('redirect.html')

# extra lines below
@app.route('/open',methods=['GET'])
def open():
    target_url = request.args.get('url')
    action = request.args.get('action', 'redirect')
    # open redirection
    if action == 'redirect':
        return redirect(target_url)
    
    # SSRF
    elif action == 'fetch':
        try:
            response = requests.get(target_url, timeout=10)
            if response.status_code == 200:
                return f"Recieved 200 ok {target_url}"
            else:
                return f"Recieved {response.status_code} from {target_url}"
        except requests.ConnectionError:
            return f"Connection Refused By {target_url}"
        except requests.Timeout:
            return f"Connection time out for {target_url}"
        except Exception as e:
            return str(e)
    return "Specify action and url parameters"










if __name__ == '__main__':
    app.run(debug=True)

































































































































































































































# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def greet():
#     return 'Hello World!'


# @app.route("/page/<int:number>")
# def bye(number):
#     return f'There is a number: {number} coming from the url'


# if __name__ == '__main__':
#     app.run(debug=True)























# # def main():
# #     print(f"File Name: {__name__}")
    

# # if __name__ == '__main__':
# #     print("Ran directly")
# # else:
# #     print("Ran from Second.py file")