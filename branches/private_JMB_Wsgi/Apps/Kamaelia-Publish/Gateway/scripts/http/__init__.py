def constructHTTPServer():
    routing = [ (/, Interface) ]    

    return ServerCore(
        protocol=HTTPProtocol(routing),
        port=8080,
        socketOptions=(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    )
