import ftplib
from bs4 import BeautifulSoup
from datetime import datetime
import lxml
import os

def formatDKTime(string, evernote=True):
    try:
        dt = datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    except:
        dt = datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")
    if evernote:
        ds = dt.strftime("%Y%m%dT%H%M%SZ")
    else:
        ds = dt.strftime("%Y年%m月%d日 %H:%M:%S".encode('unicode_escape').decode('utf8')).encode('utf-8').decode('unicode_escape')
    return ds

class kindleFTP:
    def __init__(self, ip):
        self.ip = ip
        self.defaultDir = "DK_Documents"
        self.dkx_filename = "dkx"
        self.dkx_files = []
    
    def connect(self):
        self.ftp = ftplib.FTP(self.ip, "anonymous", "password")
        self.ftp.encoding = "ANSI"
        self.ftp.cwd(self.defaultDir)
        print("连接成功！")

    def close(self):
        if self.ftp != None:
            self.ftp.quit()
            self.ftp = None

    def findDKX(self):
        self.connect()
        self.dkx_files = []
        self.recursive_find(self.ftp, "/" + self.defaultDir)
        self.close()
        return self.dkx_files
    
    def recursive_find(self, ftp, cpath):
        dirs = ftp.nlst()
        if self.dkx_filename in dirs:
            # print("Find one!", ftp.pwd())
            self.dkx_files.append(cpath)
            return ftp.pwd()
        for fd in dirs:
            # print("fd:", fd)
            try:
                ftp.cwd(fd)
                self.recursive_find(ftp, cpath + "/" + fd)
                ftp.cwd("..")
            except ftplib.error_perm:
                #print("not dir.")
                pass

    def getFile(self, path):
        self.connect()
        self.ftp.cwd(path)
        with open("ftp_dkx", "wb") as fp:
            self.ftp.retrbinary("RETR " + self.dkx_filename, fp.write)
        self.close()


if __name__ == "__main__":
    content = ""
    print("1. 当前目录下dkx文件")
    print("2. WIFI传输模式(FTP)")
    opt = input("请选择模式:").strip()
    if opt == "1":
        # Load current dkx
        if os.path.exists("dkx"):
            fr = open("dkx", 'r', encoding="utf8")
            content = fr.read()
            fr.close()
        else:
            print("Please put dkx files in this program root.")
            exit()

    elif opt == "2":
        # FTP mode
        ftpip = "192.168." + input("请输入IP地址: 192.168.")
        kFtp = kindleFTP(ftpip)
        print("正在获取笔记文件")
        dkxs = kFtp.findDKX()
        count = 0
        for dkx in dkxs:
            print(count, dkx)
            count += 1
        opt = int(input("请选择："))
        print("已选择，正在导出", dkxs[opt])
        kFtp.getFile(dkxs[opt])
        if os.path.exists("ftp_dkx"):
            fr = open("ftp_dkx", 'r', encoding="utf8")
            content = fr.read()
            fr.close()
    else:
        print("Invalid Option!")
        exit()


    # Parser dkx(xml) file
    bs_content = BeautifulSoup(content, "lxml")

    BookName = bs_content.bookname.string
    BookName = BookName[0:BookName.rfind('.')].strip()
    CreateTime = bs_content.createtime.string
    LastReadTime = bs_content.lastreadtime.string
    nowTime = datetime.now().strftime("%Y%m%dT%H%M%SZ")

    noteItems = []
    for rditem in bs_content.readingdata.findAll("readingdataitem"):
        _createTime = rditem.createtime.string
        _createTime = formatDKTime(_createTime, evernote=False)
        _chapName = rditem.chaptertitle.string
        _bookContent = rditem.bookcontent.string
        noteItems.append((_createTime, _chapName, _bookContent))

    ## Create ENEX file
    noteBody = '<div><b><span style="font-size: 18px;">书名：</span></b><span style="font-size: 18px;"><span style="color:rgb(0, 131, 229);">{}</span></span></div><div><b><span style="font-size: 16px;">创建时间：</span></b><span style="font-size: 16px;"><span style="color:rgb(0, 131, 229);">{}</span></span></div><div><b><span style="font-size: 16px;">最近阅读时间：</span></b><span style="font-size: 16px;"><span style="color:rgb(0, 131, 229);">{}</span></span></div><div style="text-align:right;"><span style="font-size: 12px;"><span style="color:rgb(191, 191, 191);">Created by My Program</span></span></div>'.format(
        BookName, formatDKTime(CreateTime, False), formatDKTime(LastReadTime, False)
    )
    count = 1
    for item in noteItems:
        noteBody += '<hr /><div><span style="font-size: 16px;">📕 {}.</span></div><div><b><span style="color:rgb(231, 159, 0);">简评</span></b><span style="color:rgb(231, 159, 0);">：</span></div><div><span style="color:rgb(231, 159, 0);"><span style="--en-markholder:true;"><br /></span></span></div><div style="text-align:right;"><span style="font-size: 14px;"><span style="color:rgb(0, 170, 179);">来源：{}</span></span><span style="font-size: 16px;">  </span><span style="font-size: 12px;"><i>{}</i></span></div><div style="--en-codeblock:true;box-sizing: border-box; padding: 8px; font-family: Monaco, Menlo, Consolas, &quot;Courier New&quot;, monospace; font-size: 16px; color: rgb(51, 51, 51); border-top-left-radius: 4px; border-top-right-radius: 4px; border-bottom-right-radius: 4px; border-bottom-left-radius: 4px; background-color: rgb(251, 250, 248); border: 1px solid rgba(0, 0, 0, 0.14902); background-position: initial initial; background-repeat: initial initial;"><div>{}</div></div><div><br /></div>'.format(
            count, item[1], item[0], item[2]
        )
        count += 1
    nBody = '<?xml version="1.0" encoding="UTF-8"?>'
    nBody += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    nBody += '<en-note>%s</en-note>' % noteBody

    nContent = '''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">
    <en-export export-date="{}" application="Evernote" version="10.2.4">
    <note>
        <title>{}</title>
        <created>{}</created>
        <updated>{}</updated>
        <note-attributes>
        </note-attributes>
        <content>
        <![CDATA[{}]]>
        </content>
    </note>
    </en-export>
    '''.format(
        nowTime, BookName, formatDKTime(CreateTime), formatDKTime(LastReadTime), nBody
    )

    with open("Output_{}.enex".format(BookName), "w", encoding="utf8") as fp:
        fp.write(nContent)

    print("Successfully Export %d Notes from %s" % (count-1, BookName))