from transmitter.repository.TransmitterRepositoryImpl import TransmitterRepositoryImpl


class ConvertToTransmitMessage:
    __instance = None
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        print("ConvertToTransmitMessage 생성자 호출")


    def convertToData(self, *arg):
        result = None
        if (type(arg[0]) == list):
            result = []
            for data in arg[0]:
                result.append(dict(data))

            # result = {"list": arr}
        else:
            try:
                result = dict(arg[0])
                print(f"data is: {result}")

            except Exception as e:
                print(e)
        return result

    def convertToTransmitMessage(self, protocolNumber:int, *arg):

        transmitterRepository = TransmitterRepositoryImpl.getInstance()
        transmitQueue = transmitterRepository.getTransmitQueue()

        combinedRequestData = {
            'protocol': protocolNumber,
            'data': self.convertToData(*arg)
        }
        print(f"combinedRequestData: {combinedRequestData}")
        transmitQueue.put(combinedRequestData)