import trio

from hip.backends.trio import TrioBackend


def test_connect_serve_context_managers():
    async def send_hello(stream):
        await stream.write(b"hello")

    async def run():
        backend = TrioBackend()

        async with backend.serve("127.0.0.1", 0, send_hello) as server:
            stream = await backend.connect(server.host, server.port)

            async with stream:
                received = b""
                while chunk := await stream.read():
                    received += chunk
                assert received == b"hello"

            assert "CLOSED" in repr(stream)

    trio.run(run)
