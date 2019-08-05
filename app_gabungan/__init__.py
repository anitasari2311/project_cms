from flask import Flask, render_template

app = Flask(__name__, static_folder='app/static/')


@app.route('/', methods=['GET'])
def index():
    return render_template("Login.html")

@app.route('/showmenu', methods=['GET'])
def showmenu():
    return render_template("menu.html")

@app.route('/request', methods=['GET'])
def request():
    return render_template("requestLaporan.html")

@app.route('/edit2')
def edit2():
    return render_template("Edit2.html")

@app.route('/revisi')
def revisi():
    return render_template("EditKolom.html")





if __name__ == "__main__":
    app.run(debug=True)
