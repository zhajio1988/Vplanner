from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse, resolve 
from django.utils.six.moves.urllib.parse import urlparse
from django.template import Context, Template, RequestContext
from planner.models import Category, Page, UserProfile, ModelToJson
from planner.models import Project, Feature, FeatureDetail, ChangeList
from planner.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from planner.forms import ProjectForm, FeatureForm, FeatureDetailForm, ChangeListForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from urllib import request, parse
import json
# Create your views here.

def index(request):
    category_like_list = Category.objects.order_by('-likes')[:3]
    category_view_list = Category.objects.order_by('-views')[:3]
    context_dict = {'categories_likes': category_like_list,
                    'categories_views': category_view_list,
                    }

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        #if (datetime.now() - last_visit_time).days > 0:
        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits
    response = render(request,'planner/index.html', context_dict)
    return response

def about(request):
    context_dict = {'editor_name': "Verilog/SystemVerilog mode test"}
    return render(request, 'planner/about.html', context_dict)

def project(request, project_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our baidu function to get the results list!
            result_list = baidu_search(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        project =Project.objects.get(slug=project_name_slug)
        context_dict['project_name'] = project.name
        features = Feature.objects.filter(project=project).order_by('-views')
        context_dict['features'] = features
        context_dict['project'] = project
    except project.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = project.name

    return render(request, 'planner/project.html', context_dict)

def add_project(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print (form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = ProjectForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'planner/add_project.html', {'form': form})

#post = get_object_or_404(Question, pk=pk)
#form = QuestionForm(instance=post)
#return render(request, 'qs/edit.html', {'form': form})

def feature(request, project_name, feature_pk):
    context_dict = {}

    try:
        project =Project.objects.get(slug=project_name)
        context_dict['project'] = project
        feature = Feature.objects.filter(project=project, pk=feature_pk)
        #feature_detail=FeatureDetail.objects.filter(feature=feature)
        feature_detail=get_object_or_404(FeatureDetail, feature=feature)
        context_dict['feature'] = feature[0]
        form = FeatureDetailForm(instance=feature_detail)
        context_dict['form'] = form
    except project.DoesNotExist or feature.DoesNotExist or feature_detail.DoesNotExist:
        pass

    return render(request, 'planner/feature.html', context_dict)

def add_page(request, project_name_slug):
    try:
        cat = Project.objects.get(slug=project_name_slug)
    except Project.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = FeatureForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.project = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                redirect_url = reverse('project', args=[project_name_slug])
                return HttpResponseRedirect(redirect_url)
                #return category(request, category_name_slug)
        else:
            print ('debug point0', form.errors)
    else:
        form = FeatureForm()

    context_dict = {'form':form, 'project': cat}

    return render(request, 'planner/add_page.html', context_dict)

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__startswith=starts_with)
    else:
        cat_list = Category.objects.all()

    if max_results > 0:
        if (len(cat_list) > max_results):
            cat_list = cat_list[:max_results]

    for cat in cat_list:
        cat.url = encode_url(cat.name)
    
    return cat_list

@login_required
def profile(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {'cat_list': cat_list}
    u = User.objects.get(username=request.user)
    
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None
    
    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('planner/profile.html', context_dict, context)

def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'planner/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/planner/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'planner/login.html', {})

@login_required
def restricted(request):
    #return HttpResponse("Since you're logged in, you can see this text!")    
    return render(request, 'planner/restricted.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/planner/')

def track_url(request):
    feature_id = None
    url = '/planner/'
    if request.method == 'GET':
        if 'feature_id' in request.GET:
            feature_id = request.GET['feature_id']
            try:
                feature = Feature.objects.get(id=feature_id)
                feature.views = feature.views + 1
                feature.save()
                #url = page.url
            except:
                pass

    return HttpResponseRedirect(url)


def baidu_search(keyword):
    results = []
    query = {'wd': keyword, "pn": "0", "rn": "50", "tn" : "json"}
    result= request.urlopen("http://www.baidu.com/s?"+ parse.urlencode(query))
    response = result.read().decode('utf-8')
    json_response = json.loads(response)    
    f = open("json_log", "w")
    for result in json_response['feed']['entry']:
        if "title" in result:
            #print (result['title'])
            #print (result['url'])
            #print (result['abs'])
            results.append({
            'title': result['title'],
            'link': result['url'],
            'summary': result['abs']})
    return results

@login_required
def like_project(request):
    project_id = None
    if request.method == 'GET':
        project_id = request.GET['project_id']

    likes = 0
    if project_id:
        project = Project.objects.get(id=int(project_id))
        if project:
            likes = project.likes + 1
            project.likes = likes
            project.save()

    return HttpResponse(likes)

def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    cat_list = get_category_list(5, starts_with)

    return render(request, 'planner/cats.html', {'cats': cat_list })

@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category, title=title, url=url)

            pages = Page.objects.filter(category=category).order_by('-views')

            # Adds our results list to the template context under name pages.
            context_dict['pages'] = pages
            context_dict['category'] = category
            context_dict['category_name'] = category.name

    return render(request, 'planner/category.html', context_dict)

@login_required
def review(request, project_name):
    #ModelToJson(project_name)
    try:
        project = Project.objects.get(slug=project_name)
    except Project.DoesNotExist:
        project = None

    context_dict = {'project': project}

    return render(request, 'planner/review.html', context_dict)

@login_required
def getzTreeNodes(request):
    if request.method == 'GET':
        project_name = request.GET['project_name']
        return HttpResponse(zTreeContent(project_name), content_type='application/json')

def zTreeContent(project_name_slug):
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
    return json.dumps(json_data, indent=2)

@login_required
def get_tree_node_content(request):
    context_dict = {}
    
    if request.method == 'GET':
        project_name = request.GET['project_name']
        feature_id = request.GET['feature_id']
        try:
            project =Project.objects.get(slug=project_name)
            context_dict['project'] = project
            feature = Feature.objects.filter(project=project, id=feature_id)
            feature_detail=get_object_or_404(FeatureDetail, feature=feature)
            context_dict['feature'] = feature[0]
            form = FeatureDetailForm(instance=feature_detail)
            context_dict['form'] = form
        except project.DoesNotExist or feature.DoesNotExist or feature_detail.DoesNotExist:
            pass

    return render(request, 'planner/ztree_node_content.html', context_dict)
