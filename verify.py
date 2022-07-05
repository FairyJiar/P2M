import os
import difflib
import astgen
import sys

#def file_diff(fa,fb):
#    with open(fa) as file_1:
#        file_1_text = file_1.readlines()
#      
#    with open(fb) as file_2:
#        file_2_text = file_2.readlines()
#  
#    for line in difflib.unified_diff(
#            file_1_text, file_2_text, fromfile=fa, 
#            tofile=fb, lineterm=''):
#        print(line)

def verify_one_file(filename):
    if(filename[-3:]!=".py"):
        return
    print(filename)
    astgen.main(["-i",filename])
    print("###############################################")
    print("%%%%%%%%%%%%%%%%M_Result%%%%%%%%%%%%%%%%%")
    os.system("M.exe -s default.m")
    m_output = open("C:\msv\_MSVOutput.txt","r")
    print("%%%%%%%%%%%%%%%%M_Output%%%%%%%%%%%%%%%%%")
    for line in m_output:
        print(line)
    print("%%%%%%%%%%%%%%Python_Result%%%%%%%%%%%%%%")
    os.system("python "+filename)
    print("###############################################")
path=sys.argv[1]
if(os.path.isdir(path)):
    for root,dirs,files in os.walk(sys.argv[1]):
        for filename in files:
            verify_one_file(root+"/"+filename)
else:
    verify_one_file(path)
        #if(filename[-8:]=="_test.py"):
        #    test = filename[:-8]
        #    test_file = root+"/"+test+"_test.py"
        #elif(filename[-3:]==".py"):
        #    test = filename[:-3]
        #    test_file = root+"/"+test+".py"
        #else:
        #    continue
        #print(test_file)
        #astgen.main(["-i",test_file])
        #print("######################################")
        #os.system("M.exe -s default.m")
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #os.system("python "+test_file)
        #print("######################################")
        #file_diff("m_result.txt","python.txt")
