from Server import Server

if __name__ == "__main__":

    server = Server()
    server.startServer()
    server.start()

    strIn = raw_input("Press to Stop Server\n")

    server.closeServer()

