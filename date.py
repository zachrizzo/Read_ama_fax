# from datetime import date ,timedelta
# today = date.today()

# # dd/mm/YY
# d1 = today.strftime("%d/%m/%Y")
# print("d1 =", d1)

# # Textual month, day and year	
# d2 = today.strftime("%B %d, %Y")
# print("d2 =", d2)

# # mm/dd/y
# d3 = today
# # .strftime("%m/%d/%y")
# print("d3 =", d3)

# # Month abbreviation, day and year	
# d4 = today.strftime("%b-%d-%Y")
# print("d4 =", d4)

# d5 = date(2022,7,15)
# delta = d3 - d5
# print(delta.days)
date_of_birth_full= '022611961'
date_of_birth_full= date_of_birth_full[0] + date_of_birth_full[1] + '/'+date_of_birth_full[2] + date_of_birth_full[3]  + '/'+ date_of_birth_full[4] + date_of_birth_full[6]+ date_of_birth_full[7] + date_of_birth_full[8] 
print(date_of_birth_full)
# string = 'EXAMH33368S47 0810312022 13SPM USBREASTUNILATLIMITEDLEFT'
# string = [exam,exam_number_line] = string.lower().split('h',1)
# [exam_number, date,order_type] = exam_number_line.split(' ')
# print (string)
print(len('121345678'))

zach = 'zach hi ho hwl hwj hwz'
count = 0
for i in zach:
    if(i.isspace()):
        count=count+1

print (count)

if count >3 :
   [h,z,a,d] =  zach.split(' ', 3 )

print( h)
print (z)
print (a)
print (d)

words = 'Bullis ReginaB Sex F DOB080511947Age175'

[rest_of_sting,  age_number ] =words.split('Age')
[name_and_sex,date_of_birth_full] = rest_of_sting.split('DOB')
[fullName, sex] = name_and_sex.split('Sex')
fullName = fullName.strip()
[lastname, firstname] =fullName.split(' ')
print(date_of_birth_full)
print(firstname, lastname)

exam = 'EXAMH32604208 080712022 114SAM MRSHOULDERWITHOUTCONTRASTCLEFD'

doc= 'referringphysicianashleedauscha'

order_number_line = '331320375 080512022 1030 pm mgscreeningmammopm bil wamplants 43d'

try:
    try:
        for i in range(9):
            [orderNumber_and_date_time,orderType] = order_number_line.split(f'{i}pm',1)
           
    except:
        for i in range(9):
           
             [orderNumber_and_date_time,orderType] = order_number_line.split(f'{i}am', 1)

except:
    try:
         [orderNumber_and_date_time,orderType] = order_number_line.split(' am', 1)
    except:
        try:
            [orderNumber_and_date_time,orderType] = order_number_line.split(' pm', 1)
        except:
            pass

orderType=orderType.replace(' ','')
[order_number, date, time] = orderNumber_and_date_time.split(' ')

print(orderType)
print(order_number)
print(date)
print(time)

#for each pdf in folder  turn into pictures 
