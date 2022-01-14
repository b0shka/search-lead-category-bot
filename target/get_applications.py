import mysql.connector
from Variables.config import IP_DB, USER_DB, PASSWORD_DB, DATABASE


db = mysql.connector.connect(host=IP_DB,
							user=USER_DB,
							password=PASSWORD_DB,
							database=DATABASE)
sql = db.cursor()


def get_data_applications():
    sql.execute("SELECT DISTINCT contact, text_application FROM `applications_target` ORDER BY id DESC;")
    applications = sql.fetchall()
    
    return applications


def main():
    COUNT_APP = 50
    applications = get_data_applications()
    
    with open("applications.txt", 'wb') as file:
        for index, app in enumerate(applications):
            data = f"{app[1]}\nКонтакт: {app[0]}\n\n{'#'*25}\n"
            file.write(data.encode())


if __name__ == "__main__":
    main()