# LG TV Remote

Small python tool to be invoked from the terminal to send commands to LG TVs with Netcast running.

There is an option for automatic discovery in the network if you do not know the IP address of the TV.
Thus, you can omit the address parameter and it will use the first one responding to the discovery call.

The command can be either a number or a string from the command list below.

## Usage

- To discover the TV and display the pairing key you can just call:

  `python3 lgtvremote.py`

- To display the pairing key on a known TV:

  `python3 lgtvremote.py -a <ip-address>`

- To send a command to a TV with automatic discovery:

  `python3 lgtvremote.py -p <pairing-key -c <command>`

- To send a command to a TV with known IP address:

  `python3 lgtvremote.py -a <ip-address> -p <pairing-key> -c <command>`

- There is also the long argument form available:

  `python3 lgtvremote.py --address <ip-address> --pairing-key <pairing-key> --command <command>`


## Command List

```
POWER = 1
NUM_0 = 2
NUM_1 = 3
NUM_2 = 4
NUM_3 = 5
NUM_4 = 6
NUM_5 = 7
NUM_6 = 8
NUM_7 = 9
NUM_8 = 10
NUM_9 = 11
UP = 12
DOWN = 13
LEFT = 14
RIGHT = 15
OK = 20
HOME = 21
MENU = 22
BACK = 23
VOLUME_UP = 24
VOLUME_DOWN = 25
MUTE = 26
CHANNEL_UP = 27
CHANNEL_DOWN = 28
BLUE = 29
GREEN = 30
RED = 31
YELLOW = 32
PLAY = 33
PAUSE = 34
STOP = 35
FF = 36
REW = 37
SKIP_FF = 38
SKIP_REW = 39
REC = 40
REC_LIST = 41
LIVE = 43
EPG = 44
INFO = 45
ASPECT = 46
EXT = 47
PIP = 48
SUBTITLE = 49
PROGRAM_LIST = 50
TEXT = 51
MARK = 52
_3D = 400
_3D_LR = 401
DASH = 402
PREV = 403
FAV = 404
QUICK_MENU = 405
TEXT_OPTION = 406
AUDIO_DESC = 407
NETCAST = 408
ENERGY_SAVE = 409
AV = 410
SIMPLINK = 411
EXIT = 412
RESERVE = 413
PIP_CHANNEL_UP = 414
PIP_CHANNEL_DOWN = 415
PIP_SWITCH = 416
APPS = 417
```
