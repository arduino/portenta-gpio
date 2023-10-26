from Portenta.GPIO.portenta_gpio_map import *
import threading
import warnings
import select
import atexit
import os

_OP_FD = "/tmp/.op_fd"

_operations_file = None
_fd_to_map_key = {}
_fd_set = set()
_mutex = None
_loop_thread = None
_event_warnings = True

def set_event_warnings(status:bool):
    global _event_warnings
    _event_warnings = status
    return

def add_gpio_to_checklist(channel):
    key = from_channel_to_dict_key(channel)
    file_descriptor = BOARD_main_header_map[key][INDEX_GPIO_OBJ].fd

    _mutex.acquire()
    _fd_to_map_key[file_descriptor] = channel
    _fd_set.add(file_descriptor)
    _mutex.release()

    os.write(_operations_file, "a".encode())

    return

def remove_gpio_from_checklist(channel):
    key = from_channel_to_dict_key(channel)
    file_descriptor = BOARD_main_header_map[key][INDEX_GPIO_OBJ].fd
    ret_val = True

    _mutex.acquire()
    try:
        del _fd_to_map_key[file_descriptor]
    except:
        ret_val = False
    
    _fd_set.remove(file_descriptor)
    _mutex.release()

    os.write(_operations_file, "r".encode())
    
    return ret_val

def _perform_read_event(gpio):
    #TODO evade all events?
    try:
        gpio.read_event()
    except:
        if(_event_warnings):
            warnings.warn("Read event failed")

    return

def _check_gpio_event(channel):
    key = from_channel_to_dict_key(channel)
    gpio_data_list =BOARD_main_header_map[key]
    gpio_obj = gpio_data_list[INDEX_GPIO_OBJ]
    _perform_read_event(gpio_obj)
    
    if(len(gpio_data_list[INDEX_EVENT_CB])):
        for callback in gpio_data_list[INDEX_EVENT_CB]:
            callback(channel)
    else:
        print("No event for GPIO")
    
    gpio_data_list[INDEX_EVENT_TRIGGD] = True

    return

def get_event_status(channel):
    key = from_channel_to_dict_key(channel)
    _mutex.acquire()
    ret_val = BOARD_main_header_map[key][INDEX_EVENT_TRIGGD]
    
    if(ret_val):
        BOARD_main_header_map[key][INDEX_EVENT_TRIGGD] = False
    
    _mutex.release()

    return ret_val

def _loop():
    global _mutex, _operations_file

    while True:
        _mutex.acquire()
        local_set = _fd_set.copy()
        local_fd_map = _fd_to_map_key.copy()
        _mutex.release()

        if(len(local_set)):
            try:
                ready_fds = select.select(local_set, [], [], None)
            except Exception as e:
                if(_event_warnings):
                    warnings.warn("GPIO file descriptor check failed error is {}".format(e))
                continue

            if(ready_fds and ready_fds[0]):
                for fd in ready_fds[0]:
                    if(fd == _operations_file):
                        os.read(_operations_file, 1)
                        continue
                    _check_gpio_event(local_fd_map[fd])

def init_interrupt_loop():
    global _loop_thread, _mutex, _operations_file

    _loop_thread = threading.Thread(target=_loop, name="Portenta.GPIO interrupt loop")
    _mutex = threading.Lock()
    
    if(not os.path.exists(_OP_FD)):
        os.mkfifo(_OP_FD)

    _operations_file = os.open(_OP_FD, os.O_RDWR | os.O_NONBLOCK)
    _fd_set.add(_operations_file)
    
    _loop_thread.start()

    atexit.register(deinint_interrupt_loop, None, None)
    
    return

def deinint_interrupt_loop():
    global _loop_thread, _mutex

    _loop_thread.join()

    os.close(_operations_file)

    return