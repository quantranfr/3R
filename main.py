import asyncio
import websockets
import os

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

async def hello(websocket, path):
    mes = await websocket.recv()
    readers = mes.split(';')
    if len(readers) == 2:
        cards = [reader.split(':')[1] for reader in readers]
        if cards[0] in methods:
            method, object = methods[cards[0]], objects[cards[1]]
        else:
            method, object = methods[cards[1]], objects[cards[0]]

        solution = solutions[(method, object)]
        os.system(f'pango-view --font=Courier --antialias=none -o image.png -t "{solution}" --margin=4,50,3,50 --dpi=150') # will produce a ..x32 image
        print(f"< {solution}")

start_server = websockets.serve(hello, "localhost", 9080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
