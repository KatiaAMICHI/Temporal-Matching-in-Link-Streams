import shlex, os
import subprocess

"""
Methos to generate data 
"""


def sortFileAR():
    pathF1 = '../res'

    for f1 in os.listdir(pathF1):
        pathF2 = pathF1 + "/" + f1

        if 'gen_B2' in pathF2 or 'gen_test' in pathF2:
            continue
        for f2 in os.listdir(pathF2):
            path = pathF2 + "/" + f2 + "/"

            if os.path.isdir(path):

                for file in os.listdir(path):
                    if file.endswith('.linkstream'):
                        print("******************************", file, "******************************")
                        fileOutput = file + 'AR'
                        cmd = 'cat ' + path + file + ' | sort  -b -u -nk2,2 -nk3,3 -nk1,1 | uniq >> ' + path + fileOutput
                        os.popen(cmd)


sortFileAR()
