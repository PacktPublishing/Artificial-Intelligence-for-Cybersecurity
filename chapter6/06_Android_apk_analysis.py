# https://github.com/PegX/Hybroid/tree/main/apk_graph_corpus
# Reference from the hybroid code

import sys
def android_apk_analysis(self, filename):
    print("Androgurad starting!")
    a = APK(filename)
    print(a)
    d = DalvikVMFormat(a.get_dex())
    print(d)
    dx = VMAnalysis(d)
    print(dx)
    gx = GVMAnalysis(dx, a)
    print(gx)

# Goal: present how to use Androguard to analyze the Android application
# python3 06_Android_apk_analysis.py **.apk
if __name__ == '__main__':
    filename = sys.argv[1]
    android_apk_analysis(filename)