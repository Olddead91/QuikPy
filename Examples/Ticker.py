import logging  # Выводим лог на консоль и в файл
from datetime import datetime  # Дата и время

from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QUIK#


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    logger = logging.getLogger('QuikPy.Ticker')  # Будем вести лог
    qp_provider = QuikPy()  # Подключение к локальному запущенному терминалу QUIK

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщения
                        datefmt='%d.%m.%Y %H:%M:%S',  # Формат даты
                        level=logging.DEBUG,  # Уровень логируемых событий NOTSET/DEBUG/INFO/WARNING/ERROR/CRITICAL
                        handlers=[logging.FileHandler('Ticker.log'), logging.StreamHandler()])  # Лог записываем в файл и выводим на консоль
    logging.Formatter.converter = lambda *args: datetime.now(tz=qp_provider.tz_msk).timetuple()  # В логе время указываем по МСК

    # Формат короткого имени для фьючерсов: <Код тикера><Месяц экспирации: 3-H, 6-M, 9-U, 12-Z><Последняя цифра года>. Пример: SiU3, RIU3
    # datanames = ('SBER',)  # Тикер без режима торгов
    datanames = ('TQBR.SBER', 'TQBR.VTBR', 'SPBFUT.SiU4', 'SPBFUT.RIU4')  # Кортеж тикеров

    for dataname in datanames:  # Пробегаемся по всем тикерам
        class_code, sec_code = qp_provider.dataname_to_class_sec_codes(dataname)  # Код режима торгов и тикер
        si = qp_provider.get_security_info(class_code, sec_code)['data']  # Получаем информацию о тикере
        logger.debug(f'Ответ от сервера: {si}')
        logger.info(f'Информация о тикере {si["class_code"]}.{si["sec_code"]} ({si["short_name"]}):')  # Короткое наименование инструмента
        logger.info(f'- Валюта: {si["face_unit"]}')
        logger.info(f'- Лот: {si["lot_size"]}')
        logger.info(f'- Шаг цены: {si["min_price_step"]}')
        logger.info(f'- Кол-во десятичных знаков: {si["scale"]}')
        trade_account = qp_provider.get_trade_account(class_code)['data']  # Торговый счет для класса тикера
        logger.info(f'- Торговый счет: {trade_account}')
        last_price = float(qp_provider.get_param_ex(class_code, sec_code, 'LAST')['data']['param_value'])  # Последняя цена сделки
        logger.info(f'- Последняя цена сделки: {last_price}')

    qp_provider.close_connection_and_thread()  # Перед выходом закрываем соединение для запросов и поток обработки функций обратного вызова