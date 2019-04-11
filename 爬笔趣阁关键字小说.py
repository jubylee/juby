#coding="utf-8"
import requests,re
from urllib.parse import urlparse

def get_url(url):
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36"}
    result = requests.get(url,headers=headers,verify=False)
    result.encoding = 'utf-8'
    return result

def download_txt(novel_name,txt):
    with open(novel_name+'.txt', 'a+') as f:
        f.write(txt)

if __name__=='__main__':
    while 1:
        #选择小说名称
        url='https://www.biqudu.com/searchbook.php?keyword='
        domain=urlparse(url).scheme+'://'+urlparse(url).netloc
        keyword=input('请输入作者或者书名：')
        result = get_url(url+keyword)
        novel_url_name=re.findall('<\/span><a href="(.*?)">\r\n\s+(.*?)\r\n\s+<\/a><\/dt>',result.text,re.S)
        if len(novel_url_name)<1:
            ag = input('查找不到你输入的小说名称，是否重新输入（y/n）：')
            if ag.lower() == 'y':
                continue
            else:
                break
        else:
            if len(novel_url_name)>1:
                for i in novel_url_name:
                    print('%d：  %s'%(novel_url_name.index(i)+1,i[1]))
                ch_novel=int(input('请选择你将要下载的小说：'))-1
            else:
                ch_novel=0

            #选择章节
            url=domain+novel_url_name[ch_novel][0]
            result=get_url(url)
            chapter_start_flag = re.search('</a></dd>\s+<dt>《'+novel_url_name[ch_novel][1]+'》.*?</dt>', result.text).span()[0]
            chapter_pat = re.compile(r'<dd> <a href="(.*?)">(.*?)</a></dd>', re.S)
            chapter_url_name = chapter_pat.findall(result.text, chapter_start_flag,)
            for i in chapter_url_name:
                print('%d： %s    '%(chapter_url_name.index(i)+1,i[1]),end='')
            ch_start_chapter=int(input('\n请选择开始下载的章节序号：'))-1
            chapter_text=novel_url_name[ch_novel][1]+'\n\n\n'
            download_txt(novel_url_name[ch_novel][1], chapter_text)
            for chapter_index in range(ch_start_chapter,len(chapter_url_name)):
                url = domain + chapter_url_name[chapter_index][0]
                result = get_url(url)
                chapter_source = re.findall('<script>readx\(\);<\/script>(.*?)<script>chaptererror\(\);<\/script>', result.text,re.S)
                chapter_text = chapter_url_name[chapter_index][1] + '\n\n    ' + chapter_source[0].replace('<br/>','\n').lstrip() +'\n\n\n' # 加上章节标题。
                download_txt(novel_url_name[ch_novel][1], chapter_text)
                print(chapter_url_name[chapter_index][1]+'    已经下载完毕！')

            ag = input('是否继续下载小说（y/n）：')
            if ag.lower() == 'y':
                continue
            else:
                break