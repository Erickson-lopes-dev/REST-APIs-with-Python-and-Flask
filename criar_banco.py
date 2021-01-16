import sqlite3

connection = sqlite3.connect('banco.db')

cursor = connection.cursor()

cria_tabela = 'CREATE TABLE IF NOT EXISTS ' \
              'hoteis (hotel_id text PRIMARY KEY, nome text, estrelas real, diaria real, cidade text)'

criar_hotel = "INSERT INTO hoteis VALUES ('alpha', 'Luisdu', 4.3, 100.55, 'Amapa')"

cursor.execute(cria_tabela)
cursor.execute(criar_hotel)
connection.commit()
connection.close()
