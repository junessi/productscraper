import datetime

def get_yyyymmdd():
    now = datetime.datetime.now()
    return "{0}".format(now.strftime("%Y%m%d"))