from django import forms
from planner.models import Page, Category, UserProfile
from planner.models import Project, Feature, FeatureDetail, ChangeList
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name', 'views', 'likes')


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class ProjectForm(forms.ModelForm):
    name = forms.CharField(max_length=128, label="Project Name")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Project
        fields = ('name', 'likes')

class FeatureForm(forms.ModelForm):
    name = forms.CharField(max_length=128, label="Feature Name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Feature

        exclude = ("project", "pid")
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')        

class FeatureDetailForm(forms.ModelForm):
    priority = forms.ChoiceField(choices=FeatureDetail.priority_choices, label="Priority")  
    sim_req = forms.CharField(max_length=128, label="Simulation Requirement", required=False)
    seq_req = forms.CharField(max_length=128, label="Sequence Requirement", required=False)
    check_desp = forms.CharField(max_length=128, label="Checking Description", required=False)
    func_cov_req = forms.CharField(max_length=128, label="Func Cov Requirement", required=False)
    measure_src = forms.CharField(widget=forms.Textarea, label="Measure Source", required=False)

    test_cov = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    line_cov = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    con_cov = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    toggle_cov = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    fsm_cov = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    branch_cov = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    assert_cov = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    func_cov = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = FeatureDetail

        exclude = ("test_cov", "line_cov", "toggle_cov", "fsm_cov", "branch_cov", "assert_cov", "func_cov")

class ChangeListForm(forms.ModelForm):
    comment = forms.CharField(max_length=128, label="Comment")

    class Meta:
        model = ChangeList
        exclude = ("name",)
