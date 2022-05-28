import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres",
                                        password="super",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="kotbase") 
except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error) #Нужен логер

class DataBaseService: 
    def db_add_user(self, user_id, user_name, dt):
        self.cursor = connection.cursor()
        insert_query = """ INSERT INTO client_tab (telegram_id, name, date_of_using) VALUES (%s, %s, %s)"""
        self.cursor.execute(insert_query, (user_id, user_name, dt))
        connection.commit() 

    def db_user_list(self, user_list):
        self.cursor = connection.cursor()
        self.cursor.execute("SELECT telegram_id from client_tab")
        self.users = self.cursor.fetchall()
        for item in self.users:
            user_list.append(item[0])
        return(user_list)

    def db_sub_notifications(self, telegram_id, cat_sub):
        self.cursor = connection.cursor()
        update_query = """ UPDATE client_tab SET cat_sub = %s WHERE telegram_id = %s"""
        self.cursor.execute(update_query, (cat_sub, telegram_id))
        connection.commit()

    def db_sub_holidays(self, telegram_id, holidays_sub):
        self.cursor = connection.cursor()
        update_query = """ UPDATE client_tab SET holidays_sub = %s WHERE telegram_id = %s"""
        self.cursor.execute(update_query, (holidays_sub, telegram_id))
        connection.commit()

    def db_amount_holidays(self, telegram_id, holidays_amount):
        self.cursor = connection.cursor()
        update_query = """ UPDATE client_tab SET holidays_amount = %s WHERE telegram_id = %s"""
        self.cursor.execute(update_query, (holidays_amount, telegram_id))
        connection.commit()