from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from .models import *
import random
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from datetime import date
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
import os
from django.shortcuts import get_object_or_404
import mimetypes
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from .forms import FileForm

def my_view(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    if request.method == 'POST':
        if 'login_account' in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")
            print(email)
            print(password)
            try:
                users = User.objects.get(email=email)
                username = users.username
            except:
                error = "Неверный логин или пароль!"
                return render(request, "authorization.html" ,{'error': error})
            print(username)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                error = "Неверный логин или пароль!"
                return render(request, "authorization.html" ,{'error': error})
        if 'check_account' in request.POST:
            email = request.POST.get("email")
           
            try:
                user = User.objects.get(email=email)
                try:
                    info = Check_Pass.objects.filter(email=email)
                    for i in info:
                        i.delete()
                except:
                    pass
                pin = ''.join(random.choices('0123456789', k=4))
          
                send_mail(
                                        "Ваш код для входа в аккаунт:",
                                        f"Ваш код для входа в аккаунт: {pin}\n" +
                                        f"Дата отправки : {date.today().strftime('%d.%m.%Y')}",
                                        EMAIL_HOST_USER,
                                        [email]
                                    )
                Check_Pass.objects.create(email=email, pin=pin)
                return redirect('check_code', email=email)
            except:
                error = "Почта ещё не зарегистрирована!"
                return render(request, "authorization.html" ,{'error': error})
        else:
            
            name = request.POST.get('name')
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                user = User.objects.get(email=email)
                error = "Почта уже зарегистрирована, попробуйте войти!"
                
                return render(request, "authorization.html" ,{'error': error})
            except:
                pin = ''.join(random.choices('0123456789', k=4))
                image = "/media/user/userimage.png"
                user_check = Create_User_Check.objects.create(username=name, email=email, password=password, pin=pin, image=image)
                id_user = user_check.id
                
          
                send_mail(
                                        "Skillwave:",
                                        f"Ваш код подтверждения: {pin}\n" +
                                        f"Дата отправки : {date.today().strftime('%d.%m.%Y')}",
                                        EMAIL_HOST_USER,
                                        [email]
                                    )
                
                return redirect('check_code_regist', id=id_user)
                
            
        
    return render(request, "authorization.html")

def check_code(request, email):
    if request.method == 'POST':
        try:
            pin_original = Check_Pass.objects.get(email=email)
            pin = request.POST.get('pin')
            if pin_original.pin == str(pin):
                pin_original.delete()
                user = User.objects.get(email=email)
                login(request, user)
                error = "OK"
                
                return render(request, "check_pin.html" ,{'error': error})
                # return redirect('homepage')
            else:
                error = "Код неверный!"
                return render(request, "check_pin.html" ,{'error': error})
            
        except:
            try:
                password = request.POST.get('password')
                user = request.user
                user.set_password(password)
                user.save()
                return redirect('homepage')
            except:
                error = "Код неверный!"
                return render(request, "check_pin.html" ,{'error': error})
            
    return render(request, "check_pin.html")


def check_code_regist(request, id):
    if request.method == 'POST':
        try:
            user_check = Create_User_Check.objects.get(id=id)
            pin = request.POST.get('pin')
            if user_check.pin == str(pin):
                user = User.objects.create_user(username=user_check.username, password=user_check.password, email=user_check.email)
                user_check = Create_User_Check.objects.get(email=user.email)
                User_Info.objects.create(user=user)
                user_check.delete()
                login(request, user)
                return redirect('homepage')
                
            else:
                error = "Код неверный!"
                return render(request, "check_pin.html" ,{'error': error})
            
        except:
            error = "Код неверный!"
            return render(request, "check_pin.html" ,{'error': error})
            
            
        
    return render(request, "check_code_regist.html")

@login_required(redirect_field_name='auth')
def homepage(request):
    direction = Napravlenii.objects.all()[:8]
    url_active = "homepage"
    napravkotoryekursy = Courses.objects.all()
    
    if request.method == 'POST':
        user_id = request.user.id
        displayCourseId = request.POST.get("displayCourseId")
        courses = Courses.objects.get(id=displayCourseId)

        user = User.objects.get(id=user_id)
        try:
            user_info = User_Info.objects.get(user=user)
        except:
            user_info = User_Info.objects.create(user=user)

        if request.POST.get('email'):
            user.email = request.POST.get('email')
            user.save()
        if request.POST.get('first_name'):
            user.first_name = request.POST.get('first_name')
            user.save()   
        if request.POST.get('number'):
            user_info.number = request.POST.get('number')
            user_info.save()  
       
        
        Datetime =datetime.now()
        try:
            Zapis.objects.create(user=user, napravlenie = courses, datetime=Datetime,number = user_info.number, email = user.email)
            messages.success(request, 'Заявка успешно отправлена.')
            return redirect('homepage')
        except:
            messages.success(request, 'Вы уже отправляли заявку. Ожидайте ответа.')
            return redirect('homepage')
            
    user = User.objects.get(id=request.user.id)
    context = {"url_active":url_active, 'direction': direction, 'kursy':napravkotoryekursy}
    return render(request, "homepage.html",context)


@login_required(redirect_field_name='auth')
def personal(request):
    if request.method == 'POST':
        user_id = request.user.id
        print(user_id)
        user = User.objects.get(id=user_id)
        try:
            user_info = User_Info.objects.get(user=user)
        except:
            user_info = User_Info.objects.create(user=user)
        if request.POST.get('username'):
            user.username = request.POST.get('usernameaFFFFFDDXSSDSSA')
            user.save()
        if request.POST.get('email'):
            user.email = request.POST.get('email')
            user.save()
        if request.POST.get('date_of_birth'):
            user_info.date_of_birth = request.POST.get('date_of_birth')
            user.save() 
        if request.POST.get('last_name'):
            user.last_name = request.POST.get('last_name')
            user.save()   
        if request.POST.get('first_name'):
            user.first_name = request.POST.get('first_name')
            user.save()   
        if request.POST.get('number'):
            user_info.number = request.POST.get('number')
            user_info.save()  
        if request.POST.get('country'):
            user_info.country = request.POST.get('country')
            user_info.save()
        if request.POST.get('city'):
            user_info.city = request.POST.get('city')
            user_info.save()
    user = User.objects.get(id=request.user.id)
    
    url_active = "personal"
    context = {"url_active":url_active, "user": user}
    return render(request, "personal.html",context)



@login_required(redirect_field_name='auth')
def directions(request):
    courses = Napravlenii.objects.all()
    url_active = "directions"
    context = {"url_active":url_active, "courses":courses}
    return render(request, "directions.html",context)

@login_required(redirect_field_name='auth')
def calendar(request):
    url_active = "calendar"
    context = {"url_active":url_active}
    return render(request, "calendar.html",context)

@login_required(redirect_field_name='auth')
def courses(request):
    user = request.user
    direction = Courses_Of_User.objects.filter(student=user)
    
    try:
        mentor = Mentors.objects.get(mentor=user)
    except Mentors.DoesNotExist:
        mentor = None
    try:
        direction1 = Courses_Of_User.objects.get(student=user)
        if direction1.sertificate == "":
            direction1.status = "В процессе"
            direction1.save()
        else:
            direction1.status = "Пройден"
            direction1.save()
    except:
        pass
    url_active = "courses"
    context = {"url_active":url_active, "direction":direction,"mentor":mentor}
    return render(request, "courses.html",context)


@login_required(redirect_field_name='auth')
def courses_info(request, id):
    napravlenii = Napravlenii.objects.get(id=id)
    courses_name  = napravlenii.name
    direction = Courses.objects.filter(napravlenii=napravlenii)
    url_active = "directions"
    if request.method == 'POST':
        user_id = request.user.id
        displayCourseId = request.POST.get("displayCourseId")
        courses = Courses.objects.get(id=displayCourseId)
        print(courses)
        print("jzjkjdhkzjhdk")
        user = User.objects.get(id=user_id)
        try:
            user_info = User_Info.objects.get(user=user)
        except:
            user_info = User_Info.objects.create(user=user)
        if request.POST.get('email'):
            user.email = request.POST.get('email')
            user.save()
        if request.POST.get('first_name'):
            user.first_name = request.POST.get('first_name')
            user.save()   
        if request.POST.get('number'):
            user_info.number = request.POST.get('number')
            user_info.save()  
        
        status = "Active"
        Datetime =datetime.now()
        try:
            Zapis.objects.create(user=user, napravlenie = courses, datetime=Datetime,status = status)
        except:
             pass
            
    user = User.objects.get(id=request.user.id)
    context = {"url_active":url_active, "courses_name":courses_name, "direction":direction, "user": user}
    return render(request, "courses_info.html",context)


@login_required(redirect_field_name='auth')
def notifications(request):
    url_active = "notifications"
    context = {"url_active":url_active}
    return render(request, "notifications.html",context)

@login_required(redirect_field_name='auth')
def allcourses(request):
    direction = Courses.objects.all()
    
    if request.method == 'POST':
        user_id = request.user.id
        displayCourseId = request.POST.get("displayCourseId")
        courses = Courses.objects.get(id=displayCourseId)

        user = User.objects.get(id=user_id)
        try:
            user_info = User_Info.objects.get(user=user)
        except:
            user_info = User_Info.objects.create(user=user)
        if request.POST.get('email'):
            user.email = request.POST.get('email')
            user.save()
        if request.POST.get('first_name'):
            user.first_name = request.POST.get('first_name')
            user.save()   
        if request.POST.get('number'):
            user_info.number = request.POST.get('number')
            user_info.save()  
        
        
        Datetime =datetime.now()
        try:
            Zapis.objects.create(user=user, napravlenie = courses, datetime=Datetime,number = user_info.number, email = user.email)
            messages.success(request, 'Заявка успешно отправлена.')
        except:
            messages.success(request, 'Вы уже отправляли заявку. Ожидайте ответа.')
    user = request.user
    try:
        mentor = Mentors.objects.get(mentor=user)
    except Mentors.DoesNotExist:
        mentor = None
            
    user = User.objects.get(id=request.user.id)
    url_active = "allcourses"
    context = {"url_active":url_active, "direction":direction, "user": user, "mentor":mentor}
    return render(request, "allcourses.html",context)




@login_required(redirect_field_name='auth')
def themes(request, id):
    courses_of_user = Courses_Of_User.objects.get(id=id)
    courses_name = courses_of_user.courses.name
    themes = Themes.objects.filter(napravlenie=courses_of_user.courses)
    progress_by_theme = []

    data_start= courses_of_user.date_start
    for theme in themes:
        
        progress = Progress.objects.filter(course_of_user=courses_of_user, themes=theme).first()
        progress_by_theme.append({
            'theme': theme,
            'id': theme.id,
            'status': progress.status if progress else 'Не пройден',
            'ocenka': progress.ocenka if progress else 'Нет баллов',
            
        })

    context = {
        'url_active': 'themes',
        'courses_name': courses_name,
        'progress_by_theme': progress_by_theme,
        "data_start":data_start,
    }

    return render(request, "themes.html", context)



@login_required(redirect_field_name='auth')
def themesmentor(request, id):
    courses_of_user = Courses_Of_User.objects.get(id=id)
    courses_name = courses_of_user.courses.name
    nnnaame = courses_of_user.student.first_name
    # Получить все темы, связанные с этим курсом
    themes = Themes.objects.filter(napravlenie=courses_of_user.courses)
    # id_themes = themes.id
    # Создать список для хранения прогресса по каждой теме
    progress_by_theme = []
    
    # Для каждой темы получить прогресс из модели Progress
    data_start= courses_of_user.date_start
    for theme in themes:
        
        progress = Progress.objects.filter(course_of_user=courses_of_user, themes=theme).first()
        # themeee = Themes.objects.filter(napravlenie=courses_of_user.courses, id=theme).first()
        progress_by_theme.append({
            'theme': theme,
            'id': theme.id,
            'status': progress.status if progress else 'Не пройден',
            'ocenka': progress.ocenka if progress else 'Нет баллов',
            
        })
    user = request.user
    mentor = Mentors.objects.get(mentor=user)
    courses = Courses.objects.get(id = courses_of_user.courses.id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.themes = Themes.objects.get(id=id)
            file_instance.save()
        Themes.objects.create(title=title, description=description, napravlenie=courses, teacher=mentor)
        return redirect('themesmentor', id=id)
    else:
        form = FileForm()
    # Передать данные в шаблон
    context = {
        'url_active': 'themes',
        'courses_name': courses_name,
        'progress_by_theme': progress_by_theme,
        "data_start":data_start,
        'nnnaame': nnnaame,
        'form': form
    }

    return render(request, "themesmentor.html", context)



@login_required(redirect_field_name='auth')

def lesson(request, id):
    theme = get_object_or_404(Themes, id=id)
    user = request.user
    try:
        mentor = Mentors.objects.get(mentor=user)
    except Mentors.DoesNotExist:
        mentor = None
    # Получение курсов, где текущий пользователь является студентом
    user_courses_as_student = Courses_Of_User.objects.filter(student=request.user)
    
    # Получение курсов, где текущий пользователь является ментором
    user_as_mentor = Mentors.objects.filter(mentor=request.user).first()
    user_courses_as_teacher = Courses_Of_User.objects.filter(teacher=user_as_mentor) if user_as_mentor else Courses_Of_User.objects.none()
    
    # Объединение двух запросов
    user_courses = user_courses_as_student | user_courses_as_teacher
    
    # Проверка, связан ли курс с текущей темой
    if not user_courses.filter(courses=theme.napravlenie).exists():
        return redirect('home')  # или другая страница с ошибкой
    
    messages = Message.objects.filter(theme=theme).order_by('timestamp')
    
    files = Files.objects.filter(themes=theme)
    files_data = [{'id': document.id, 'file_name': os.path.basename(document.file.name)} for document in files]
   

    context = {
        'url_active': 'lesson',
        'themes_title': theme.title,
        'themes_description': theme.description,
        'files_data': files_data,
        'theme': theme,
        'messages': messages,
        'mentor':mentor,
    }
    return render(request, "lesson.html", context)


def download_document(request, document_id):
    files = get_object_or_404(Files, id=document_id)
    file_path = files.file.path
    file_name = os.path.basename(file_path)

    # Определение типа MIME файла
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # В случае, если тип MIME не определён

    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response


def doc(request):
     
     context = {"url_active":"doc"}
     return render(request, "document_list.html", context)

from django.db.models import Count
def coursesofmentor(request):
    user = request.user
    mentor = Mentors.objects.get(mentor=user)
    courses = Courses_Of_User.objects.filter(teacher=mentor)
    unique_courses = []
    course_names = set()
    for course in courses:
        if course.courses.name not in course_names:
            unique_courses.append(course)
            course_names.add(course.courses.name)
    context = {"url_active":"coursesOfMentor","courses":unique_courses}
    return render(request, "coursesofmentor.html", context)




def tableofmentor(request,id):
    user = request.user
    mentor = Mentors.objects.get(mentor=user)
    courses_of_user = Courses_Of_User.objects.filter(id=id, teacher = mentor)
    
    if not courses_of_user.exists():
        return redirect('home')  # Перенаправить на домашнюю страницу или другую страницу в случае, если курс не найден
    
    course_of_user = courses_of_user.first()
    courses_name = course_of_user.courses.name
    
    students = Courses_Of_User.objects.filter(courses=course_of_user.courses, teacher=mentor).select_related('student').distinct()
    
    students_data = []
    for course in students:
        student_info = {
            'first_name': course.student.first_name,
            'last_name': course.student.last_name,
            'email': course.student.email,
            'number': course.student.user_info.number,
            'status': course.status,
            'id': course.id,
        }
        students_data.append(student_info)

    context = {"url_active":"tableofmentor", 
            "courses_of_user":courses_of_user,
            "students": students_data,
            "courses_name":courses_name}
    return render(request, "tableofmentor.html", context)



# def lobby(request):
#     return render(request, 'chat/lobby.html',{})
# views.py

# def room(request,room_name):
#     return render(request, 'chat/messangeroom.html',{
#         'room_name':room_name
#     })