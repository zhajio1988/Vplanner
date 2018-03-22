from django.contrib import admin
from planner.models import Image, Category, Page, UserProfile
from planner.models import Project, Feature, FeatureDetail, ChangeList

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class FeatureAdmin(admin.ModelAdmin):
    pass    

class FeatureDetailAdmin(admin.ModelAdmin):
    pass

class ChangeListAdmin(admin.ModelAdmin):
    pass    

#admin.site.register(Category)
admin.site.register(Category, CategoryAdmin)
#admin.site.register(Page)
admin.site.register(Page, PageAdmin)
admin.site.register(Image)
admin.site.register(UserProfile)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(FeatureDetail, FeatureDetailAdmin)
admin.site.register(ChangeList, ChangeListAdmin)
