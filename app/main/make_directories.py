import os
from shutil import copyfile
from flask import request
from config import Config
from app.main.email import send_support_notification_email

ROOT_APP_DIR = Config.ROOT_APP_DIR
CLIENT_ROOT = Config.CLIENT_ROOT

def makeRootProjectPath(projectType, client, brand, solution, form):
    subDirList = []
    try:
        subDirCount = int(request.form.get('hiddenNum'))
        for i in range(subDirCount):
            subdirData = request.form.get('subdir' + str(i+1)).replace(" ", "_")
            if subdirData != "Animation":
                subDirList.append(subdirData)
            else:
                return None
    except:
        subDirCount = None
    if projectType == 'client_REPLACE':
        path = CLIENT_ROOT + "/" + client + "/" + brand + "/" + solution
    else:
        path = CLIENT_ROOT + "/" + projectType + "/" + client + "/" + brand + "/" + solution
    if subDirList:
        for subdir in subDirList:
                path += "/" + subdir
    return path

def getTemplateData(templatePath, projectCode):    
    templateData = []
    with open(templatePath, 'r') as file:
        for line in file:
            templateData.append(line.rstrip().replace("GENAC", projectCode))
    return templateData

def makeDirectories(user, projectPath, projectCode):
    user_agent = request.user_agent
    platform = user_agent.platform
    log = ["  "]    
    ''' Creates the directory structure for a Viscira project '''    
    folderTemplateData = getTemplateData(ROOT_APP_DIR + "/app/static/folderTemplate.txt", projectCode)
    fileTemplateData = getTemplateData(ROOT_APP_DIR + "/app/static/fileTemplate.txt", projectCode)
    for line in folderTemplateData:
        path = ((projectPath + line).lstrip().rstrip())
        previewpath = path
        if platform == 'windows':
            previewpath = path.replace("/mnt/optimus", "O:")
        if not os.path.exists(path):
            log.append( "Making directory: " + previewpath)
            os.makedirs(path)
            pass
    log.append("  ")
    for line in fileTemplateData:
        path = ((projectPath + line).lstrip().rstrip())
        if platform == 'windows':
            previewpath = path.replace("/mnt/optimus", "O:")
        log.append( "Moving files: " + ROOT_APP_DIR + "/app/static/project_files/" + line.split('/')[-1])
        log.append( "To: " + previewpath)
        log.append("  ")
        copyfile(ROOT_APP_DIR + "/app/static/project_files/" + line.split('/')[-1], path)    
    send_support_notification_email(user, projectPath, projectCode)
    return log
        
        
        
        
        
        
        
        
        

