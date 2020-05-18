Bluetooth LE Peripheral Demo Firmware for Renesas RX23W Target Board  
# Bluetooth LE ���x�Z���T rx23w_temperature.mot  

�n�[�h�����s�v! �R���p�C���s�v! Renesas RX23W Target Board �p  
## Bluetooth LE ���x�Z���T �� Blueotooth ��̌����悤  
by Wataru KUNINO [bokunimo.net](https://bokunimo.net/)  

--------------------------------------------------------------------------------

## ���e

���l�T�X�� Bluetooth LE �^�[�Q�b�g�E�{�[�h RX23W Target Board ������ ���x�Z���T
�ő��肵�� ���x�l���ABletooth ���M���܂��B  
���M���� Bluetooth �M���̎�M�ɂ́A[ble_logger_gatt.py](../ble_logger_gatt.py)��
���p�ł��܂��B��M�������x�l�� UDP/IP ��LAN���ɓ]��������AIoT�Z���T�p�N���E�h�E
�T�[�r�X[Ambient](http://ambidata.io)�Œ~�ς��A�O���t�\�����邱�Ƃ��o���܂��B  

--------------------------------------------------------------------------------

## �������ݕ��@

�ȉ��Ƀ{�[�h�ւ̏������ݎ菇�������܂��B

1.	[rx23w_temperature.mot](https://github.com/bokunimowakaru/ble/tree/master/rx23w_temperature)�̕ۑ�  
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
	    Temperature   = 31.17 ��

	dev =4, Handle = 0x12, Notify = 2d0c
	    Temperature   = 31.17 ��

	UDP/192.168.0.255/1024 = temp._4,31.17

### gattool �ł� ����m�F����

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
	handle: 0x0012, uuid: 00002a6e-0000-1000-8000-00805f9b34fb <-- ���x����
	handle: 0x0013, uuid: 00002902-0000-1000-8000-00805f9b34fb <-- �������M
	handle: 0x0014, uuid: 00002803-0000-1000-8000-00805f9b34fb
	handle: 0x0015, uuid: 5883c32f-5f05-4267-ab01-b4968e8efce0

	(���x�𑪒肷��)
	[D0:69:E2:XX:XX:XX][LE]> char-read-hnd 0x0012
	Characteristic value/descriptor: 2d 00

	(���x���茋�ʂ��������M����)
	D0:69:E2:XX:XX:XX][LE]> char-write-req 0x0013 01 00
	Characteristic value was written successfully
	Notification handle = 0x0012 value: 17 0c
	Notification handle = 0x0012 value: 17 0c
	Notification handle = 0x0012 value: 2d 0c
	Notification handle = 0x0012 value: 2d 0c
	Notification handle = 0x0012 value: 17 0c

--------------------------------------------------------------------------------
## �Z�p���
�Z�p���ɂ��ẮA[�{�y�[�W�̏��](https://github.com/bokunimowakaru/ble/tree/master/README.md)�Ȃ�тɁA���l�T�X�Ђ�[RX23W�O���[�v BLE Module Firmware Integration Technology �A�v���P�[�V�����m�[�g�ir01an4860xx0110-rx23w-ble-fit.zip�j](https://www.renesas.com/jp/ja/software/D6004123.html)�Ȃǂ��Q�Ƃ��������B  

## �⏞����уT�|�[�g  
�����́A�{�\�t�g�E�F�A�irx23w_temperature.mot�j�Ɋւ���⏞�Ȃ�тɃT�|�[�g���A
��؁A�������܂���B

## �\�[�X�R�[�h  
�z�z�������܂���B

## �������  
�{�T���v���̓��l�T�X�Ђ��z�z����T���v���E�\�t�g�E�F�Able_demo_tbrx23w_profile_server���x�[�X�ɁA�쐬���܂����B  
���ϕ��ȊO�̌����̓��l�T�X�ЂɋA�����A���ϕ��̌����͓����ɋA�����܂��B  


