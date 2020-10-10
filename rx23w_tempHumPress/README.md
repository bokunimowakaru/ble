Bluetooth LE Peripheral Demo Firmware for Renesas RX23W Target Board  
## Bluetooth LE ���x�E���x�E�C���Z���T �� Blueotooth ��̌����悤  

--------------------------------------------------------------------------------

## ���e

���l�T�X�� Bluetooth LE �^�[�Q�b�g�E�{�[�h RX23W Target Board �Ɋ��Z���T
BME280�iBosch���j��ڑ����A���x�E���x�E�C���l���ABletooth ���M���܂��B  
���M���� Bluetooth �M���̎�M�ɂ́A[ble_logger_gatt.py](../ble_logger_gatt.py)��
���p�ł��܂��B��M�������x�l�� UDP/IP ��LAN���ɓ]��������AIoT�Z���T�p�N���E�h�E
�T�[�r�X[Ambient](http://ambidata.io)�Œ~�ς��A�O���t�\�����邱�Ƃ��o���܂��B  

--------------------------------------------------------------------------------

## �������ݕ��@

�ȉ��Ƀ{�[�h�ւ̏������ݎ菇�������܂��B

1.	[rx23w_temperature.mot](https://github.com/bokunimowakaru/ble/tree/master/rx23w_tempHumPress)�̕ۑ�  
	PC �փ_�E�����[�h���ĉ������B

2.	Renesas Flash Programmer �̃_�E�����[�h  
	[���l�T�X�Ђ̃E�F�u�T�C�g](https://www.renesas.com/)�ɂāA�L�[���[�h�u Renesas
	Flash Programmer �v�Ō������s���A�������ʁu���i���v�Ɋ܂܂�� Flash Programmer
	( Programming GUI )���_�E�����[�h���A�p�\�R���փC���X�g�[�����A�N�����Ă��������B

3.	RX23W �p �^�[�Q�b�g�E�{�[�h�̐ڑ�  
	RX23W �p �^�[�Q�b�g�E�{�[�h��� DIP�X�C�b�`ESW1 �̍����i2�ԁj���������ɃX���C�h���A
	USB�P�[�u���Ńp�\�R���ɐڑ�����ƁA�G�~�����[�^���� LED ACT ���_�ł��J�n���܂��B

4.	Renesas Flash Programmer �p�v���W�F�N�g�̍쐬  
	Renesas Flash Programmer �̃��j���[[�t�@�C��]����V�����v���W�F�N�g�̍쐬�����s���A
	���ځu�}�C�N���R���g���[���v��[RX200]��I�����A�v���W�F�N�g���ƍ쐬�ꏊ��ݒ肵�A
	���ځu�c�[���v��[E2 Emulator Lite]���A���ځu�C���^�t�F�[�X�v��[FINE]��I������
	���������B[�ڑ�]���N���b�N����ƁARX23W�p�^�[�Q�b�g�E�{�[�h�Ƃ̐ڑ������s����܂��B

5.	RX23W�p�^�[�Q�b�g�E�{�[�h�ւ̏�������  
	�t�@�C���̃p�X���A�u�v���O�����t�@�C���v�ɓ��͂��A[�X�^�[�g]�{�^���ŏ������݂�
	�J�n���܂��BID�R�[�h�̓��͂𑣂��ꂽ�ꍇ�́A�u45FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF�v��
	���͂��܂��B

6.	�u����I���v���\�����ꂽ��ADIP�X�C�b�`�����ɖ߂��܂��i2�Ƃ�������EOFF�j�B

--------------------------------------------------------------------------------

## �{�\�t�g�� Service UUID �ƁACharacteristic UUID

### gattool �ł� ����m�F����

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
	    Temperature   = 26.06 ��

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
## �Z�p���
�Z�p���ɂ��ẮA[�{�y�[�W�̏��](https://github.com/bokunimowakaru/ble/tree/master/README.md)�Ȃ�тɁA���l�T�X�Ђ�[RX23W�O���[�v BLE Module Firmware Integration Technology �A�v���P�[�V�����m�[�g�ir01an4860xx0110-rx23w-ble-fit.zip�j](https://www.renesas.com/jp/ja/software/D6004123.html)�Ȃǂ��Q�Ƃ��������B  

## �⏞����уT�|�[�g  
�����́A�{�\�t�g�E�F�A�irx23w_tempHumPress.mot�j�Ɋւ���⏞�Ȃ�тɃT�|�[�g���A
��؁A�������܂���B

## �\�[�X�R�[�h  
�z�z�������܂���B

## �������  
�{�T���v���� Adrian Bica �����z�z���� RX23WPeripheral (https://github.com/adrianbica/BLE_thpsensor_RX23W)�� ���l�T�X�Ђ��z�z����\�t�g�E�F�A�����J����Renesas e2 studio �Ȃ�т� CC-RX Compiler�R���p�C�� ���g�p���č쐬���܂����B  
�\�t�g�E�F�A�̌����� Adrian Bica ������у��l�T�X�ЂɋA�����܂��B
�{�h�L�������g�Ȃǂ̐��������̌����͓����ɋA�����AMIT���C�Z���X �Ƃ��܂��B
�s��⑹���Ȃǂ��������ꍇ�ł����Ă��A�����́A��؂̐ӔC�𕉂��܂���B  

�Ȃ��A�{�y�[�W�� Adrian Bica ���� ���l�T�X�Ђ̍쐬���ł͂���܂���B

	RX23WPeripheral
	https://github.com/adrianbica/BLE_thpsensor_RX23W

by [bokunimo.net](https://bokunimo.net)
