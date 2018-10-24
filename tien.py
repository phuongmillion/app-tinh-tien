import datetime
# def tinhtien():
#
#     CA = {"name": "C.An",
#           "ngay_muon": datetime.date(2018, 7, 24)}
#     Son = {"name": "Son",
#            "ngay_muon": datetime.date(2018, 9, 24)}
#     Chi ={"name": "Chi_mun",
#               "ngay_muon": datetime.date(2018, 10, 11)}
#     Quan ={"name": "Quan_taxi",
#            "ngay_muon": datetime.date(2018, 10, 13)}
#     tong_nguoi = []
#     tong_nguoi.append(CA)
#     tong_nguoi.append(Son)
#     tong_nguoi.append(Chi)
#     tong_nguoi.append(Quan)
#     for a in tong_nguoi:
#         now = datetime.date.today()
#         print("Hom nay: %s" % now)
#         ngay = now - a["ngay_muon"]
#         print("Ten: %s" % a["name"], "- Ngay vay: %s" % a["ngay_muon"], "- Tong cong: %s ngay" % ngay.days)
#         tong_tien_thu_duoc = (ngay.days // 10) * 250000
#         tien_trong_thang = tong_tien_thu_duoc % 1500000
#         print("Tien trong thang nay: %s " % tien_trong_thang)
#         print("Tong Tien Thu Duoc cua %s: %s " % (a["name"], tong_tien_thu_duoc))
#         tong_tien_trong_thang = tong_tien_trong_thang + tien_trong_thang
#         tong_tien = tong_tien + tong_tien_thu_duoc
#         print("******************************************")
#     print("Tong tien trong thang nay:%s " % tong_tien_trong_thang)
#     print("Tong Cong: %s" % tong_tien)

class NguoiVay:
    def __init__(self, name=None, ngay_muon=None, ngay_ket_thuc=None, tien_lai_10_ngay=None ):
        self.name = name
        self.ngay_muon = ngay_muon
        self.ngay_ket_thuc = ngay_ket_thuc
        self.tien_lai_10_ngay = tien_lai_10_ngay


if __name__ == '__main__':
    tong_nguoi = []
    b = "y"
    tien_lai_10_ngay = 250000
    while(b!="n"):
        tien_lai = input("Nhap tien lai 10 ngay: (mac dinh = 250.000) ")
        name = input("Nhap ten nguoi vay:")
        date_borrow = input("Nhap ngay vay (vd: 2018/07/24): ")
        split_year_borrow , split_month_borrow, split_date_borrow = date_borrow.split("/")
        date_back = input("Nhap ngay tra (Khong nhap dc tinh toi ngay hien tai la %s): " % datetime.datetime.today().date())
        if tien_lai:
            tien_lai_10_ngay = tien_lai
        if not date_back:
            date_back = datetime.date.today()
            nguoi_vay = NguoiVay(name=name,
                                 ngay_muon=datetime.date(int(split_year_borrow), int(split_month_borrow), int(split_date_borrow)),
                                 ngay_ket_thuc=date_back, tien_lai_10_ngay=int(tien_lai_10_ngay))

        else:
            split_y_back, split_m_back, split_d_back = date_back.split("/")
            nguoi_vay = NguoiVay(name=name,
                                 ngay_muon=datetime.date(int(split_year_borrow), int(split_month_borrow), int(split_date_borrow)),
                                 ngay_ket_thuc=datetime.date(int(split_y_back), int(split_m_back), int(split_d_back)),
                                 tien_lai_10_ngay=int(tien_lai_10_ngay))
        tong_nguoi.append(nguoi_vay)
        b = input("Nhap tiep nguoi vay? y/n?: ")

    tong_tien = 0
    tong_tien_trong_thang = 0
    print("\n")
    print("***********Tinh Tien**************")
    print("\n")
    for a in tong_nguoi:
        print("Hom nay: %s" % a.ngay_ket_thuc)
        ngay = a.ngay_ket_thuc - a.ngay_muon
        print("Ten: %s" % a.name, "- Ngay vay: %s" % a.ngay_muon, "- Tong cong: %s ngay" % ngay.days)
        tong_tien_thu_duoc = (ngay.days // 10) * a.tien_lai_10_ngay
        tien_trong_thang = tong_tien_thu_duoc % (a.tien_lai_10_ngay * 3)
        print("Tien trong thang nay: %s " % tien_trong_thang)
        print("Tong Tien Thu Duoc cua %s: %s " % (a.name, tong_tien_thu_duoc))
        tong_tien_trong_thang = tong_tien_trong_thang + tien_trong_thang
        tong_tien = tong_tien + tong_tien_thu_duoc
        print("******************************************")
    print("Tong tien trong thang nay:%s " % tong_tien_trong_thang)
    print("Tong Cong: %s" % tong_tien)


