import os
import subprocess
import shlex
import pprint


def decomData(resultAR, enronFile, pathOutPut):
    cmd = 'awk \'$1~/^[0-9]+$/ {print $1}\' ' + resultAR + ' | uniq'
    # secList = os.popen(cmd).read().split('\n')
    secList = list(map(str, range(401, 3601)))
    for s in secList:
        if s == '':
            continue
        launchScript = '../scripts/decomData.sh 1 ' + enronFile + ' ' + pathOutPut + s + ' ' + s
        subprocess.call(shlex.split(launchScript))


def main():
    pathOutPutEnron = '../res/gen_enron/enron'
    enronResultAR = '../resultatsAntoinePartie/resultas_enron.txt'
    enronFile = '../res/enron/enronClean'

    pathOutPutRollernet = '../res/decoData/rollernet'
    rollernetResultAR = '../resultatsAntoinePartie/resultas_rollernet.txt'
    rollernetFile = '../res/rollernet/rollernetClean'

    # decomData(enronResultAR, enronFile, pathOutPutEnron)
    decomData(rollernetResultAR, rollernetFile, pathOutPutRollernet)


main()
