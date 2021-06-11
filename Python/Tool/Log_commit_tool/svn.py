import subprocess
import os
import pathlib
import Download

def svn_commit():
    file_name = 'Apache-Subversion-1.13.0/bin'
    path = pathlib.Path().absolute()   # svn.pyのあるディレクトリ
    path /= '●●●●/'

    bin_path = os.path.join(path, file_name)

    environment_variable_list = []

    for environment_variable in os.environ['●●●'].split(";"):
        if file_name in os.environ.get('●●●') :
            pass
        else:
            os.environ['●●●'] += bin_path
    # print(os.environ['Path'])

    path /= '../'

    os.chdir(path)  # ディレクトリ移動
    
    subprocess.run('svn update', shell=True)
    subprocess.run(f'svn add {str(path) + "/" + Download.parent_folder} --force', shell=True)
    # subprocess.run('svn st', shell=True)
    subprocess.run(f'svn commit -m "{str(Download.webdav_folder) + "更新"}"')

if __name__ == '__main__':
    svn_commit()