import requests,re,os

keyword=input('请输入你将要下载的图片关键字：')
num=int(input('请输入你将要下载的图片数量：'))
url='https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1551271741236_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word='
result=requests.get(url+keyword)
pic_url=re.findall('"objURL":"(.*?)",',result.text,re.S)
if num>30:
    for i in range(1, num // 30 + 1):
        params = {'tn':'resultjson_com','catename':'pcindexhot','ipn':'rj','ct':'201326592','is':'','fp':'result','queryWord':'','cl':'2','lm':'-1','ie':'utf-8','oe':'utf-8','adpicid':'','st':'-1','z':'','ic':'0','face':'0','istype':'2','qc':'','nc':'1','fr':'','pn':'0','rn':'30'}
        params['word']=keyword
        params['pn'] = 30*i
        response = requests.get('https://image.baidu.com/search/avatarjson', params=params)
        pic_url+=re.findall('"objURL":"(.*?)",',response.text,re.S)
if not os.path.exists("图片"):
        os.mkdir("图片")
if not os.path.exists("图片\\"+keyword):
        os.mkdir("图片\\"+keyword)
for i in range(num):
    pic =requests.get(pic_url[i])
    with open("图片\\"+keyword+"\\"+keyword+str(i+1)+'.jpg','wb') as f:
        f.write(pic.content)
    print('第%d张图片已下载，地址：\t%s' %(i+1,pic_url[i]))
