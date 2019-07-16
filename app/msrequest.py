from flask import Flask, render_template
import requestlaporan


app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'

@app.route('/requestbaru')
def request():
    
    return render_template('requestLaporan.html')
    laporan = requestlaporan.RequestLaporan()




    #laporan.validasiSession()
    #hasil = laporan.requestLaporanBaru(.......................)


#app.route('editlaporan'):
#    ........
#    .......
#    .......
