from bleak import discover, BleakClient
import asyncio
from sys import stdout
import math
import pyvjoy


address = "00:E0:4C:00:03:8E"
UUID = "00000001-1000-1000-8000-00805f9b34fb"
loop = asyncio.get_event_loop()
controller = pyvjoy.VJoyDevice(1)
#client = BleakClient(adress,loop)


def notification_handler(sender,data):
    global controller
    #global isClickDown,isAppDown,isHomeDown,isVolMinDown,isVolUpDown

    time = ((data[0] & 0xFF) << 1 | (data[1] & 0x80) >> 7)
    isClickDown = (data[18] & 0x1) > 0
    isAppDown = (data[18] & 0x4) > 0
    isHomeDown = (data[18] & 0x2) > 0
    isVolMinDown = (data[18] & 0x8) > 0
    isVolUpDown = (data[18] & 0x10) > 0
    seq= ((data[1] & 0x7C) >> 2)
    
    xOri = (data[1] & 0x03) << 11 | (data[2] & 0xFF) << 3 | (data[3] & 0x80) >> 5
    xOri = (xOri << 19) >> 19
    xOri *= (2 * math.pi / 4095.0)
    
    yOri = (data[3] & 0x1F) << 8 | (data[4] & 0xFF)
    yOri = (yOri << 19) >> 19
    yOri *= (2 * math.pi / 4095.0)
    
    zOri = (data[5] & 0xFF) << 5 | (data[6] & 0xF8) >> 3
    zOri = (zOri << 19) >> 19
    zOri *= (2 * math.pi / 4095.0)
    
    xAcc = (data[6] & 0x07) << 10| (data[7] & 0xFF) << 2 | (data[8] & 0xC0) >> 6
    xAcc = (xAcc << 19) >> 19
    xAcc *= (2 * 9.8 / 4095.0)

    yAcc = (data[8] & 0x3F) << 7| (data[9] & 0xFE) >> 1
    yAcc = (yAcc << 19) >> 19
    yAcc *= (2 * 9.8 / 4095.0)

    zAcc = (data[9] & 0x01) << 12| (data[10] & 0xFF) << 4 | (data[11] & 0xF0) >> 4
    zAcc = (zAcc << 19) >> 19
    zAcc *= (2 * 9.8 / 4095.0)

    xGyro = (data[11] & 0x0F) << 9 | (data[12] & 0xFF) << 1 | (data[13] & 0x80) >> 7
    xGyro = (xGyro << 19) >> 19
    xGyro *= (2048 / 180 * math.pi / 4095.0)
    
    yGyro = (data[13] & 0x7F) << 6 | (data[14] & 0xFC) >> 2
    yGyro = (yGyro << 19) >> 19
    yGyro *= (2048 / 180 * math.pi / 4095.0)
    
    zGyro = (data[14] & 0x03) << 11 | (data[15] & 0xFF) << 3 | (data[16] & 0xE0) >> 5
    zGyro = (zGyro << 19) >> 19
    zGyro *= (2048 / 180 * math.pi / 4095.0)

    xtouch = ((data[16] & 0x1F) << 3 | (data[17] & 0xE0) >> 5) / 255.0
    ytouch = ((data[17] & 0x1F) << 3 | (data[18] & 0xE0) >> 5) / 255.0
    if xtouch == 0 and ytouch == 0:
        xtouch = 0.5
        ytouch = 0.5


    """
    controller.set_button(1,isClickDown)

    controller.set_axis(pyvjoy.HID_USAGE_X,2*(xtouch-0.5))
    controller.set_axis(pyvjoy.HID_USAGE_Y,2*((1-ytouch)-0.5))

    """
    controller.data.lButtons = isClickDown+(isAppDown<<1)+(isHomeDown<<2)+(isVolMinDown<<3)+(isVolUpDown<<4)
    controller.data.wAxisX = int(0x8000*(xtouch))
    controller.data.wAxisY = int(0x8000*(ytouch))

    controller.update()
    


devices = []
async def scan():
    dev = await discover()
    for i in range(0,len(dev)):
        print("["+str(i)+"]"+str(dev[i]))
        devices.append(dev[i])

async def run(address, loop):
    async with BleakClient(address, loop=loop, timeout=20.0) as client:
        x = await client.is_connected()
        print("connected.")
        await client.start_notify(UUID, notification_handler)
        await asyncio.sleep(1200.0,loop=loop)
        await client.stop_notify(UUID)

loop = asyncio.get_event_loop()
#loop.run_until_complete(scan())
print("Scan done")
loop.run_until_complete(run(address, loop))
