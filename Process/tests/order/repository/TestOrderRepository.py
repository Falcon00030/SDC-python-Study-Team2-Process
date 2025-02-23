import unittest

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from mysql.MySQLDatabase import MySQLDatabase
from order.repository.OrderRepositoryImpl import OrderRepositoryImpl
from order.entity.Order import ProductOrder



class TestProductRepository(unittest.TestCase):
    def setUp(self):
        mysqlDatabase = MySQLDatabase.getInstance()
        mysqlDatabase.connect()

    def tearDown(self):
        # Clean up any resources after each test
        pass

    def testSave(self, orderInfo):
        repository = OrderRepositoryImpl.getInstance()
        dbSession = sessionmaker(bind=repository.getInstance().engine)
        session = dbSession()

        try:
            session.add(orderInfo)
            session.commit()

            print(f"order - id: {orderInfo.getId()}")
            return orderInfo

        except SQLAlchemyError as exception:
            session.rollback()
            print(f"DB 저장 중 에러 발생: {exception}")
            return None


    def testSaveOrderInfo(self):
        repository = OrderRepositoryImpl.getInstance()
        order_data = {
            "accountId": 12,
            "productId": 25
        }
        order = ProductOrder(**order_data)

        result = repository.save(order)

        self.assertTrue(result)




