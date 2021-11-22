import datetime 
#from datetime import datetime
import dateutil.relativedelta
import calendar 
from datetime import date



d = datetime.datetime.strptime("2021-09-02", "%Y-%m-%d") 
d2 = d - dateutil.relativedelta.relativedelta(months=1)
print(d2)
print(d2.month)

today = datetime.date.today()
print(today)
print(today.month)
d3 = today - dateutil.relativedelta.relativedelta(months=1)#Use thos as last month
print(d3.month)

def monthdelta(date, delta):    
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12    
    if not m: m = 12    
    d = min(date.day, calendar.monthrange(y, m)[1])  
    #print(d)  
    return date.replace(day=d,month=m, year=y)
next_month = monthdelta(date.today(), 1) 
#print(next_month)

d4 = today - dateutil.relativedelta.relativedelta(years=1)#Use thos as last month
print(d4.year)

l = [1,2,3,4,5,6,7,8,90]
l2 = [11,22,43,64,85,96,45,80,90]
l3 = ['josh', 'bwen', 'cosmos', 'hutyui']


total = sum([cont for cont in l])
print(total)
l3.insert(3, 'lufafa')
print(l3)


