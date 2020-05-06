#!/usr/bin/env python3
# coding: utf-8

################################################################################
# BLE Logger SW GATT
#
# git clone https://github.com/bokunimowakaru/ble.git
#
#                                          Copyright (c) 2019-2020 Wataru KUNINO
################################################################################

#【インストール方法】
#   bluepy (Bluetooth LE interface for Python)をインストールしてください
#       sudo pip3 install bluepy
#
#【実行方法】
#   実行するときは sudoを付与してください
#       sudo ./ble_logger_sens_scan.py &
#
#【参考文献】
#   本プログラムを作成するにあたり下記を参考にしました
#   https://ianharvey.github.io/bluepy-doc/scanner.html
#   https://ianharvey.github.io/bluepy-doc/notifications.html

ambient_chid='00000'                # ここにAmbientで取得したチャネルIDを入力
ambient_wkey='0123456789abcdef'     # ここにはライトキーを入力
ambient_interval = 30               # Ambientへの送信間隔
interval = 1.01                     # 動作間隔
savedata = True                     # ファイル保存の要否
username = 'pi'                     # ファイル保存時の所有者名
udp_sendto = '255.255.255.255'      # UDP送信宛先
udp_port   = 1024                   # UDP送信先ポート番号
udp_suffix = '4'                    # UDP送信デバイス名に付与する番号
udp_interval = 30                   # UDP/GATT送信間隔
target_rssi = -60                   # 接続対象デバイスの最低受信強度

# ここに接続するデバイス名とサービスUUIDを入力 ## Nordicは動作未確認
target_devices = [  'cq_ex21_ble_led',\
                    'cq_ex22_ble_sw',\
                    'Nordic_Blinky',\
                    'RBLE-DEV',\
                    'AB Shutter3       ']
target_services = [ '00001523-1212-efde-1523-785feabcd123',\
                    '00001523-1212-efde-1523-785feabcd123',\
                    '00001523-1212-efde-1523-785feabcd123',\
                    '58831926-5f05-4267-ab01-b4968e8efce0',\
                    '00001812-0000-1000-8000-00805f9b34fb']
notify_cnf_hnd = [0x000e, 0x000e, 0x000e, 0x0013, 0x0014]
notify_val_hnd = [0x000d, 0x000d, 0x000d, 0x0012, 0x0013]

from bluepy import btle
from bluepy.btle import Peripheral, DefaultDelegate
from sys import argv
import getpass
from shutil import chown
from time import sleep
import urllib.request                           # HTTP通信ライブラリを組み込む
import json                                     # JSON変換ライブラリを組み込む
import datetime
import subprocess
import socket

url_s = 'https://ambidata.io/api/v2/channels/'+ambient_chid+'/data' # アクセス先
head_dict = {'Content-Type':'application/json'} # ヘッダを変数head_dictへ

class MyDelegate(DefaultDelegate):

    def __init__(self, params):
        DefaultDelegate.__init__(self)
        self.index = -1
        self.val = b'\x00'

    def handleNotification(self, cHandle, data):
        if self.index < 0:
            return
        print('\nHandle =',hex(cHandle),', Notify =',data.hex())
        if cHandle == notify_val_hnd[self.index]:
            self.val = data

    def value(self):
        return self.val

def udp_sender(udp):
    if udp_port <= 0:
        return
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # ソケットを作成
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    except Exception as e:                                  # 例外処理発生時
        print('ERROR:',e)                                            # エラー内容を表示
        exit()                                              # プログラムの終了
    if sock:                                                # 作成に成功したとき
        udp = udp.strip('\r\n')                             # 改行を削除してudpへ
        print('UDP Sender =', udp)
        udp=(udp + '\n').encode()                           # 改行追加とバイト列変換
        sock.sendto(udp,('255.255.255.255',udp_port))       # UDPブロードキャスト送信
        sock.close()                                        # ソケットの切断

def udp_sender_sensor(sensors):
    d1 = sensors.get('Temperature')
    d2 = sensors.get('Humidity')
    d3 = sensors.get('Pressure')
    if d1 is not None:
        if d2 is not None and d3 is None and d2 != 0.:
            udp_sender( 'humid_' + udp_suffix + ',' + str(round(d1,2)) + ' ,' + str(round(d2,2)) )
            return
        if d2 is None and d3 is not None:
            udp_sender( 'press_' + udp_suffix + ',' + str(round(d1,2)) + ' ,' + str(round(d3,3)) )
            return
        if d2 is not None and d3 is not None:
            udp_sender( 'envir._' + udp_suffix + ',' + str(round(d1,2)) + ' ,' + str(round(d2,2)) + ' ,' + str(round(d3,3)) )
            return
        udp_sender( 'temp._' + udp_suffix + ',' + str(round(d1,2)) )
        return
    d1 = sensors.get('Illuminance')
    if d1 is not None:
        udp_sender( 'illum_' + udp_suffix + ',' + str(d1) )
        return
    if len(sensors.get('Button')) >= 4:
        udp_sender( 'btn_s_' + udp_suffix + ',' + sensors['Button'][3]\
                                         + ', ' + sensors['Button'][2]\
                                         + ', ' + sensors['Button'][1]\
                                         + ', ' + sensors['Button'][0])
        return

