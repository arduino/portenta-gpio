from Portenta.GPIO.portenta_gpio_map import *
from Portenta.GPIO.event_producer import *
import periphery
import warnings
import os

# sysfs root
_GPIOCHIP_ROOT = "/dev/gpiochip5"

if not os.access(_GPIOCHIP_ROOT, os.W_OK):
    raise RuntimeError(f"The current user does not have permissions set to access the library functionalites. Please configure permissions or use the root user to run this. It is also possible that {_GPIOCHIP_ROOT} does not exist. Please check if that file is present.")

init_interrupt_loop()

_base_gpiochip_path = "/dev/gpiochip"
_gpio_warnings = True
    
def _output_single_channel( channel, value):
        
    tmp_key = from_channel_to_dict_key(channel)

    gpio_obj = BOARD_main_header_map[tmp_key][INDEX_GPIO_OBJ]

    if(gpio_obj):
        if(gpio_obj.direction == "out"):
            gpio_obj.write(bool(value))
        else:
            raise RuntimeError(f"GPIO {channel} not configured as output")
    else:
        raise RuntimeError(f"GPIO {channel} is not configured yet, use setup function first")
        
    return

def _setup_single_channel( channel, direction, pull_up_down, initial_state):
    tmp_direction = ""
    tmp_key = from_channel_to_dict_key(channel)
    current_mode = get_mode()

    if(direction == IN):
        tmp_direction = "in"
    elif (direction == OUT):
        tmp_direction = "out"

    if (BOARD_main_header_map[tmp_key][INDEX_GPIO_OBJ]):
        mode_name = "BOARD"
        if (current_mode == X8):
            mode_name = "X8"
        elif (current_mode == IMX):
            mode_name = "IMX"
        elif (current_mode == BCM):
            mode_name = "BCM"

        raise RuntimeError(f"GPIO {channel} in mode {mode_name} already configured")
    
    tmp_bias = "default"

    if(pull_up_down == PUD_DOWN):
        tmp_bias = "pull_down"
    elif(pull_up_down == PUD_UP):
        tmp_bias = "pull_up"
        
    gpio_data = BOARD_main_header_map[tmp_key]

    try:
        current_gpio = periphery.GPIO(_base_gpiochip_path+str(gpio_data[INDEX_GPIOCHIP_INFO][INDEX_GPIOCHIP_NUM]),
                                      gpio_data[INDEX_GPIOCHIP_INFO][INDEX_GPIO], tmp_direction, bias = tmp_bias)
    except:
        raise RuntimeError(f"Unexpected error during GPIO {channel} configuration")
    
    BOARD_main_header_map[tmp_key][INDEX_GPIO_OBJ] = current_gpio

    if(initial_state and direction == OUT):
        _output_single_channel(channel, initial_state)

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
    key = from_channel_to_dict_key(channel)

    gpio_obj = BOARD_main_header_map[key][INDEX_GPIO_OBJ]

    if(gpio_obj):
        gpio_obj.close()
        BOARD_main_header_map[key][INDEX_GPIO_OBJ] = None
    else:
        if(_gpio_warnings):
            warnings.warn(f"GPIO {channel} not configured it does not need cleaning")
        return
    
    return

def _cleanup_all_channels():
    current_mode = get_mode()
    curr_dict = BOARD_main_header_map 

    if (current_mode == X8):
        curr_dict = X8_main_header_map
    elif (current_mode == IMX):
        curr_dict = IMX_main_header_map
    elif (current_mode == BCM):
        curr_dict = BCM_main_header_map

    for key in curr_dict.keys():
        _cleanup_single_channel(key)

    return

def setwarnings(state:bool, module=WARNINGS_BOTH):
    global _gpio_warnings
    
    if(module == WARNINGS_EVENT):
        set_event_warnings(state)
    elif(module == WARNINGS_GPIO):
        _gpio_warnings = state
    elif(module == WARNINGS_BOTH):
        _gpio_warnings = state
        set_event_warnings(state)
    else:
        raise ValueError("Selected module is not recognized as valid, please select between WARNINGS_EVENT, WARNINGS_GPIO or WARNNGS_BOTH")

    return

def setmode(new_mode):
    
    internal_setmode(new_mode)

    return

def getmode():
    return get_mode()

def setup(channels, direction, pull_up_down=PUD_OFF, initial=None, consumer='portenta-gpio'):
    channel_list = _make_iterable(channels)
    
    for channel in channel_list:
        try:
            _setup_single_channel(channel, direction, pull_up_down, initial)
        except:
            if(len(channel_list) > 1):
                print(f"Error configuring GPIO {channel} during multiple channel configuration skipping. Check this error.")
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
    tmp_key = from_channel_to_dict_key(channel)

    gpio_obj = BOARD_main_header_map[tmp_key][INDEX_GPIO_OBJ]

    if(gpio_obj):
        ret_val = int(gpio_obj.read())
        if(gpio_obj.direction == "out" and _gpio_warnings):
            warnings.warn(f"Performing a read on an GPIO {channel} configured as GPIO.OUT")
    else:
        raise RuntimeError(f"GPIO {channel} is not configured yet, use setup function first")
    
    return ret_val

