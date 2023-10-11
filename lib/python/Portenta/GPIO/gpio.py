from Portenta.GPIO.portenta_gpio_map import * 
import periphery
import warnings
import os

# sysfs root
_GPIOCHIP_ROOT = "/dev/gpiochip5"

if not os.access(_GPIOCHIP_ROOT, os.W_OK):
    raise RuntimeError("The current user does not have permissions set to access the library functionalites. Please configure permissions or use the root user to run this. It is also possible that {} does not exist. Please check if that file is present.".format(_GPIOCHIP_ROOT))
    
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

_mode = BOARD
_base_gpiochip_path = "/dev/gpiochip"

def _from_channel_to_dict_key(channel):
    key = channel

    if (_mode == X8):
        key = X8_main_header_map[channel]
    elif (_mode == IMX):
        key = IMX_main_header_map[channel]
    elif (_mode == BCM):
        key = BOARD_main_header_map[channel]

    return key

def _setup_single_channel( channel, direction, pull_up_down):
    tmp_direction = ""
    tmp_key = _from_channel_to_dict_key(channel)
        
    if(direction == IN):
        tmp_direction = "in"
    elif (direction == OUT):
        tmp_direction = "out"

    if (BOARD_main_header_map[tmp_key][4]):
        mode_name = "BOARD"
        if (_mode == X8):
            mode_name = "X8"
        elif (_mode == IMX):
            mode_name = "IMX"
        elif (_mode == BCM):
            mode_name = "BCM"

        raise RuntimeError("GPIO {} in mode {} already configured".format(channel, mode_name))

    gpio_data = BOARD_main_header_map[tmp_key]

    try:
        print("setup single channel")
        current_gpio = periphery.GPIO(_base_gpiochip_path+str(gpio_data[2][0]),
                                      gpio_data[2][1], tmp_direction)
    except:
        raise RuntimeError("Unexpected error during GPIO {} configuration".format(channel))
    
    BOARD_main_header_map[tmp_key][4] = current_gpio

    return
    
def _output_single_channel( channel, value):
        
    tmp_key = _from_channel_to_dict_key(channel)

    gpio_obj = BOARD_main_header_map[tmp_key][4]

    if(gpio_obj):
        if(gpio_obj.direction == "out"):
            gpio_obj.write(bool(value))
        else:
            raise RuntimeError("GPIO {} not configured as output".format(channel))
    else:
        raise RuntimeError("GPIO {} is not configured yet, use setup function first".format(channel))
        
    return

def _make_iterable(iterable, single_length=None):
    if isinstance(iterable, str):
        iterable = [iterable]
    try:
        for x in iterable:
            break
    except:
        iterable = [iterable]
    if single_length is not None and len(iterable) == 1:
        iterable = iterable * single_length
    return iterable
    
def _cleanup_single_channel(channel):
    key = _from_channel_to_dict_key(channel)

    gpio_obj = BOARD_main_header_map[key][4]

    if(gpio_obj):
        gpio_obj.close()
        BOARD_main_header_map[key][4] = None
    else:
        warnings.warn("GPIO {} not configured it does not need cleaning".format(channel))
        return
    
    return

def _cleanup_all_channels():

    for key in BOARD_main_header_map.keys() :
        if(BOARD_main_header_map[key][4]):
            _cleanup_single_channel(key)

    return

def setmode(mode):
    global _mode 
    modes = {"BOARD": BOARD,
             "BCM"  : BCM,
             "X8"   : X8,
             "IMX"  : IMX}
    
    if (mode in modes.keys()):
            _mode = modes[mode]
    elif(mode in modes.values()):
        _mode = mode
    else:
        raise ValueError("{} is not recognized as a valid mode. Modes are: BOARD, BCM, X8, IMX".format(mode))
    
    return

def getmode():
    return _mode

def setup(channels, direction, pull_up_down=PUD_OFF, initial=None, consumer='Portenta-gpio'):
    channel_list = _make_iterable(channels)
    
    for channel in channel_list:
        _setup_single_channel(channel, direction, pull_up_down)

    return

def output(channels, values):
    channel_list = _make_iterable(channels)
    values_list = _make_iterable(values, len(channel_list))

    if(len(values_list) != len(channel_list)):
        raise RuntimeError("Number of values != number of channels")
        
    for channel, value in zip(channel_list, values_list):
        _output_single_channel(channel, value)

    return
    
def input(channel):
    ret_val = None
    tmp_key = _from_channel_to_dict_key(channel)

    gpio_obj = BOARD_main_header_map[tmp_key][4]

    if(gpio_obj):
        if(gpio_obj.direction == "in"):
            if(gpio_obj.read()):
                ret_val = HIGH
            else:
                ret_val = LOW
        else:
            raise RuntimeError("GPIO {} is not configured ad input".format(channel))
    else:
        raise RuntimeError("GPIO {} is not configured yet, use setup function first".format(channel))
    
    return ret_val

def cleanup(channels=None):
    
    if(channels):
        channel_list = _make_iterable(channels)

        for channel in channel_list:
            _cleanup_single_channel(channel)
    else:
        _cleanup_all_channels()

    return