def save(filename, data):
    try:
        fp = open(filename, mode='a')                   # 書込用ファイルを開く
    except Exception as e:                              # 例外処理発生時
        print('ERROR:',e)                                        # エラー内容を表示
    fp.write(data + '\n')                               # dataをファイルへ
    fp.close()                                          # ファイルを閉じる
    chown(filename, username, username)                 # 所有者をpiユーザへ

def payval(num, bytes=1, sign=False):
    global val
    a = 0
    if num < 2 or len(val) < (num - 2 + bytes) * 2:
        print('ERROR: data length',len(val))
        return 0
    for i in range(0, bytes):
        a += (256 ** i) * int(val[(num - 2 + i) * 2 : (num - 1 + i) * 2],16)
    if sign:
        if a >= 2 ** (bytes * 8 - 1):
            a -= 2 ** (bytes * 8)
    return a

def printval(dict, name, n, unit):
    value = dict.get(name)
    if value == None:
        return
    if type(value) is not str:
        if n == 0:
            value = round(value)
        else:
            value = round(value,n)
    print('    ' + name + ' ' * (14 - len(name)) + '=', value, unit, end='')
    if name == 'Accelerometer' or name == 'Geomagnetic':
        print(' (',round(sensors[name + ' X'],n),\
            round(sensors[name + ' Y'],n),\
            round(sensors[name + ' Z'],n), unit + ')')
    else:
        print()

def parser(dev):
    sensors = dict()
    sensors['isRohmMedal'] = None
    sensors['service'] = None
    sensors['index'] = None
    sensors['vals'] = None
    for (adtype, desc, value) in dev.getScanData():
        print("  %3d %s = %s (%d)" % (adtype, desc, value, len(value)))  # ad_t=[{8:'Short Local Name'},{9:'Complete Local Name'}]

        # GATT サービス
        if (adtype == 2 or adtype == 7) and (value in target_services):
            sensors['service'] = value
            sensors['index'] = target_services.index(value)
        if (adtype == 8 or adtype == 9) and (value in target_devices):
            sensors['isRohmMedal'] = value
            sensors['index'] = target_devices.index(value)

        # ビーコンデータ
        if desc == 'Manufacturer':
            sensors['vals'] = value

    print('    isRohmMedal   =',sensors['isRohmMedal'], '(' + str(sensors['index']) + ')')
    return sensors


# MAIN
if getpass.getuser() != 'root':
    print('使用方法: sudo', argv[0], '[対象MACアドレス]...')
    exit()
scanner = btle.Scanner()
time_amb = 999
time_udp = 999
if ambient_interval < 30:
    ambient_interval = 30
val = ''

