from planner.models import AbstractFeature, Feature, FeatureDetail, ChangeList, Project
proj=Project(name="smmu", views=10)
proj.save()
f1 = Feature(project=proj, name="clk and rst")
f1.save()

f11 = Feature(project=proj,parent_feature=f1, name="clk")
f11.save()
f12 = Feature(project=proj,parent_feature=f1, name="rst")
f12.save()


fi11=FeatureItem(feature=f11, priority='P1',sim_req="sdfjksdhfjsdhfcxfjsdhfusdjf")
fi11.save()
op11=OperationLogs(feature=f11, user="jude", content="just for test")
op11.save()

fi12=FeatureItem(feature=f12, priority='P2',sim_req="sdfjksdhfjsdhfcxfjsdhfusdjf")
fi12.save()
op12=OperationLogs(feature=f12, user="jude", content="just for test1")
op12.save()
