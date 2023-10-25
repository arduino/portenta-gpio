# Portenta.GPIO - RPi.GPIO for Arduino Portenta X8

Arduino Hat carrier contains a 40 pin GPIO
header, similar to the 40 pin header in the Raspberry Pi. These GPIOs can be
controlled for digital input and output using the Python library provided in the
Portenta GPIO Library package. The library has the same API as the RPi.GPIO
library for Raspberry Pi in order to provide an easy way to move applications
running on the Raspberry Pi to the Portenta Hat carrier.

This document walks through what is contained in The Portenta GPIO library
package, how to configure the system and run the provided sample applications,
and the library API.

# Package Components

In addition to this document, the Portenta GPIO library package contains the
following:

1. The `lib/python/` subdirectory contains the Python modules that implement all
library functionality. The gpio.py module is the main component that will be
imported into an application and provides the needed APIs. The `portenta_gpio_map.py` and `event_producer.py` modules are used by the `gpio.py` module and must not be imported directly in to an application.

# Installation

These are the way to install Portenta.GPIO python modules on your system. For the samples applications, please clone this repository to your system. 

## Using pip

The easiest way to install this library is using `pip`:
```shell
sudo pip install Portenta.GPIO
```

## Manual download 

You may clone this git repository, or download a copy of it as an archive file
and decompress it. You may place the library files anywhere you like on your
system. You may use the library directly from this directory by manually
setting `PYTHONPATH`, or install it using `setup.py`:
```shell
sudo python3 setup.py install
```

# Complete library API

The Portenta GPIO library provides all public APIs provided by the RPi.GPIO
library. The following discusses the use of each API:

#### 1. Importing the library

To import the Portenta.GPIO module use:
```python
import Portenta.GPIO as GPIO
```

This way, you can refer to the module as GPIO throughout the rest of the
application. The module can also be imported using the name RPi.GPIO instead of
Portenta.GPIO for existing code using the RPi library.

#### 2. Pin numbering

The Portenta GPIO library provides four ways of numbering the I/O pins. The first
two correspond to the modes provided by the RPi.GPIO library, i.e BOARD and BCM
which refer to the pin number of the 40 pin GPIO header and the Broadcom SoC
GPIO numbers respectively. The remaining two modes, X8 and IMX use strings for X8 mode and NXP standard pin numbering.
X8 mode use the same naming in the HAT Carrier serigraphy.

To specify which mode you are using use the following function
call otherwise BOARD mode is default:
```python
GPIO.setmode(GPIO.BOARD)
# or
GPIO.setmode(GPIO.BCM)
# or
GPIO.setmode(GPIO.X8)
# or
GPIO.setmode(GPIO.IMX)
```

To check which mode has be set, you can call:
```python
mode = GPIO.getmode()
```

#### 3. Set up a channel

The GPIO channel must be set up before use as input or output. To configure
the channel as input, call:
```python
# (where channel is based on the pin numbering mode discussed above)
GPIO.setup(channel, GPIO.IN)
```

To set up a channel as output, call:
```python
GPIO.setup(channel, GPIO.OUT)
```

It is also possible to specify an initial value for the output channel:
```python
GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
```

When setting up a channel as output, it is also possible to set up more than one
channel at once:
```python
# add as many as channels as needed. You can also use tuples: (18,12,13)
channels = [18, 12, 13]
GPIO.setup(channels, GPIO.OUT)
```

#### 4. Input

To read the value of a channel, use:

```python
GPIO.input(channel)
```

This will return either GPIO.LOW or GPIO.HIGH.

#### 5. Output

To set the value of a pin configured as output, use:

```python
GPIO.output(channel, state)
```

where state can be GPIO.LOW or GPIO.HIGH.

You can also output to a list or tuple of channels:

```python
channels = [18, 12, 13] # or use tuples
GPIO.output(channels, GPIO.HIGH) # or GPIO.LOW
# set first channel to LOW and rest to HIGH
GPIO.output(channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
```

#### 6. Clean up

At the end of the program, it is good to clean up the channels so that all pins
are set in their default state. To clean up all channels used, call:

```python
GPIO.cleanup()
```

If you don't want to clean all channels, it is also possible to clean up
individual channels or a list or tuple of channels:

```python
GPIO.cleanup(chan1) # cleanup only chan1
GPIO.cleanup([chan1, chan2]) # cleanup only chan1 and chan2
GPIO.cleanup((chan1, chan2))  # does the same operation as previous statement
```

#### 7. Interrupts

Aside from busy-polling, the library provides three additional ways of
monitoring an input event:

##### The wait_for_edge() function

This function blocks the calling thread until the provided edge(s) is
detected. The function can be called as follows:

```python
GPIO.wait_for_edge(channel, GPIO.RISING)
```

The second parameter specifies the edge to be detected and can be
GPIO.RISING, GPIO.FALLING or GPIO.BOTH. If you only want to limit the wait
to a specified amount of time, a timeout can be optionally set:

```python
# timeout is in milliseconds
GPIO.wait_for_edge(channel, GPIO.RISING, timeout=500)
```

The function returns the channel for which the edge was detected or None if a
timeout occurred.

##### The event_detected() function

This function can be used to periodically check if an event occurred since the
last call. The function can be set up and called as follows:

```python
# set rising edge detection on the channel
GPIO.add_event_detect(channel, GPIO.RISING)
run_other_code()
if GPIO.event_detected(channel):
    do_something()
```

As before, you can detect events for GPIO.RISING, GPIO.FALLING or GPIO.BOTH.

##### A callback function run when an edge is detected

This feature can be used to run a second thread for callback functions. Hence,
the callback function can be run concurrent to your main program in response
to an edge. This feature can be used as follows:

```python
# define callback function
def callback_fn(channel):
    print("Callback called from channel %s" % channel)

# add rising edge detection
GPIO.add_event_detect(channel, GPIO.RISING, callback=callback_fn)
```

More than one callback can also be added if required as follows:

```python
def callback_one(channel):
    print("First Callback")

def callback_two(channel):
    print("Second Callback")

GPIO.add_event_detect(channel, GPIO.RISING)
GPIO.add_event_callback(channel, callback_one)
GPIO.add_event_callback(channel, callback_two)
```

The two callbacks in this case are run sequentially, not concurrently since
there is only thread running all callback functions.

If the edge detection is not longer required it can be removed as follows:

```python
GPIO.remove_event_detect(channel)
```

A timeout option can be set to wait for an event detection
to be removed, or else it is 0.5 seconds by default. It is
recommended that the timeout for removal should be at
least twice as much as the poll time.

#### 8. Check function of GPIO channels

This feature allows you to check the function of the provided GPIO channel:

```python
GPIO.gpio_function(channel)
```

The function returns either GPIO.IN or GPIO.OUT.

The mode must be one of GPIO.BOARD, GPIO.BCM, GPIO.X8, GPIO.IMX.

#### 9. Warnings

It is possible that the GPIO you are trying to use is already being used
external to the current application. In such a condition, the Portenta GPIO
library will warn you if the GPIO being used is configured to anything but the
default direction (input). It will also warn you if you try cleaning up before
setting up the mode and channels. To disable warnings, call:
```python
GPIO.setwarnings(False)
```

It is also possible to differentiate warnings using the <code>module</code> variable (default is <code>WARNING_BOTH</code>). Module targeted could be <code>WARNING_EVENT</code> or <code>WARNING_GPIO</code> or <code>WARNING_BOTH</code>.
To enable warnings only for the GPIO part, call:
```python
GPIO.setwarnings(True, module=WARNING_GPIO)
```