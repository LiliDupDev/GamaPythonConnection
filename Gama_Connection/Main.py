import random
from collections import defaultdict
from Network.Multithread_Server import Server


if __name__ == "__main__":

    server = Server("localhost",9999,"localhost",9877,"ummisco.gama.network.common.CompositeGamaMessage",2048,"./contents/string")
    server.run_server()
