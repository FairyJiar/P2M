def function_name(parameter1,parameter2):
    print("start")
    while(1):
        if(parameter1 == 0):
            if(parameter2 == 0):
                return 0
            print("statement1")
            break
        print("statement2")
        break
    if(parameter1 == 0):
        while(1):
            for count in range(0,5):
                if(count<=2):
                    if(count == 0):
                        print("statement3")
                        continue
                    if(count == 1):
                        print("statement4")
                        continue
                    else:
                        print("statement5")
                    if(count == 2):
                        print("statement6")
                        break
                    print("statement7")
                else:
                    print("statement8")
                print("statement9")
            else:
                print("statement10")
            if(parameter1 == 0):
                print("statement11")
                break
            print("statement12")
            break
        else:
            print ("statement13")
        print("statement14")
        return 1
    print("end")
    return -1

ret = function_name(0,0)
print("First return value = ",ret)
ret = function_name(0,1)
print("Second return value = ",ret)