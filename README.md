## Prerequisite
You need Bleak to connect to the daydream controller through BLE
I used pyvJoy to emulate a game controller through python, so you need to install vJoy (as described [here](https://github.com/tidzo/pyvjoy)

## Usage
You might need to set address to the mac adress of your daydream controller. you can know this by scanning nearby bluetooth devices with your controller in pairing mode.
or uncomment 
`#loop.run_until_complete(scan())`
After configuring your vJoy controller emulator just run the file with python and it should work
In the file provided, only the touchpad and the physical buttons are mapped to the virtual controller, you can map others inputs (accelerometers and gyroscopes) by processing them accordingly.
