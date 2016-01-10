__author__ = 'hunterhug'
import random
import re
# 代理ip函数
# 183.239.167.122:8080
def daili():
        geshi=re.compile(r'(.*)@(.*)')
        file =open('daili.txt','rb')
        data=file.read().decode('utf-8','ignore').split('\n')
        location=[]
        #random.shuffle(data) # ip数组打乱
        for i in range(0,len(data)):
                temp=geshi.match(data[i]).group(1).split('.')
                location.append(geshi.match(data[i]).group(2))
                data[i]='.'.join([temp[1],temp[2],temp[3]])
        file.close()
        file =open('daili1.txt','w')
        file.write('\n'.join(data))
        file.close()
        return data

if __name__=='__main__':
        a,b=daili()
        print(a)

