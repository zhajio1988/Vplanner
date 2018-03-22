from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import json
from django.core import serializers
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder, Serializer
from django.utils.encoding import force_text
import django.utils.timezone as timezone
from django.core.validators import MaxValueValidator

# Create your models here.

class CategoryManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Category(models.Model):
    objects = CategoryManager()
    name = models.CharField(max_length=128, unique=True)
    #name = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name

class CategoryEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, Category):  
            print("debug point0\n", obj.name, obj.views, obj.likes)
            return [obj.name, obj.views, obj.likes]
        return json.JSONEncoder.default(self, obj)

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        self.ToJson()
        super(Page, self).save(*args, **kwargs) 

    def ToJson(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
    
        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)
            print (attr, d[attr])
        with open('page.json', 'a') as outfile:
            print ("debug point1\n", d)
            json.dump(d, outfile, indent=4, cls=CategoryEncoder)

class Image(models.Model):
    image = models.ImageField(max_length=100, upload_to="image/%Y/%m", default=u"image/default.png", verbose_name=u'logo')

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

#class LazyEncoder(DjangoJSONEncoder):
#    def default(self, obj):
#        if isinstance(obj, Category):
#            return [obj.name, obj.views, obj.likes]
#        return super(LazyEncoder, self).default(obj)

#def ModelToJson(category_name_slug):
#    JSONSerializer = serializers.get_serializer("json")
#    json_serializer = JSONSerializer()
#    category = Category.objects.get(slug=category_name_slug)
#    with open("category.json", "w") as out:
#        json_serializer.serialize(Page.objects.filter(category=category), stream=out, indent=4, use_natural_foreign_keys=True)
#

class Project(models.Model):
    name = models.CharField(max_length=128, unique=True)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()
    pid = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.likes < 0:
            self.likes = 0
        self.slug = slugify(self.name)
        self.pid = 0;
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class AbstractFeature(models.Model):  
    parent_feature = models.ForeignKey('self', blank=True, null=True, related_name='child_set')  
    class Meta:  
        abstract = True

class Feature(AbstractFeature):
    project = models.ForeignKey(Project, related_name='project_set')
    name = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    pid = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.parent_feature:
            self.pid = self.parent_feature.id
            self.project = self.parent_feature.project
            if not "." in self.name:
                self.name = self.parent_feature.name + "." + self.name
        else:
            self.pid = self.project.id
            if not "." in self.name:
                self.name = self.project.name + "." + self.name
        super(Feature, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class FeatureDetail(models.Model):
    feature = models.OneToOneField(Feature)
    priority_choices = (
        ('p1', 'P1'),
        ('p2', 'P2'),
        ('p3', 'P3'),
    )
    priority = models.CharField(max_length=10, choices=priority_choices, default='p1')
    sim_req = models.CharField(max_length=128, verbose_name='Simulation Requirement')
    seq_req = models.CharField(max_length=128, verbose_name='Sequence Requirement')
    check_desp = models.CharField(max_length=128, verbose_name='Checking Description')
    func_cov_req = models.CharField(max_length=128, verbose_name='Func Cov Requirement')
    measure_src = models.TextField(verbose_name='Measure Source')

    test_cov = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name='Testcase Coverage')    
    line_cov = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name='Line Coverage')
    con_cov = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name='Conditional Coverage')    
    toggle_cov = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name='Toggle Coverage')
    fsm_cov = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name='FSM Coverage')    
    branch_cov = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name='Branch Coverage')    
    assert_cov = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name='Assertion Coverage')    
    func_cov = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name='Functional Coverage')

    def __str__(self):
        return self.feature.name

class ChangeList(models.Model):
    feature= models.ForeignKey(Feature)
    name = models.CharField(max_length=128, default=feature.name, verbose_name='feature name')
    user = models.CharField(max_length=128, verbose_name='change by whom')
    comment = models.CharField(max_length=128, verbose_name='change comments')
    content = models.TextField(verbose_name='change content')
    date_record = models.DateTimeField(default = timezone.now, verbose_name="lastest modify date")

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.feature.name 
        super(ChangeList, self).save(*args, **kwargs)

    def __str__(self):
        return self.feature.name

def ModelToJson(project_name_slug):
    json_data=[]
    result = {}
    project = Project.objects.get(slug=project_name_slug)
    result["id"] = project.id 
    result["pID"] = project.pid 
    result["name"] = project.name
    result["open"] = True
    json_data.append(result)

    for feature in Feature.objects.filter(project=project):
        result = {}
        if (len(feature.child_set.all())) > 0:
            result["open"] = True
        result["id"] = feature.id 
        result["pId"] = feature.pid 
        result["name"] = feature.name.split(".")[-1]
        json_data.append(result)

    json_indent_data = json.dumps(json_data, indent=2)
    print(json_indent_data)
