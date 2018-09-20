import requests
import time
def fetch(res):
    print('we have fired this off')
    return res.text

def main():
    start = time.time()
    tes = fetch(requests.get('https://httpbin.org/get'))
    print('we are before')
    print(tes)
    print('we are after')
    end = time.time()
    print(start-end)

main()
