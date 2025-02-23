from sqlalchemy.orm import Session

from account.repository.AccountRepositoryImpl import AccountRepositoryImpl
from account.repository.SessionRepositoryImpl import SessionRepositoryImpl
from account.service.AccountService import AccountService
from account.service.request.AccountDeleteRequest import AccountDeleteRequest
from account.service.request.AccountLoginRequest import AccountLoginRequest
from account.service.request.AccountLogoutRequest import AccountLogoutRequest
from account.service.request.AccountRegisterRequest import AccountRegisterRequest
from account.service.response.AccountDeleteResponse import AccountDeleteResponse
from account.service.response.AccountLoginReponse import AccountLoginResponse
from account.service.response.AccountLogoutReponse import AccountLogoutResponse
from account.service.response.AccountRegisterResponse import AccountRegisterResponse


class AccountServiceImpl(AccountService):
    __instance = None

    def __new__(cls, repository):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.repository = repository

        return cls.__instance

    def __init__(self, repository):
        print("TaskManageServiceImpl 생성자 호출")
        self.__accountRepository = AccountRepositoryImpl()
        self.__sessionRepository = SessionRepositoryImpl()

    @classmethod
    def getInstance(cls, repository=None):
        if cls.__instance is None:
            cls.__instance = cls(repository)
        return cls.__instance

    def registerAccount(self, *args, **kwargs):
        print("registerAccount()")
        print(f"args: {args}")
        print(f"kwargs: {kwargs}")

        cleanedElements = args[0]
        print(f"cleanedElements: {cleanedElements}")

        # for i, element in enumerate(cleanedElements):
        #     print(f"각각의 요소 {i + 1}: {element}")

        accountRegisterRequest = AccountRegisterRequest(*cleanedElements)
        print(f"accountRegisterRequest: {accountRegisterRequest}")
        storedAccount = self.__accountRepository.save(accountRegisterRequest.toAccount())

        if storedAccount.getId() is not None:
            return AccountRegisterResponse(True)

        return AccountRegisterResponse(False)

    def loginAccount(self, *args, **kwargs):
        print("loginAccount()")
        print(f"args: {args}")

        cleanedElements = args[0]
        print(f"cleanedElements: {cleanedElements}")

        accountLoginRequest = AccountLoginRequest(*cleanedElements)
        foundAccount = self.__accountRepository.findByAccountId(accountLoginRequest.getAccountId())
        print(f"foundAccount: {foundAccount}")
        if foundAccount is None:
            return AccountLoginResponse(-1)

        if foundAccount.checkPassword(accountLoginRequest.getPassword()):
            # sessionRepository = SessionRepositoryImpl.getInstance()
            accountSession = Session(foundAccount.getId())
            # sessionRepository.save(accountSession)
            self.__sessionRepository.save(accountSession)

            return AccountLoginResponse(foundAccount.getId())

        return AccountLoginResponse(-1)

    def logoutAccount(self, *args, **kwargs):
        print("AccountService - logoutAccount()")
        print(f"args: {args}")

        cleanedElements = args[0]
        print(f"cleanedElements: {cleanedElements}")

        accountLoginRequest = AccountLogoutRequest(*cleanedElements)
        foundAccount = self.__accountRepository.findById(accountLoginRequest.getAccountSessionId())
        print(f"foundAccount: {foundAccount}")
        if foundAccount is None:
            return AccountLogoutResponse(False)

        self.__sessionRepository.deleteBySessionId(foundAccount.getId())

        return AccountLogoutResponse(True)

    def deleteAccount(self, *args, **kwargs):
        print("AccountService - deleteAccount()")

        cleanedElements = args[0]

        accountLoginRequest = AccountDeleteRequest(*cleanedElements)
        foundAccount = self.__accountRepository.findById(accountLoginRequest.getAccountSessionId())
        print(f"foundAccount: {foundAccount}")
        if foundAccount is None:
            return AccountDeleteResponse(False)

        self.__sessionRepository.deleteBySessionId(foundAccount.getId())
        self.__accountRepository.deleteById(foundAccount.getId())

        return AccountDeleteResponse(True)

    