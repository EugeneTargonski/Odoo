###########################################################
# API НБРБ
###########################################################

CURRENCY_LIST_URL = 'http://www.nbrb.by/API/ExRates/Currencies'
""" url списка валют """
CURRENCY_RATE_URL = 'http://www.nbrb.by/API/ExRates/Rates/'
""" при добавлении в конец внутреннего ИД валюты получим url курса конкретной валюты на сегодня """
RECORD_CUR_DATE_BEGIN_NAME = 'Cur_DateStart'
""" имя поля начала действия валюты """
RECORD_CUR_DATE_END_NAME = 'Cur_DateEnd'
""" имя поля конца действия валюты """
RECORD_CUR_ABBR_NAME = 'Cur_Abbreviation'
""" имя поля аббривеатуры валюты """
RECORD_CUR_ID_NAME = 'Cur_ID'
""" имя поля ИД валюты """
RECORD_CUR_SCALE_NAME = 'Cur_Scale'
""" имя поля базы курса валюты """
RECORD_CUR_OFFRATE_NAME = 'Cur_OfficialRate'
""" имя поля курса валюты """
ATTR_DATE = '?onDate='
""" атрибут даты курса валюты """
BASE_CURRENCY = "BYN"
""" базовая валюта """

