import asyncio
import websockets
import json
from pybooklid import LidSensor

async def handler(websocket):
    print("\nWeb App connected!")
    with LidSensor() as sensor:
        for angle in sensor.monitor(interval=0.05):
            print(f"\rCurrent Lid Angle: {angle:.2f}°   ", end="", flush=True)
            
            try:
                await websocket.send(json.dumps({"angle": angle}))
            except websockets.ConnectionClosed:
                print("\nWeb App disconnected.")
                break

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Bridge active! Waiting for your web app on port 8765...")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Bridge...")
