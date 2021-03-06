#coding=utf-8
import  os , string   , logging
import  interface,utls.rg_sh

from utls.rg_io  import rgio ,rg_logger
from string import Template
from res.base   import *
import  utls.check , utls.dbc



class link(interface.resource,res_utls):
    """
    !R.link :
        dst: "/home/q/system/mysys"
        src: "$${PRJ_ROOT}/src/apps/console"
    """
    force   = False
    dst     = ""
    src     = ""
    def _before(self,context):
        self.dst = utls.rg_var.value_of(self.dst)
        self.src = utls.rg_var.value_of(self.src)

    def _config(self,context):
        cmdtpl = ""
        if self.force is True :
            cmdtpl ="if test -L $DST ; then rm -rf  $DST ; fi ; dirname $DST | xargs mkdir -p ; ln -s  $SRC $DST"
        else :
            cmdtpl ="if ! test -L $DST ; then   dirname $DST | xargs mkdir -p ;  ln -s   $SRC $DST ; fi;  "
        cmd = Template(cmdtpl).substitute(DST=self.dst,SRC =self.src)
        self.execmd(cmd)

    def _clean(self,context):
        cmdtpl = "if test -L $DST ; then rm -rf  $DST ; fi ; "
        cmd    = Template(cmdtpl).substitute(DST=self.dst)
        self.execmd(cmd)

    def _check(self,context):
        self._check_print(os.path.exists(self.dst),self.dst)

    def _info(self,context):
        rgio.struct_out("link")
        rgio.struct_out("src: " + self.src,1)
        rgio.struct_out("dst: " + self.dst,1)

# class copy(resource,restag_file):
#     """
#     !R.copy:
#         dst: "/home/q/system/mysys/a.txt"
#         src: "$${PRJ_ROOT}/src/apps/console/a.txt"
#     """
#     _dst=None
#     _src=None
#     _force=True
#
#     def _before(self,context):
#         self.dst = env_exp.value(self.dst)
#         self.src = env_exp.value(self.src)
#
#     def _config(self,context):
#         cmdtpl = ""
#         if self.force is True :
#             cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi ; dirname $DST | xargs mkdir -p ; cp -r  $SRC $DST"
#         else :
#             cmdtpl ="if ! test -e $DST ; then   dirname $DST | xargs mkdir -p ; cp -r  $SRC $DST ; fi;  "
#         cmd = Template(cmdtpl).substitute(DST=self.dst,SRC =self.src)
#         self.execmd(cmd)
#     def _check(self,context):
#         self._check_print(os.path.exists(self.dst),self.dst)
#     def _clean(self,context):
#         cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi ; "
#         cmd = Template(cmdtpl).substitute(DST=self.dst,SRC =self.src)
#         self.execmd(cmd)
#

class path(interface.resource,res_utls):
    """
    !R.path:
        dst: "/home/q/system/mysys/,/home/q/system/mysys2"
        keep: True
    """
    dst        = None
    keep       = False
    chmod      = "o+w"

    def _before(self,context):
        self.paths= []
        if self.dst is None:
            return
        self.dst   = utls.rg_var.value_of(self.dst)
        self.paths = self.dst.split(',')

    def _checkWrite(self,dst) :
        while  True  :
            if os.path.exists(dst) :
                return  os.access(dst, os.W_OK)
            else :
                dst = os.path.dirname(dst)
            if dst == "/"  or dst == "" or dst == "."  or dst == "./"  or dst ==  None :
                break
        return False



    def _config(self,context):
        for v in self.paths :
            if os.path.exists(v)  and self._checkWrite(v) :
                continue
            else :
                if not self._checkWrite(v) :
                    if not self.sudo :
                        raise interface.rigger_exception( "%s ä¸å¯è®¿é®" %(v) )
            cmdtpl ="if test ! -e $DST; then   mkdir -p $DST ; fi ;   chmod $CHMOD  $DST; "
            cmd = Template(cmdtpl).substitute(DST=v,CHMOD=self.chmod)
            self.execmd(cmd)

    def _check(self,context):
        for v in self.paths :
            self._check_print(os.path.exists(v),v)

    def _clean(self,context):
        if self.keep :
            return
        cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi ;  "
        for v in self.paths :
            cmd = Template(cmdtpl).substitute(DST=v)
            self.execmd(cmd)

    def _info(self,context):
        rgio.struct_out("path :" )
        for path in self.paths:
            rgio.struct_out("%s" %path,1 )

    def _depend(self,m,context):
        for v in self.paths :
            m._check_writeable(v)
