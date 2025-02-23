import ast

from account.service.request.AccountDeleteRequest import AccountDeleteRequest
from account.service.request.AccountLoginRequest import AccountLoginRequest
from account.service.request.AccountLogoutRequest import AccountLogoutRequest
from account.service.request.AccountRegisterRequest import AccountRegisterRequest
from custom_protocol.entity.CustomProtocol import CustomProtocol
from product.service.request import ProductRequestList
from product.service.request.ProductRequestAdd import ProductRequestAdd
from product.service.request.ProductRequestEdit import ProductRequestEdit
from product.service.request.ProductRequestFind import ProductRequestFind
from product.service.request.ProductRequestRemove import ProductRequestRemove
from request_generator.service.RequestGeneratorService import RequestGeneratorService


class RequestGeneratorServiceImpl(RequestGeneratorService):
    __instance = None
    __requestFormGenerationTable = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__requestFormGenerationTable[
                CustomProtocol.ACCOUNT_LOGIN.value] = cls.__instance.generateAccountLoginRequest

            cls.__requestFormGenerationTable[
                CustomProtocol.ACCOUNT_REGISTER.value] = cls.__instance.generateAccountRegisterRequest

            cls.__requestFormGenerationTable[
                CustomProtocol.ACCOUNT_LOGOUT.value] = cls.__instance.generateAccountLogoutRequest

            cls.__requestFormGenerationTable[
                CustomProtocol.ACCOUNT_DELETE.value] = cls.__instance.generateAccountDeleteRequest

            cls.__requestFormGenerationTable[
                CustomProtocol.PRODUCT_LIST.value] = cls.__instance.generateProductRequestList

            cls.__requestFormGenerationTable[
                CustomProtocol.PRODUCT_INFO.value] = cls.__instance.generateProductRequestFind

            cls.__requestFormGenerationTable[
                CustomProtocol.PRODUCT_ADD.value] = cls.__instance.generateProductRequestAdd

            cls.__requestFormGenerationTable[
                CustomProtocol.PRODUCT_EDIT.value] = cls.__instance.generateProductRequestEdit

            cls.__requestFormGenerationTable[
                CustomProtocol.PRODUCT_REMOVE.value] = cls.__instance.generateProductRequestRemove



        return cls.__instance

    def __init__(self):
        print("RequestGeneratorServiceImpl 생성자 호출")

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def findRequestGenerator(self, protocolNumber):
        print("request generator를 찾아옵니다")
        print(f"protocol number:  {protocolNumber}")
        print(f"Table: {self.__requestFormGenerationTable}")
        if self.__requestFormGenerationTable[protocolNumber] is not None:
            return self.__requestFormGenerationTable[protocolNumber]

        else:
            print(f"이 프로토콜 번호({protocolNumber}) 를 처리 할 수 있는 함수가 없습니다.")

    def generateAccountRegisterRequest(self, arguments):
        print("AccountRegisterRequest 생성")
        return AccountRegisterRequest(
            __accountId=arguments["__accountId"],
            __password=arguments["__password"]
        )
    def generateAccountLoginRequest(self, arguments):
        print("RequestGeneratorService - AccountLoginRequest 생성")
        return AccountLoginRequest(
            __accountId=arguments["__accountId"],
            __password=arguments["__password"]
        )

    def generateAccountLogoutRequest(self, arguments):
        return AccountLogoutRequest(
            __accountSessionId=arguments["__accountSessionId"]
        )

    def generateAccountDeleteRequest(self, arguments):
        return AccountDeleteRequest(
            __accountSessionId=arguments["__accountSessionId"]
        )

    def generateProductRequestFind(self, arguments):
        print("ProductRequestFind 생성")
        return ProductRequestFind(
            arguments["id"]
        )

    def generateProductRequestAdd(self, arguments):
        print("ProductRequestAdd 생성")
        return ProductRequestAdd(
                arguments["name"],
                arguments["price"],
                arguments["info"]
        # arg = list(dict(arguments).values())
        # print(f"arguments: {arg}")
        # return ProductRequestAdd(
        #     arg[0],
        #     int(arg[1]),
        #     arg[2]
        )

    def generateProductRequestEdit(self, arguments):
        print("ProductRequestEdit 생성")
        return ProductRequestEdit(
            arguments["id"],
            arguments["name"],
            arguments["price"],
            arguments["info"]
        )

    def generateProductRequestRemove(self, arguments):
        print("ProductRequestRemove 생성")
        return ProductRequestRemove(
            arguments["id"]
        )

    def generateProductRequestList(self, arguments):
        print("ProductRequestList 생성")
        print(f"arguments: {arguments}")
        return ProductRequestList
