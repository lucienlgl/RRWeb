from django.db import models


class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True, null=False)
    name = models.CharField(max_length=255)
    review_count = models.IntegerField(default=0, null=False)
    yelping_since = models.DateField()
    useful = models.IntegerField(default=0, null=False)
    funny = models.IntegerField(default=0, null=False)
    cool = models.IntegerField(default=0, null=False)
    fans = models.IntegerField(default=0, null=False)
    compliment_hot = models.IntegerField(default=0, null=False)
    compliment_more = models.IntegerField(default=0, null=False)
    compliment_profile = models.IntegerField(default=0, null=False)
    compliment_cute = models.IntegerField(default=0, null=False)
    compliment_list = models.IntegerField(default=0, null=False)
    compliment_note = models.IntegerField(default=0, null=False)
    compliment_plain = models.IntegerField(default=0, null=False)
    compliment_cool = models.IntegerField(default=0, null=False)
    compliment_funny = models.IntegerField(default=0, null=False)
    compliment_writer = models.IntegerField(default=0, null=False)
    compliment_photos = models.IntegerField(default=0, null=False)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.id


class Restaurant(models.Model):
    id = models.CharField(max_length=50, primary_key=True, null=False)
    name = models.CharField(max_length=255, null=False)
    neighborhood = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    stars = models.FloatField()
    review_count = models.IntegerField(default=0)
    is_open = models.BooleanField()

    class Meta:
        db_table = "restaurants"

    def __str__(self):
        return self.id


class Tip(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    text = models.TextField()
    date = models.DateField()
    likes = models.IntegerField()

    class Meta:
        db_table = "tip"

    def __str__(self):
        return str(self.id)


class Review(models.Model):
    id = models.CharField(max_length=50, primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    stars = models.IntegerField()
    date = models.DateField()
    text = models.TextField()
    useful = models.IntegerField()
    funny = models.IntegerField()
    cool = models.IntegerField()

    class Meta:
        db_table = "review"

    def __str__(self):
        return self.id


class Photo(models.Model):
    id = models.CharField(max_length=50, primary_key=True, null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    caption = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

    class Meta:
        db_table = "photo"

    def __str__(self):
        return str(self.id)


class Hours(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    day = models.CharField(max_length=50)
    hours = models.CharField(max_length=50)

    class Meta:
        db_table = "hours"

    def __str__(self):
        return str(self.id)


class Friend(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    friend_id = models.CharField(max_length=50)

    class Meta:
        db_table = "friend"

    def __str__(self):
        return str(self.id)


class Elite(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    year = models.CharField(max_length=4)

    class Meta:
        db_table = "elite"

    def __str__(self):
        return str(self.id)
