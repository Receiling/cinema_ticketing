from django.contrib import admin
from ticketing.models import Cinema, Customer, Employee, Movie, Session, \
    House, House_all, Order, Cinema_comment, Movie_comment

# Register your models here.

admin.site.register(Cinema)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Movie)
admin.site.register(Session)
admin.site.register(House)
admin.site.register(House_all)
admin.site.register(Order)
admin.site.register(Cinema_comment)
admin.site.register(Movie_comment)