def cleanup(channels=None):
    
    if(channels):
        channel_list = _make_iterable(channels)

        for channel in channel_list:
            _cleanup_single_channel(channel)
    else:
        _cleanup_all_channels()

    return

def add_event_detect(channel, edge, callback=None, bouncetime=None, polltime=0.2):
    key = from_channel_to_dict_key(channel)

    if (not callable(callback)) and callback is not None:
        raise TypeError("Callback Parameter must be callable")
    
    gpio_obj = BOARD_main_header_map[key][INDEX_GPIO_OBJ]
    
    if(gpio_obj):
        if(gpio_obj.direction != "in"):
            raise RuntimeError(f"GPIO {channel} is not configured ad input")
    else:
        raise RuntimeError(f"GPIO {channel} is not configured yet, use setup function first")
    
    if edge != RISING and edge != FALLING and edge != BOTH:
        raise ValueError("The edge must be set to RISING, FALLING, or BOTH")
    
    if(edge == RISING):
        gpio_obj.edge = "rising"
    elif(edge == FALLING):
        gpio_obj.edge = "falling"
    else:
        gpio_obj.edge = "both"

    if(callback):
        BOARD_main_header_map[key][INDEX_EVENT_CB].append(callback)

    add_gpio_to_checklist(channel)

    return

def remove_event_detect(channel, timeout=0.5):
    key = from_channel_to_dict_key(channel)
    gpio_obj = BOARD_main_header_map[key][INDEX_GPIO_OBJ]

    if(gpio_obj):
        if(gpio_obj.edge != "none"):
            if(not remove_gpio_from_checklist(channel) and _gpio_warnings):
                warnings.warn(f"GPIO {channel} event detect is not set")
            try:
                gpio_obj.edge = "none"
            except Exception as e:
                print(e)
        else:
            if(_gpio_warnings):
                warnings.warn(f"GPIO {channel} has not an event set")
    else:
        raise RuntimeError(f"GPIO {channel} is not configured yet, use setup function first")

    BOARD_main_header_map[key][INDEX_EVENT_TRIGGD] = False
    BOARD_main_header_map[key][INDEX_EVENT_CB].clear()

    return

def event_detected(channel):
    key = from_channel_to_dict_key(channel)
    gpio_obj = BOARD_main_header_map[key][INDEX_GPIO_OBJ]
    
    if(gpio_obj):
        if(gpio_obj.direction != "in"):
            raise RuntimeError(f"GPIO {channel} is not configured ad input")
    else:
        raise RuntimeError(f"GPIO {channel} is not configured yet, use setup function first")
    
    return get_event_status(channel)

def add_event_callback(channel, callback):
    key = from_channel_to_dict_key(channel)
    gpio_obj = BOARD_main_header_map[key][INDEX_GPIO_OBJ]
    
    if(gpio_obj):
        if(gpio_obj.direction == "in"):
            if(gpio_obj.edge != "none"):
                if(callable(callback)):
                    BOARD_main_header_map[key][INDEX_EVENT_CB].append(callback)
                else:
                    raise TypeError("Callback Parameter must be callable")
            else:
                raise ValueError("There is non event set, it must be RISING, FALLING, or BOTH")
        else:
            raise RuntimeError(f"GPIO {channel} is not configured ad input")
    else:
          raise RuntimeError(f"GPIO {channel} is not configured yet, use setup function first")
      
    return

def wait_for_edge(channel, edge, bouncetime=None, timeout=None):
    key = from_channel_to_dict_key(channel)
    gpio_obj = BOARD_main_header_map[key][INDEX_GPIO_OBJ]
    
    if(gpio_obj):
        if(gpio_obj.direction != "in"):
            raise RuntimeError(f"GPIO {channel} is not configured ad input")
    else:
        raise RuntimeError(f"GPIO {channel} is not configured yet, use setup function first")
    
    if edge != RISING and edge != FALLING and edge != BOTH:
        raise ValueError("The edge must be set to RISING, FALLING, or BOTH")
    
    if(edge == RISING):
        gpio_obj.edge = "rising"
    elif(edge == FALLING):
        gpio_obj.edge = "falling"
    elif(edge == BOTH):
        gpio_obj.edge = "both"

    if(timeout and  not isinstance(timeout, (int, float))):
        raise ValueError("Timeout should be int, float or None")
    
    if (gpio_obj.poll(timeout)):
        gpio_obj.read_event()
    
    gpio_obj.event = "none"
    
    return

def get_gpio_properties(channel):
    key = from_channel_to_dict_key(channel)

    return BOARD_main_header_map[key]

def gpio_function(channel):
    key = from_channel_to_dict_key(channel)
    gpio_obj = BOARD_main_header_map[key][INDEX_GPIO_OBJ]

    func = UNKNOWN

    if(gpio_obj):
        if(gpio_obj.direction == "in"):
            func = IN
        elif(gpio_obj.direction == "out"):
            func = OUT
        else:
            raise RuntimeError(f"Unexpected behavior on GPIO {channel}")
    else:
        if(_gpio_warnings):
            warnings.warn(f"GPIO {channel} not configured")

    return func
