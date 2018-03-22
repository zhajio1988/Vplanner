import os
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wplanner.settings')

import django
django.setup()

from planner.models import Project, Feature, FeatureDetail, ChangeList

def populate():
    ddr_proj = add_proj('ddrproj', 128)

    f1 = add_feature(proj=ddr_proj, name="feature1")

    f11 = add_sub_feature(f1, "sub1 clk and rst")
    f12 = add_sub_feature(f1, "sub1 rst")
    f13 = add_sub_feature(f1, "sub1 clk")

    p11 = add_feature_detail(f11, 'p1', "detail1 clk and rst", 10)
    p12 = add_feature_detail(f12, 'p2', "detail1 rst", 20)
    p13 = add_feature_detail(f13, 'p3', "detail1 clk", 30)

    add_change_list(f11, "jude", "sub1 test1")
    add_change_list(f12, "haha", "sub1 test2")
    add_change_list(f13, "hehe", "sub1 test3")

    f2 = add_feature(proj=ddr_proj, name="feature2")

    f21 = add_sub_feature(f2, "sub2 clk and rst")
    f22 = add_sub_feature(f2, "sub2 rst")
    f23 = add_sub_feature(f2, "sub2 clk")

    p21 = add_feature_detail(f21, 'p1', "detail2 clk and rst", 10)
    p22 = add_feature_detail(f22, 'p2', "detail2 rst", 20)
    p23 = add_feature_detail(f23, 'p3', "detail2 clk", 30)

    add_change_list(f21, "jude", "sub2 test1")
    add_change_list(f22, "haha", "sub2 test2")
    add_change_list(f23, "hehe", "sub2 test3")    

    f3 = add_feature(proj=ddr_proj, name="feature3") 

    f31 = add_sub_feature(f3, "sub3 clk and rst")
    f32 = add_sub_feature(f3, "sub3 rst")
    f33 = add_sub_feature(f3, "sub3 clk")

    p31 = add_feature_detail(f31, 'p1', "detail3 clk and rst", 10)
    p32 = add_feature_detail(f32, 'p2', "detail3 rst", 20)
    p33 = add_feature_detail(f33, 'p3', "detail3 clk", 30)

    add_change_list(f31, "jude", "sub3 test1")
    add_change_list(f32, "haha", "sub3 test2")
    add_change_list(f33, "hehe", "sub3 test3")
    time.sleep(3)
    add_change_list(f33, "haha", "sub3 test3")
    time.sleep(3)
    add_change_list(f32, "hehe", "sub3 test3")

def add_proj(name, views=0):
    c = Project.objects.get_or_create(name=name)[0]
    c.views = views
    c.save()
    return c

def add_feature(proj, name):
    p = Feature.objects.get_or_create(project=proj, name=name)[0]
    p.save()
    return p

def add_sub_feature(feature, name):
    p = Feature.objects.get_or_create(parent_feature=feature, name=name)[0]
    p.save()
    return p

def add_feature_detail(feature, priority, sim_req, test_cov=0):
    p = FeatureDetail.objects.get_or_create(feature=feature)[0]
    p.sim_req = sim_req
    p.priority = priority
    p.test_cov=test_cov
    p.save()
    return p

def add_change_list(feature, user, content):
    p = ChangeList.objects.get_or_create(feature=feature, user=user)[0]
    p.user=user
    p.content=content
    p.save()
    return p

# Start execution here!
if __name__ == '__main__':
    print ("Starting Planner population script...")
    populate()
