from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User 
from django.utils.translation import gettext_lazy as _

class Check_Pass(models.Model):
    email = models.CharField( verbose_name="E-MAIL", max_length=255)
    pin = models.CharField(verbose_name="Пин код", max_length=255)
    def __str__(self):
        return str(self.email)
    class Meta:
        verbose_name = "Проваерка пароля"
        verbose_name_plural = "Проверка пароля"

class Create_User_Check(models.Model):
    username = models.CharField(verbose_name="Имя пользователя", max_length=255)
    password = models.CharField(verbose_name="Пароль", max_length=255)
    email = models.CharField(verbose_name="E-MAIL", max_length=255)
    pin = models.CharField(verbose_name="Пин код", max_length=255)
    image = models.FileField(verbose_name="Фото", default="/static/images/user/profile_image/userimage.png")
    def __str__(self):
        return str(self.email)
    class Meta:
        verbose_name = "Проваерка пользователя при авторизации"
        verbose_name_plural = "Проверка пользователей при авторизации"

class User_Info(models.Model):
    user = models.OneToOneField(User,verbose_name="Пользователь",  on_delete=models.CASCADE, null=True, related_name="user_info")
    patronymic = models.CharField(verbose_name="Отчество",max_length=255, null=True , blank=True)
    date_of_birth =  models.DateField(verbose_name="Дата рождения", null=True )
    status = models.CharField(verbose_name="Статус",max_length=255, null=True )
    image = models.FileField(verbose_name="Фото", upload_to="media/user/", default="/media/user/userimage.png")
    number = models.CharField(verbose_name="Номер телефона",max_length=255, null=True )
    country = models.CharField(verbose_name="Страна",max_length=255, null=True )
    city = models.CharField(verbose_name="Город",max_length=255, null=True )
    def __str__(self):
        return str(self.user.email)
    
    class Meta:
        verbose_name = "Информация о пользователе"
        verbose_name_plural = "Информация о пользователях"

class Napravlenii(models.Model):
    icon = models.FileField(verbose_name="Фото",upload_to="media/courses", null=True )
    name = models.CharField(verbose_name="Наименование направления",max_length=255, null=True )
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"

class Courses(models.Model):
    name = models.CharField(verbose_name="Наименование курса",max_length=255, null=True )
    photo = models.FileField(verbose_name="Изображение",upload_to="media/napravlenii", null=True )
    level= models.CharField(verbose_name="Уровень",max_length=255, null=True )
    reiting = models.IntegerField(verbose_name="Рейтинг", null=True )
    napravlenii = models.ForeignKey(Napravlenii,on_delete=models.SET_NULL, verbose_name="Направление", null=True )
    status = models.CharField(verbose_name="Статус",max_length=255, null=True )
    price = models.IntegerField(verbose_name="Цена", null=True )
    info_url = models.CharField(verbose_name="Ссылка на ознакомление",max_length=255, null=True )
    
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = "Курсы"
        verbose_name_plural = "Курсы"

