import requests,json
while 1:
    #输入音乐名关键字
    song_name=input('请输入你将要下载的音乐名：')
    song_search_url='https://songsearch.kugou.com/song_search_v2'
    song_search_params={"pagesize": 30,"keyword":song_name,"platform": "WebFilter"}     #pagesize：酷狗热度排行前*首,默认30
    song_name_result=json.loads(requests.get(song_search_url,params=song_search_params).text)['data']['lists']
    for i in range(len(song_name_result)):
        print("%d:%s"%(i+1,song_name_result[i]['FileName']))
    ch_song_id=int(input('请输入你将要下载的版本序号：'))
    song_hash=song_name_result[ch_song_id-1]['FileHash']

    #获取音频文件下载地址
    hash_url='https://wwwapi.kugou.com/yy/index.php'
    hash_params={"r": "play/getdata","hash": song_hash}
    hash_result=requests.get(hash_url,params=hash_params)
    music_url=json.loads(hash_result.text)['data']['play_url']
    #music_lyrics=json.loads(hash_result.text)['data']['lyrics']                        #歌词

    #下载音频文件
    music =requests.get(music_url)
    with open(song_name_result[ch_song_id-1]['FileName']+'.'+music_url.split('.')[-1],'wb') as f:
        f.write(music.content)
    print('音乐：\t%s\t下载成功！地址：%s' %(song_name_result[ch_song_id-1]['FileName'],music_url))

    #是否继续下载音乐
    ag=input('是否继续下载音乐（y/n）：')
    if ag.lower()=='y':
        continue
    else:
        break