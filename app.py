import datetime
import json
import os
from time import sleep

from flask import Flask, render_template, flash, request, redirect
from flask_mail import Mail, Message
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from templates import config


# App config.
DEBUG = True
app = Flask(__name__)
app.config.update(config.mail_settings)
chitaomoibiet = Mail(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    tienlai = TextField('tienlai:', validators=[validators.required()])
    ngayvay = TextField('ngayvay:', validators=[validators.required()])
    ngaytra = TextField('ngaytra:', validators=[validators.required()])

class NguoiVay:
    def __init__(self, name=None, ngay_muon=None, ngay_ket_thuc=None, tien_lai_10_ngay=None, sdt=None, ngay_chua_lay=None):
        self.name = name
        self.ngay_muon = ngay_muon
        self.ngay_chua_lay = ngay_chua_lay
        self.ngay_ket_thuc = ngay_ket_thuc
        self.tien_lai_10_ngay = tien_lai_10_ngay
        self.sdt = sdt
        self.thanhtien = self.thanhtien()
        # self.tientrongthang = self.tientrongthang()
        self.tienchualay = self.tienchualay()

    def thanhtien(self):
        ngay = self.ngay_ket_thuc - self.ngay_muon
        tong_tien_thu_duoc = (ngay.days // 10) * self.tien_lai_10_ngay
        return int(tong_tien_thu_duoc)

    # def tientrongthang(self):
    #     ngay = self.ngay_ket_thuc - self.ngay_muon
    #     tong_tien_thu_duoc = (ngay.days // 10) * self.tien_lai_10_ngay
    #     tien_trong_thang = tong_tien_thu_duoc % (self.tien_lai_10_ngay * 3)
    #     return int(tien_trong_thang)

    def tienchualay(self):
        ngay = self.ngay_ket_thuc - self.ngay_chua_lay
        tien_chua_lay = (ngay.days // 10) * self.tien_lai_10_ngay
        return int(tien_chua_lay)


def get_tong_nguoi():
    with open('./data.json', 'r') as f:
        list_nguoi = json.loads(f.read())
    return list_nguoi
tong_nguoi = get_tong_nguoi()


def get_tong_tien():
    tien = 0
    for nguoi in tong_nguoi:
        tien = tien + nguoi["thanhtien"]
    return tien
tong_tien = get_tong_tien()


# def get_tong_tien_trong_thang():
#     tien = 0
#     for nguoi in tong_nguoi:
#         tien = tien + nguoi["tientrongthang"]
#     return tien
# tong_tien_trong_thang = get_tong_tien_trong_thang() + 1750000

def get_tong_tien_chua_lay():
    tien = 0
    for nguoi in tong_nguoi:
        tien = tien + nguoi["tienchualay"]
    return tien
tong_tien_chua_lay = get_tong_tien_chua_lay()


@app.route("/", methods=['GET', 'POST'])
def hello():
    global tong_nguoi
    # global tong_tien_trong_thang
    global tong_tien_chua_lay
    global tong_tien
    global list_nguoi
    form = ReusableForm(request.form)
    if request.method == 'POST':
        split_year_borrow, split_month_borrow, split_date_borrow = request.form['ngayvay'].split("-")
        split_y_back, split_m_back, split_d_back = request.form['ngaytra'].split("-")
        split_chua_lay_y, split_chua_lay_m, split_chua_lay_d = request.form['ngaychualay'].split("-")
        nguoi_vay = NguoiVay(name=request.form['name'],
                             ngay_muon=datetime.date(int(split_year_borrow), int(split_month_borrow),
                                                     int(split_date_borrow)),
                             ngay_ket_thuc=datetime.date(int(split_y_back), int(split_m_back), int(split_d_back)),
                             tien_lai_10_ngay=int(request.form['tienlai']),
                             sdt=int(request.form['sdt']),
                             ngay_chua_lay=datetime.date(int(split_chua_lay_y), int(split_chua_lay_m), int(split_chua_lay_d)))

        if form.validate():
            # tong_nguoi.append(nguoi_vay)
            # tong_tien_trong_thang = tong_tien_trong_thang + nguoi_vay.tientrongthang
            tong_tien = tong_tien + nguoi_vay.thanhtien
            tong_tien_chua_lay = tong_tien_chua_lay + nguoi_vay.tienchualay
            with open('./data.json', 'w') as f:
                nguoi = {
                    "name": nguoi_vay.name,
                    "ngay_muon": str(nguoi_vay.ngay_muon),
                    "ngay_chua_lay": str(nguoi_vay.ngay_chua_lay),
                    "ngay_ket_thuc": str(nguoi_vay.ngay_ket_thuc),
                    "tien_lai_10_ngay": nguoi_vay.tien_lai_10_ngay,
                    "sdt": nguoi_vay.sdt,
                    "thanhtien": nguoi_vay.thanhtien,
                    # "tientrongthang": nguoi_vay.tientrongthang,
                    "tienchualay": nguoi_vay.tienchualay
                }
                tong_nguoi.append(nguoi)
                json.dump(tong_nguoi, f)
            msg = Message(subject="Hello",
                          sender=app.config.get("MAIL_USERNAME"),
                          recipients=["millionsmiles2017@gmail.com"])
            with app.open_resource("data.json") as fp:
                msg.attach("data.json", "application/json", fp.read())
            chitaomoibiet.send(msg)
        else:
            flash('Error: All the form fields are required. ')


    return render_template('home.html', tong_nguoi=tong_nguoi, tong=tong_tien, tongchualay=tong_tien_chua_lay)


@app.route("/danhsach", methods=['GET'])
def get_danh_sach():
    return render_template('danhsach.html', tong_nguoi=tong_nguoi, tong=tong_tien, tongchualay=tong_tien_chua_lay)


@app.route("/danhsach", methods=['POST'])
def dele_danh_sach():
    global tong_tien
    # global tong_tien_trong_thang
    global tong_tien_chua_lay
    try:
        tong_tien = tong_tien - tong_nguoi[int(request.data.decode("utf-8")) - 1]["thanhtien"]
        # tong_tien_trong_thang = tong_tien_trong_thang - tong_nguoi[int(request.data.decode("utf-8")) - 1]["tientrongthang"]
        tong_tien_chua_lay = tong_tien_chua_lay - tong_nguoi[int(request.data.decode("utf-8")) - 1]["tienchualay"]
        tong_nguoi.pop(int(request.data.decode("utf-8")) - 1)
        with open('./data.json', 'w') as f:
            json.dump(tong_nguoi, f)
    except:
        return redirect('/danhsach')
    return redirect('/danhsach')

@app.route("/danhsach/", methods=['POST'])
def edit_danh_sach():
    global tong_nguoi
    # global tong_tien_trong_thang
    global tong_tien_chua_lay
    global tong_tien
    global list_nguoi
    form = ReusableForm(request.form)
    if request.method == 'POST':
        for nguoi in tong_nguoi:
            if nguoi["name"] == request.form['name']:
                tong_tien = tong_tien - nguoi["thanhtien"]
                tong_tien_chua_lay = tong_tien_chua_lay - nguoi["tienchualay"]
                tong_nguoi.remove(nguoi)
        split_year_borrow, split_month_borrow, split_date_borrow = request.form['ngayvay'].split("-")
        split_y_back, split_m_back, split_d_back = request.form['ngaytra'].split("-")
        split_chua_lay_y, split_chua_lay_m, split_chua_lay_d = request.form['ngaychualay'].split("-")
        nguoi_vay = NguoiVay(name=request.form['name'],
                             ngay_muon=datetime.date(int(split_year_borrow), int(split_month_borrow),
                                                     int(split_date_borrow)),
                             ngay_ket_thuc=datetime.date(int(split_y_back), int(split_m_back), int(split_d_back)),
                             tien_lai_10_ngay=int(request.form['tienlai']),
                             sdt=int(request.form['sdt']),
                             ngay_chua_lay=datetime.date(int(split_chua_lay_y), int(split_chua_lay_m),
                                                         int(split_chua_lay_d)))

        if form.validate():
            # tong_nguoi.append(nguoi_vay)
            # tong_tien_trong_thang = tong_tien_trong_thang + nguoi_vay.tientrongthang
            tong_tien = tong_tien + nguoi_vay.thanhtien
            tong_tien_chua_lay = tong_tien_chua_lay + nguoi_vay.tienchualay
            with open('./data.json', 'w') as f:
                nguoi = {
                    "name": nguoi_vay.name,
                    "ngay_muon": str(nguoi_vay.ngay_muon),
                    "ngay_chua_lay": str(nguoi_vay.ngay_chua_lay),
                    "ngay_ket_thuc": str(nguoi_vay.ngay_ket_thuc),
                    "tien_lai_10_ngay": nguoi_vay.tien_lai_10_ngay,
                    "sdt": nguoi_vay.sdt,
                    "thanhtien": nguoi_vay.thanhtien,
                    # "tientrongthang": nguoi_vay.tientrongthang,
                    "tienchualay": nguoi_vay.tienchualay
                }
                tong_nguoi.append(nguoi)
                json.dump(tong_nguoi, f)
            msg = Message(subject="Hello",
                          sender=app.config.get("MAIL_USERNAME"),
                          recipients=["millionsmiles2017@gmail.com"])
            with app.open_resource("data.json") as fp:
                msg.attach("data.json", "application/json", fp.read())
            chitaomoibiet.send(msg)
        else:
            flash('Error: All the form fields are required. ')
        return redirect('/danhsach')

@app.route("/contact", methods=['GET'])
def get_contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="localhost", port=8080, threaded=True)