from src.DevopsTfsApi import DevopsTfsApi

tfs = DevopsTfsApi(tfs_url='https://{instance}/', api_version='api-version=6.0')
collectionName='Dev_Collection'


projects = tfs.get_all_projects(collectionName)
for project in projects:
    file = open('D:/cikti/+' + project + '.txt', 'w', encoding="utf-8")
    builds = tfs.getListofBuilds(collectionName, project)
    for build in builds['value']:
        name = build['name']
        id = build['id']
        propertyBuilds = tfs.getPropertiesofBuilds(collectionName, project, build_id=id)
        try:
            phaseFF = propertyBuilds['process']['phases'][1]
            print(name)
            file.write("%s\n" % name)
        except():
            continue
file.close()
