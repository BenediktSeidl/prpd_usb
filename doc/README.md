# Documentation

## Serial

### Settings

* 115200 baud
* one stop bit
* no parity

### Format

#### Request

```
5a0071050000dc07a5
## -> start
  ## -> request
    #### -> command
        #### -> request payload length
            #### -> crc: modbus
                ## -> end
```

#### Response

```
5aff7105000c0000000000000000017e4cc02057a5
## -> start
  ## -> response
    #### -> response to command
        #### -> response payload length
            ######################## -> payload
                                    #### -> crc: modbus
                                        ## -> end
```

See [prpd_usb/schema.py](prpd_usb/schema.py) for known payloads
