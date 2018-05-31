from django.db import models

# Create your models here.


class Cinema(models.Model):
    """影院表"""
    cinema_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    tel = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    score = models.FloatField(default=0)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.name


class Customer(models.Model):
    """顾客表"""
    username = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    gender_list = (
        (1, '男'),
        (0, '女'),
    )
    gender = models.IntegerField(choices=gender_list)
    age = models.IntegerField()
    password = models.CharField(max_length=50)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.username


class Employee(models.Model):
    """影院职工表"""
    username = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    gender_list = (
        (1, '男'),
        (0, '女'),
    )
    gender = models.IntegerField(choices=gender_list)
    age = models.IntegerField()
    password = models.CharField(max_length=50)
    cinema_id = models.ForeignKey(to='Cinema', to_field='cinema_id', on_delete=models.CASCADE)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.username


class Movie(models.Model):
    """电影表"""
    movie_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    length = models.IntegerField()
    type = models.CharField(max_length=50)
    director = models.CharField(max_length=50)
    score = models.FloatField(default=0)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.name


class Session(models.Model):
    """电影场次表"""
    session_id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey(to='Movie', to_field='movie_id', on_delete=models.CASCADE)
    house_id = models.ForeignKey(to='House', to_field='house_id', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    date = models.DateField()
    time = models.TimeField()
    price = models.FloatField()

    def __str__(self):
        """返回模型的字符串表示"""
        return str(self.session_id)


class House(models.Model):
    """放映厅表"""
    house_id = models.AutoField(primary_key=True)
    cinema_id = models.ForeignKey(to='Cinema', to_field='cinema_id', on_delete=models.CASCADE)
    house_name = models.CharField(max_length=50)
    house_type = models.ForeignKey(to='House_all', to_field='house_type', on_delete=models.CASCADE)

    class Meta:
        unique_together = (("cinema_id", "house_name"),)

    def __str__(self):
        """返回模型的字符串表示"""
        return str(str(self.cinema_id) + '_' + self.house_name)


class House_all(models.Model):
    """不同类型的放映厅表"""
    house_type = models.CharField(max_length=10, primary_key=True)
    rows = models.IntegerField()
    columns = models.IntegerField()

    def __str__(self):
        """返回模型的字符串表示"""
        return self.house_type


class Order(models.Model):
    """订单表"""
    order_id = models.AutoField(primary_key=True)
    session_id = models.ForeignKey(to='Session', to_field='session_id', on_delete=models.CASCADE)
    username = models.ForeignKey(to='Customer', to_field='username', on_delete=models.CASCADE)
    time = models.IntegerField()
    seat_row = models.IntegerField()
    seat_column = models.IntegerField()
    status = models.IntegerField()
    price = models.FloatField()

    class Meta:
        unique_together = (("session_id", "username", "time", "seat_row", "seat_column"),)

    def __str__(self):
        """返回模型的字符串表示"""
        return str(str(self.session_id) + '_' + str(self.username))


class Cinema_comment(models.Model):
    """电影院表"""
    cinema_id = models.ForeignKey(to='Cinema', to_field='cinema_id', on_delete=models.CASCADE)
    username = models.ForeignKey(to='Customer', to_field='username', on_delete=models.CASCADE)
    comment = models.TextField()
    score_list = (
        (1.0, '1'),
        (2.0, '2'),
        (3.0, '3'),
        (4.0, '4'),
        (5.0, '5'),
        (6.0, '6'),
        (7.0, '7'),
        (8.0, '8'),
        (9.0, '9'),
        (10.0, '10'),
    )
    score = models.FloatField(choices=score_list)

    class Meta:
        unique_together = (("cinema_id", "username"),)

    def __str__(self):
        """返回模型的字符串表示"""
        return str(str(self.username) + '_' + str(self.cinema_id))


class Movie_comment(models.Model):
    """电影院表"""
    movie_id = models.ForeignKey(to='Movie', to_field='movie_id', on_delete=models.CASCADE)
    username = models.ForeignKey(to='Customer', to_field='username', on_delete=models.CASCADE)
    comment = models.TextField()
    score_list = (
        (1.0, '1'),
        (2.0, '2'),
        (3.0, '3'),
        (4.0, '4'),
        (5.0, '5'),
        (6.0, '6'),
        (7.0, '7'),
        (8.0, '8'),
        (9.0, '9'),
        (10.0, '10'),
    )
    score = models.FloatField(choices=score_list)

    class Meta:
        unique_together = (("movie_id", "username"),)

    def __str__(self):
        """返回模型的字符串表示"""
        return str(str(self.username) + '_' + str(self.movie_id))


