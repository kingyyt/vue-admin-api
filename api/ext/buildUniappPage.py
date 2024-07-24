from api.ext.template.uniappTemplate import template,script,pagesJson,appVue,toPage,onLoad,methods,methodsNoTabbar
import re
import os
import shutil
import json


# 创建 pages.json App.vue toPage.js 及路由页面
def create_page(data_list,new_folder_name,data_tabbar,type,id):
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
    try:
    # 清空文件夹
        shutil.rmtree(f'buildCode/DoneCode/{new_folder_name}/src/pages/index')        
    except Exception as e:
            # 处理异常，例如记录日志或返回错误信息给用户
        pass
    
    # 创建文件夹
    create_url = f'buildCode/DoneCode/{new_folder_name}/src/pages/index'
    os.makedirs(create_url)

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
                    "navigationBarTitleText":tabbar[item]['name']
                }
            })
            create_single_page(tabbar[item]['json'],f'{create_url}/tabbar{str(item)}.vue',item,tabbar_type)

    else:
        pages_json['pages'].append({
            "path":f"pages/index/index",
            "style":{
                "navigationBarTitleText":data['name']
            }
        })
        create_single_page(data['json'],f'{create_url}/index.vue',0,tabbar_type)
    # writeFile(url,pages_json)

    with open(url, "w", encoding="utf-8") as f:
        json.dump(pages_json, f,ensure_ascii=False, indent=4)
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
        pages = pages + f'case "{tabbar[item]["name"]}":\nreturn "/pages/index/tabbar{item}"\n'
    result = re.sub(pattern, pages, toPage)
    writeFile(url,result)
# 创建page页面
def create_single_page(data,new_folder_name,index,tabbar_type):
    importText = ''
    templateText = ''
    componentText = ''
    dataText = ''
    for item in range(len(data)):
        componentName = f"{data[item]['id'].split('-')[0]}Component"
        componentHTML = f"{data[item]['id'].split('-')[0]}-component"
        # 生成import文本
        currentImport = f"import {componentName} from '@/packages/basic/{data[item]['id'].split('-')[0]}/index'"
        # 去重
        if not currentImport in importText:
            importText = f"{importText}\n{currentImport}"
            componentText = f"{componentText}\n{componentName},"
        # 生成templateText文本
        if tabbar_type == 'notTabbar':
            currentTemplateText = f'<{componentHTML} :props="tabbars[{item}].model" />'
            templateText = f"{templateText}\n{currentTemplateText}"
        else:
            currentTemplateText = f'<{componentHTML} :props="tabbars.tabbars.tabbars[{index}].json[{item}].model" />'
            templateText = f"{templateText}\n{currentTemplateText}"
        # data 文本
        dataText = f'tabbars:null,\n'
    if tabbar_type == 'tabbar':
        # import tabbar
        tabbarImport = f"import tabbarComponent from '@/packages/tabbar/index'"
        importText = f"{importText}\n{tabbarImport}"
        # com tabbar
        tabbarTemplateText = f'<tabbar-component :props="tabbars.tabbars" />'
        templateText = f"{templateText}\n{tabbarTemplateText}"
        componentText = f"{componentText}\ntabbarComponent,"


    build_template(new_folder_name,importText,templateText,componentText,dataText,tabbar_type)
    
# 拼接模版
def build_template(new_folder_name,importText,templateText,componentText,dataText,tabbar_type):
    templateTotleText = f"{replace_import('template',templateText,'')}\n{replace_import('import',importText,componentText,dataText,onLoad,methods)}\n"
    if tabbar_type == 'notTabbar':
        templateTotleText = f"{replace_import('template',templateText,'')}\n{replace_import('import',importText,componentText,dataText,onLoad,methodsNoTabbar)}\n"
    writeFile(new_folder_name,templateTotleText)

# 替换文本
def replace_import(type,text,text2='',text3='',onLoad='',methods=''):
    pattern = ""
    templateText = ""
    if type == 'import':
        pattern = r"\{\{\s*import\s*\}\}"
        pattern2 = r"\{\{\s*components\s*\}\}"
        pattern3 = r"\{\{\s*data\s*\}\}"
        pattern4 = r"\{\{\s*onLoad\s*\}\}"
        pattern5 = r"\{\{\s*methods\s*\}\}"
        templateText = re.sub(pattern5,methods,re.sub(pattern4,onLoad,re.sub(pattern3, text3, re.sub(pattern2, text2, script))))
    elif type == 'template':
        pattern = r"\{\{\s*template\s*\}\}"
        templateText = template

    result = re.sub(pattern, text, templateText)
    
    return result


