from datetime import datetime, date, timedelta

today = datetime.today()
first = date(day=1, month=today.month, year=today.year)
first_year = date(day=1, month=1, year=today.year)

lastMonth = first - timedelta(days=1)
semana = first + timedelta(days=7)

def fecha_hoy():
    return datetime.utcnow() + timedelta(days=-1)

def fecha_mañana():
    return datetime.utcnow() + timedelta(days=1)

def fecha_semana():
    return datetime.utcnow() + timedelta(days=-6)

def fecha_mes():
    return first

def fecha_year():
    return first_year