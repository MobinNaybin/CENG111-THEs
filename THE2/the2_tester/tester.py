from the2 import check_month


resultList = []
theList = []
with open("results.txt", "r") as results:
    for line in results:
        line = line.strip("\n")
        result = eval(line)
        resultList.append(result)
with open("test.txt", "r") as test:
    i = 0
    for line in test:
        i += 1
        line = line.strip("\n").split(" ")
        # if i == 20996:
        #    print(line)
        #    quit()
        theResult = check_month(line)
        theList.append(theResult)
    # quit()
for i in range(len(resultList)):
    if isinstance(resultList[i], list) and isinstance(theList[i], list):
        if resultList[i].sort() != theList[i].sort():
            print(f"Test Case {i + 1} Failed.")
            continue
    elif isinstance(resultList[i], int) and isinstance(resultList[i], int):
        if resultList[i] != theList[i]:
            print(f"Test Case {i + 1} Failed.correct:{resultList[i]} urs:{theList[i]} ")
            continue
    else:
        print(f"Test Case {i + 1} Failed.")