while True:
    # BLEスキャン
    try:
        devices = scanner.scan(interval)
    except Exception as e:
        print("ERROR",e)
        print("Rebooting HCI, please wait...")
        subprocess.call(["hciconfig", "hci0", "down"])
        sleep(5)
        subprocess.call(["hciconfig", "hci0", "up"])
        sleep(interval)
        continue
    sensors = dict()
    target_index = None
    isRohmMedal = None
    address = None
    addrType = 'random'

    # 受信データについてBLEデバイス毎の処理
    for dev in devices:
        if dev.rssi < target_rssi:
            continue
        print("\nDevice %s (%s), RSSI=%d dB, Connectable=%s" % (dev.addr, dev.addrType, dev.rssi, dev.connectable))
        if len(argv) == 1:
            sensors = parser(dev)
        else:
            for i in range(1, len(argv)):
                if argv[i].lower() == dev.addr:
                    sensors = parser(dev)
        target_index = sensors.get('index')
        if target_index is not None:
            isRohmMedal = sensors.get('isRohmMedal')
            address = dev.addr
            addrType = dev.addrType
            # print("    9 Complete Local Name =",isRohmMedal)
            break
    if (target_index is None) or (isRohmMedal is None) or (address is None):
        continue  # スキャンへ戻る

    # GATT処理部1.接続
    print('GATT Connect to',address,isRohmMedal,'(' + str(target_index) + ')')
    try:
        p = Peripheral(address, addrType = addrType)
    except btle.BTLEDisconnectError as e:
        print('ERROR:',e)
        continue # スキャンへ戻る
    myDelegate = MyDelegate(DefaultDelegate)
    myDelegate.index = target_index
    p.setDelegate(myDelegate)

    # GATT処理部2.サービス確認
    svcs = p.getServices();
    print('CONNECTED')
    for svc in svcs:
        print(svc)
    try:
        svc = p.getServiceByUUID(target_services[target_index])
    except btle.BTLEGattError as e:
        print('ERROR:',e)
        print('no service,',target_services[target_index])
        p.disconnect()
        del p
        continue  # スキャンへ戻る

    # GATT処理部3.Notify登録 Setup to turn notifications on
    hnd = notify_cnf_hnd[target_index]
    data = b'\x01\x00'
    print('write Notify Config =', hex(hnd), data.hex(), end=' > ')
    print(p.writeCharacteristic(hnd, data, withResponse=True).get('rsp'))

    val = p.readCharacteristic(hnd)
    print('read  Notify Config =', hex(hnd), val.hex() )
    if val != data:
        print('ERROR: Notifications Setting')
        p.disconnect()
        del p
        continue # スキャンへ戻る

    # GATT処理部4.Notify待ち受け
    print('Waiting for Notify...')
    while True:
        try:
            notified = p.waitForNotifications(interval)
        except btle.BTLEDisconnectError as e:
            print('ERROR:',e)
            del notified
            break
        time_udp += interval
        time_amb += interval
        if notified:
            notified_val = myDelegate.value()
            if (type(notified_val) is bytes) and len(notified_val) > 0:
                print('    Value =',notified_val.hex())
                sensors['Button'] = format(notified_val[0], '04b')

            # センサ個別値のファイルを保存
            date=datetime.datetime.today()
            if savedata:
                for sensor in sensors:
                    if (sensor.find(' ') >= 0 or len(sensor) <= 5 or sensor == 'Magnetic') and sensor != 'Color R':
                        continue
                    s = date.strftime('%Y/%m/%d %H:%M')
                    # s += ', ' + sensor
                    if sensor == 'isRohmMedal' or sensor == 'service' or sensor == 'index' or sensor == 'vals':
                        continue
                    if sensor == 'Button':
                        s += ', ' + sensors['Button'][3]
                        s += ', ' + sensors['Button'][2]
                        s += ', ' + sensors['Button'][1]
                        s += ', ' + sensors['Button'][0]
                    else:
                        s += ', ' + str(round(sensors[sensor],3))
                    if sensor == 'Color R':
                        s += ', ' + str(round(sensors['Color R'],3))
                        s += ', ' + str(round(sensors['Color G'],3))
                        s += ', ' + str(round(sensors['Color B'],3))
                        s += ', ' + str(round(sensors['Color IR'],3))
                        sensor = 'Color'
                    if sensor == 'Accelerometer':
                        s += ', ' + str(round(sensors['Accelerometer X'],3))
                        s += ', ' + str(round(sensors['Accelerometer Y'],3))
                        s += ', ' + str(round(sensors['Accelerometer Z'],3))
                    if sensor == 'Geomagnetic':
                        s += ', ' + str(round(sensors['Geomagnetic X'],3))
                        s += ', ' + str(round(sensors['Geomagnetic Y'],3))
                        s += ', ' + str(round(sensors['Geomagnetic Z'],3))
                    # print(s, '-> ' + sensor + '.csv') 
                    save(sensor + '.csv', s)

            # UDP送信
            if time_udp >= udp_interval / interval:
                time_udp = 0
                udp_sender_sensor(sensors)

            # クラウドへの送信処理
            if time_amb >= ambient_interval / interval:
                time_amb = 0
                body_dict = {'writeKey':ambient_wkey}
                body_dict['d1'] = sensors.get('Temperature')
                body_dict['d2'] = sensors.get('Humidity')
                if not body_dict['d2']:
                    body_dict['d2'] = sensors.get('Proximity')
                body_dict['d3'] = sensors.get('Pressure')
                body_dict['d4'] = sensors.get('Illuminance')
                if len(sensors.get('Button')) >= 4:
                    for i in range(4):
                        if body_dict['d' + str(i+1)] is None:
                            body_dict['d' + str(i+1)] = sensors['Button'][3-i]
                body_dict['d5'] = sensors.get('Accelerometer')
                body_dict['d6'] = sensors.get('Geomagnetic')
                body_dict['d7'] = sensors.get('Steps')
                if body_dict['d7'] is None:
                    body_dict['d7'] = sensors.get('Color R')
                body_dict['d8'] = sensors.get('Battery Level')
                if body_dict['d8'] is None:
                    body_dict['d8'] = sensors.get('Color IR')

                for i in range(8):
                    if body_dict['d' + str(i+1)] is None:
                        del body_dict['d' + str(i+1)]
                print(head_dict)                                # 送信ヘッダhead_dictを表示
                print(body_dict)                                # 送信内容body_dictを表示
                if int(ambient_chid) != 0:
                    post = urllib.request.Request(url_s, json.dumps(body_dict).encode(), head_dict)
                                                                    # POSTリクエストデータを作成
                    try:                                            # 例外処理の監視を開始
                        res = urllib.request.urlopen(post)          # HTTPアクセスを実行
                    except Exception as e:                          # 例外処理発生時
                        print(e,url_s)                              # エラー内容と変数url_sを表示
                    res_str = res.read().decode()                   # 受信テキストを変数res_strへ
                    res.close()                                     # HTTPアクセスの終了
                    if len(res_str):                                # 受信テキストがあれば
                        print('Response:', res_str)                 # 変数res_strの内容を表示
                    else:
                        print('Done')                               # Doneを表示
    p.disconnect()
    del p
    continue # スキャンへ戻る


