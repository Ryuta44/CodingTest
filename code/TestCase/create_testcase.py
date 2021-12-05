import random
import datetime

TIMEOUT_LIMIT = 4000

# テストデータの作成
if __name__ == '__main__':
    time = datetime.datetime(2020,10,19,13,31)
    second = [24,25,34,35]
    address = ['10.20.30.1/16','10.20.30.2/16','192.168.1.1/24','192.168.1.2/24']
    with open('TestCase/test.txt', 'w') as f:
        for _ in range(10):
            time = time + datetime.timedelta(minutes = 1)
            time_text = time.strftime('%Y%m%d%H%M')
            for i in range(4):
                ping = random.randint(0,5000)
                if ping >= TIMEOUT_LIMIT:
                    ping = '-'
                f.write(f'{time_text}{second[i%4]},{address[i%4]},{ping}\n')