class Zapis(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь",  on_delete=models.CASCADE, null=True, related_name="user_zapis")
    napravlenie = models.OneToOneField(Courses,on_delete=models.SET_NULL, verbose_name="Курсы", null=True )
    datetime = models.DateTimeField(verbose_name="Дата и время записи",  null=True, blank=True)
    email = models.CharField(verbose_name="E_MAIL",max_length=255, null=True )
    number = models.CharField(verbose_name="Номер телефона",max_length=255, null=True )
    def __str__(self):
        return "Запись студента: " + self.user.email + "___ на курс: " + self.napravlenie.name
    
    class Meta:
        verbose_name = "Заявки на курсы"
        verbose_name_plural = "Заявки на курсы"

class Mentors(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor')
    
    def __str__(self):
        return str(self.mentor)
    class Meta:
        verbose_name = "Ментор"
        verbose_name_plural = "Менторы"

class Courses_Of_User(models.Model):
    student = models.ForeignKey(User, verbose_name="Обучающийся",  on_delete=models.CASCADE, null=True, related_name="student_courses")
    teacher = models.ForeignKey(Mentors,verbose_name="Ментор", on_delete=models.CASCADE, null=True, related_name="teacher_courses")
    courses = models.ForeignKey(Courses,on_delete=models.CASCADE, verbose_name="Курсы", null=True, related_name="user_course")
    date_start = models.DateField(verbose_name="Дата начала", null=True, blank=True)
    sertificate = models.FileField(verbose_name="Сертификат",upload_to="media/sertificate", null=True, blank=True)
    status = models.CharField(verbose_name="Статус(В процессе / Пройден)",max_length=255, null=True, blank=True )
    def __str__(self):
        return  self.courses.name + "____ Студент: " + self.student.first_name + "____ Ментор: "+ str(self.teacher.mentor)
    
    class Meta:
        verbose_name = "Курсы пользователя"
        verbose_name_plural = "Курсы пользователей"

class Themes(models.Model):
    title = models.CharField(verbose_name="Наименование темы",max_length=255, null=True )
    description = models.CharField(verbose_name="Описание",max_length=1000, null=True )
    napravlenie = models.ForeignKey(Courses,on_delete=models.SET_NULL, verbose_name="Курсы", null=True )
    teacher = models.ForeignKey(Mentors,verbose_name="Ментор", on_delete=models.CASCADE, null=True, related_name="teacher_themes")
    def __str__(self):
        return str(self.title) + "____ " + str(self.napravlenie.name)
    
    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Progress(models.Model):
    course_of_user = models.ForeignKey(Courses_Of_User,on_delete=models.SET_NULL, verbose_name="Курсы", null=True )
    themes = models.ForeignKey(Themes,on_delete=models.SET_NULL, verbose_name="Тема", null=True )
    answer = models.CharField(verbose_name="Ответ",max_length=255, null=True )
    ocenka = models.CharField(verbose_name="Оценка",max_length=255, null=True )
    status = models.CharField(verbose_name="Статус(В процессе / Пройден)",max_length=255, null=True )
    def __str__(self):
        return str(self.course_of_user.student.email) + "____"+ str(self.themes)
    
    class Meta:
        verbose_name = "Прогресс"
        verbose_name_plural = "Прогрессы"

class Files(models.Model):
    file = models.FileField(verbose_name="Файлы по теме",upload_to="media/themes", null=True )
    themes = models.ForeignKey(Themes,on_delete=models.SET_NULL, verbose_name="Тема", null=True )
    
    def __str__(self):
        return str(self.themes)
    
    class Meta:
        verbose_name = "Файлы по теме"
        verbose_name_plural = "Файлы по темам"


# class Chat(models.Model):
#     student = models.OneToOneField(User, verbose_name="Обучающийся", on_delete=models.CASCADE, null=True, related_name="student_chat_courses")
#     teacher = models.OneToOneField(User, verbose_name="Ментор", on_delete=models.CASCADE, null=True, related_name="teacher_chat_courses")
#     courses = models.ForeignKey(Courses,on_delete=models.SET_NULL, verbose_name="Курсы", null=True )
#     def __str__(self):
#         return str(self.courses)
    
#     class Meta:
#         verbose_name = "Чат"
#         verbose_name_plural = "Чат"

# class Messengers(models.Model):
#     user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True, related_name="user_messenge")
#     chat = models.ForeignKey(Chat,verbose_name="Чат", on_delete=models.SET_NULL,  null=True )
#     messenges = models.CharField(verbose_name="Сообщение",max_length=255, null=True )
#     def __str__(self):
#         return str(self.user.email)
    
#     class Meta:
#         verbose_name = "Сообщение"
#         verbose_name_plural = "Сообщения"

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    theme = models.ForeignKey(Themes, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} in {self.theme.title}"
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"




class ZapisMentors(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='mentorzapis')
    course = models.OneToOneField(Courses,on_delete=models.SET_NULL, verbose_name="Курсы", null=True, blank=True )
    addnewcourse = models.CharField(verbose_name="Предложение на добавление нового курса",max_length=255, null=True, blank=True )
    datetime = models.DateTimeField(verbose_name="Дата и время записи",  null=True, blank=True)
    email = models.CharField(verbose_name="E_MAIL",max_length=255, null=True )
    number = models.CharField(verbose_name="Номер телефона",max_length=255, null=True )
    def __str__(self):
        return "Заявка  пользователя: " + str(self.user.email) 
    class Meta:
        verbose_name = "Заявка на ментора"
        verbose_name_plural = "Заявки на ментора"