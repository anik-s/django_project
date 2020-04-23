
def get_formatted_date(year, month, day):
    day_s = ''
    month_s = ''
    if day != '':
        day_s = day + ' '
    if month != '':
        month_s = month + ', '
    f_date = "{0}{1}{2}".format(day_s, month_s, year)
    return f_date
