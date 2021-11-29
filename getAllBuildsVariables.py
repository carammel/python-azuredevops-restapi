from src.DevopsTfsApi import DevopsTfsApi
import csv

tfs = DevopsTfsApi(tfs_url='https://{instance}/', api_version='api-version=6.0')
collectionName = 'Default_Collection'
project_Name = ['AI','Backend', 'Web']


file = csv.writer(open('D:/Repos/rapor/AzureDevopsBuildOpVariables.csv', 'w', encoding='utf16'), delimiter='\t', lineterminator='\n')
file.writerow(["Project Name","OP Build Name", "AppName", "ConfigFolder","PackageName", "TargetNamespace"])
#file = open('D:/cikti/AzureDevopsBuildOpVariables.txt', 'w', encoding="utf-8")
for pj in project_Name:
    builds = tfs.getListofBuilds(collectionName, pj)
    for build in builds['value']:
        name = build['name']
        id = build['id']
        if ".openshift" in name:
            bild = tfs.getPropertiesofBuilds(collectionName, project_name=pj, build_id=id)
            AppName = bild['variables']['AppName']['value']
            ConfigFolder = bild['variables']['ConfigFolder']['value']
            PackageName = bild['variables']['PackageName']['value']
            TargetNamespace = bild['variables']['TargetNamespace']['value']
            lines= (pj,name,AppName,ConfigFolder,PackageName,TargetNamespace)
            print(pj,name, AppName,ConfigFolder,PackageName,TargetNamespace)
            file.writerow(lines)
