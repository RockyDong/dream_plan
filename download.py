# 定义函数,将网址转化为html内容
# 使用requests模块，教程参见：http://www.python-requests.org/en/master/
import requests
import re
import os
def url2html_requests(url,encoding='utf-8'):
    # 输入:网址
    # 输出:网页内容
    
    # 检查网址是否以http://开头,少数网站是以https://开头的
    if not url.startswith('http://'):
        url = 'http://' + url
    try:
        # 获取网页内容
        r = requests.get(url,timeout=120) 
    except requests.exceptions.ConnectTimeout:
        
        #120s没有反应就报错
        print('输入的网址有误,请检查')
    else:
        if r.status_code == 200:
            # 默认编码格式为utf-8
            # 查看网页编码格式方法：Chrome浏览器Ctrl+U,搜索关键字charset，如果有，那么后面接着的就是编码格式
            # 不是所有网页都有charset关键字，可以试一下utf-8或者gbk
            r.encoding = encoding
            content = r.text
        
        # 返回网页内容
        return content
# 从静态html页面中提取带有图片的网络链接


# 关于python正则表达式，可以参考：http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html
def html2imgurl(html_content):
    # detect image url in html content
    # return img url list

    pattern = re.compile('(https?)?//([\w\/\-\.]+)(bmp|jpg|tiff|gif|png)') # re.S for . representate any characters
    list_raw = re.findall(pattern,html_content) # raw list is made up of 2 parts
    
    list_img_url = ['http://'+''.join(i) for i in list_raw]

    return list_img_url
# 定义保存图片的函数

def saveimg_requests(imgurl,filename=''):
#http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
    try:
        r = requests.get(imgurl)
    except requests.exception.ConnectTimeout:
        print('Img NOT found')
    else:
        r.encoding = 'UFT-8'
        if filename =='':
            filename = imgurl.split('/').pop()#imgurl.split("/").pop()
            print(filename)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r:
                    f.write(chunk)


# 设置图片保存地址
dir2save = "F:\\OwnGame\\pictures"
if not os.path.isdir(dir2save):
    os.makedirs(dir2save)
os.chdir(dir2save)

# 此处爬取xmind官网分享的mindmap缩略图
url = 'http://www.yxdown.com/zt/dotahero/'
print('visiting page: %s'%url)

# 读取该页面的html信息
html_content = url2html_requests(url,encoding='utf-8')#部分网站是gbk编码

# 分析网页发现图片网址的格式为http://www.xmind.net/m/9VPU，html中显示为/m/9vPU，即后4位是大小写字母和数字组成
p_img = re.compile('<img src="(.*?)" alt=".* - (.*?)"\s?>')
img_info = re.findall(p_img,html_content)
# 获取图片链接列表list
#print(img_info)

# 使用set集合来去重
for url_mark,name in set(img_info):
    #拼接网址
    print(url_mark)
    img_url = url + url_mark
    name = name.strip()
    if img_url.endswith('jpg'):
        name = name + ".jpg"
    else:
        name = name + ".gif"
    #print(name)
    saveimg_requests(img_url, name)
    # html = url2html_requests("http://www.yxdown.com/zt/dotahero/"+url_mark,encoding='utf-8')
    #获取图片链接
    # img_urls = html2imgurl(html)
    # for img_url in set(img_urls):
        #每个大图页面只有一张需要的图，是png格式的
        # if img_url.endswith('jpg'):
            # saveimg_requests(img_url,name+'.jpg')

# 报告保存了多少图片
# print('%d imgs is saved in %s'%(len(img_urls),dir2save))

