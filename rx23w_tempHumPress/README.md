Bluetooth LE Peripheral Demo Firmware for Renesas RX23W Target Board  
## Bluetooth LE 温度・湿度・気圧センサ で Blueotooth を体験しよう  

--------------------------------------------------------------------------------

## 内容

ルネサス製 Bluetooth LE ターゲット・ボード RX23W Target Board に環境センサ
BME280（Bosch製）を接続し、温度・湿度・気圧値を、Bletooth 送信します。  
送信した Bluetooth 信号の受信には、[ble_logger_gatt.py](../ble_logger_gatt.py)が
利用できます。受信した温度値を UDP/IP でLAN内に転送したり、IoTセンサ用クラウド・
サービス[Ambient](http://ambidata.io)で蓄積し、グラフ表示することも出来ます。  

--------------------------------------------------------------------------------

## 書き込み方法

以下にボードへの書き込み手順を示します。

1.	[rx23w_temperature.mot](https://github.com/bokunimowakaru/ble/tree/master/rx23w_tempHumPress)の保存  
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

	pi@raspberrypi:~ $ gatttool -I -t public -b 74:90:50:ff:ff:ff
	[74:90:50:ff:ff:ff][LE]> connect
	Attempting to connect to 74:90:50:ff:ff:ff
	Connection successful

	[74:90:50:ff:ff:ff][LE]> primary
	attr handle: 0x0001, end grp handle: 0x000b uuid: 00001800-0000-1000-8000-00805f9b34fb
	attr handle: 0x000c, end grp handle: 0x000f uuid: 00001801-0000-1000-8000-00805f9b34fb
	attr handle: 0x0010, end grp handle: 0x0019 uuid: b2b70000-0001-4cb2-b34a-6550cc0e998c
	attr handle: 0x001a, end grp handle: 0x001d uuid: b2b70000-0003-4cb2-b34a-6550cc0e998c

	[74:90:50:ff:ff:ff][LE]> char-desc
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

	BME280
	handle: 0x0010, uuid: 2a042a01-2a00-1800-2803-280228012800
	handle: 0x0011, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x0012, uuid: 00002a6e-0000-1000-8000-00805f9b34fb Temperature, resolution of 0.01 Celsius
	handle: 0x0013, uuid: 00002902-0000-1000-8000-00805f9b34fb <- Config
	handle: 0x0014, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x0015, uuid: 00002a6f-0000-1000-8000-00805f9b34fb Humidity, resolution of 0.1%
	handle: 0x0016, uuid: 00002902-0000-1000-8000-00805f9b34fb <- Config
	handle: 0x0017, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x0018, uuid: 00002a6d-0000-1000-8000-00805f9b34fb Pressure, resolution of 0.1Pa
	handle: 0x0019, uuid: 00002902-0000-1000-8000-00805f9b34fb <- Config

	handle: 0x001a, uuid: 2a042a01-2a00-1800-2803-280228012800
	handle: 0x001b, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x001c, uuid: 00002a56-0000-1000-8000-00805f9b34fb
	handle: 0x001d, uuid: 00002902-0000-1000-8000-00805f9b34fb
	------------------------------------------------------------------------------------------
	pi@raspberrypi:~/ble $ sudo ./ble_logger_gatt.py

	Device 74:90:50:ff:ff:ff (public), RSSI=-35 dB, Connectable=True
	    1 Flags = 06 (2)
	    9 Complete Local Name = RBLE-DEV (8)
	    isTargetDev   = RBLE-DEV (3)

	GATT Connect to 74:90:50:ff:ff:ff RBLE-DEV (3)
	CONNECTED
	Service <uuid=Generic Attribute handleStart=12 handleEnd=15>
	Service <uuid=Generic Access handleStart=1 handleEnd=11>
	Service <uuid=b2b70000-0001-4cb2-b34a-6550cc0e998c handleStart=16 handleEnd=25>
	Service <uuid=b2b70000-0003-4cb2-b34a-6550cc0e998c handleStart=26 handleEnd=29>
	write Notify Config = 0x13 0100 > ['wr']
	read  Notify Config = 0x13 0100
	write Notify Config = 0x16 0100 > ['wr']
	read  Notify Config = 0x16 0100
	write Notify Config = 0x19 0100 > ['wr']
	read  Notify Config = 0x19 0100
	Waiting for Notify...

	dev =4, Handle = 0x12, Notify = 2e0a
	    Temperature   = 26.06 ℃

	dev =4, Handle = 0x15, Notify = d416
	    Humidity      = 58.44 %

	dev =4, Handle = 0x18, Notify = 78c50e00
	    Pressure      = 968.056 hPa

	UDP Sender = envir_4,26.06 ,58.44 ,968.056

	to Ambient:
	    head {'Content-Type': 'application/json'}
	    body {'d3': 968.056, 'writeKey': '0123456789abcdef', 'd1': 26.06, 'd2': 58.44}
	    Done


--------------------------------------------------------------------------------
## 技術情報
技術情報については、[本ページの情報](https://github.com/bokunimowakaru/ble/tree/master/README.md)ならびに、ルネサス社の[RX23Wグループ BLE Module Firmware Integration Technology アプリケーションノート（r01an4860xx0110-rx23w-ble-fit.zip）](https://www.renesas.com/jp/ja/software/D6004123.html)などを参照ください。  

## 補償およびサポート  
当方は、本ソフトウェア（rx23w_tempHumPress.mot）に関する補償ならびにサポートを、
一切、いたしません。

## ソースコード  
配布いたしません。

## 権利情報  
本サンプルは Adrian Bica 氏が配布する RX23WPeripheral (https://github.com/adrianbica/BLE_thpsensor_RX23W)を ルネサス社が配布するソフトウェア統合開発環境Renesas e2 studio ならびに CC-RX Compilerコンパイラ を使用して作成しました。  
ソフトウェアの権利は Adrian Bica 氏およびルネサス社に帰属します。
本ドキュメントなどの説明資料の権利は当方に帰属し、MITライセンス とします。
不具合や損失などが生じた場合であっても、当方は、一切の責任を負いません。  

なお、本ページは Adrian Bica 氏や ルネサス社の作成物ではありません。

	RX23WPeripheral
	https://github.com/adrianbica/BLE_thpsensor_RX23W

by [bokunimo.net](https://bokunimo.net)