''' Gatt Toolを使った接続テストの例

Nordic
pi@raspberrypi:~ $ gatttool -I -t random -b xx:xx:xx:xx:xx:xx
[xx:xx:xx:xx:xx:xx][LE]> connect
Attempting to connect to xx:xx:xx:xx:xx:xx
Connection successful
[xx:xx:xx:xx:xx:xx][LE]> primary
attr handle: 0x0001, end grp handle: 0x0009 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x000a, end grp handle: 0x000a uuid: 00001801-0000-1000-8000-00805f9b34fb
attr handle: 0x000b, end grp handle: 0xffff uuid: 00001523-1212-efde-1523-785feabcd123 <-- Genサービス
[xx:xx:xx:xx:xx:xx][LE]> char-desc 0x000b
handle: 0x000b, uuid: 00002800-0000-1000-8000-00805f9b34fb
handle: 0x000c, uuid: 00002803-0000-1000-8000-00805f9b34fb
handle: 0x000d, uuid: 00001524-1212-efde-1523-785feabcd123 <-- Read Notify
handle: 0x000e, uuid: 00002902-0000-1000-8000-00805f9b34fb <-- Read Notify Client Char Config
handle: 0x000f, uuid: 00002803-0000-1000-8000-00805f9b34fb
handle: 0x0010, uuid: 00001525-1212-efde-1523-785feabcd123 <-- LEDキャラクタリスティクス・ディスクリプタ
[xx:xx:xx:xx:xx:xx][LE]> char-read-hnd 000e
Characteristic value/descriptor: 00 00
[xx:xx:xx:xx:xx:xx][LE]> char-write-req 000e 01 00
Characteristic value was written successfully
Notification handle = 0x000d value: 01
Notification handle = 0x000d value: 00
Notification handle = 0x000d value: 01
Notification handle = 0x000d value: 00
------------------------------------------------------------------------------------------
RX21W
pi@raspberrypi:~/ble $ gatttool -I -t random -b xx:xx:xx:xx:xx:xx
[xx:xx:xx:xx:xx:xx][LE]> connect
Attempting to connect to xx:xx:xx:xx:xx:xx
Connection successful
[xx:xx:xx:xx:xx:xx][LE]> primary
attr handle: 0x0001, end grp handle: 0x000b uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x000c, end grp handle: 0x000f uuid: 00001801-0000-1000-8000-00805f9b34fb
attr handle: 0x0010, end grp handle: 0x0015 uuid: 58831926-5f05-4267-ab01-b4968e8efce0
[xx:xx:xx:xx:xx:xx][LE]> char-desc 0x0010
handle: 0x0010, uuid: 2a042a01-2a00-1800-2803-280228012800
handle: 0x0011, uuid: 00002803-0000-1000-8000-00805f9b34fb
handle: 0x0012, uuid: 58837f57-5f05-4267-ab01-b4968e8efce0 <-- Read Notify
handle: 0x0013, uuid: 00002902-0000-1000-8000-00805f9b34fb <-- Read Notify Client Char Config
handle: 0x0014, uuid: 00002803-0000-1000-8000-00805f9b34fb
handle: 0x0015, uuid: 5883c32f-5f05-4267-ab01-b4968e8efce0 <-- LEDキャラクタリスティクス・ディスクリプタ
[xx:xx:xx:xx:xx:xx][LE]> char-read-hnd 0x0012
Error: Characteristic value/descriptor read failed: Attribute can't be read
[xx:xx:xx:xx:xx:xx][LE]> char-read-hnd 0x0015
Characteristic value/descriptor: 00
[xx:xx:xx:xx:xx:xx][LE]> char-write-req 0x0013 01 00
Characteristic value was written successfully
Notification handle = 0x0012 value: 01
Notification handle = 0x0012 value: 01
'''
