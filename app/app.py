from flask import Flask, render_template, redirect, url_for, request

# create the application object
app = Flask(__name__)


@app.route('/123')
def home():
    return "Hello, World!"

@app.route('/welcomeef')
def welcome():
    return render_template('welcome.html')

# route for handling the login page logic
@app.route('/loginnn', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'secret':
            error = 'Invalid Username/Password.'
        else:
            return redirect(url_for('home'))
    return render_template('loginnn.htm', error=error)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
