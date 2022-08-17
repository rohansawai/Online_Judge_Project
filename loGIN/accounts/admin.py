from django.contrib import admin

from accounts.models import Problem, Solution, TestCase, user_score

# Register your models here


admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(user_score)
admin.site.register(TestCase)
