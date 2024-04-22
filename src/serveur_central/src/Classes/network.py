class Network:

    def __init__(self, idNetwork,ip, subnetMask, lastUpdate):
        self.idNetwork = idNetwork
        self.ip = ip
        self.subnetMask = subnetMask
        self.lastUpdate = lastUpdate
        self.cameras = []