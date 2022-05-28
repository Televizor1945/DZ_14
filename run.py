from flask import Flask, jsonify

from views import api_netflix_blueprint # Импортируем блюпринт
import logger

import sqlite3
import prettytable

app = Flask(__name__)                    # Создаем экземпляр Flask
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False

logger.create_logger()
app.register_blueprint(api_netflix_blueprint)  # регистрируем блюпринт





if __name__ == "__main__":               # Запускаем сервер только, если файл запущен, а не импортирован
    app.run(debug=True)