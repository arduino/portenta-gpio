INDEX_TAG = 0
INDEX_CAPABILITIES = 1
INDEX_GPIOCHIP_INFO = 2
INDEX_HD_CONN_POSITION = 3
INDEX_GPIO_OBJ = 4
INDEX_EVENT_TRIGGD = 5
INDEX_EVENT_CB = 6

INDEX_GPIOCHIP_NUM = 0
INDEX_GPIO = 1

UNKNOWN = -1

BCM = 0
X8 = 1
IMX = 2
BOARD = 3

LOW = 0
HIGH = 1

IN = 0
OUT = 1

PUD_OFF  = 2
PUD_UP   = 3
PUD_DOWN = 4

RISING  = 1
FALLING = 2
BOTH    = 3

WARNINGS_GPIO = 1
WARNINGS_EVENT = 2
WARNINGS_BOTH = 3

mode = BOARD

def from_channel_to_dict_key(channel):
    global mode

    key = channel

    if (mode == X8):
        key = X8_main_header_map[channel]
    elif (mode == IMX):
        key = IMX_main_header_map[channel]
    elif (mode == BCM):
        key = BCM_main_header_map[channel]

    return key

def internal_setmode(new_mode):
    global mode 
    modes = {"BOARD": BOARD,
             "BCM"  : BCM,
             "X8"   : X8,
             "IMX"  : IMX}
    
    if (new_mode in modes.keys()):
        mode = modes[new_mode]
    elif(new_mode in modes.values()):
        mode = new_mode
    else:
        raise ValueError(f"{mode} is not recognized as a valid mode. Modes are: BOARD, BCM, X8, IMX")
    
    return

def get_mode():
    global mode
    return mode

BOARD_main_header_map = {
# INDEX    TAG       CAPABILITIES                CHIP#+GPIO#    HD CONNECTOR    GPIO OBJECT    EVENT TRIGGERED  EVENT CB
    1  : ["3v3"     ,None                        ,None          ,None,          None,          False,           []],
    2  : ["5v"      ,None                        ,None          ,None,          None,          False,           []],
    3  : ["GPIO02"  ,["GPIO","I2C2_SDA"]         ,(4,21)        ,"J2-45",       None,          False,           []],
    4  : ["5v"      ,None                        ,None          ,None,          None,          False,           []],
    5  : ["GPIO03"  ,["GPIO","I2C2_SCL"]         ,(4,20)        ,"J2-47",       None,          False,           []],
    6  : ["GND"     ,None                        ,None          ,None,          None,          False,           []],
    7  : ["GPIO04"  ,["GPIO","1WIRE","PWM0"]     ,(5,23)        ,"J2-59",       None,          False,           []],
    8  : ["GPIO14"  ,["GPIO","UART3_TX"]         ,(4,29)        ,"J2-25",       None,          False,           []],
    9  : ["GND"     ,None                        ,None          ,None,          None,          False,           []],
    10 : ["GPIO15"  ,["GPIO","UART3_RX"]         ,(4,28)        ,"J2-27",       None,          False,           []],
    11 : ["GPIO17"  ,["GPIO"]                    ,(5,2)         ,"J2-50",       None,          False,           []],
    12 : ["GPIO18"  ,["GPIO","PCM_CLK","I2S_CK"] ,(2,23)        ,"J1-56",       None,          False,           []],
    13 : ["GPIO27"  ,["GPIO"]                    ,(5,6)         ,"J2-58",       None,          False,           []],
    14 : ["GND"     ,None                        ,None          ,None,          None,          False,           []],
    15 : ["GPIO22"  ,["GPIO","SAI_DO"]           ,(3,12)        ,"J2-53",       None,          False,           []],
    16 : ["GPIO23"  ,["GPIO","SAI_CK"]           ,(3,11)        ,"J2-49",       None,          False,           []],
    17 : ["3v3"     ,None                        ,None          ,None,          None,          False,           []],
    18 : ["GPIO24"  ,["GPIO","SAI_FS"]           ,(3,10)        ,"J2-51",       None,          False,           []],
    19 : ["GPIO10"  ,["GPIO","SPI1_MOSI"]        ,(4,7)         ,"J2-42",       None,          False,           []],
    20 : ["GND"     ,None                        ,None          ,None,          None,          False,           []],
    21 : ["GPIO09"  ,["GPIO","SPI1_MISO"]        ,(4,8)         ,"J2-40",       None,          False,           []],
    22 : ["GPIO25"  ,["GPIO","PWM1"]             ,(5,24)        ,"J2-61",       None,          False,           []],
    23 : ["GPIO11"  ,["GPIO","SPI1_SCLK"]        ,(4,6)         ,"J2-38",       None,          False,           []],
    24 : ["GPIO08"  ,["GPIO","SPI1_CE0_N"]       ,(4,9)         ,"J2-36",       None,          False,           []],
    25 : ["GND"     ,None                        ,None          ,None,          None,          False,           []],
    26 : ["GPIO07"  ,["GPIO","SPI1_CE1_N","PWM2"],(5,25)        ,"J2-63",       None,          False,           []],
    27 : ["RESERVED",["GPIO","I2C0_SDA"]         ,(4,19)        ,"J1-44",       None,          False,           []],
    28 : ["RESERVED",["GPIO","I2C0_SCL"]         ,(4,18)        ,"J1-46",       None,          False,           []],
    29 : ["GPIO05"  ,["GPIO","UART1_RX"]         ,(3,31)        ,"J1-35",       None,          False,           []],
    30 : ["GND"     ,None                        ,None          ,None,          None,          False,           []],
    31 : ["GPIO06"  ,["GPIO","PWM3"]             ,(5,26)        ,"J2-65",       None,          False,           []],
    32 : ["GPIO12"  ,["GPIO","UART1_TX"]         ,(4,0)         ,"J1-33",       None,          False,           []],
    33 : ["GPIO13"  ,["GPIO","PWM4"]             ,(5,27)        ,"J2-67",       None,          False,           []],
    34 : ["GND"     ,None                        ,None          ,None,          None,          False,           []],
    35 : ["GPIO19"  ,["GPIO","I2S_WS"]           ,(2,22)        ,"J1-58",       None,          False,           []],
    36 : ["GPIO16"  ,["GPIO","PWM5"]             ,(5,28)        ,"J2-60",       None,          False,           []],
    37 : ["GPIO26"  ,["GPIO","PWM6"]             ,(5,29)        ,"J2-62",       None,          False,           []],
    38 : ["GPIO20"  ,["GPIO","I2S_SDI"]          ,(2,21)        ,"J1-60",       None,          False,           []],
    39 : ["GND"     ,None                        ,None          ,None,          None,          False,           []],
    40 : ["GPIO21"  ,["GPIO","I2S_SDO"]          ,(2,24)        ,"J1-62",       None,          False,           []],
}

