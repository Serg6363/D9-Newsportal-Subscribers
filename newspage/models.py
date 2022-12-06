from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self, update_rate):
        self.rating = update_rate
        self.save()

    def __str__(self):
        return '%s' % (self.user,)


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)
    user_subscriber = models.ManyToManyField(User, through='Subscriber')
    information = models.TextField(verbose_name='Описание категории')

    def __str__(self):
        return '%s' % (self.name_category,)


class Post(models.Model):
    news = 'N'
    article = 'A'

    type = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    type_post = models.CharField(max_length=1, choices=type, default=article, verbose_name='Тип публикации')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    time_write = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=False, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    rating = models.IntegerField(default=0)
    post_category = models.ManyToManyField(Category, through='Postcategory')

    def __str__(self):
        return '%s, %s' % (self.title, self.time_write,)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview_text = 124 if len(self.text) > 124 else len(self.text)
        return self.text[:preview_text]+'...'


class Postcategory(models.Model):
    name_post_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_write = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
