###########################################################
# 
###########################################################

QUERY = """select DateOper, Dop, NameAn, DrobnoeChislo1 from MBAnalit 
                            where MBAnalit.Vid = 3704 
                            and Date2 = """
""" Запрос. Последняя строка - поле типа дата таблицы, по которому будет производится отбор данных """

DRIVER = "ODBC Driver 17 for SQL Server"
""" Драйвер ODBC. Инструкция по установке:
    https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2016
    """

SERVER = '10.30.100.102'
""" Адрес сервера базы данных"""

DATABASE='directum'
""" Имя базы данных"""

UID='sa'
""" Имя пользователя"""

PWD='Qwaser082'
""" Пароль"""



