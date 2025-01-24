from datetime import date, timedelta

def check_16_older(birthday: date):
    return birthday <= date.today()-timedelta(days=16*365)

def check_18_older(birthday: date):
    return birthday <= date.today()-timedelta(days=18*365)