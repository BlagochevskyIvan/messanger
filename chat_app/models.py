from django.db import models
from user_app.models import User


class DiaCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} ({self.id})'


class TypeMessage(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} ({self.id})'

class Dialog(models.Model):
    category = models.ForeignKey(to = DiaCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars_dialog', default='default.png')

    def __str__(self):
        return f'{self.id}. Категория: {self.category.name}. Название: {self.name}'
    
    def get_name(self):
        if self.category_id == 1:
            print(Member.objects.filter(dialog  = self))
        else:
            print(self.name)


class Message(models.Model):
    type_message = models.ForeignKey(to = TypeMessage, on_delete=models.CASCADE) 
    text = models.CharField(max_length=5000, null=True, blank=True)
    attached_photo = models.ImageField(null=True, blank=True ,upload_to='dialog_images')
    attached_file = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    author = models.ForeignKey(to = User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}. Тип: {self.type_message}. Автор: {self.author} Текст {self.text}'


class Member(models.Model):
    dialog = models.ForeignKey(to=Dialog, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}. Пользователь: {self.user}. Диалог: {self.dialog}'
    

class Content(models.Model):
    dialog = models.ForeignKey(to=Dialog, on_delete=models.CASCADE)
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)

    @property
    def dialog_info(self):
        dia = Dialog.objects.get(id=self.dialog_id)
        return dia
