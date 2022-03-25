import telebot
import pymysql
import app_logger
from config import host, password, db_name, user

logger = app_logger.get_logger(__name__)

channel_id = -1001681592401
token_moderator_bot = '5135637646:AAHVrMe60n4znw8xfbh_s4sY2yFB5ousVrg'
token_surendoy_bot = '5060088113:AAFKWEpLAfee1tFwa2oSs86yUXTbx3QGdzI'

bot = telebot.TeleBot(token_moderator_bot)
bot_surendoy = telebot.TeleBot(token_surendoy_bot)


def send_stats_on_channel(_list_matches):
    text = str()
    revenue = 0

    for _dict_match in _list_matches:
        text += "<b>" + str(_dict_match['Players'][0]) + "</b>  VS  <b>" + str(_dict_match['Players'][1]) + "</b>\n"
        text += "Коэффициент: " + str(_dict_match['Coefficient'][_dict_match['Choose']]) + "\n"

        text += "Ставка на "
        if _dict_match['Choose'] == 0:
            text += "<b>" + str(_dict_match['Players'][0]) + "</b>\n"
        elif _dict_match['Choose'] == 2:
            text += "<b>" + str(_dict_match['Players'][1]) + "</b>\n"
        elif _dict_match['Choose'] == 1:
            text += "<b>НИЧЬЮ</b>\n"

        text += "Размер ставки: " + str(_dict_match['Bet']) + " р.\n"
        text += "<b>" + str(_dict_match['Status']) + "</b>\n"

        if _dict_match['Status'] == "Ставка зашла":
            revenue += 107

        text += "Банк после ставки: " + str(_dict_match['Current bank']) + " p.\n\n"

    text += "---------------------------" + "\n"
    text += "Выручка за матчи: <u>" + str(revenue) + " p.</u>\n"
    bot.send_message(channel_id, text, parse_mode='html')


def send_bet_for_premium(_dict_match):
    text = str()

    text += "🔥<b>" + str(_dict_match['Players'][0]) + "</b>  VS  <b>" + str(_dict_match['Players'][1]) + "</b>🔥\n"

    text += "Ставка на "
    if _dict_match['Choose'] == 0:
        text += "<b>" + str(_dict_match['Players'][0]) + "</b>\n"
    elif _dict_match['Choose'] == 2:
        text += "<b>" + str(_dict_match['Players'][1]) + "</b>\n"
    elif _dict_match['Choose'] == 1:
        text += "<b>НИЧЬЮ</b>\n"

    text += "Коэффициент: " + str(_dict_match['Coefficient'][_dict_match['Choose']]) + "\n"
    text += "Размер ставки: " + str(_dict_match['Bet']) + " р.\n"
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        logger.info("Подключение выполнено успешно...")

        try:
            with connection.cursor() as cursor:
                select_all_id = "SELECT telegram_id FROM premium_users;"
                cursor.execute(select_all_id)
                rows = cursor.fetchall()
                for row in rows:
                    bot_surendoy.send_message(row['telegram_id'], text, parse_mode='html')
                logger.info("Рассылка прошла успешно...")

        except Exception as ex:
            logger.error(ex)
        finally:
            connection.close()

    except Exception as ex:
        logger.info("Не удалось подключиться к БД...")
        logger.error(ex)
