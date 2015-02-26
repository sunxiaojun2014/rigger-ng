#coding=utf8
import  re , os , sys, logging ,string
from string  import Template
import  setting
_logger = logging.getLogger()

class prompt:
    @staticmethod
    def recommend(find, keys):
        find_len = len(find)
        wordlen =3
        if find_len >=13 :
            wordlen=5
        if find_len >=9 :
            wordlen=4
        recommend = []
        beg=0
        for x in range(wordlen-1,find_len,wordlen):
            end=x+1
            pice=find[beg:end]
            if len(pice) < 2:
                    continue;
            recommend  = recommend +  prompt.match(pice,keys)
            beg=end
        return recommend
    @staticmethod
    def match(find ,keys):
        match=[]
        if len(find) > 0  :
            for key in keys:
                if re.compile(find).search(key):
                    match.append(key)
        return match;



class scope_iotag :
    tags = []
    def __init__(self,tag,method="",settingo=""):
        self.tag      = tag
        self.method   = method
        self.settingo = settingo
    def __enter__(self):
        rgio.catch_start()
        rgio.has_err   = False
        trace = string.join(rgio.trace,'.')
        _logger.debug("=====>  (%s)[%s]" %(self.method,self.tag))
        _logger.debug("--------------------------------------")

    def __exit__(self, exc_type, exc_value, traceback ):
        out = rgio.buf
        rgio.catch_end()
        if setting.debug  or rgio.has_err :
            if out  is not None and len(out) > 0 :
                if  setting.god.stdout :
                    print("*******************************************************************************************")
                    print("(%s)[%s]" %(self.method,self.tag))
                    print("-------------------------------------------------------------------------------------------")
                    print(out)
                    print("---------------------------------------------END-------------------------------------------")
                    print("\n")
                _logger.error(out)
            else:
                pass
        rgio.has_err   = False
        _logger.debug(" <==== (%s)[%s]  " %(self.method,self.tag))
        _logger.debug("--------------------------------------")

class rgio:
    buf     = None
    has_err = False
    trace   = []
    logger  = None

    @staticmethod
    def using_logger(l):
        rgio.logger =  l


    @staticmethod
    def push_trace(settingo):
        # if not rgio.trace.has_key(key):
        #     rgio.trace[key] = []
        rgio.trace.append(settingo)


    @staticmethod
    def pop_trace():
        rgio.trace.pop()
        # settingo =rgio.trace[key].pop()
#        pass
    @staticmethod
    def catch_start():
        rgio.buf = ""
    @staticmethod
    def catch_end():
        rgio.buf = None

    @staticmethod
    def list2str(lst):
        s = ""
        for v in lst :
            if len(s) == 0 :
                s =  str(v)
            else:
                s = s + "," +  str(v)
        return s
    @staticmethod
    def prompt(*args,**kws):
        msg=args[0]
        settingo = Template(msg).substitute(kws)
        if rgio.buf is not None:
            rgio.buf  += settingo  + "\n"
        else:
            print(settingo)
            _logger.error(settingo)


    @staticmethod
    def inred( s ):
        return "%s[31;2m%s%s[0m"%(chr(27), s, chr(27))

    @staticmethod
    def error(msg):
        if rgio.buf is not None:
            rgio.buf  += msg  + "\n"
        rgio.has_err   = True
        print( rgio.inred(msg))
        _logger.error(msg)

    @staticmethod
    def simple_out(msg):
        if rgio.buf is not None:
            rgio.buf  += msg + "\n"
        else:
            print(msg)
            _logger.info(msg)

#class uxio:
def confirm(message):
    res = get_input_line(message + "(y/n)")
    return  res.strip().lower()== 'y'
def getchose(message,quit='q',check=None):
    while True:
        rgio.prompt(message + " Quit(" + quit +  ")" )
        import sys,tty,termios
        fd = sys.stdin.fileno()
        ch = sys.stdin.read(1)
        if ch.lower() ==  quit.lower() :
            return None
        if str.isdigit(ch):
            ch = int(ch)
            if check is None :
                return ch
            if not check is None and check(ch):
                return ch
        rgio.prompt("Input error, try again!")

class in_result:
    GOOD        =  0
    CHOSE_OTHER =  1
    QUIT        =  3
    BAD         =  9
    def __init__(self,content=None):
        self.status  = in_result.GOOD
        self.content = content

def get_input_line(message,default=None,quit='q',check=None):
    if default is None :
        print("%s exit( %s ) " %(message,quit) )
    else:
        print("%s default(%s) exit(%s) " %(message,default,quit) )

    while True:
        import sys,tty,termios
        line = sys.stdin.readline().strip()
        if  len(line) == 0 :
            if default is not None:
                return  default
            continue
        if line.lower() ==  quit.lower() :
            raise error.user_break("You stop Input!")
#            return None
        return line.strip()



def get_chose_index(message,maxnum,quit='q'):
#    message += "其它(%s)" %other
    ch = get_input_line(message,None,quit)
    if ch is None:
        return None
    if str.isdigit(ch):
        ch = int(ch)
        if ch >= 1 and ch <= maxnum :
            return ch
    rgio.prompt("输入错误，请重新输入")

def chose_item(items,name):
    index = 1
    for item in  items :
        print( str(index) + "\t: " + item)
        index += 1
    print("%d\t other %s" %(index,name))
    chose_line = get_chose_index("please chose %s" %name ,index)
    if chose_line is None:
        return  None
    chose = int(chose_line)
    if chose == index:
        other = get_input_line("please input %s" %name )
        return other
    if chose >= 1 and chose <= index :
        return  items[chose-1]
    return  None

def get_mutichose_index(message,maxnum,quit='q'):
    line = get_input_line(message,quit)
    index = []
    if line is None:
        return index
    chs = line.split(",")
    for ch in chs:
        if str.isdigit(ch):
            ch = int(ch)
            if ch >= 1 and ch <= maxnum :
                index.append(ch)
    return index

