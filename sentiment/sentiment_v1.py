import json,re,sys
from textblob import TextBlob
from mpi4py import MPI



def processText(line,textDict):
    currentText = json.loads(line[:-2])['doc']['text']
    currentText = re.sub("RT |(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",currentText)
    analysis = TextBlob(currentText)
    
    if analysis.sentiment.polarity > 0: 
        textDict['positive'] += 1
    elif analysis.sentiment.polarity == 0: 
        textDict['neutral'] += 1
    else:
        textDict['negative'] += 1
    return


def mergeDict(dictS):
    result = {}
    for i in dictS:
        for key, value in i.items():
            if key not in result:
                result[key] = value
            else:
                result[key] += value
    return result


def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()


    textDict = {'neutral':0, 'positive':0,'negative':0}


    with open(sys.argv[1], 'r', encoding="utf-8") as f:
        row = 0
        for line in f:
            try:
                row += 1
                if rank == (row % size):
                    processText(line,textDict)
            except:
                continue
        comm.barrier()
        textDict2 = comm.gather(textDict, root=0)       

        if rank == 0:
            mergedDict = mergeDict(textDict2)
            print(mergedDict)

if __name__ == '__main__':
    main()