import datetime

LOG_FILE = 'TestCase/test3.txt'
OUTPUT_FILE = 'Results/result_q3.txt'
COUNT_LIMIT = 3 # タイムアウトの回数制限
JUDGE_COUNT = 3 # 参照する直近のログの数
LIMIT_AVARAGE_RESPONSE = 300 # 平均応答時間の制限

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

def output_failure(server_log,count_limit=1):
    output = []
    for address in server_log:
        fault_flag = 0   # タイムアウトが連続している場合は'1',それ以外は'0'
        count = 0   # タイムアウトの連続回数
        fault = {}
        for log in server_log[address]:
            if fault_flag == 0 and log[1] == '-':   #タイムアウトの開始時の処理
                fault['type'] = 'failure'
                fault['address'] = address
                fault['start_time'] = log[0]
                fault_flag = 1
                count = 1
            elif fault_flag == 1 and log[1] != '-':   # タイムアウトから復活時の処理
                if count >= count_limit:    # 連続した回数がcount_limit以上だった保存する
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
    return output    # [{'type':'failure', 'address':'10.20.30.2/16', 'start_time':datetime(2020,10,19,13,33,34), 'end_time':datetime(2020,10,19,13,36,34)}]

def output_overload(server_log,judge_num,limit_time):
    output = []
    for address in server_log:
        fault = {}
        flag = 0   #過負荷状態が続いている場合は'1',それ以外は'0'
        ping = [0 for _ in range(judge_num)]   # 直近judge_num回のping値のリスト
        for index, log in enumerate(server_log[address]):
            if log[1]!='-':
                ping[index%judge_num] = int(log[1])
                if flag == 0 and sum(ping) >= limit_time*judge_num:
                    fault['type'] = 'overload'
                    fault['address'] = address
                    fault['start_time'] = server_log[address][index-judge_num+1][0]
                    fault['end_time'] = log[0]
                    flag = 1
                elif flag ==1 and sum(ping) >= limit_time*judge_num:  # pingの合計値が'平均応答時間の制限*参照するlogの数'を超えていたらend_timeを更新する
                    fault['end_time'] = log[0]
                elif flag == 1 and sum(ping) < limit_time*judge_num:
                    output.append(fault)
                    flag = 0
                    fault = {}
            else:   # logがタイムアウトになった時の処理
                if flag == 1:
                    output.append(fault)
                    flag = 0
                ping = [0 for _ in range(judge_num)]   #タイムアウト時はping値をリセット
                ping[index%judge_num] = -10 ** 5   #タイムアウト時を含まないように強大な負の値をセット
    return output    # [{'type':'overload', 'address':'10.20.30.2/16', 'start_time':datetime(2020,10,19,13,33,34), 'end_time':datetime(2020,10,19,13,36,34)}]


if __name__ == '__main__':

    server_log = format_log(LOG_FILE)
    failure_log = output_failure(server_log, COUNT_LIMIT)
    overload_log = output_overload(server_log, JUDGE_COUNT, LIMIT_AVARAGE_RESPONSE)
    error_log = failure_log + overload_log
    error_log.sort(key=lambda x:x['start_time'])
    

    with open(OUTPUT_FILE, 'w') as f:
        result = {}
        for log in error_log:
            if log['address'] not in result:
                result[log['address']] = []
            start = f'{log["start_time"].year}年{log["start_time"].month}月{log["start_time"].day}日 {log["start_time"].hour:02}:{log["start_time"].minute:02}:{log["start_time"].second:02}'
            if log['end_time'] != None:
                end = f'{log["end_time"].year}年{log["end_time"].month}月{log["end_time"].day}日 {log["end_time"].hour:02}:{log["end_time"].minute:02}:{log["end_time"].second:02}'
            else:
                end = '     ----------'
            result[log['address']].append(f'{log["type"]:8} : {start} - {end}')
        for address in result:
            f.write(f'\nIPアドレス:{address}\n')
            for failure_text in result[address]:
                f.write(failure_text+'\n')

""" log終了時に故障していた場合はcountの回数に関係なしに出力する """
