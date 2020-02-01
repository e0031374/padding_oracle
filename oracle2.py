import requests

cTotal = "0e2c2fcfe136b5e94d12afb02055bf2180a53343add3f3efb8fa0606cd22c6d90788e5cd1c876437a18ae7f2e45517d3547b9f5cd98a4b34a33bd26c36581a70f988febe2487007ef3989f4aa9871680"

#c2 = "80a53343add3f3efb8fa0606cd22c6d9"
#c3 = "0788e5cd1c876437a18ae7f2e45517d3"
#c4 = "547b9f5cd98a4b34a33bd26c36581a70"
#c5 = "f988febe2487007ef3989f4aa9871680"
blockNo = 1
c4 = cTotal[(blockNo - 1) * 32:blockNo * 32]
c5 = cTotal[blockNo * 32: (blockNo + 1) * 32]
print("c4: " + c4)
print("c5: " + c5)

i5 = ["-1", "-1", "-1","-1","-1","-1","-1","-1","-1","-1","-1","-1","-1","-1","-1","-1","-1"] 

#arguments are strings of hex only
def c4prime_gen(pad, cell):
    cell_str = str(cell)
    print("pad: " + pad + " cell: " + cell_str)
    i5cell = i5[int(cell_str)]
    if(i5cell == "-1"):
        print("error")
    i5cellhex = int(i5cell, 16)
    padhex = int(pad, 16)
    return hex(padhex ^ i5cellhex) 

#print(str(c4prime_gen("03", "16")))

def xoracle(a,b):
    print("xoracle a: " + a)
    a2 = int(a,16)
    b2 = int(b,16)
    return hex(a2 ^ b2)

url = "http://ctf.noi-sg.com:2773/"
p5 = ""


for v in range(16):
    #note v starts with 0
    c4prime_end = ""
    fromback = v + 1 
    print(fromback)
    padn = hex(fromback)
    
    for w in range(fromback - 1):
        #c4'[n]
        c4prime_atn = c4prime_gen(padn, 16 - w).zfill(2)
        print("c4prime_atn: " + c4prime_atn)
        c4prime_atn = c4prime_atn[2:].zfill(2)
        print("c4prime_atn: " + c4prime_atn)
        c4prime_end = c4prime_atn + c4prime_end
    
    element = 16 - fromback + 1
    c4prime = ""
    
    
    for x in range(255):
        cprime = str(hex(x)[2:]) + c4prime_end
        cprime = cprime.zfill(32)
#        c5 = "f988febe2487007ef3989f4aa9871680"
        payload = cprime + c5
    #    print(payload)
        payload = {'ciphertext':payload}
        r = requests.post(url, payload)
        with open("requests_results.html", "w") as f:
        #    print(r.content)
            f.write(r.content.decode("utf-8"))
        
        if 'Decryption was successful' in open("requests_results.html").read():
            print("Success " + cprime)
            c4prime = cprime
            break
        if 'Error: Invalid hex string' in open("requests_results.html").read():
            print("error invalid hex string")
        if 'Error: Invalid padding' in open("requests_results.html").read():
            print("Error: Invalid padding " + cprime)
    
    c4prime_atn = c4prime[len(c4prime) - 2*(fromback):len(c4prime) - 2*(fromback - 1) ]
    print("c4prime_atn " + c4prime_atn)
    #i5[n]
    i5[element] = xoracle(c4prime_atn, padn)
    print("i5[element] " + i5[element])
    # c4[n]
    c4_atn = c4[len(c4prime) - 2*(fromback):len(c4prime) - 2*(fromback - 1) ]
    # p5[n]
    p5_atn = str(xoracle(c4_atn, i5[element]))
    p5 = p5_atn[2:].zfill(2) + p5
    print(p5)


print("p5 " + p5)

