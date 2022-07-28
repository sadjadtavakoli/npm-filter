from os import walk
import json 

files_path = "./projects/"
projects = []


def filter():    
    file_names = next(walk(files_path), (None, None, []))[2]
    for f in file_names:
        file_path = files_path+f
        if(file_path.endswith("__results.json")):
            with open(file_path, 'r') as f:
                data = json.load(f)
                scritp_result = data.get('scripts_over_code', None)
                if(scritp_result):
                    output = scritp_result["/Users/sadjadtavakoli/University/lab/npm-filter/configs/get_rel_commits.sh"]['output']
                    length = len(output.split(","))
                    if(length>2):
                        project_link = data['metadata']['repo_link']
                        projects.append([project_link, length])
                        continue
                print(file_path)
                # os.remove(file_path)

    projects.sort(key=lambda x: x[1], reverse=True)
    sorted_json_data = json.dumps(projects) 

    with open('summary.json', 'w') as output:
        output.write(sorted_json_data)

def filter2():  
      
    f = open('./projects/react-nodejs-npm/summary.json')
    selected_projects = json.load(f)
    selected_projects_names = [project[0] for project in selected_projects]
    f = open('summary.json')
    all_projects = json.load(f)

    for project in all_projects:
        print(project[0])
        if project[0] in selected_projects_names:
            print("yes!")
            project.append("candidate")
    with open('summary.json', 'w') as output:
        output.write(json.dumps(all_projects))

