from __future__ import annotations
from aiohttp import web
import aiohttp_cors
from multiprocessing import Queue


def debug_sever(target_vel_queue: Queue[tuple[float, float, float]]):
    routes = web.RouteTableDef()

    @routes.post("/target_vel")
    async def target_vel(request: web.Request) -> web.Response:
        data = await request.json()

        target_vel_queue.put((data["x"], data["y"], data["w"]))

        return web.Response()

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
