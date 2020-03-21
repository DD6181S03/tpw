from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from testsearching import *
from os import environ

app = Flask(__name__)
#app.config['ENV'] = 'development'
# 如果手动部署，需修改此处csrf_token
app.config['SECRET_KEY'] = environ['CSRFTOKEN']
bootstrap = Bootstrap(app)


class BusInputForm(FlaskForm):
    bsi = StringField('线路', validators=[DataRequired()])
    submitline = SubmitField('查线路')
    submitstn = SubmitField('查车站')


@app.route('/line/<lineid>')
def showline(lineid):
    return render_template('lineinfo.html', dplist=getlineinfo(lineid))


@app.route('/bus/<busid>')
def businfo(busid):
    lineid = request.referrer.rsplit('/', 1)[-1]
    if lineid:
        return render_template('bus.html', busifm=nbloc(busid, lineid))
    else:
        ret4 = busloc(busid)
        if ret4:
            return render_template('bus.html', busifm=ret4)
        return render_template('bus.html', message='查不到')


@app.route('/linec/<lineinput>')
def chooseline(lineinput):
    return render_template('linechoose.html', lines=getlineid(lineinput))


@app.route('/stnc/<stninput>')
def choosestn(stninput):
    return render_template('stationchoose.html', stns=getstnid(stninput))


@app.route('/stn/<stnid>')
@app.route('/stn/<stnid>/<det>')
def stninfo(stnid, det=''):
    return render_template('stationinfo.html', lines=getstninfo(stnid, det))


@app.route('/', methods=['GET', 'POST'])
def index():
    searchform = BusInputForm()
    if searchform.validate_on_submit():
        if searchform.submitline.data:
            return redirect(url_for('chooseline', lineinput=searchform.bsi.data))
        elif searchform.submitstn.data:
            return redirect(url_for('choosestn', stninput=searchform.bsi.data))
        else:
            return redirect(url_for('businfo', busid=searchform.bsi.data))
    return render_template('index.html', form=searchform)


@app.route('/getroute')
def getroute():
    return render_template('getroute.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/noticelist')
def noticelist():
    return render_template('noticelist.html', notices=getnoticelist())


@app.route('/notd/<noticeid>')
def notd(noticeid):
    return render_template('noticedetail.html', notice=getnoticedetail(noticeid))


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    app.run()
