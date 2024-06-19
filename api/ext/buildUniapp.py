import shutil
import os
import uuid
import re
from api.ext.buildUniappPage import create_page

def read_and_build_file(data_list):
    # 定义源文件夹的路径
    source_folder = 'buildCode/uniCodeTemplate/uni-app'
    folder_path = 'packages/'

    # 生成一个新的 UUID 作为文件夹名称的一部分
    new_folder_name = f"{uuid.uuid4().hex}_uni-app"
    # 构建新的目标文件夹路径
    target_folder = os.path.join('buildCode/DoneCode', new_folder_name)

    # 确保目标文件夹不存在，因为 copytree() 要求目标文件夹不存在
    if os.path.exists(target_folder):
        raise FileExistsError(f"Target folder {target_folder} already exists")

    # 复制整个文件夹
    shutil.copytree(source_folder, target_folder)
    
    # 根据 json id 获取组件
    for item in data_list:
        if(item['id'].split('-')[0]):
            # 获取所有子文件夹
            all_subfolders = get_subfolders(folder_path)
            for subfolder in all_subfolders:
                # 根据id 复制组件
                if(item['id'].split('-')[0] == subfolder.split('/')[-2]):
                    copyPackage(subfolder.replace("/index.vue", ""),new_folder_name)
    
    # 创建page页面
    create_page(data_list)

    return new_folder_name

# 获取所有文件夹路径
def get_subfolders(folder_path):
    vue_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('index.vue'):
                vue_files.append(os.path.join(root, file))
    return vue_files

# 根据id复制组件文件
def copyPackage(subfolder,new_folder_name):
    if(check_file_exists(f'buildCode/DoneCode/{new_folder_name}/src/{subfolder}')):
        return
    else:
        copy_directory_with_exclusion(subfolder, f'buildCode/DoneCode/{new_folder_name}/src/{subfolder}')
        # 复制文件结束后需要进行条件编译
        content = ''
        pattern = r'// ?IF EDITOR[\s\S]*?// ?END EDITOR'
        with open(f'buildCode/DoneCode/{new_folder_name}/src/{subfolder}/index.vue', 'r+',encoding="utf-8") as file:
            content = file.read()
        processed_content = re.sub(pattern, "\n", content, flags=re.DOTALL)
        with open(f'buildCode/DoneCode/{new_folder_name}/src/{subfolder}/index.vue', "w", encoding="utf-8") as file:
            file.write(processed_content)
    
# 检查文件是否存在
def check_file_exists(file_path):
    return os.path.exists(file_path)
# 复制文件
def copy_directory_with_exclusion(src, dst):
    # 需要排除的文件
    exclude_files=['data.tsx']
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        src_item_path = os.path.join(src, item)
        dst_item_path = os.path.join(dst, item)

        if item in exclude_files:
            continue

        if os.path.isfile(src_item_path):
            shutil.copy2(src_item_path, dst_item_path)
        elif os.path.isdir(src_item_path):
            copy_directory_with_exclusion(src_item_path, dst_item_path, exclude_files)

