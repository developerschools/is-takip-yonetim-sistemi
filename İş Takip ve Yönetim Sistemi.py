import sys
import sqlite3
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QDateEdit, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()

        # SQLite veritabanı bağlantısını oluşturuyoruz
        self.baglanti = sqlite3.connect('İş Takip ve Yönetim Sistemi.db')
        self.cursor = self.baglanti.cursor()

        # Veritabanı tablosunu oluşturuyoruz
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS projeler (
                                id INTEGER PRIMARY KEY,
                                proje_ad TEXT,
                                baslangic_tarihi TEXT,
                                bitis_tarihi TEXT,
                                gorev_ad TEXT,
                                sorumlu_kisi TEXT,
                                calisan_ad TEXT,
                                ilerleme TEXT,
                                takvim_tarih TEXT,
                                resim BLOB
                                )''')
        self.baglanti.commit()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("İş Takip ve Yönetim Sistemi")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Fotoğrafı göstermek için QLabel oluştur
        self.photo_label = QLabel()
        self.fetch_photo_from_url("https://flowi.net/wp-content/uploads/departman-bazinda-flowi-is-takip-programi.jpg")
        self.layout.addWidget(self.photo_label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        self.proje_label = QLabel("Proje Adı:")
        self.proje_input = QLineEdit()

        self.baslangic_label = QLabel("Başlangıç Tarihi:")
        self.baslangic_input = QDateEdit()
        self.baslangic_input.setCalendarPopup(True)

        self.bitis_label = QLabel("Bitiş Tarihi:")
        self.bitis_input = QDateEdit()
        self.bitis_input.setCalendarPopup(True)

        self.gorev_label = QLabel("Görev Adı:")
        self.gorev_input = QLineEdit()

        self.sorumlu_label = QLabel("Sorumlu Kişi:")
        self.sorumlu_input = QLineEdit()

        self.calisan_label = QLabel("Çalışan Adı:")
        self.calisan_input = QLineEdit()

        self.ilerleme_label = QLabel("İlerleme (%):")
        self.ilerleme_input = QComboBox()
        for i in range(0, 101, 5):  # 0'dan 100'e kadar %5'lik artışlarla seçenekler oluşturuluyor
            self.ilerleme_input.addItem(f"%{i}")

        self.takvim_label = QLabel("İlerleme Kaydedilen Tarih:")
        self.takvim_input = QDateEdit()
        self.takvim_input.setCalendarPopup(True)

        self.proje_ekle_button = QPushButton("Proje Ekle")
        self.proje_ekle_button.clicked.connect(self.proje_ekle)

        self.layout.addWidget(self.proje_label)
        self.layout.addWidget(self.proje_input)

        self.layout.addWidget(self.baslangic_label)
        self.layout.addWidget(self.baslangic_input)

        self.layout.addWidget(self.bitis_label)
        self.layout.addWidget(self.bitis_input)

        self.layout.addWidget(self.gorev_label)
        self.layout.addWidget(self.gorev_input)

        self.layout.addWidget(self.sorumlu_label)
        self.layout.addWidget(self.sorumlu_input)

        self.layout.addWidget(self.calisan_label)
        self.layout.addWidget(self.calisan_input)

        self.layout.addWidget(self.ilerleme_label)
        self.layout.addWidget(self.ilerleme_input)

        self.layout.addWidget(self.takvim_label)
        self.layout.addWidget(self.takvim_input)

        self.layout.addWidget(self.proje_ekle_button)

        self.sonuc_text = QTextEdit()
        self.layout.addWidget(self.sonuc_text)

        self.setLayout(self.layout)

    def proje_ekle(self):
        proje_adı = self.proje_input.text()
        başlangıç_tarihi = self.baslangic_input.date().toString("dd/MM/yyyy")
        bitiş_tarihi = self.bitis_input.date().toString("dd/MM/yyyy")
        görev_adı = self.gorev_input.text()
        sorumlu_kişi = self.sorumlu_input.text()
        çalışan_adı = self.calisan_input.text()
        ilerleme = self.ilerleme_input.currentText()
        takvim_tarih = self.takvim_input.date().toString("dd/MM/yyyy")

        # Resmi web üzerinden URL'den alıyoruz
        resim_url = "https://idenfit.com/blog/wp-content/uploads/2020/01/GO%CC%88REV@2x.png"
        resim_icerik = requests.get(resim_url).content

        # Veritabanına yeni proje bilgilerini ve resmi ekliyoruz
        self.cursor.execute('''INSERT INTO projeler (proje_ad, baslangic_tarihi, bitis_tarihi, gorev_ad, sorumlu_kisi, calisan_ad, ilerleme, takvim_tarih, resim)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (proje_adı, başlangıç_tarihi, bitiş_tarihi, görev_adı, sorumlu_kişi, çalışan_adı, ilerleme, takvim_tarih, resim_icerik))
        self.baglanti.commit()

        self.sonuc_text.append("Yeni proje eklendi.")

    def fetch_photo_from_url(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.photo_label.setPixmap(pixmap.scaledToWidth(300))
        except Exception as e:
            print("Error fetching photo:", e)

    def closeEvent(self, event):
        # Uygulama kapatıldığında SQLite bağlantısını kapatıyoruz
        self.baglanti.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ana_pencere = AnaPencere()
    ana_pencere.show()
    sys.exit(app.exec_())
