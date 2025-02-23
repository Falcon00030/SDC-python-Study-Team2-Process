import errno
import unittest
from socket import socket

from custom_protocol.repository.CustomProtocolRepositoryImpl import CustomProtocolRepositoryImpl
from main import initEachDomain
from request_generator.service.RequestGeneratorServiceImpl import RequestGeneratorServiceImpl
from transmitter.repository.TransmitterRepositoryImpl import TransmitterRepositoryImpl
from utility.converter.ConvertToTransmitMessage import ConvertToTransmitMessage


class TestReceiveRepository(unittest.TestCase):

    def setUp(self):
        self.repository = CustomProtocolRepositoryImpl()
        self.requestGenerator = RequestGeneratorServiceImpl()


    def sample(self, *arg):
        print(f"sample arg[0]: {arg[0]}")
        result = None
        if(type(arg[0]) == list):
            print(f"arg is list!!")
            result = []
            for data in arg[0]:
                result.append(dict(data))

            #result = {"list": arr}
        else:
            try:
                result = dict(arg[0])
                print(f"data is: {result}")

            except Exception as e:
                print(e)
        return result

    def sample2(self, protocolNumber, *arg):


        combinedRequestData = {
            'protocol': protocolNumber,
            'data': self.sample(*arg)
        }
        print(f"combinedRequestData: {combinedRequestData}")

    def testReceive(self):
        # receivedForm = {
        #     "protocol": 2,
        #     "data": {
        #         "__accountId": "test_user",
        #         "__password": "password"
        #     }
        # }

        receivedForm = {
            "protocol": 3,
            "data": {
                "__accountId": "123",
                "__password" : "123"


            }
        }

        initEachDomain()

        transmitterRepository = TransmitterRepositoryImpl.getInstance()
        transmitQueue = transmitterRepository.getTransmitQueue()

        customProtocolRepository = CustomProtocolRepositoryImpl.getInstance()
        requestGeneratorService = RequestGeneratorServiceImpl.getInstance()

        converter = ConvertToTransmitMessage.getInstance()

        try:

            protocolNumber = receivedForm["protocol"]
            receivedRequestForm = receivedForm["data"]

            print(f"typeof protocolNumber: {type(protocolNumber)}")
            print(f"protocolNumber: {protocolNumber}")
            print(f"typeof requestForm: {type(receivedRequestForm)}")
            print(f"receivedRequestForm: {receivedRequestForm}")

            requestGenerator = requestGeneratorService.findRequestGenerator(protocolNumber)
            print(f"requestGenerator: {requestGenerator}")
            requestForm = requestGenerator(receivedRequestForm)
            print(f"requestForm: {requestForm}")

            print(f"receiverRepository RequestForm: {requestForm.__dict__}")
            response = customProtocolRepository.execute(int(protocolNumber), tuple(requestForm.__dict__.values()))
            print(f"response: {response}")

            #data = dict(response)
           # self.sample(response)
            converter.convertToTransmitMessage(protocolNumber, response)
            #transmitQueue.put(response)

        except socket.error as exception:
            if exception.errno == errno.EWOULDBLOCK:
                pass

