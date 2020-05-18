Bluetooth LE Peripheral Demo Firmware for Renesas RX23W Target Board  
# Bluetooth LE 温度センサ rx23w_temperature.mot  

ハード改造不要! コンパイル不要! Renesas RX23W Target Board 用  
## Bluetooth LE 温度センサ で Blueotooth を体験しよう  
by Wataru KUNINO [bokunimo.net](https://bokunimo.net/)  

--------------------------------------------------------------------------------

## 内容

ルネサス製 Bluetooth LE ターゲット・ボード RX23W Target Board 内蔵の 温度センサ
で測定した 温度値を、Bletooth 送信します。  
送信した Bluetooth 信号の受信には、[ble_logger_gatt.py](../ble_logger_gatt.py)が
利用できます。受信した温度値を UDP/IP でLAN内に転送したり、IoTセンサ用クラウド・
サービス[Ambient](http://ambidata.io)で蓄積し、グラフ表示することも出来ます。  

--------------------------------------------------------------------------------

## 書き込み方法

以下にボードへの書き込み手順を示します。

1.	[rx23w_temperature.mot](https://github.com/bokunimowakaru/ble/tree/master/rx23w_temperature)の保存  
	PC へダウンロードして下さい。

2.	Renesas Flash Programmer のダウンロード  
	[ルネサス社のウェブサイト](https://www.renesas.com/)にて、キーワード「 Renesas
	Flash Programmer 」で検索を行い、検索結果「製品情報」に含まれる Flash Programmer
	( Programming GUI )をダウンロードし、パソコンへインストールし、起動してください。

3.	RX23W 用 ターゲット・ボードの接続  
	RX23W 用 ターゲット・ボード上の DIPスイッチESW1 の左側（2番）を下向きにスライドし、
	USBケーブルでパソコンに接続すると、エミュレータ部の LED ACT が点滅を開始します。

4.	Renesas Flash Programmer 用プロジェクトの作成  
	Renesas Flash Programmer のメニュー[ファイル]から新しいプロジェクトの作成を実行し、
	項目「マイクロコントローラ」で[RX200]を選択し、プロジェクト名と作成場所を設定し、
	項目「ツール」で[E2 Emulator Lite]を、項目「インタフェース」で[FINE]を選択して
	ください。[接続]をクリックすると、RX23W用ターゲット・ボードとの接続が実行されます。

5.	RX23W用ターゲット・ボードへの書き込み  
	ファイルのパスを、「プログラムファイル」に入力し、[スタート]ボタンで書き込みを
	開始します。IDコードの入力を促された場合は、「45FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF」を
	入力します。

6.	「正常終了」が表示されたら、DIPスイッチを元に戻します（2つとも上向き・OFF）。

--------------------------------------------------------------------------------

## 本ソフトの Service UUID と、Characteristic UUID

### gattool での 動作確認結果

	pi@raspberrypi:~/ble $ sudo ./ble_logger_gatt.py

	Device 51:45:d5:XX:XX:XX (random), RSSI=-39 dB, Connectable=True
	    1 Flags = 1a (2)
	   10 Tx Power = 0c (2)
	  255 Manufacturer = 4c0010051c18445edd (18)
	    isTargetDev   = None (None)

	Device d0:69:e2:XX:XX:XX (random), RSSI=-43 dB, Connectable=True
	    1 Flags = 06 (2)
	    9 Complete Local Name = RBLE-TEMP (9)
	    isTargetDev   = RBLE-TEMP (4)

	GATT Connect to d0:69:e2:XX:XX:XX RBLE-TEMP (4)
	CONNECTED
	Service <uuid=Generic Attribute handleStart=12 handleEnd=15>
	Service <uuid=97e780d0-6fca-4d8d-8c95-e02c5dfc7c99 handleStart=16 handleEnd=21>
	Service <uuid=Generic Access handleStart=1 handleEnd=11>
	write Notify Config = 0x13 0100 > ['wr']
	read  Notify Config = 0x13 0100
	Waiting for Notify...

	dev =4, Handle = 0x12, Notify = 2d0c
	    Temperature   = 31.17 ℃

	dev =4, Handle = 0x12, Notify = 2d0c
	    Temperature   = 31.17 ℃

	UDP/192.168.0.255/1024 = temp._4,31.17

### gattool での 動作確認結果

	pi@raspberrypi:~/ble $ sudo hcitool lescan

	LE Scan ...
	68:A0:82:XX:XX:XX (unknown)
	F8:80:EB:XX:XX:XX nRF5x
	7F:25:F3:XX:XX:XX (unknown)
	7F:25:F3:XX:XX:XX (unknown)
	D0:69:E2:XX:XX:XX RBLE-TEMP		<-- rx23w_temperature.mot
	51:45:D5:XX:XX:XX (unknown)
	D0:69:E2:XX:XX:XX RBLE-TEMP		<-- rx23w_temperature.mot
	47:AE:30:XX:XX:XX (unknown)
	47:AE:30:XX:XX:XX (unknown)
	51:5E:CD:XX:XX:XX (unknown)
	44:F6:EF:XX:XX:XX (unknown)
	44:F6:EF:XX:XX:XX (unknown)
	E8:A0:3C:XX:XX:XX nRF5x
	51:45:D5:XX:XX:XX (unknown)
	51:5E:CD:XX:XX:XX (unknown)
	68:A0:82:XX:XX:XX (unknown)
	^C
	pi@raspberrypi:~/ble $ gatttool -I -t random -b D0:69:E2:XX:XX:XX

	[D0:69:E2:XX:XX:XX][LE]> connect
	Attempting to connect to D0:69:E2:XX:XX:XX
	Connection successful

	[D0:69:E2:XX:XX:XX][LE]> primary
	attr handle: 0x0001, end grp handle: 0x000b uuid: 00001800-0000-1000-8000-00805f9b34fb
	attr handle: 0x000c, end grp handle: 0x000f uuid: 00001801-0000-1000-8000-00805f9b34fb
	attr handle: 0x0010, end grp handle: 0x0015 uuid: 97e780d0-6fca-4d8d-8c95-e02c5dfc7c99

	[D0:69:E2:XX:XX:XX][LE]> char-desc
	handle: 0x0001, uuid: 00002800-0000-1000-8000-00805f9b34fb
	handle: 0x0002, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x0003, uuid: 00002a00-0000-1000-8000-00805f9b34fb
	handle: 0x0004, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x0005, uuid: 00002a01-0000-1000-8000-00805f9b34fb
	handle: 0x0006, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x0007, uuid: 00002a04-0000-1000-8000-00805f9b34fb
	handle: 0x0008, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x0009, uuid: 00002aa6-0000-1000-8000-00805f9b34fb
	handle: 0x000a, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x000b, uuid: 00002ac9-0000-1000-8000-00805f9b34fb
	handle: 0x000c, uuid: 00002800-0000-1000-8000-00805f9b34fb
	handle: 0x000d, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x000e, uuid: 00002a05-0000-1000-8000-00805f9b34fb
	handle: 0x000f, uuid: 00002902-0000-1000-8000-00805f9b34fb
	handle: 0x0010, uuid: 2a042a01-2a00-1800-2803-280228012800
	handle: 0x0011, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x0012, uuid: 00002a6e-0000-1000-8000-00805f9b34fb <-- 温度測定
	handle: 0x0013, uuid: 00002902-0000-1000-8000-00805f9b34fb <-- 自動送信
	handle: 0x0014, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x0015, uuid: 5883c32f-5f05-4267-ab01-b4968e8efce0

	(温度を測定する)
	[D0:69:E2:XX:XX:XX][LE]> char-read-hnd 0x0012
	Characteristic value/descriptor: 2d 00

	(温度測定結果を自動送信する)
	D0:69:E2:XX:XX:XX][LE]> char-write-req 0x0013 01 00
	Characteristic value was written successfully
	Notification handle = 0x0012 value: 17 0c
	Notification handle = 0x0012 value: 17 0c
	Notification handle = 0x0012 value: 2d 0c
	Notification handle = 0x0012 value: 2d 0c
	Notification handle = 0x0012 value: 17 0c

--------------------------------------------------------------------------------
## 技術情報
技術情報については、[本ページの情報](https://github.com/bokunimowakaru/ble/tree/master/README.md)ならびに、ルネサス社の[RX23Wグループ BLE Module Firmware Integration Technology アプリケーションノート（r01an4860xx0110-rx23w-ble-fit.zip）](https://www.renesas.com/jp/ja/software/D6004123.html)などを参照ください。  

## 補償およびサポート  
当方は、本ソフトウェア（rx23w_temperature.mot）に関する補償ならびにサポートを、
一切、いたしません。

## ソースコード  
配布いたしません。

## 権利情報  
本サンプルはルネサス社が配布するサンプル・ソフトウェアble_demo_tbrx23w_profile_serverをベースに、作成しました。  
改変部以外の権利はルネサス社に帰属し、改変部の権利は当方に帰属します。  


