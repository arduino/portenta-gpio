# Portenta.GPIO - Linux for Arduino Portenta X8

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
imported into an application and provides the needed APIs. The `portenta_gpio_map.py` module is used by the `gpio.py` module and must not be
imported directly in to an application.


# Installation

These are the way to install Portenta.GPIO python modules on your system. For the samples applications, please clone this repository to your system. 

## Using pip

The easiest way to install this library is using `pip`:
```shell
sudo pip install Portenta.GPIO
```

NOT AVAILABLE YET

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

#### 1. Importing the libary

To import the Portenta.GPIO module use:
```python
import Portenta.GPIO as GPIO
```

This way, you can refer to the module as GPIO throughout the rest of the
application. The module can also be imported using the name RPi.GPIO instead of
Portenta.GPIO for existing code using the RPi library.

