import logging
import requests
import urllib.parse
from queue import Queue
import threading
import time
import json
from io import BytesIO
from hdfs import InsecureClient
#setup client connect hadoop

 # dia chi luu file tren namenode hadoop

#setup crawl
cookie = '__wpkreporterwid_=09059016-1d58-41a1-844f-286a38370b71; t_fv=1726545547385; t_uid=1bPrBGXvzhkZdZRsTX6IFC0FW4Zc6Pfa; hng=VN|en|VND|704; userLanguageML=en; lwrid=AgGR%2FiJRiKsDu0qM4aUde1x29KZi; lzd_cid=6d1d83ff-bb36-42a5-8cd5-b3b4e6177901; epssw=5*mmLHh7WEONOHiE7khre2xVIp63Ep5UZSzL_KrHRK0Ho3Rl8M8kNKzH8rmtpOrgkEYkbvZ8clHvPyQQpXp2xgbFlmmgm5JJKXsNgMTC1SpEmNWsYYWEEXaemNdSVgdEmNsURrPfwemBPfGsQyV0U1uOcdw2m_YfeUs2bJNeCQ12sMA0ZEn4VsCFbBUqeevMZx6e1QhmmmmeljFwwEPvbXPfPfC587TH6bW9V78mJifyrsEYiLhiwpKP4M62fQ2KakbBYNvblr4jB-dcxV_oTgOV0di8mmmmWmHYkhmLRmmHjFVN..; _m_h5_tk=e8b8d094b3d85f7b149e1000702a9985_1726638988602; _m_h5_tk_enc=82d798244d75103bccc0a3fb9a4ea559; cna=jOxvH6aLAVQCAXRi8zkU6Lzb; isg=BODgWoh9kslaBy7P9G3dyyDIsuey6cSz5ezAMlrxrfuOVYB_A_gWQiCm7WVVfnyL; lwrtk=AAEEZuq9G1JRJUVghqdp/WPlk4+OrfvboKmu/CnmADoM6+fijuKmpT0=; xlly_s=1; lazada_share_info=840093957_1_9300_200321712768_840093957_null; miidlaz=miidgismtl1i81jmeaup04i; exlaz=c_lzd_byr:mm_222591283_65253263_2024253195!vn1296001:clkgismtl1i81jmeamp04h::; lzd_click_id=clkgismtl1i81jmeamp04h; t_sid=grkw7qIEOTJdTK8FVVQLShVbmFP9hAoA; utm_channel=NA; lzd_sid=138dc9486c22622807276da4175d9e15; _tb_token_=eae63ae8e3313; tfstk=fFqnTDAYAEvSxFYwtNoCr0sFOw7xOpiSW7K-w0hP7fl69BKLUTmuK7qRd8k8r5VzZ3BQwDdusDZTJ3hdO02zMmfAMiIYdJix4sCvXsmWF0kP2bJjLTNjV05A6iIYdJi7M-nWuT2NIvHXa0uEzdWipxnyY4-e7Cls_bor8eRwbvMraUleYO2Z1YoraQ198XZzvl5IJVGb_JtUbv0nZyhwmnW-K2c0LfDsClqr-jyEs3ffin_mTxrV6eMm-70aX8pv2ya0nz30S6YnTq2YkDZVsnlu8WNnSPCl46YwuZXyVAW8jUTt8AMiMA3sdrU2JVYNIOY2F2ksLjBGIUTS8AMiMOXMuUgECvbF.; bx-cookie-test=1; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434a2f6f714c634745495733744d54392f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070514d444d774f475a6d4d4441774d4441774d4441774d4441774f44426a4d4441774d4441774d4441774d4441774d4441784d4441774d4441774d4441774d4441304e7a51324d6d597a4d7a6b344d7a49785a4467344e57526a4d44597a5a6a67304d4441774d4441774d44413d222c22733b32223a2238336538333561643136333931323465227d'
nam = "áo"

def Requests_url(name, Page_Num = 1):
    name_ = urllib.parse.quote(name)
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'bx-v': '2.5.14',
        'cookie': f'{cookie}',
        'referer': 'https://www.lazada.vn/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    url = f"https://www.lazada.vn/catalog/?ajax=true&isFirstRequest=true&page={Page_Num}&q={name_}"
    response = requests.get(url , headers=headers)
    if response.status_code == 200:
        try:
            response = response.json()
            Sl_Item = response['mods']['filter']['filteredQuatity']
            List_Item = response['mods']['listItems']
            return Sl_Item , List_Item # trả về 100 (số sản phẩm) , [{},{},{},{},{}] data crawl
        except Exception as e:
            return 0,e
    else:
        return 0,'Khong the ket noi '

p , d = Requests_url(nam)
print(d)
sl_page = int(int(p) // 40)
#data_queue = Queue() # lưu data crawl về
list_queue = Queue() # Lưu number page
print('so' ,sl_page)
for i in range(2,sl_page+1):#sl mới đổi , sl_page+1
    list_queue.put(i)
# lưu vào hdfs
client = InsecureClient('http://127.0.0.1:9870', user = 'cong')
def save_hdfs(data , index):
    try:
        json_data = json.dumps(data, indent = 4 , ensure_ascii=False)
        path_file_hdfs = f'/user/cong/noi_luu_file_hdfs/data_page{index}.json'

        with client.write(path_file_hdfs , overwrite =True) as f:
            f.write(json_data.encode('utf-8'))

        logging.info(f'da lu thanh cong {path_file_hdfs}')
    except Exception as e:
        logging.error(f'loi khi tai len hdfs {e}')

save_hdfs(d , 1)
# thêm vào queue danh sách các page

# hàm lấy num page từ queue-> Requests -> data -> queue

def data_to_queue(name):
    while not list_queue.empty():
        page = list_queue.get()
        _ , d = Requests_url(name , Page_Num = page) # lấy data từ page 2
        save_hdfs(d , page)
        logging.info('lay_data_page{0}'.format(page))
        list_queue.task_done()# kiểm tra xem nó hoàn thành chưa
        print('da crawl_data {}'.format(page))
        time.sleep(0.5)

# luồng xử lý crawl -> queue
Thread_queue = list()
for i in range(1 ,5):
    thread = threading.Thread(target=data_to_queue , args=(nam,))
    thread.start()
    Thread_queue.append(thread)

for Thread in Thread_queue:
    Thread.join()

list_queue.join()




# lấy từng item từ data_queue([{},{}]) -> json -> lưu vào database
#
#
# def Queue_to_json():
#     while not data_queue.empty():
#         item = data_queue.get()
#         for it in item:
#             #lưu vào hdfs
#             print(it)
#         data_queue.task_done()
#
# # 2 luồng xử lý lưu trữ
# Thread_save = list()
# for i in range(1,3):
#     thread = threading.Thread(target = Queue_to_json)
#     thread.start()
#     Thread_save.append(thread)
#
# for thread in Thread_save:
#     thread.join()
#
# data_queue.join()
# list_queue.join()
# print('\n',l)

# try:
#     # Tạo tên file dựa trên số trang
#     filename = f'/path/to/hdfs/data_page_{page}.json'
#     # Ghi dữ liệu vào HDFS
#     with client.write(filename, overwrite=True) as writer:
#         writer.write(json.dumps(data).encode('utf-8'))
#     print(f"Dữ liệu từ trang {page} đã được lưu vào HDFS")
# except Exception as e:
#     print(f"Lỗi khi lưu dữ liệu vào HDFS: {e}")