X8_main_header_map = {
    "I2C2_SDA"  : 3 ,
    "I2C2_SCL"  : 5 ,
    "PWM0"      : 7 ,
    "TX3"       : 8 ,
    "RX3"       : 10,
    "GPIO2"     : 11,
    "I2S_CK"    : 12,   
    "GPIO6"     : 13,
    "SAI_DO"    : 15,   
    "SAI_CK"    : 16,   
    "SAI_FS"    : 18,   
    "SPI1_COPI" : 19,   
    "SPIO1_CIPO": 21,   
    "PWM1"      : 22,
    "SPI1_SCK"  : 23,   
    "SPI1_CE"   : 24,   
    "PWM2"      : 26,
    "I2C0_SDA"  : 27,   
    "I2C0_SCL"  : 28,   
    "RX1"       : 29,
    "PWM3"      : 31,
    "TX1"       : 32,
    "PWM4"      : 33,
    "I2S_WS"    : 35,   
    "PWM5"      : 36,
    "PWM6"      : 37,
    "I2S_SDI"   : 38,   
    "I2S_SDO"   : 40,   
}

IMX_main_header_map = {
   149 :  3, 
   148 :  5, 
   183 :  7,       
   157 :  8, 
   156 : 10, 
   87  : 12,       
   108 : 15, 
   107 : 16, 
   106 : 18, 
   135 : 19, 
   136 : 21, 
   184 : 22, 
   134 : 23, 
   137 : 24, 
   185 : 26, 
   147 : 27, 
   146 : 28, 
   127 : 29, 
   186 : 31, 
   128 : 32, 
   187 : 33, 
   86  : 35, 
   188 : 36, 
   189 : 37, 
   85  : 38, 
   88  : 40, 

}

BCM_main_header_map = {
    2  : 3, 
    3  : 5,
    4  : 7,
    5  : 29,
    6  : 31,
    7  : 26,
    8  : 24,
    9  : 21,
    10 : 19,
    11 : 23,
    12 : 32,
    13 : 33,
    14 : 8,
    15 : 10,
    16 : 36,
    17 : 11,
    18 : 12,
    19 : 35,
    20 : 38,
    21 : 40,
    22 : 15,
    23 : 16,
    24 : 18,
    25 : 22,
    26 : 37,
    27 : 13,
}

'''
BCM_analog_header_map = {
    1  : ("A0", ["GPIO"],),
    2  : ("A1", ["GPIO"],),
    3  : ("A2", ["GPIO"],),
    4  : ("A3", ["GPIO"],),
    5  : ("A4", ["GPIO"],),
    6  : ("A5", ["GPIO"],),
    7  : ("A6", ["GPIO"],),
    8  : ("A7", ["GPIO"],),
    9  : ("PWM7", ["GPIO"],),
    10 : ("PWM8", ["GPIO"],),
    11 : ("LICELL", ,),
    12 : ("GPIO0", None,),
    13 : ("3v3", None, None),
    14 : ("UART2_TX", ["GPIO"],),
    15 : ("GND", None, None),
    16 : ("UART2_RX", ["GPIO"],),
}

BCM_fan_connector_map = {
    1  : ("PWM9", ["GPIO"],),
    2  : ("NC", None, None),
    3  : ("5V", None, None),
    4  : ("GND", None, None),
}
'''