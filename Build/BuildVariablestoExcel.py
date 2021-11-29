from src.DevopsTfsApi import DevopsTfsApi
from JsonFile import jsonTask
import csv

tfs = DevopsTfsApi(tfs_url="https://{instance}/", api_version='api-version=6.1')

collection = ['Default_Collection','External_Collection']

file = csv.writer(open('D:/Repos/variables2.csv', 'w', encoding='utf16'), delimiter='\t', lineterminator='\n')
file.writerow(["Collection Name", "Project Name", "Build Name", "Build ID", "FortifyProject","TeamEmail", "TeamID"])
for coll in collection:
    projects = tfs.get_all_projects(collection_name=coll)
    for project in projects['value']:
        projName = project['name']
        builds =tfs.getAllBuilds(collection_name=coll, project_name=projName)
        for build in builds["value"]:
            buildid = build["id"]
            buildName = build["name"]
            if "FF" in buildName:
                buildDefinitionDetails = tfs.getPropertiesofBuilds(collection_name=coll, project_name=projName, build_id=buildid)
                variables = buildDefinitionDetails["variables"]
                try:
                    if "FortifyProject" in variables:
                        if "TeamEmail" and "TeamID" not in variables:
                            FortifyProject = variables["FortifyProject"]
                            TeamEmail = "empty"
                            TeamID = "empty"
                            lines = (coll, projName, buildName, buildid, FortifyProject['value'], TeamEmail['value'], TeamID['value'])
                            file.writerow(lines)
                            print(FortifyProject['value'],TeamEmail, TeamID)
                        elif "TeamEmail" and "TeamID" in variables:
                            FortifyProject = variables["FortifyProject"]
                            TeamEmail= variables["TeamEmail"]
                            TeamID = variables["TeamID"]
                            lines = (coll, projName, buildName, buildid, FortifyProject['value'], TeamEmail['value'], TeamID['value'])
                            file.writerow(lines)
                            print(FortifyProject['value'], TeamEmail['value'], TeamID['value'])
                except:
                    continue
            else:
                continue
