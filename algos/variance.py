import os
import statistics as st
import statistics


def getVar(file, fileLS, B1BBR19=False, DEC=False):
    if B1BBR19:
        dataVarianceNbGM = "cat " + file + " | awk -F',' '{print $6}'"
    else:
        dataVarianceNbGM = "cat " + file + " | awk -F',' '{print $9}'"

    listVariances = os.popen(dataVarianceNbGM).read().split('\n')[1::]
    del listVariances[-1]

    data = list(map(int, listVariances))
    stdevNB = st.pstdev(data)
    print("NB var " + file + " : ", round(stdevNB, 4))

    print("1 Standard Deviation of the sample is % s " % (statistics.stdev(data)))
    if B1BBR19:
        dataVarNbGMTime = "cat " + file + " | awk -F',' '{print $4}'"
        dataVarGEsSTime = "cat " + file + " | awk -F',' '{print $3}'"
    else:
        dataVarNbGMTime = "cat " + file + " | awk -F',' '{print $7}'"
        dataVarGEsSTime = "cat " + file + " | awk -F',' '{print $6}'"

    dataVarLKSTime = "cat " + fileLS + " | awk -F',' '{print $3}'"
    listVarGM = os.popen(dataVarNbGMTime).read().split('\n')[1::]
    del listVarGM[-1]

    listVarGEs = os.popen(dataVarGEsSTime).read().split('\n')[1::]
    del listVarGEs[-1]

    listVarLK = os.popen(dataVarLKSTime).read().split('\n')[1::]
    del listVarLK[-1]

    dataGM = list(map(float, listVarGM))
    dataGEs = list(map(float, listVarGEs))
    dataLK = list(map(float, listVarLK))

    dataTime = list(map(sum, zip(dataGM, dataGEs, dataLK)))

    stdevTime = st.pstdev(dataTime)
    print("TIME var " + file + " : ", round(stdevTime, 4))
    print("2 Standard Deviation of the sample is % s " % (statistics.stdev(dataTime)))


def getVarDec(file):
    dataVarianceNbGM = "cat " + file + " | awk -F',' '{print $4}'"
    listVariances = os.popen(dataVarianceNbGM).read().split('\n')[1::]
    del listVariances[-1]

    data = list(map(int, listVariances))
    stdevNB = st.pstdev(data)
    print("NB var " + file + " : ", round(stdevNB, 4))

    dataVarianceNbGM = "cat " + file + " | awk -F',' '{print $3}'"
    listVariances = os.popen(dataVarianceNbGM).read().split('\n')[1::]
    del listVariances[-1]

    data = list(map(float, listVariances))
    stdevNB = st.pstdev(data)
    print("Time var " + file + " : ", round(stdevNB, 4))


fileDEC = '../outPutFile/DEC/resultG2gen_B1'
fileEnronLSG2 = 'dataVarianceEnronG2'
fileB2LSG2 = '../outPutFile/LS/resultG2B2gen_B2'
fileB1LSG2 = '../outPutFile/LSB1/LS/resultLSG2B1'
fileRollernetLSG2 = '../outPutFile/LS/resultG2LSRollernet'

fileEnronBBR19G2 = '../outPutFile/BBR19/resultG2Enrongen_enron'
fileRollernetBBR19G2 = '../outPutFile/BBR19/resultG2rollernetgen_rollernet'
fileB1BBR19G2 = '../outPutFile/BBR19/resultB1BBR19G2'
fileB2BBR19G2 = '../outPutFile/BBR19/resultG2B2gen_B2'

fileResultB1Cover = '../outPutFile/cover/resultB1G2Cover'
fileResultB2Cover = '../outPutFile/cover/resultB2G2Cover'
fileResultEnronCover = '../outPutFile/cover/resultEnronG2Cover'
fileResultRollernetCover = '../outPutFile/cover/resultRorenetG2Cover'

print("***************BBR19**************")
# NB/Time BBR19
getVar(fileEnronBBR19G2, fileResultEnronCover)
getVar(fileRollernetBBR19G2, fileResultRollernetCover)
getVar(fileB1BBR19G2, fileResultB1Cover, B1BBR19=True)
getVar(fileB2BBR19G2, fileResultB2Cover)

print("***************LS**************")
# NB/Time LS
getVar(fileEnronLSG2, fileResultEnronCover)
getVar(fileRollernetLSG2, fileResultRollernetCover)
getVar(fileB1LSG2, fileResultB1Cover)
getVar(fileB2LSG2, fileResultB2Cover)

print("***************DEC**************")
getVarDec(fileDEC)

# awk -F',' '{sum+=($9*$9-696.634*696.634);}END{print sqrt(sum)/1000;}' outPutFile/LS/resultG2LSRollernet
