import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QDateEdit, QPushButton

class ReportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание отчётов")
        self.layout = QVBoxLayout()

        # Добавляем виджеты выбора даты
        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.layout.addWidget(self.start_date_edit)

        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.layout.addWidget(self.end_date_edit)

        # Добавляем кнопки "Сохранить" и "Отмена"
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_report)
        self.layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.close)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def save_report(self):
        start_date = self.start_date_edit.date().toString("dd.MM.yyyy")
        end_date = self.end_date_edit.date().toString("dd.MM.yyyy")
        print("Сохраняем отчёт за период:", start_date, "-", end_date)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ReportDialog()
    dialog.show()
    sys.exit(app.exec_())
