responses = []
requests= []

# read data
with open('original.txt', 'r') as f:
    #
    isRes = False 
    isReq = False

    data = f.readline()

    while data:
        if "Request" in data:
            isReq = True
            isRes = False
            data = f.readline()

        elif "Response" in data:
            isReq = False
            isRes = True
            data = f.readline()

        if isReq:
            print(1)
        elif isRes:
            print(2)
        data = f.readline()

    # store in keyvalue pairs

  