#
# class file_merge(resource,restag_file):
#     """
#     !R.file_merge
#         dst : "$${PRJ_ROOT}/conf/used/my.conf
#         src : "$${PRJ_ROOT}/conf/option/a/:$${PRJ_ROOT}/conf/option/b/"
#         filter: ".*\.conf"
#
#     """
#     _dst        = None
#     _src        = None
#     _filter     = ".*\.conf"
#     _note       = "#"
#     _mod        = "a+w"
#     def _before(self,context):
#         self.dst        = env_exp.value(self.dst)
#         self.src        = env_exp.value(self.src)
#         self.note       = env_exp.value(self.note)
#         self.mod        = env_exp.value(self.mod)
#         self.filter     = env_exp.value(self.filter)
#     def _config(self,context):
#         with open(self.dst, 'w+') as self.dstfile :
#             srclist = self.src.split(":")
#             for src in srclist:
#                 if not os.path.exists(src):
#                     raise error.rigger_exception("path not exists: %s" %src)
#                 os.path.walk(src,self.proc_file,None)
#         if os.getuid() == os.stat(self.dst).st_uid :
#             # Ã¥ÂÂ¶Ã¥Â®ÂÃ¤ÂºÂºÃ¥ÂÂ¯Ã¤Â»Â¥Ã¨Â¿ÂÃ¨Â¡ÂÃ¤Â¿Â®Ã¦ÂÂ¹Ã¯Â¼Â
#             self.execmd("chmod %s %s " %(self.mod, self.dst))
#
#
#     def reload(self,context):
#         self._config(context)
#
#     def _check(self,context):
#         self._check_print(os.path.exists(self.dst),self.dst)
#     def _clean(self,context):
#         cmdtpl ="if  test -e $DST ; then rm -f $DST ;fi"
#         cmd = Template(cmdtpl).substitute(DST=self.dst)
#         self.execmd(cmd)
#
#     def proc_file(self,arg,dirname,names):
#         names = sorted(names)
#         for n in names:
#             if re.match(self.filter, n):
#                 src_path = os.path.join(dirname , n )
#                 self.dstfile.write("\n%s file: %s\n" %(self.note,src_path))
#                 self.dstfile.write("%s ------------------------------\n" %(self.note))
#                 if not os.path.exists(src_path) :
#                     warn_msg = "file_merge %s not exists" %src_path
#                     print("warning:  %s" %warn_msg)
#                     rg_logger.warning(warn_msg)
#                     continue
#                 with open(src_path,'r') as srcfile :
#                     for line in srcfile:
#                         self.dstfile.write(line)
#
# class merge(resource,restag_file):
#     """
#     !R.file_merge
#         dst : "$${PRJ_ROOT}/conf/used/my.conf
#         files:
#             - "$${PRJ_ROOT}/a.conf"
#             - "$${PRJ_ROOT}/b.conf"
#     """
#     _files = []
#     _dst = None
#
#     def _before(self,context):
#         self.efiles= []
#         self.dst = env_exp.value(self.dst)
#         for v in self.files:
#             v=  env_exp.value(v)
#             self.efiles.append( v )
#     def _config(self,context):
#         self.execmd(Template("cat /dev/null > $DST; " ).substitute(DST=self.dst))
#         cmdtpl ="cat $SRC >> $DST ;"
#         for v in self.efiles:
#             cmd = Template(cmdtpl).substitute(SRC=v,DST=self.dst)
#             self.execmd(cmd)
#     def _check(self,context):
#         self._check_print(os.path.exists(self.dst),self.dst)
#     def _clean(self,context):
#         cmdtpl ="if  test -e $DST ; then rm -f $DST ; fi  "
#         cmd = Template(cmdtpl).substitute(DST=self.dst)
#         self.execmd(cmd)
#

class intertpl(interface.resource,res_utls):
    """
    !R.tpl
       tpl = "${PRJ_ROOT}/conf/used/ngx.conf"
       dst = "${PRJ_ROOT}/conf/tpl/ngx.conf"
    """
    dst = ""
    tpl = ""
    def _before(self,context):
        self.dst  = utls.rg_var.value_of(self.dst)
        self.tpl  = utls.rg_var.value_of(self.tpl)

    def _config(self,context):
        import utls.tpl
        utls.tpl.tplworker().execute(self.tpl,self.dst)

    def _check(self,context):
        self._check_print(os.path.exists(self.dst),self.dst)

    def _clean(self,context):
        cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi "
        cmd = Template(cmdtpl).substitute(DST=self.dst)
        self.execmd(cmd)

    def _info(self):
        return self.dst
    def _depend(self,m,context):
        m._check_writeable(self.dst)

class tpl_builder:
    @staticmethod
    def build(tplfile,dstfile):
        tpl=open(tplfile, 'r')
        dst=open(dstfile, 'w')
        for line in tpl:
            data= utls.rg_var.value_of(line)
            dst.write(data)

class file_tpl(interface.resource,res_utls):
    """
    !R.tpl
       tpl = "${PRJ_ROOT}/conf/used/ngx.conf"
       dst = "${PRJ_ROOT}/conf/tpl/ngx.conf"
    """
    dst    = ""
    tpl    = ""
    mod    = "o+w"

    def _before(self,context):
        self.dst        = utls.rg_var.value_of(self.dst)
        self.tpl        = utls.rg_var.value_of(self.tpl)
        self.mod        = utls.rg_var.value_of(self.mod)
        utls.check.must_true(os.path.exists(self.tpl),"tpl not exists : %s" %(self.tpl))

    def _config(self,context):
        tpl_builder.build(self.tpl,self.dst)
        self.execmd("chmod %s %s " %(self.mod, self.dst))

    def _path(self,context):
        return  self.dst

    def _check(self,context):
        self._check_print(os.path.exists(self.dst),self.dst)

    def _clean(self,context):
        cmdtpl ="if test -e $DST ; then rm -rf  $DST ; fi "
        cmd = Template(cmdtpl).substitute(DST=self.dst)
        self.execmd(cmd)
    def _info(self,context):
        rgio.struct_out("file_tpl")
        rgio.struct_out("tpl: %s" %self.tpl ,1)
        rgio.struct_out("dst: %s" %self.dst ,1)
