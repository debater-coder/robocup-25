from __future__ import annotations
from aiohttp import web, WSMsgType
import aiohttp_cors
from multiprocessing import Queue
import asyncio

import posetree


def debug_sever(
    target_vel_queue: Queue[tuple[float, float, float]],
    current_pose: Queue[tuple[float, float, float]],
):
    """
    Debug server running in a different process. Uses queues for communication.

    Arguments:
    target_vel_queue: Queue of (vx, vy, vw) written to from this function
    current_pose: Queue of (x, y, w) read from this function
    """
    routes = web.RouteTableDef()

    @routes.post("/target_vel")
    async def target_vel(request: web.Request) -> web.Response:
        data = await request.json()

        target_vel_queue.put((data["x"], data["y"], data["w"]))

        return web.Response()

    async def send_current_pose(ws: web.WebSocketResponse):
        def get_current_pose() -> tuple[float, float, float]:
            return current_pose.get()

        while True:
            x, y, w = await asyncio.to_thread(get_current_pose)
            await ws.send_json(
                {
                    "x": x,
                    "y": y,
                    "w": w,
                }
            )

    @routes.get("/pose")
    async def pose(request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        task = asyncio.create_task(send_current_pose(ws))

        async for msg in ws:
            if msg.type == WSMsgType.ERROR:
                print("ws connection closed with exception %s" % ws.exception())

        task.cancel()

        return ws

    app = web.Application()
    app.add_routes(routes)

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        },
    )
    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app)
