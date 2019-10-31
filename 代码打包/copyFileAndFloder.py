#  文件打包器
'''
1.列出一个文件夹(deplorePath)中所有的文件,按修改时间倒序;
2.选择你需要复制出来的一些文件;
3.将文件复制复制到目标(copyPath)文件夹下,并根据源地址创建相同文件夹
'''
import os
import time
import shutil
import platform
#  jboss  部署文件夹
deplorePath = "D:/javaTest/jboss-5.1.0.GA/server/default/deploy/"
#   文件打包的地方
copyPath = "E:/copyFiles/"
# 最新的50个文件
updateFilesLength = 50



def getFileAndUpdateTime(p):
    maps = {}
    iteers(p,maps)
    maps = sorted(maps.items(), key=lambda x: x[1],reverse=True)
    return maps[0:updateFilesLength]

def copyFils(old,newF):
    ndir = os.path.dirname(newF)
    if not os.path.exists(ndir):
        os.makedirs(ndir)
    shutil.copyfile(old, newF)


def iteers(path,atts):
    files= os.listdir(path)
    for file in files: #遍历文件夹
        if not os.path.isdir(path+"/"+file):
            try:
                mtime = os.stat(path+"/"+file).st_mtime
                file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))

                atts[path+"/"+file] = file_modify_time
            except Exception as e:
                pass
        else :
            if os.path.isdir(path+"/"+file):
                iteers(path+"/"+file,atts)

def main():
    wars = ["Admin.war","User.war","example.war"]
    for i,val in enumerate(wars):
        print("%d : %s " % (i,val))
    projectWars = input("请选择你要部署的项目/自己输入文件夹地址:")
    if projectWars.isnumeric() and int(projectWars) < len(wars) :
        projectWars = deplorePath+wars[int(projectWars)]
    listFils=getFileAndUpdateTime(projectWars)
    
    print("%-5s|%-40s|%-30s " % ('序号',"文件名","修改时间"))
    for j,val_j in enumerate(listFils):
        print("%-5s%-40s%-30s " % (j,val_j[0][val_j[0].rfind("/")+1:],val_j[1]))
    print(" 请选择要保存的文件: ")
    msg = """ 如:
                第5个: 5
                第5个和前3个 : 0-3,5
    """ 
    print(msg)
    num = input("请选择文件:")
    chooses = num.split(",")
    chooseFile = []
    for i in chooses:
        if i.find("-") > 0:
            splosts = i.split("-")
            chooseFile.extend(listFils[int(splosts[0]):int(splosts[1])+1])
        else:
            if i.isnumeric():
                chooseFile.append(listFils[int(i)])
    chooseFile = [i[0] for i in chooseFile]
    DirName = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    
    print("保存路径为文件夹名字为: %-10s" % copyPath+DirName)
    for i in chooseFile:
        copyFils(i,i.replace(deplorePath,copyPath+DirName+"/"))
    print(" 复制完成!")
    # sysstr = platform.system()
    # if(sysstr =="Windows"):
        # print(os.popen(" tree  %s  /F" % copyPath+DirName).read())
main()
exit(1)
