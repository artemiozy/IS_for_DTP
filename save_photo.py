def save_photo(self):
    try:
        if self.photo_path:
            # Открываем изображение и читаем его в бинарном режиме
            with open(self.photo_path, 'rb') as f:
                photo_data = f.read()

            # Подключаемся к базе данных
            conn = sqlite3.connect('LR_2.db')
            curs = conn.cursor()

            # Выполняем SQL-запрос INSERT, используя параметризованный запрос
            curs.execute(
                "UPDATE Происшествия SET Фотографии = ? WHERE id_происшествия = ?",
                (photo_data, self.current_incident_id))

            # Подтверждаем изменения в базе данных
            conn.commit()

            # Закрываем соединение с базой данных
            conn.close()

            QtWidgets.QMessageBox.information(self, "Успех", "Фотография успешно сохранена в базе данных.")
        else:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Сначала выберите фотографию для сохранения.")
    except Exception as e:
        print("An error occurred:", e)