from Portenta.GPIO.portenta_gpio_map import *
from periphery import GPIO as GPIO
from time import sleep
import threading
import warnings
import select

LOOP_SLEEP_TIME = 0.5

_fd_to_map_key = {}
_fd_set = set()
_mutex = None
_loop_thread = None
_event_warnings = True

''' TEST START
g_in = GPIO("/dev/gpiochip2", 24, "in", edge="rising")
gpio_list = [g_in]

for gpio in gpio_list:
    _fd_set.add(gpio.fd)
    fd_to_gpio_map[gpio.fd] = gpio

while True:
    while len(_fd_set) > 0:
        ready_fds = select.select(_fd_set, [], [], 0.1)
        
        if(len(ready_fds[0])):
            for fd in ready_fds:
                gpio = fd_to_gpio_map[fd]
                print("triggered GPIO with file descriptor #{}".format(fd))
                print(gpio.read_event())

#TEST STOP '''

def set_event_warnings(status:bool):
    global _event_warnings
    _event_warnings = status
    return

def add_gpio_to_checklist(key):
    file_descriptor = BOARD_main_header_map[key][INDEX_GPIO_OBJ].fd

    _mutex.acquire()
    _fd_to_map_key[file_descriptor] = key
    _fd_set.add(file_descriptor)
    _mutex.release()

    return

def remove_gpio_from_checklist(key):
    file_descriptor = BOARD_main_header_map[key][INDEX_GPIO_OBJ].fd
    ret_val = True

    _mutex.acquire()
    try:
        del _fd_to_map_key[file_descriptor]
    except:
        ret_val = False
    
    _fd_set.remove(file_descriptor)
    _mutex.release()
    
    return ret_val

def _perform_read_event(gpio):
    #TODO evade all events?
    try:
        gpio.read_event()
    except:
        if(_event_warnings):
            warnings.warn("Read event failed")

    return

def _check_gpio_event(file_descriptor):
    _mutex.acquire()
    key = _fd_to_map_key[file_descriptor]
    _mutex.release() 

    gpio_data_list =BOARD_main_header_map[key]
    gpio_obj = gpio_data_list[INDEX_GPIO_OBJ]
    _perform_read_event(gpio_obj)
    
    if(gpio_data_list[INDEX_EVENT_CB]):
        gpio_data_list[INDEX_EVENT_CB]()
    else:
        print("No event for GPIO")
    
    gpio_data_list[INDEX_EVENT_TRIGGD] = True

    return

def get_event_status(key):
    _mutex.acquire()
    ret_val = BOARD_main_header_map[key][INDEX_EVENT_TRIGGD]
    
    if(ret_val):
        BOARD_main_header_map[key][INDEX_EVENT_TRIGGD] = False
    
    _mutex.release()

    return ret_val

def _loop():
    global _mutex

    while True:
        if(len(_fd_set)):
            _mutex.acquire()
            try:
                ready_fds = select.select(_fd_set, [], [], 0.1)
            except:
                if(_event_warnings):
                    warnings.warn("GPIO file descriptor check failed")
            _mutex.release()

            if(ready_fds[0]):
                for fd in ready_fds[0]:
                    _check_gpio_event(fd)
        
        sleep(LOOP_SLEEP_TIME)

    return

def init_interrupt_loop():
    global _loop_thread, _mutex

    _loop_thread = threading.Thread(target=_loop, name="Portenta.GPIO interrupt loop")
    _mutex = threading.Lock()

    _loop_thread.start()
    
    return

def deinint_interrupt_loop():
    global _loop_thread, _mutex

    _loop_thread.join()

    return