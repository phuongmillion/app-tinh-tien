import datetime
import json

from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    tienlai = TextField('tienlai:', validators=[validators.required()])
    ngayvay = TextField('ngayvay:', validators=[validators.required()])
    ngaytra = TextField('ngaytra:', validators=[validators.required()])

class NguoiVay:
    def __init__(self, name=None, ngay_muon=None, ngay_ket_thuc=None, tien_lai_10_ngay=None ):
        self.name = name
        self.ngay_muon = ngay_muon
        self.ngay_ket_thuc = ngay_ket_thuc
        self.tien_lai_10_ngay = tien_lai_10_ngay

tong_nguoi = []

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        split_year_borrow, split_month_borrow, split_date_borrow = request.form['ngayvay'].split("-")
        split_y_back, split_m_back, split_d_back = request.form['ngaytra'].split("-")
        nguoi_vay = NguoiVay(name=request.form['name'],
                             ngay_muon=datetime.date(int(split_year_borrow), int(split_month_borrow),
                                                     int(split_date_borrow)),
                             ngay_ket_thuc=datetime.date(int(split_y_back), int(split_m_back), int(split_d_back)),
                             tien_lai_10_ngay=int(request.form['tienlai']))

        if form.validate():
            # Save the comment here.
            tong_nguoi.append(nguoi_vay)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('home.html')

@app.route("/danhsach", methods=['GET'])
def get_danh_sach():
    return render_template('danhsach.html', tong_nguoi=tong_nguoi)

@app.route("/danhsach/", methods=['POST'])
def dele_danh_sach():
    tong_nguoi.pop(int(request.data.decode("utf-8")) - 1)
    return redirect("/danhsach")


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="localhost", port=8080, threaded=True)