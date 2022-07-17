from turtle import title
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
import re
import mysql.connector

mydb=mysql.connector.connect(host="localhost",user="root",password="",charset='utf8',database="udaan")

def insert(regi_no, name, dob, gender, email, phone_no, address, pin, district, state, name_10, board_10, year_10, omarks_10, tmarks_10, percentage_10, name_12, board_12, year_12, omarks_12, tmarks_12, percentage_12, name_e, board_e, year_e, omarks_e, tmarks_e, percentage_e, photo_name, income_name, address_name, marksheet_name):
    cursor=mydb.cursor(buffered=True)

    cursor.execute('INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (regi_no, name, dob, gender, email, phone_no, address, pin, district, state, name_10, board_10, year_10, omarks_10, tmarks_10, percentage_10, name_12, board_12, year_12, omarks_12, tmarks_12, percentage_12, name_e, board_e, year_e, omarks_e, tmarks_e, percentage_e, photo_name, income_name, address_name, marksheet_name))
    print(cursor)
    mydb.commit()

def insert2(regi_no, i_name, i_exam, i_email, i_phone_no, password, i_website, brochure_name, identity_name, address_name, pan_name, fee_name):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('INSERT INTO institute VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (regi_no, i_name, i_exam, i_email, i_phone_no, password, i_website, brochure_name, identity_name, address_name, pan_name, fee_name))
    print(cursor)
    mydb.commit()
 
def account(email, dob):
    cursor=mydb.cursor()
    cursor.execute('SELECT * FROM student WHERE email = %s and dob = %s', (email, dob))
    account = cursor.fetchone()
    if account:
        return True
    return False

def i_account(email, password):
    cursor=mydb.cursor()
    cursor.execute('SELECT * FROM institute WHERE email = %s and password = %s', (email, password))
    account = cursor.fetchone()
    if account:
        return True
    return False

def reg_no():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT registration_no FROM student ORDER BY registration_no DESC')
    a=cursor.fetchone()
    return a[0]

def i_reg_no():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT registration_no FROM institute ORDER BY registration_no DESC')
    a=cursor.fetchone()
    return a[0]

def profile_info():
    global session_email, session_dob
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT * FROM student WHERE email = %s and dob = %s', (session_email, session_dob))
    a=cursor.fetchone()
    return a

def student():
    b=[]
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT name, email, phone_no, address, photo address FROM student')
    a=cursor.fetchone()
    while a:
        c={'name':a[0],'email':a[1],'phone_no':a[2],'address':a[3],'photo':a[4]}
        b.append(c)
        a=cursor.fetchone()
    return b
def institute():
    b=[]
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT name, email, phone_no, website, exam address FROM institute')
    a=cursor.fetchone()
    while a:
        c={'name':a[0],'email':a[1],'phone_no':a[2],'website':a[3],'exam':a[4]}
        b.append(c)
        a=cursor.fetchone()
    return b

def sno():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT sno FROM notice ORDER BY sno DESC')
    a=cursor.fetchone()
    return a[0]

def insert_notice(sno, title, file):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('INSERT INTO notice VALUES (%s, %s, %s)', (sno, title, file))
    print(cursor)
    mydb.commit()
    
def get_notice():
    b=[]
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT title, file FROM notice')
    a=cursor.fetchone()
    while a:
        c={'title':a[0],'link':a[1]}
        b.append(c)
        a=cursor.fetchone()
    return b

loggedin=False
session_email=''
session_dob=''
name=''
dob=''
gender=''
email=''
phone_no=0
address=''
pin=0
district=''
state=''
name_10=''
board_10=''
year_10=0
omarks_10=0
tmarks_10=0
percentage_10=0
name_12=''
board_12=''
year_12=0
omarks_12=0
tmarks_12=0
percentage_12=0
name_e=''
board_e=''
year_e=0
omarks_e=0
tmarks_e=0
percentage_e=0
i_name=''
i_exam=''
i_website=''
i_email=''
password=''
i_phone_no=0

def home(request):
    param={'notice':get_notice()}
    return render(request,'home.html',param)

def s_list(request):
    param={'student':student()}
    return render(request,'student.html',param)

def i_list(request):
    param={'student':institute()}
    return render(request,'institute.html',param) 

def notice(request):
    if request.method == "POST":
        title=request.POST.get('title','')
        file=request.FILES['notice_file']
        if title != '':
            n=sno()+1
            file_name="notice_"+str(n)+"."+(file.name).split('.')[-1]
            insert_notice(n, title, file_name)
            fs = FileSystemStorage()
            fs.save(file_name,file)
            return redirect('student')
    return render(request,'notice.html')

def personal_details(request):
    global name, dob, gender, email, phone_no
    msg=''
    name1=request.POST.get('name','')
    dob1=request.POST.get('dob','')
    gender1=request.POST.get('gender','')
    email1=request.POST.get('email','')
    phone_no1=request.POST.get('phone_no',0)
    if name1 != '' and dob1 != '' and gender1 != '' and email1 != '' and phone_no1 != 0:
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email1):
            msg = 'Invalid email address!'
        elif re.match(r'[0-9]+', name1):
            msg = 'Name must contain only characters'
        elif re.match(r'[0-9]+', gender1):
            msg = 'Gender must contain only characters'
        elif len(phone_no1)!=10:
            msg = 'Phone Number must contain only 10 digits!'
        # elif account(email):
        #     msg = 'Already registeration is done from this Email!'
        else:
            name=name1
            dob=dob1
            gender=gender1
            email=email1
            phone_no=int(phone_no1)
            return redirect('c_details')
    param={'msg':msg, 'name':name1,'dob':dob1,'gender':gender1, 'email':email1, 'phone_no':phone_no1}
    return render(request,'personalddetails.html',param)

def login(request):
    global loggedin, session_email, session_dob
    msg=''
    email=request.POST.get('email','none')
    dob=request.POST.get('dob','none')
    param={'msg':msg}
    if(email!='none' and dob!='none'):
        if account(email,dob):
            loggedin=True
            session_email=email
            session_dob=dob
            return redirect('profile')
        else:
            msg = 'Incorrect username or password'
    param={'msg':msg,'name':'Student ','url':"register",'url1':"login"}
    return render(request,'login.html',param)

def i_login(request):
    global loggedin
    msg=''
    email=request.POST.get('email','none')
    password=request.POST.get('password','none')
    param={'msg':msg}
    if(email!='none' and password!='none'):
        if i_account(email,password):
            loggedin=True
            return render(request,'home.html')
        else:
            msg = 'Incorrect username or password'
    param={'msg':msg,'name':'Student ','url':"register",'url1':"login"}
    return render(request,'i_login.html',param)

def communication_details(request):
    global name, dob, gender, email, phone_no, address, pin, district, state,name_10, board_10, year_10, omarks_10,tmarks_10, percentage_10,name_12, board_12, year_12, omarks_12,tmarks_12, percentage_12, name_e, board_e, year_e, omarks_e, tmarks_e, percentage_e
    msg=''
    address1=request.POST.get('address','')
    pin1=request.POST.get('pin',0)
    district1=request.POST.get('district','')
    state1=request.POST.get('state','')
    param={'msg':msg, 'name':address1,'dob':pin1 ,'gender':district1, 'email':state1}
    if name == '' and dob == '' and gender == '' and email == '' and phone_no == 0:
        return redirect('p_details')
    elif address1 != '' and pin1 != 0 and district1 != '' and state1 != '':
        if len(pin1)!=6:
            msg = 'PIN must contain only 6 digits!'
        else:
            address=address1
            pin=int(pin1)
            district=district1
            state=state1
            return redirect('e_details')
    param={'msg':msg, 'name':address1,'dob':pin1 ,'gender':district1, 'email':state1} 
    return render(request,'communicationdetails.html',param)

def education_details(request):
    global name, dob, gender, email, phone_no, address, pin, district, state, name_10, board_10, year_10, omarks_10, tmarks_10, percentage_10, name_12, board_12, year_12, omarks_12, tmarks_12, percentage_12, name_e, board_e, year_e, omarks_e, tmarks_e, percentage_e
    name_101=request.POST.get('name_10','')
    board_101=request.POST.get('board_10','')
    year_101=request.POST.get('year_10',0)
    omarks_101=request.POST.get('omarks_10',0)
    tmarks_101=request.POST.get('tmarks_10',0)
    percentage_101=request.POST.get('percentage_10',0)
    name_121=request.POST.get('name_12','')
    board_121=request.POST.get('board_12','')
    year_121=request.POST.get('year_12',0)
    omarks_121=request.POST.get('omarks_12',0)
    tmarks_121=request.POST.get('tmarks_12',0)
    percentage_121=request.POST.get('percentage_12',0)
    name_e1=request.POST.get('name_e','')
    board_e1=request.POST.get('board_e','')
    year_e1=request.POST.get('year_e',0)
    omarks_e1=request.POST.get('omarks_e',0)
    tmarks_e1=request.POST.get('tmarks_e',0)
    percentage_e1=request.POST.get('percentage_e',0)
    param={'name_10':name_101, 'board_10':board_101, 'year_10':year_101, 'omarks_10':omarks_101, 'tmarks_10':tmarks_101, 'percentage_10':percentage_101, 'name_12':name_121 , 'board_12':board_121, 'year_12':year_121, 'omarks_12':omarks_121, 'tmarks_12':tmarks_121, 'percentage_12':percentage_121, 'name_e':name_e1, 'board_e':board_e1, 'year_e':year_e1, 'omarks_e':omarks_e1, 'tmarks_e':tmarks_e1, 'percentage_e':percentage_e1}
    if name == '' and dob == '' and gender == '' and email == '' and phone_no == 0:
        return redirect('p_details')
    elif address == '' and pin == 0 and district == '' and state == '':
        return redirect('c_details')
    elif name_101 != '' and board_101 != '' and year_101 != 0 and omarks_101 != 0 and tmarks_101 != 0 and percentage_101 != 0:
        name_10=name_101
        board_10=board_101
        year_10=int(year_101)
        omarks_10=int(omarks_101)
        tmarks_10=int(tmarks_101)
        percentage_10=int(percentage_101)
        if name_121 != '' and board_121 != '' and year_121 != 0 and omarks_121 != 0 and tmarks_121 != 0 and percentage_121 != 0:
            name_12=name_121
            board_12=board_121
            year_12=int(year_121)
            omarks_12=int(omarks_121)
            tmarks_12=int(tmarks_121)
            percentage_12=int(percentage_121)
            if name_e1 != '' and board_e1 != '' and year_e1 != 0 and omarks_e1 != 0 and tmarks_e1 != 0 and percentage_e1 != 0:
                name_e=name_e1
                board_e=board_e1
                year_e=int(year_e1)
                omarks_e=int(omarks_e1)
                tmarks_e=int(tmarks_e1)
                percentage_e=int(percentage_e1)
        return redirect('u_document')
    return render(request,'educationdetails.html',param)

def document_upload(request):
    global name, dob, gender, email, phone_no, address, pin, district, state, name_10, board_10, year_10, omarks_10, tmarks_10, percentage_10, name_12, board_12, year_12, omarks_12, tmarks_12, percentage_12, name_e, board_e, year_e, omarks_e, tmarks_e, percentage_e
    if request.method == "POST":
        if name == '' and dob == '' and gender == '' and email == '' and phone_no == 0:
            return redirect('p_details')
        elif address == '' and pin == 0 and district == '' and state == '':
            return redirect('c_details')
        elif name_10 == '' and board_10 == '' and year_10 == 0 and omarks_10 == 0 and tmarks_10 == 0 and percentage_10 == 0:
            return redirect('e_details')
        else:
            regi_no=int(reg_no())+1
            photo=request.FILES['photo']
            photo_name=str(regi_no)+"_photo."+(photo.name).split('.')[-1]
            income=request.FILES['income']
            print(photo)
            income_name=str(regi_no)+"_income."+(income.name).split('.')[-1]
            addressf=request.FILES['address']
            address_name=str(regi_no)+"_address."+(addressf.name).split('.')[-1]
            marksheet=request.FILES['marksheet']
            marksheet_name=str(regi_no)+"_marksheet."+(marksheet.name).split('.')[-1]
            fs = FileSystemStorage()
            fs.save(photo_name,photo)
            fs.save(income_name,income)
            fs.save(address_name,addressf)
            fs.save(marksheet_name,marksheet)
            insert(regi_no, name, dob, gender, email, phone_no, address, pin, district, state, name_10, board_10, year_10, omarks_10, tmarks_10, percentage_10, name_12, board_12, year_12, omarks_12, tmarks_12, percentage_12, name_e, board_e, year_e, omarks_e, tmarks_e, percentage_e, photo_name, income_name, address_name, marksheet_name)
    return render(request,'uploaddocument.html')

def institute_details(request):
    global i_name, i_exam, i_website, i_email, i_phone_no, password
    msg=''
    i_name1=request.POST.get('name','')
    i_exam1=request.POST.get('exam','')
    i_email1=request.POST.get('email','')
    i_phone_no1=request.POST.get('phone_no',0)
    i_website1=request.POST.get('website','')
    password1=request.POST.get('password','')
    c_password1=request.POST.get('c_password','')
    param={'msg':msg, 'name':i_name1,'exam':i_exam1, 'email':i_email1, 'phone_no':i_phone_no1,'website':i_website1, 'password':password1,'c_password':c_password1}
    if i_name1 != '' and i_exam1 != '' and i_email1 != '' and i_phone_no1 != 0:
        if not re.match(r'[^@]+@[^@]+\.[^@]+', i_email1):
            msg = 'Invalid email address!'
        elif re.match(r'[0-9]+', i_name1):
            msg = 'Name must contain only characters'
        elif password1 != c_password1:
            msg = 'Confirm password does not match'
        elif len(i_phone_no1)!=10:
            msg = 'Phone Number must contain only 10 digits!'
        # elif account(email):
        #     msg = 'Already registeration is done from this Email!'
        else:
            i_name=i_name1
            i_exam=i_exam1
            i_email=i_email1
            i_phone_no=int(i_phone_no1)
            i_website=i_website1
            password=password1
            return redirect('i_document')
    param={'msg':msg, 'name':i_name1,'exam':i_exam1, 'email':i_email1, 'phone_no':i_phone_no1,'website':i_website1, 'password':password1,'c_password':c_password1}
    return render(request,'institutedetails.html', param)

def i_document_upload(request):
    global i_name, i_exam, i_email, i_phone_no, i_website, password
    if request.method == "POST":
        if i_name == '' and i_exam == '' and i_email == '' and i_phone_no == 0:
            return redirect('i_details')
        else:
            regi_no=int(i_reg_no())+1
            brochure=request.FILES['brochure']
            brochure_name=str(regi_no)+"_brochure."+(brochure.name).split('.')[-1]
            identity=request.FILES['identity']
            identity_name=str(regi_no)+"_identity."+(identity.name).split('.')[-1]
            address=request.FILES['address']
            address_name=str(regi_no)+"_address."+(address.name).split('.')[-1]
            pan=request.FILES['pan']
            pan_name=str(regi_no)+"_pan."+(pan.name).split('.')[-1]
            fee=request.FILES['fee']
            fee_name=str(regi_no)+"_fee."+(fee.name).split('.')[-1]
            fs = FileSystemStorage()
            fs.save(brochure_name,brochure)
            fs.save(identity_name,identity)
            fs.save(address_name,address)
            fs.save(pan_name,pan)
            fs.save(fee_name,fee)
            insert2(regi_no, i_name, i_exam, i_email, i_phone_no, password, i_website, brochure_name, identity_name, address_name, pan_name, fee_name)
    return render(request,'uploadinstitutedoc.html')

def profile(request):
    global loggedin
    if loggedin:
        info=profile_info()
        photo='media/'+info[28]
        param={'reg_no':info[0],'name':info[1],'dob':info[2],'gender':info[3],'email':info[4],'phone_no':info[5],'address':info[6],'pin':info[7],'district':info[8],'state':info[9],'name_10':info[10],'board_10':info[11],'year_10':info[12],'omarks_10':info[13],'tmarks_10':info[14],'percentage_10':info[15],'name_12':info[16],'board_12':info[17],'year_12':info[18],'omarks_12':info[19],'tmarks_12':info[20],'percentage_12':info[21],'name_e':info[22],'board_e':info[23],'year_e':info[24],'omarks_e':info[25],'tmarks_e':info[26],'percentage_e':info[27], 'photo_url':photo}
        return render(request, 'profilepg.html', param)
    return redirect('login')

def dashboard(request):
    global loggedin
    if loggedin:
        info=profile_info()
        photo='media/'+info[28]
        param={'reg_no':info[0],'name':info[1],'dob':info[2],'gender':info[3],'email':info[4],'phone_no':info[5],'address':info[6], 'photo_url':photo}
        return render(request,'dashboard.html',param)
    return redirect('login')

