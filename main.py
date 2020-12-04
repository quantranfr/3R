import asyncio
import websockets
import os
import subprocess
from time import time

methods = {
  "79 AB 75 B2": "Tái chế",
  "12 7F 3F 34": "Tiết giảm",
  "49 0F 54 B3": "Tái sử dụng"
}

objects = {
  "D0 44 58 32": "Túi nylon",
  "99 21 71 B2": "Chai nước",
  "14 17 09 2B": "Pin"
}

solutions = { # from the point of view of an ordinary citizen
  ("Tái chế", "Túi nylon"): "Dễ dàng tái chế túi nhựa HDPE và PP, hãy đưa cho người thu gom xử lý.",
  ("Tái chế", "Chai nước"): "Dễ dàng tái chế chai nhựa PET, hãy đưa cho người thu gom xử lý.",
  ("Tái chế", "Pin"): "Hãy vứt pin bỏ đi vào hộp dành riêng ở các siêu thị, tòa nhà để chúng được xử lý an toàn.",
  ("Tái sử dụng", "Túi nylon"): "Hãy dùng lại túi nylon thêm ít nhất một lần trước khi vứt đi!",
  ("Tái sử dụng", "Chai nước"): "Chai nhựa PET có thể được dùng lại một cách sáng tạo trong căn nhà, nhưng đừng dùng lại để uống nước!",
  ("Tái sử dụng", "Pin"): "Hãy dùng pin sạc được!",
  ("Tiết giảm", "Túi nylon"): "Hãy từ chối nhận túi nylon khi đi mua hàng!",
  ("Tiết giảm", "Chai nước"): "Hãy đem chai nước cá nhân khi đi ra ngoài!",
  ("Tiết giảm", "Pin"): "Hạn chế tặng đồ chơi dùng pin cho trẻ em!"
}

last_solution = None # last message shown on the display
last_time = 0        # last timestamp of a valid operation
p = None             # a Popen object
displayer = input("Path to the demo program of rpi-rgb-led-matrix library [/home/pi/Soft/rpi-rgb-led-matrix/examples-api-use/demo]:")
if displayer == "":
    displayer = "/home/pi/Soft/rpi-rgb-led-matrix/examples-api-use/demo"

async def hello(websocket, path):
    global last_solution, p, last_time, displayer
    
    mes = await websocket.recv()
    readers = mes.split(';')
    if len(readers) == 2:
        cards = [reader.split(':')[1] for reader in readers]
        if cards[0] in methods:
            method, obj = methods[cards[0]], objects[cards[1]]
        else:
            method, obj = methods[cards[1]], objects[cards[0]]

        solution = solutions[(method, obj)]
        
        if solution == last_solution:
            if time() - last_time > 60:
                p.terminate()
            return
        else:
            if p is not None:
                p.terminate()
                
        last_solution = solution
        last_time = time()
        
        command = f'pango-view --font=Courier --background=black --foreground=white -qo image.png -t "{solution}" --margin=4,50,3,50 --dpi=150' # will produce a ..x32 image
        os.system(command)
                
        print(f"< {solution}")
        os.system('convert image.png image.ppm')
        command = f'{displayer} --led-rows=32 --led-cols=64 --led-slowdown-gpio=4 --led-chain=3 -D1 image.ppm --led-no-hardware-pulse'
        p = subprocess.Popen(command.split(' '))

start_server = websockets.serve(hello, "localhost", 9080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
