import asyncio
from bleak import BleakClient, BleakScanner
from datetime import datetime
import logging
import asyncpg

# Create a logger object
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def callback(sender, data):
    current_time = datetime.now()
    # Assuming data format is similar to standard
    # heart rate measurement characteristic
    logger.info(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} - Heart Rate: {data[1]}")

async def run():
    scanner = BleakScanner()
    while True:
        devices = await scanner.discover()
        tickr_device = None

        for device in devices:
            if "TICKR" in device.name:
                logger.info(f"Found TICKR device: {device.address}: {device.name}")
                tickr_device = device
                break

        if tickr_device is None:
            logger.info("TICKR device not found, retrying...")
            await asyncio.sleep(5)
            continue

        try:
            async with BleakClient(tickr_device.address, timeout=20.0) as client:
                logger.info(f"Connected: {client.is_connected}")

                await client.start_notify(
                    "00002a37-0000-1000-8000-00805f9b34fb", callback
                )

                while client.is_connected:
                    await asyncio.sleep(1)

        except Exception as e:
            logger.info(f"An error occurred: {e}")

        logger.info("Disconnected, trying to reconnect...")
        await asyncio.sleep(5)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
