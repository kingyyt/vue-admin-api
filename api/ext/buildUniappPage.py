from api.ext.template.uniappTemplate import template,script,pagesJson,appVue,toPage
import re
import os
import shutil


# 创建 pages.json App.vue toPage.js 及路由页面
def create_page(data_list,all_subfolders,new_folder_name,data_tabbar,type,id):
    print(data_list,'------')
    print(data_tabbar)
    if "isUseTabbar" in data_tabbar and data_tabbar['isUseTabbar']:
        # pages.json
        create_pages_json(data_tabbar,'tabbar',new_folder_name)
        # App.vue 
        create_app_vue(id,new_folder_name)
        # toPage.js
        create_toPage_js(data_tabbar,new_folder_name)
    else:
        # pages.json
        create_pages_json(data_list,'notTabbar',new_folder_name)
        # App.vue 
        create_app_vue(id,new_folder_name)
        # toPage.js
        shutil.rmtree(f'buildCode/DoneCode/{new_folder_name}/src/utils')
        shutil.rmtree(f'buildCode/DoneCode/{new_folder_name}/src/packages/tabbar')
        
def writeFile(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(content)) 
 

def create_pages_json(data,tabbar_type,new_folder_name):
    url = f'buildCode/DoneCode/{new_folder_name}/src/pages.json'
    pages_json = {
        "pages":[],
        "globalStyle":pagesJson['globalStyle']
    }
    if tabbar_type == 'tabbar':
        tabbar = data['tabbars']['tabbars']
        for item in range(len(tabbar)):
            pages_json['pages'].append({
                "path":f"pages/index/tabbar"+str(item),
                "style":{
                    "navigationBarTitleText":tabbar[item]['pageName']
                }
            })
    else:
        pages_json['pages'].append({
            "path":f"pages/index/index",
            "style":{
                "navigationBarTitleText":"首页"
            }
        })
    writeFile(url,pages_json)
def create_app_vue(id,new_folder_name):
    url = f'buildCode/DoneCode/{new_folder_name}/src/App.vue'
    pattern = r"\{\{\s*id\s*\}\}"
    result = re.sub(pattern, str(id), appVue)
    writeFile(url,result)

def create_toPage_js(data_tabbar,new_folder_name):
    url = f'buildCode/DoneCode/{new_folder_name}/src/utils/toPage.js'
    pattern = r"\{\{\s*toPage\s*\}\}"
    tabbar = data_tabbar['tabbars']['tabbars']
    pages = ''
    for item in range(len(tabbar)):
        pages = pages + f'case "{tabbar[item]["pageName"]}":\nreturn "/page/index/tabbar{item}"\n'
    result = re.sub(pattern, pages, toPage)
    writeFile(url,result)
# 创建page页面
def create_single_page(data_list,all_subfolders,new_folder_name,data_tabbar,type):
    importText = ''
    templateText = ''
    componentText = ''
    for item in data_list:
        for subfolder in all_subfolders:
            # 根据id 复制组件
            if(item['id'].split('-')[0] == subfolder.split('/')[-2]):
                componentName = f"{item['id'].split('-')[0]}Component"
                componentHTML = f"{item['id'].split('-')[0]}-component"
                # 生成import文本
                currentImport = f"import {componentName} from '@/{subfolder}'"
                if not currentImport in importText:
                    importText = f"{importText}\n{currentImport}"
                    componentText = f"{componentText}\n{componentName},"
                # 生成templateText文本
                currentTemplateText = f'<{componentHTML} :props="{item["model"]}" />'
                templateText = f"{templateText}\n{currentTemplateText}"
    
    build_template(new_folder_name,importText,templateText,componentText)
    
# 拼接模版
def build_template(new_folder_name,importText,templateText,componentText):
    templateTotleText = f"{replace_import('template',templateText,'')}\n{replace_import('import',importText,componentText)}\n"
    with open(f"buildCode/DoneCode/{new_folder_name}/src/pages/index/index.vue", "w", encoding="utf-8") as f:
        f.write(templateTotleText)

# 替换文本
def replace_import(type,text,text2,text3=''):
    pattern = ""
    templateText = ""
    if type == 'import':
        pattern = r"\{\{\s*import\s*\}\}"
        pattern2 = r"\{\{\s*components\s*\}\}"
        pattern3 = r"\{\{\s*data\s*\}\}"
        templateText = re.sub(pattern3, text3, re.sub(pattern2, text2, script))
    elif type == 'template':
        pattern = r"\{\{\s*template\s*\}\}"
        templateText = template
    result = re.sub(pattern, text, templateText)
    
    return result


