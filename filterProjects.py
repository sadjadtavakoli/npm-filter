from os import walk
import json 

files_path = "./projects/react-nodejs-npm-projects/"
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
                    if(length<140):
                        project_link = data['metadata']['repo_link']
                        projects.append([project_link, length])
                        continue
                # print(file_path)

    projects.sort(key=lambda x: x[1], reverse=True)
    sorted_json_data = json.dumps(projects) 

    with open('./projects/react-nodejs-npm-details/summary_probably_pure_js.json', 'w') as output:
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


def extract_candidates_info():  
    f = open('./projects/react-nodejs-npm-details/summary_previously_eliminated.json')
    projects = json.load(f)
    candidate_projects = [project for project in projects if len(project)>2]
    candiate_projects_info = []
    for f in candidate_projects:
        candidate = {'repo':"git@github.com:"+f[0].split('github.com/')[-1]+".git" }
        f_name = f[0].split('/')[-1]
        file_path = files_path+f_name+"__results.json"
        with open(file_path, 'r') as file:
            data = json.load(file)
            scritp_result = data.get('installation', None)
            if(scritp_result):
                installer_command = scritp_result.get('installer_command', None)
                candidate['install'] = installer_command
        candiate_projects_info.append(candidate)

    with open('candidates_info_previously_eliminated.json', 'w') as output:
        output.write(json.dumps(candiate_projects_info))


def mohammad_projects_link_generator():

    projects = []
    with open('./projects_data/mohammad_mocha.txt') as f:
        lines = f.readlines()
        for line in lines:
            projects.append("github.com/"+line.split(",")[0])
    with open('./projects_data/mohammad_mocha_links.json', 'w') as output:
        output.write(json.dumps(projects))

extract_candidates_info()