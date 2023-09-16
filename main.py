
import asyncio
from bleak import BleakClient, BleakScanner
from datetime import datetime

def callback(sender, data):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Assuming data format is similar to standard
    # heart rate measurement characteristic
    print(f"{current_time} - Heart Rate: {data[1]}") 

async def run():
    scanner = BleakScanner()
    
    while True:
        devices = await scanner.discover()
        tickr_device = None

        for device in devices:
            if "TICKR" in device.name:
                print(f"Found TICKR device: {device.address}: {device.name}")
                tickr_device = device
                break

        if tickr_device is None:
            print("TICKR device not found, retrying...")
            await asyncio.sleep(5)
            continue

        try:
            async with BleakClient(tickr_device.address, timeout=20.0) as client:
                print(f"Connected: {await client.is_connected()}")
                
                await client.start_notify("00002a37-0000-1000-8000-00805f9b34fb", callback)

                while await client.is_connected():
                    await asyncio.sleep(1)

        except Exception as e:
            print(f"An error occurred: {e}")
        
        print("Disconnected, trying to reconnect...")
        await asyncio.sleep(5)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
