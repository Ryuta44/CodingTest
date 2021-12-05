import datetime
import re

LOG_FILE = 'TestCase/test4.txt'
OUTPUT_FILE = 'Results/result_q4.txt'
COUNT_LIMIT = 4 #Limit of Timeout Count

def format_log(file):
    with open(file) as f:
        data = f.readlines()

    server_log = {}
    for log in data:
        data_element = log.split(',')
        data_time = datetime.datetime.strptime(data_element[0], '%Y%m%d%H%M%S')
        address = data_element[1]
        response_result = data_element[2].rstrip('\n')
        if address not in server_log:
            server_log[address] = [[data_time,response_result]]
        else:
            server_log[address].append([data_time,response_result])
    return server_log    # {'192.168.1.1/24':[[datetime(2020,10,19,13,33,34),372],[datetime(2020,10,19,13,36,34),583]]}

def get_network_address(address):
    server_address = re.split('[./]',address)
    ipaddress = ''
    for i in range(4):
        ipaddress += format(int(server_address[i]), '08b')
    host_number = int(server_address[4])
    binary_network_address = format(int('0b'+ipaddress,0) & (2**32-1 << host_number), '032b')
    network_address = ''
    for i in range(4):
        network_address += str(int(binary_network_address[i*8:i*8+8],2)) + '.'
    return network_address[:-1]

def output_switch_failure(server_log,count_limit=1):
    output = []
    subnet_log = {}   # サブネットアドレス毎のlogのデータを格納する {subnet_address:[datetime,ping]}
    for address in server_log:   # 同サブネットのlogを結合させる
        subnet = get_network_address(address)
        if subnet not in subnet_log:
            subnet_log[subnet] = []
        subnet_log[subnet] += server_log[address]
        subnet_log[subnet].sort(key=lambda x:x[0])
    for subnet_address in subnet_log:
        fault_flag = 0   # タイムアウトが続いている場合は'1',それ以外は'0'
        count = 0
        fault = {}
        for log in subnet_log[subnet_address]:
            if fault_flag == 0 and log[1] == '-':   #タイムアウトの開始時の処理
                fault['type'] = 'failure'
                fault['subnet_address'] = subnet_address
                fault['start_time'] = log[0]
                fault_flag = 1
                count = 1
            elif fault_flag == 1 and log[1] != '-':   # タイムアウトから復活時の処理
                if count >= count_limit:   # 連続した回数がcount_limit以上だった場合,end_timeを更新し保存する。
                    fault['end_time'] = log[0]
                    output.append(fault)
                fault = {}
                fault_flag = 0
                count = 0
            elif fault_flag == 1 and log[1] == '-':
                count += 1
        if fault_flag == 1:   # ログ内でタイムアウトから復活しない場合の処理
            fault['end_time'] = None
            output.append(fault)
            fault = {}
            fault_flag = 0
            count = 0
    return output   # [{'type':'failure', 'subnet_address':'10.20.0.0', 'start_time':datetime(2020,10,19,13,33,34), 'end_time':datetime(2020,10,19,13,36,34)}]


if __name__ == '__main__':
    server_log = format_log(LOG_FILE)
    failure_log = output_switch_failure(server_log, COUNT_LIMIT)

    with open(OUTPUT_FILE, 'w') as f:
        result = {}
        for log in failure_log:
            if log['subnet_address'] not in result:
                result[log['subnet_address']] = []
            start = f'{log["start_time"].year}年{log["start_time"].month}月{log["start_time"].day}日 {log["start_time"].hour:02}:{log["start_time"].minute:02}:{log["start_time"].second:02}'
            if log['end_time'] != None:
                end = f'{log["end_time"].year}年{log["end_time"].month}月{log["end_time"].day}日 {log["end_time"].hour:02}:{log["end_time"].minute:02}:{log["end_time"].second:02}'
            else:
                end = '     ----------'
            result[log['subnet_address']].append(f'{log["type"]} : {start} - {end}')
        for address in result:
            f.write(f'\nサブネットアドレス:{address}\n')
            for failure_text in result[address]:
                f.write(failure_text+'\n')