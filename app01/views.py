from django.shortcuts import render , HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import auth
import os
import subprocess
from django.contrib.auth import authenticate, login,logout
# Create your views here.
import json
def login(request):
    if request.method=="GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        vialdCode = request.POST.get("vialdCode")
        ret = {"flag":False,"error_msg":None}
        if vialdCode.upper() == request.session.get("keep_valid_code").upper():
            user = auth.authenticate(username=username, password=password)
            if user:
                #如果验证成功就让登录
                auth.login(request,user)
                ret["flag"] = True
            else:
                ret["error_msg"] = "用户名和密码错误"
        else:
            ret["error_msg"] = "验证码错误"
    return HttpResponse(json.dumps(ret))

def index(request):
    #验证是不是当前进来的那个用户，如果用户已经登录了就可以看到页面
    # 如果没有登录就不让看见主页面，就直接返回登录页面
    if not request.user.is_authenticated():
        return redirect("/login/")
    else:
        return render(request, "index.html")

def log_out(request):
    auth.logout(request)
    return redirect("/login/")
def get_vaildCode_img(request):
    # 方式一：这样的方式吧路径写死了，只能是那一张图片
    # import os
    # path = os.path.join(settings.BASE_DIR,"static","image","3.jpg")
    # with open(path,"rb") as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 方式二：每次都显示不同的图片，利用pillow模块，安装一个pillow模块
    # from PIL import Image
    # img = Image.new(mode="RGB",size=(120,40),color="green") #首先自己创建一个图片,参数size=(120,40) 代表长和高
    # f = open("validcode.png","wb")#然后把图片放在一个指定的位置
    # img.save(f,"png")  #保存图片
    # f.close()
    # with open("validcode.png","rb") as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 方式三：
    # 方式二也不怎么好，因为每次都要创建一个保存图片的文件，我们可以不让吧图片保存到硬盘上，
    # 在内存中保存，完了自动清除，那么就引入了方式三：利用BytesIO模块
    # from io import BytesIO
    # from PIL import Image
    # img = Image.new(mode="RGB",size=(120,40),color="blue")
    # f = BytesIO()  #内存文件句柄
    # img.save(f,"png")  #保存文件
    # data = f.getvalue()#打开文件(相当于python中的f.read())
    # return HttpResponse(data)

    # 方式四：1、添加画笔，也就是在图片上写上一些文字
    #         2、并且字体随机，背景颜色随机
    from io import BytesIO
    from PIL import Image,ImageDraw,ImageFont
    import random
    #随机创建图片
    img = Image.new(mode="RGB",size=(120,40),color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    draw = ImageDraw.Draw(img,"RGB")
    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, 120)
        y1 = random.randint(0, 40)
        x2 = random.randint(0, 120)
        y2 = random.randint(0, 40)

        draw.line((x1, y1, x2, y2), fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    font = ImageFont.truetype("static/font/batang.ttc",20)  #20表示20像素

    str_list = []  #吧每次生成的验证码保存起来
    # 随机生成五个字符
    for i in range(5):
        random_num = str(random.randint(0, 9))  # 随机数字
        random_lower = chr(random.randint(65, 90))  # 随机小写字母
        random_upper = chr(random.randint(97, 122))  # 随机大写字母
        random_char = random.choice([random_num, random_lower, random_upper])
        print(random_char,"random_char")
        str_list.append(random_char)
        # (5 + i * 24, 10)表示坐标，字体的位置
        draw.text((5+i*24,10),random_char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
    print(str_list,"str_list")
    f = BytesIO()#内存文件句柄
    img.save(f,"png")   #img是一个对象
    data = f.getvalue()  #读取数据并返回至HTML
    valid_str = "".join(str_list)
    print(valid_str,"valid_str")
    request.session["keep_valid_code"] = valid_str   #吧保存到列表的东西存放至session中
    return HttpResponse(data)



def conntect(request):
    import glob
    '''
    dic = {}
    list1 = []
    list = glob.glob(r'*.py')
    b = 0
    for i in list:
        dic['id'] = b
        dic['key'] = i
        list1.append(dic)
        b += 1
        dic = {}
    print(list1)
    '''
    list = glob.glob(r'*.conf')
#    list = glob.glob(r'/etc/nginx/*.conf')

    return  render(request,"connect.html",{'list':list})
    # print(glob.glob(r'*.py'))


def list(request,nid):
    # with open('111.py', 'w') as f:
    #     print('write')
    #     f.write('sdfsdfsfsdfs\nsdfsafa\nsfasfasf')
    print(nid)
    f = open(nid,'rb')
    content = f.read()
    f.close()
    a='nginx: the configuration file /etc/nginx/nginx.conf syntax is ok \n nginx: configuration file /etc/nginx/nginx.conf test is successful'
    # a="'nginxtheconfigurationfile"
    # res=subprocess.Popen('nginx -t',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    # a = res.stderr.read()
    print("nginx -t",a)
    # return HttpResponse(200)
    return render(request,"list.html",{'content':content,'a':a,'nid':nid})


def list_post(request,nid):
    print('-->',nid)
    if request.method =="POST":
        a = request.POST.get("file")
        # print(type(a))
        a=a.encode('utf8').strip()
        new_file=nid+"new"
        with open(new_file, 'wb') as f:
            print('write',nid)
            print('new_file',new_file)
            f.write(a)
        os.remove(nid)
        os.rename(new_file,nid)
        # res = subprocess.Popen('nginx -t', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # res=res.stderr.read()

    return redirect("/list-%s/" %nid)

