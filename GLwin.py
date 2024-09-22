from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QDialogButtonBox, QMessageBox, QDialog, QVBoxLayout, QLabel, \
    QLineEdit, QPushButton, QDateEdit
from PyQt5.QtCore import QDateTime
import sqlite3

conn = sqlite3.connect('LR_2.db')
curs = conn.cursor()


class ReportDialog(QDialog):
    def __init__(self, table_widget):
        super().__init__()
        self.setWindowTitle("Создание отчётов")
        self.layout = QVBoxLayout()
        self.resize(350, 350)

        # Добавляем виджеты выбора даты
        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.layout.addWidget(self.start_date_edit)

        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.layout.addWidget(self.end_date_edit)

        # Добавляем кнопку "Создать отчёт"
        self.create_report_button = QPushButton("Создать отчёт")
        self.create_report_button.clicked.connect(self.create_report)
        self.layout.addWidget(self.create_report_button)

        self.setLayout(self.layout)

        # Сохраняем ссылку на tableWidget
        self.tableWidget = table_widget

    def create_report(self):
        try:
            # Получаем значения выбранных дат
            start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
            end_date = self.end_date_edit.date().toString("yyyy-MM-dd")

            # Подключаемся к базе данных
            conn = sqlite3.connect('LR_2.db')
            curs = conn.cursor()

            # Выполняем SQL-запрос для получения происшествий за выбранный период
            curs.execute(
                "SELECT id_происшествия, Дата_и_время, Место_происшествия FROM Происшествия WHERE Дата_и_время BETWEEN ? AND ?",
                (start_date, end_date))
            incidents = curs.fetchall()

            # Создаем таблицу для отчёта
            self.tableWidget.setColumnCount(3)  # Указываем количество столбцов
            self.tableWidget.setRowCount(len(incidents) + 2)  # Увеличиваем количество строк на 2

            self.tableWidget.setHorizontalHeaderLabels(["ID", "Дата и время", "Место происшествия"])

            # Заполняем таблицу данными
            for i, incident in enumerate(incidents):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(incident[0])))  # id_происшествия
                self.tableWidget.setItem(i, 1, QTableWidgetItem(incident[1]))  # Дата_и_время
                if i > 0:  # Пропускаем первую строку третьего столбца
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(incident[2]))  # Место_происшествия

            # Перезаписываем содержимое первой строки
            self.tableWidget.setItem(0, 0, QTableWidgetItem(f"Начало периода: {start_date}"))
            self.tableWidget.setItem(0, 1, QTableWidgetItem(f"Конец периода: {end_date}"))

            # Заполняем количество происшествий в последней строке
            self.tableWidget.setItem(len(incidents) + 1, 0,
                                     QTableWidgetItem(f"Количество происшествий: {len(incidents)}"))
            self.tableWidget.resizeColumnsToContents()

            # Закрываем соединение с базой данных
            conn.close()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {str(e)}")

class AddPhotoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(600, 800)
        self.setWindowTitle("Добавить фотографию")

        self.photo_label = QLabel()
        self.photo_label.setScaledContents(True)

        self.add_photo_button = QPushButton("Добавить фотографию")
        self.add_photo_button.clicked.connect(self.add_photo)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_photo)
        self.save_button.setDisabled(True)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.photo_label)
        layout.addWidget(self.add_photo_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

        self.photo_path = None

    def add_photo(self):
        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(self, "Выберите фотографию", "",
                                                       "Images (*.png *.jpg *.jpeg *.bmp *.gif)",
                                                       options=options)
            if file_name:
                self.photo_path = file_name
                pixmap = QtGui.QPixmap(file_name)
                self.photo_label.setPixmap(pixmap)
                self.save_button.setEnabled(True)
        except Exception as e:
            print("An error occurred:", e)

    def save_photo(self):
        # Здесь добавить логику сохранения фотографии
        self.close()


class DeleteIdInputDialog(QDialog):
    def __init__(self, parent=None):
        super(DeleteIdInputDialog, self).__init__(parent)
        self.setWindowTitle("Введите ID происшествия для удаления")
        self.setModal(True)
        self.resize(550, 100)

        layout = QVBoxLayout(self)
        self.lineEdit = QLineEdit(self)
        layout.addWidget(self.lineEdit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_id(self):
        return self.lineEdit.text()


# Определение диалогового окна для ввода ID происшествия
class IdInputDialog(QDialog):
    def __init__(self, parent=None):
        super(IdInputDialog, self).__init__(parent)
        self.setWindowTitle("Введите ID происшествия")
        self.resize(400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("ID происшествия:")
        layout.addWidget(self.label)

        self.id_input = QLineEdit()
        layout.addWidget(self.id_input)

        self.submit_button = QPushButton("Отправить")
        self.submit_button.clicked.connect(self.accept)
        layout.addWidget(self.submit_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def get_id(self):
        return self.id_input.text()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1150, 600)
        MainWindow.setMinimumSize(QtCore.QSize(400, 300))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_5.setStyleSheet("background-color: rgb(165, 225, 255);\n"
                                   "font: 14pt \"Times New Roman\";")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.page)
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_4 = QtWidgets.QPushButton(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.page)
        self.label_4.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_4.setStyleSheet("background-color: rgb(165, 225, 255);\n"
                                   "font: 14pt \"Times New Roman\";")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.page)
        self.label_3.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_3.setStyleSheet("background-color: rgb(165, 225, 255);\n"
                                   "font: 14pt \"Times New Roman\";")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.page)
        self.tableWidget_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget_3, 1, 0, 1, 1)
        self.tableWidget_4 = QtWidgets.QTableWidget(self.page)
        self.tableWidget_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(0)
        self.tableWidget_4.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget_4, 1, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(self.page)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.page)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_15 = QtWidgets.QPushButton(self.page)
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_15.setStyleSheet("background-color: rgb(170, 170, 215);")
        self.verticalLayout_2.addWidget(self.pushButton_15)
        self.pushButton_16 = QtWidgets.QPushButton(self.page)  # Добавлена кнопка pushButton_16
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_16.setStyleSheet("background-color: rgb(170, 170, 215);")
        self.verticalLayout_2.addWidget(self.pushButton_16)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.stackedWidget.addWidget(self.page)

        MainWindow.setCentralWidget(self.centralwidget)
        # self.retranslateUi(MainWindow)  # Эту строку убираем
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Отчёты
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pushButton_5 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_5.setStyleSheet("font: 10pt \"Times New Roman\";\n"
                                        "background-color: rgb(170, 170, 255);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_3.addWidget(self.pushButton_5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableWidget = QtWidgets.QTableWidget(self.page_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout_4.addWidget(self.tableWidget)
        self.pushButton_6 = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setMinimumSize(QtCore.QSize(75, 51))
        self.pushButton_6.setMaximumSize(QtCore.QSize(75, 51))
        self.pushButton_6.setStyleSheet("font: 10pt \"Times New Roman\";\n"
                                        "background-color: rgb(170, 170, 255);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_4.addWidget(self.pushButton_6)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.stackedWidget.addWidget(self.page_2)

        # Добавить происшествие
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.page_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_7 = QtWidgets.QPushButton(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout.addWidget(self.pushButton_7)
        self.label_6 = QtWidgets.QLabel(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                   "background-color: rgb(165, 225, 255);")
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateTimeEdit.sizePolicy().hasHeightForWidth())
        self.dateTimeEdit.setSizePolicy(sizePolicy)
        self.dateTimeEdit.setMinimumSize(QtCore.QSize(256, 0))
        self.dateTimeEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.verticalLayout.addWidget(self.dateTimeEdit)
        self.label_2 = QtWidgets.QLabel(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                   "background-color: rgb(165, 225, 255);")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.textEdit_2 = QtWidgets.QTextEdit(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_2.sizePolicy().hasHeightForWidth())
        self.textEdit_2.setSizePolicy(sizePolicy)
        self.textEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "font: 12pt \"Times New Roman\";")
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout.addWidget(self.textEdit_2)
        self.label_7 = QtWidgets.QLabel(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                   "background-color: rgb(165, 225, 255);")
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.textEdit_3 = QtWidgets.QTextEdit(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_3.sizePolicy().hasHeightForWidth())
        self.textEdit_3.setSizePolicy(sizePolicy)
        self.textEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "font: 12pt \"Times New Roman\";")
        self.textEdit_3.setObjectName("textEdit_3")
        self.verticalLayout.addWidget(self.textEdit_3)
        self.pushButton_8 = QtWidgets.QPushButton(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout.addWidget(self.pushButton_8)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                   "background-color: rgb(165, 225, 255);")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_6.addWidget(self.label_8)
        self.textEdit = QtWidgets.QTextEdit(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_6.addWidget(self.textEdit)
        self.horizontalLayout_5.addLayout(self.verticalLayout_6)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_11 = QtWidgets.QLabel(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                    "background-color: rgb(165, 225, 255);")
        self.label_11.setObjectName("label_11")
        self.verticalLayout_8.addWidget(self.label_11)
        self.pushButton_9 = QtWidgets.QPushButton(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        self.pushButton_9.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "font: 12pt \"Times New Roman\";")
        self.pushButton_9.setObjectName("pushButton_9")
        self.verticalLayout_8.addWidget(self.pushButton_9)
        self.label_9 = QtWidgets.QLabel(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                   "background-color: rgb(165, 225, 255);")
        self.label_9.setObjectName("label_9")
        self.verticalLayout_8.addWidget(self.label_9)
        self.comboBox = QtWidgets.QComboBox(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout_8.addWidget(self.comboBox)
        self.label_10 = QtWidgets.QLabel(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                    "background-color: rgb(165, 225, 255);")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_8.addWidget(self.label_10)
        self.textEdit_4 = QtWidgets.QTextEdit(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_4.sizePolicy().hasHeightForWidth())
        self.textEdit_4.setSizePolicy(sizePolicy)
        self.textEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "font: 12pt \"Times New Roman\";")
        self.textEdit_4.setObjectName("textEdit_4")
        self.verticalLayout_8.addWidget(self.textEdit_4)
        self.pushButton_10 = QtWidgets.QPushButton(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_10.sizePolicy().hasHeightForWidth())
        self.pushButton_10.setSizePolicy(sizePolicy)
        self.pushButton_10.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout_8.addWidget(self.pushButton_10)
        self.horizontalLayout_5.addLayout(self.verticalLayout_8)
        self.stackedWidget.addWidget(self.page_3)

        # Изменить происшесвтие
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.page_4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pushButton_11 = QtWidgets.QPushButton(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_11.sizePolicy().hasHeightForWidth())
        self.pushButton_11.setSizePolicy(sizePolicy)
        self.pushButton_11.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout_9.addWidget(self.pushButton_11)
        self.label_12 = QtWidgets.QLabel(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                    "background-color: rgb(165, 225, 255);")
        self.label_12.setObjectName("label_12")
        self.verticalLayout_9.addWidget(self.label_12)
        self.dateTimeEdit_2 = QtWidgets.QDateTimeEdit(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateTimeEdit_2.sizePolicy().hasHeightForWidth())
        self.dateTimeEdit_2.setSizePolicy(sizePolicy)
        self.dateTimeEdit_2.setMinimumSize(QtCore.QSize(256, 0))
        self.dateTimeEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        self.verticalLayout_9.addWidget(self.dateTimeEdit_2)
        self.label_13 = QtWidgets.QLabel(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                    "background-color: rgb(165, 225, 255);")
        self.label_13.setObjectName("label_13")
        self.verticalLayout_9.addWidget(self.label_13)
        self.textEdit_5 = QtWidgets.QTextEdit(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_5.sizePolicy().hasHeightForWidth())
        self.textEdit_5.setSizePolicy(sizePolicy)
        self.textEdit_5.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "font: 12pt \"Times New Roman\";")
        self.textEdit_5.setObjectName("textEdit_5")
        self.verticalLayout_9.addWidget(self.textEdit_5)
        self.label_14 = QtWidgets.QLabel(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                    "background-color: rgb(165, 225, 255);")
        self.label_14.setObjectName("label_14")
        self.verticalLayout_9.addWidget(self.label_14)
        self.textEdit_6 = QtWidgets.QTextEdit(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_6.sizePolicy().hasHeightForWidth())
        self.textEdit_6.setSizePolicy(sizePolicy)
        self.textEdit_6.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "font: 12pt \"Times New Roman\";")
        self.textEdit_6.setObjectName("textEdit_6")
        self.verticalLayout_9.addWidget(self.textEdit_6)
        self.pushButton_12 = QtWidgets.QPushButton(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_12.sizePolicy().hasHeightForWidth())
        self.pushButton_12.setSizePolicy(sizePolicy)
        self.pushButton_12.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton_12.setObjectName("pushButton_12")
        self.verticalLayout_9.addWidget(self.pushButton_12)
        self.horizontalLayout_6.addLayout(self.verticalLayout_9)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_15 = QtWidgets.QLabel(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                    "background-color: rgb(165, 225, 255);")
        self.label_15.setObjectName("label_15")
        self.verticalLayout_10.addWidget(self.label_15)
        self.textEdit_7 = QtWidgets.QTextEdit(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_7.sizePolicy().hasHeightForWidth())
        self.textEdit_7.setSizePolicy(sizePolicy)
        self.textEdit_7.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_7.setObjectName("textEdit_7")
        self.verticalLayout_10.addWidget(self.textEdit_7)
        self.horizontalLayout_6.addLayout(self.verticalLayout_10)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_16 = QtWidgets.QLabel(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                    "background-color: rgb(165, 225, 255);")
        self.label_16.setObjectName("label_16")
        self.verticalLayout_11.addWidget(self.label_16)
        self.pushButton_13 = QtWidgets.QPushButton(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy)
        self.pushButton_13.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                         "font: 12pt \"Times New Roman\";")
        self.pushButton_13.setObjectName("pushButton_13")
        self.verticalLayout_11.addWidget(self.pushButton_13)
        self.label_17 = QtWidgets.QLabel(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                    "background-color: rgb(165, 225, 255);")
        self.label_17.setObjectName("label_17")
        self.verticalLayout_11.addWidget(self.label_17)
        self.comboBox_2 = QtWidgets.QComboBox(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.verticalLayout_11.addWidget(self.comboBox_2)
        self.label_18 = QtWidgets.QLabel(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setStyleSheet("font: 12pt \"Times New Roman\";\n"
                                    "background-color: rgb(165, 225, 255);")
        self.label_18.setObjectName("label_18")
        self.verticalLayout_11.addWidget(self.label_18)
        self.textEdit_8 = QtWidgets.QTextEdit(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_8.sizePolicy().hasHeightForWidth())
        self.textEdit_8.setSizePolicy(sizePolicy)
        self.textEdit_8.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "font: 12pt \"Times New Roman\";")
        self.textEdit_8.setObjectName("textEdit_8")
        self.verticalLayout_11.addWidget(self.textEdit_8)
        self.pushButton_14 = QtWidgets.QPushButton(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_14.sizePolicy().hasHeightForWidth())
        self.pushButton_14.setSizePolicy(sizePolicy)
        self.pushButton_14.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton_14.setObjectName("pushButton_14")
        self.verticalLayout_11.addWidget(self.pushButton_14)
        self.horizontalLayout_6.addLayout(self.verticalLayout_11)
        self.stackedWidget.addWidget(self.page_4)
        self.verticalLayout_7.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.pushButton_2.clicked.connect(self.otchety)
        self.pushButton_3.clicked.connect(self.izmp)
        self.pushButton.clicked.connect(self.dobp)
        self.pushButton_6.clicked.connect(self.backOtch)
        self.pushButton_11.clicked.connect(self.backOtch)
        self.pushButton_7.clicked.connect(self.backOtch)
        self.pushButton_8.clicked.connect(self.clear_form)
        self.pushButton_12.clicked.connect(self.clear_form1)
        self.pushButton_10.clicked.connect(self.open_dialog)
        self.pushButton_9.clicked.connect(self.open_add_photo_dialog)
        self.pushButton_13.clicked.connect(self.open_add_photo_dialog)
        self.pushButton_5.clicked.connect(self.open_report_dialog)
        self.tableWidget_3.itemClicked.connect(self.open_edit_incident_window)
        self.tableWidget_4.itemClicked.connect(self.open_edit_incident_window)
        self.pushButton_15.clicked.connect(self.update_table_data)
        self.pushButton_14.clicked.connect(self.save_changes_to_database)
        self.pushButton_16.clicked.connect(self.remove_incident_from_database)
        self.lineEdit.editingFinished.connect(self.search_and_select_incident)
        self.main_window = MainWindow

        # Получаем данные из базы данных
        curs.execute("SELECT id_происшествия, Место_происшествия FROM Происшествия WHERE Статус = 'Завершено'")
        data = curs.fetchall()

        # Устанавливаем количество строк и столбцов в таблице
        ui.tableWidget_3.setRowCount(len(data))
        ui.tableWidget_3.setColumnCount(2)  # Два столбца: id_происшесвтия и Место_происшествия
        # Установка заголовков столбцов
        ui.tableWidget_3.setHorizontalHeaderLabels(['ID', 'Место происшествия'])

        # Установка размера шрифта
        font = ui.tableWidget_3.horizontalHeader().font()
        font.setPointSize(8)  # Установите желаемый размер шрифта
        ui.tableWidget_3.horizontalHeader().setFont(font)

        # Заполняем таблицу данными из базы данных
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                ui.tableWidget_3.setItem(row_num, col_num, item)

        # Получаем данные из базы данных
        curs.execute("SELECT id_происшествия, Место_происшествия FROM Происшествия WHERE Статус = 'В расследовании'")
        data = curs.fetchall()

        ui.tableWidget_4.setRowCount(len(data))
        ui.tableWidget_4.setColumnCount(2)  # Два столбца: id_происшесвтия и Место_происшествия
        # Установка заголовков столбцов
        ui.tableWidget_4.setHorizontalHeaderLabels(['ID', 'Место происшествия'])

        # Установка размера шрифта
        font = ui.tableWidget_4.horizontalHeader().font()
        font.setPointSize(8)  # Установите желаемый размер шрифта
        ui.tableWidget_4.horizontalHeader().setFont(font)

        # Заполняем таблицу данными из базы данных
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                ui.tableWidget_4.setItem(row_num, col_num, item)
        self.tableWidget_4.resizeColumnsToContents()
        self.tableWidget_3.resizeColumnsToContents()
    #поиск
    def search_and_select_incident(self):
        try:
            # Получаем ID происшествия из QLineEdit
            incident_id_str = self.lineEdit.text()

            # Пытаемся преобразовать строку в число
            incident_id = int(incident_id_str)

            # Подключаемся к базе данных
            conn = sqlite3.connect('LR_2.db')
            curs = conn.cursor()

            # Выполняем SQL-запрос для получения происшествия по его ID
            curs.execute("SELECT * FROM Происшествия WHERE id_происшествия = ?", (incident_id,))
            incident = curs.fetchone()

            if incident:
                # Определяем статус происшествия
                status = incident[6]

                # Очищаем tableWidget_3 и tableWidget_4
                self.tableWidget_3.clearSelection()
                self.tableWidget_4.clearSelection()

                # Выводим происшествие в соответствующий tableWidget
                if status == "Завершено":
                    for row in range(self.tableWidget_3.rowCount()):
                        if self.tableWidget_3.item(row, 0).text() == str(incident_id):
                            self.tableWidget_3.selectRow(row)
                elif status == "В расследовании":
                    for row in range(self.tableWidget_4.rowCount()):
                        if self.tableWidget_4.item(row, 0).text() == str(incident_id):
                            self.tableWidget_4.selectRow(row)
                else:
                    QMessageBox.warning(self.centralwidget, "Ошибка", "Неизвестный статус происшествия")

            else:
                QMessageBox.warning(self.centralwidget, "Ошибка", "Происшествие с указанным ID не найдено")

            # Закрываем соединение с базой данных
            conn.close()

        except ValueError:
            QMessageBox.warning(self.centralwidget, "Ошибка", "Некорректный формат ID происшествия")
        except Exception as e:
            QMessageBox.warning(self.centralwidget, "Ошибка", f"Произошла ошибка: {str(e)}")

    def remove_incident_from_database(self):
        try:
            # Отображаем диалоговое окно для ввода ID происшествия
            dialog = DeleteIdInputDialog(
                self.main_window)  # Используем экземпляр QMainWindow в качестве родительского виджета
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                id_incident = dialog.get_id()

                # Проверяем, введен ли ID
                if id_incident:
                    # Подключаемся к базе данных
                    conn = sqlite3.connect('LR_2.db')
                    curs = conn.cursor()

                    # Удаляем происшествие из базы данных по ID
                    curs.execute("DELETE FROM Происшествия WHERE id_происшествия = ?",
                                 (id_incident,))

                    # Commit изменений
                    conn.commit()

                    # Обновляем данные в таблицах
                    self.update_table_data()

                    # Закрываем соединение с базой данных
                    conn.close()

        except Exception as e:
            print("An error occurred:", e)

    def save_changes_to_database(self):
        try:
            # Получаем данные из виджетов
            date_time = self.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd HH:mm")
            place = self.textEdit_5.toPlainText()
            participants = self.textEdit_6.toPlainText()
            description = self.textEdit_7.toPlainText()
            details = self.textEdit_8.toPlainText()
            status = self.comboBox_2.currentText()

            selected_item = self.tableWidget_3.currentItem()
            if selected_item is None:
                selected_item = self.tableWidget_4.currentItem()

            if selected_item is not None:  # Проверяем, выбран ли элемент
                # Получаем ID происшествия или место происшествия из выбранного элемента
                id_incident = selected_item.text()

                # Подключаемся к базе данных
                conn = sqlite3.connect('LR_2.db')
                curs = conn.cursor()

                # Выполняем запрос к базе данных для обновления данных о происшествии
                curs.execute("""
                            UPDATE Происшествия 
                            SET Дата_и_время = ?, Место_происшествия = ?, Участники = ?, Описание = ?, Детали = ?, Статус = ?
                            WHERE id_происшествия = ? OR Место_происшествия = ?
                            """, (
                    date_time, place, participants, description, details, status, id_incident, id_incident))

                # Commit изменений
                conn.commit()

                # Обновляем данные в таблицах
                self.update_table_data()

                # Закрываем соединение с базой данных
                conn.close()

            QtWidgets.QMessageBox.information(self.main_window, "Успех",
                                              "Данные о происшествии успешно обновлены.")
        except Exception as e:
            print("An error occurred:", e)

    def update_table_data(self):
        try:
            # Подключение к базе данных
            conn = sqlite3.connect('LR_2.db')
            curs = conn.cursor()

            # Обновление данных в tableWidget_3 для происшествий со статусом "Завершено"
            curs.execute("SELECT id_происшествия, Место_происшествия FROM Происшествия WHERE Статус=?",
                         ("Завершено",))
            data_completed = curs.fetchall()
            self.update_table_widget(self.tableWidget_3, data_completed)

            # Обновление данных в tableWidget_4 для происшествий со статусом "В расследовании"
            curs.execute("SELECT id_происшествия, Место_происшествия FROM Происшествия WHERE Статус=?",
                         ("В расследовании",))
            data_investigation = curs.fetchall()
            self.update_table_widget(self.tableWidget_4, data_investigation)

        except Exception as e:
            print("An error occurred:", e)
        finally:
            # Закрытие соединения с базой данных в блоке finally
            if conn:
                conn.close()

    def update_table_widget(self, table_widget, data):
        # Очистка таблицы
        table_widget.clearContents()
        table_widget.setRowCount(0)

        # Обновление данных в таблице
        table_widget.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                table_widget.setItem(row, col, item)

    # Переход с таблицы в изменение
    def open_edit_incident_window(self, item):
        try:
            # Получаем выбранный ID происшествия или место происшествия
            id_incident = item.text()  # Предполагается, что ID происшествия хранится в тексте элемента

            # Подключаемся к базе данных
            conn = sqlite3.connect('LR_2.db')
            curs = conn.cursor()

            # Выполняем запрос к базе данных для получения данных о происшествии по выбранному ID или месту происшествия
            curs.execute(
                "SELECT Дата_и_время, Место_происшествия, Участники, Описание, Детали, Статус FROM Происшествия WHERE id_происшествия = ? OR Место_происшествия = ?",
                (id_incident, id_incident))
            incident_data = curs.fetchone()

            # Заполняем виджеты на странице "Изменить происшествие" данными из базы данных
            self.dateTimeEdit_2.setDateTime(
                QtCore.QDateTime.fromString(incident_data[0], "yyyy-MM-dd HH:mm"))
            self.textEdit_5.setPlainText(incident_data[1])  # Место происшествия
            self.textEdit_6.setPlainText(incident_data[2])  # Участники
            self.textEdit_7.setPlainText(incident_data[3])  # Описание
            self.textEdit_8.setPlainText(incident_data[4])  # Детали
            self.comboBox_2.setCurrentText(incident_data[5])  # Статус

            # Закрываем соединение с базой данных
            conn.close()

            # Переключаемся на страницу "Изменить происшествие"
            self.stackedWidget.setCurrentIndex(3)

        except Exception as e:
            print("An error occurred:", e)

    def open_dialog(self):
        try:
            # Создание и отображение диалогового окна для ввода ID происшествия
            dialog = IdInputDialog(self.main_window)  # Передаем главное окно в качестве родителя
            if dialog.exec_():
                id_text = dialog.get_id()
                if id_text:
                    # Если ID происшествия введено, вызываем функцию для добавления данных в базу данных
                    self.add_data_to_database(id_text)
                    QMessageBox.information(self.main_window, "Сообщение",
                                            f"Успешно отправлено. \n ID происшествия: {id_text}")
                else:
                    QMessageBox.warning(self.main_window, "Предупреждение",
                                        "Пожалуйста, введите ID происшествия")
        except Exception as e:
            print("An error occurred:", e)

    def add_data_to_database(self, id_text):
        try:
            # Получаем значения из виджетов
            date_time = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm")
            location = self.textEdit_2.toPlainText()
            participants = self.textEdit_3.toPlainText()
            description = self.textEdit.toPlainText()
            details = self.textEdit_4.toPlainText()
            status = self.comboBox.currentText()

            # Подключаемся к базе данных
            conn = sqlite3.connect('LR_2.db')
            curs = conn.cursor()

            # Выполняем SQL-запрос INSERT
            curs.execute(
                "INSERT INTO Происшествия (id_происшествия, Дата_и_время, Место_происшествия, Участники, Описание, Детали, Статус) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (id_text, date_time, location, participants, description, details, status))

            # Подтверждаем изменения в базе данных
            conn.commit()

            # Закрываем соединение с базой данных
            conn.close()

            # Очищаем поля ввода после добавления данных
            self.dateTimeEdit.clear()
            self.textEdit.clear()
            self.textEdit_2.clear()
            self.textEdit_3.clear()
            self.textEdit_4.clear()

            # Опционально: вы можете добавить сообщение об успешном добавлении данных
            QtWidgets.QMessageBox.information(self.main_window, "Успех", "Данные успешно добавлены в базу данных.")

        except Exception as e:
            print("An error occurred:", e)

    # Окно отчетов
    def open_report_dialog(self):
        dialog = ReportDialog(self.tableWidget)
        dialog.exec_()

    def open_add_photo_dialog(self):
        # Создаем экземпляр диалогового окна для добавления фотографии
        add_photo_dialog = AddPhotoDialog()
        add_photo_dialog.exec_()

    def clear_form1(self):
        self.textEdit_5.clear()
        self.dateTimeEdit_2.setDateTime(QDateTime.currentDateTime())
        self.textEdit_6.clear()
        self.textEdit_7.clear()
        self.textEdit_8.clear()

    def clear_form(self):
        self.textEdit.clear()
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.textEdit_2.clear()
        self.textEdit_3.clear()
        self.textEdit_4.clear()

    def backOtch(self):
        self.stackedWidget.setCurrentIndex(0)

    def otchety(self):
        self.stackedWidget.setCurrentIndex(1)

    def dobp(self):
        self.stackedWidget.setCurrentIndex(2)

    def izmp(self):
        self.stackedWidget.setCurrentIndex(3)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setToolTip(
            _translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_5.setWhatsThis(
            _translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "Поиск происшествий(введите id)"))
        self.pushButton_4.setText(_translate("MainWindow", "Подтвердить"))
        self.label_4.setToolTip(
            _translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_4.setWhatsThis(
            _translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "Завершённые"))
        self.label_3.setToolTip(
            _translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_3.setWhatsThis(
            _translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "В расследовании"))
        self.pushButton.setText(_translate("MainWindow", "Добавить\n"
                                                         "происшествие "))
        self.pushButton_3.setText(_translate("MainWindow", "Изменить \n"
                                                           "происшествие"))
        self.pushButton_2.setText(_translate("MainWindow", "Отчёты"))
        self.pushButton_15.setText(_translate("MainWindow", "Обновить"))
        self.pushButton_16.setText(_translate("MainWindow", "Удалить"))

        # Отчёты
        self.label.setText(_translate("MainWindow", "Отчёт"))
        self.pushButton_5.setText(_translate("MainWindow", "Сформировать отчёт"))
        self.pushButton_6.setText(_translate("MainWindow", "Назад"))

        # Добавить происшесвтие
        self.pushButton_7.setText(_translate("MainWindow", "Назад"))
        self.label_6.setText(_translate("MainWindow", "Дата и время происшествия"))
        self.label_2.setText(_translate("MainWindow", "Место происшествия"))
        self.label_7.setText(_translate("MainWindow", "Участник происшествия"))
        self.pushButton_8.setText(_translate("MainWindow", "Сбросить всё"))
        self.label_8.setText(_translate("MainWindow", "Описание происшествия"))
        self.label_11.setText(_translate("MainWindow", "Прикрепление фотографий"))
        self.pushButton_9.setText(_translate("MainWindow", "Добавить фотографию"))
        self.label_9.setText(_translate("MainWindow", "Статус происшествия"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Завершено"))
        self.comboBox.setItemText(1, _translate("MainWindow", "В расследовании"))
        self.label_10.setText(_translate("MainWindow", "Другие детали"))
        self.pushButton_10.setText(_translate("MainWindow", "Отправить"))

        # Изменить Проишествие
        self.pushButton_11.setText(_translate("MainWindow", "Назад"))
        self.label_12.setText(_translate("MainWindow", "Дата и время происшествия"))
        self.label_13.setText(_translate("MainWindow", "Место происшествия"))
        self.label_14.setText(_translate("MainWindow", "Участник происшествия"))
        self.pushButton_12.setText(_translate("MainWindow", "Сбросить всё"))
        self.label_15.setText(_translate("MainWindow", "Описание происшествия"))
        self.label_16.setText(_translate("MainWindow", "Прикрепление фотографий"))
        self.pushButton_13.setText(_translate("MainWindow", "Изменить фотографию"))
        self.label_17.setText(_translate("MainWindow", "Статус происшествия"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Завершено"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "В расследовании"))
        self.label_18.setText(_translate("MainWindow", "Другие детали"))
        self.pushButton_14.setText(_translate("MainWindow", "Сохранить изменения"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
