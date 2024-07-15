from api.ext.template.uniappTemplate import template,script
import re
import os

# 创建page页面
def create_page(data_list,all_subfolders,new_folder_name,tabbar_component):
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

