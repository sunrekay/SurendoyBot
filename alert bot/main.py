from selenium import webdriver
from datetime import datetime
from webdriver_manager.firefox import GeckoDriverManager
import app_logger
import moderator_bot
import time

logger = app_logger.get_logger(__name__)

options = webdriver.FirefoxOptions()
options.set_preference("dom.webdriver.enabled", False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0")
options.headless = True

driver = webdriver.Firefox(
    executable_path=GeckoDriverManager().install(),
    options=options
)


def get_list_matches():
    try:
        driver.get(url="https://winline.ru/")
        time.sleep(60)
        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

        html_list = html.split('class="statistic__date ng-star-inserted">')
        html_list.pop(0)
        _list_matches = []
        for match in html_list:
            date = match[:match.find("statistic__date ng-star-inserted") + 50]
            date = date[:date.find("<")]
            if date == 'c__match" data-':
                date = "Сейчас"

            m_time = match[match.find("statistic__time ng-star-inserted") + 34:
                           match.find("statistic__time ng-star-inserted") + 60]
            m_time = m_time[:m_time.find("<")]
            if m_time == 'c__match" data-no-apply-c':
                m_time = "Сейчас"

            players = match[match.find("ng-binding") + 12:match.find("ng-binding") + 60]
            players = players[:players.find("<")]
            players_list = players.split(" - ")

            coefficients = match.split('"Исход 1')
            coefficients.pop(0)
            coefficients_list = []
            for coefficient in coefficients:
                coefficient = coefficient[coefficient.find(">")+1:]
                coefficient = coefficient[:coefficient.find("<")]
                coefficients_list.append(coefficient)
            if len(coefficients_list) == 2:
                coefficients_list.insert(1, '0')

            stats = match[match.find('/stats/match/') + 13:match.find('/stats/match/') + 50]
            stats = stats[:stats.find('"')]
            stats_url = "https://winline.ru/stats/match/" + stats + "/"

            _dict_match = {
                'Date': date,
                'Time': m_time,
                'Players': players_list,
                'Coefficient': coefficients_list,
                'Stats': stats_url,
            }
            _list_matches.append(_dict_match)
        return _list_matches
    except Exception as ex:
        logger.warning(ex)
    finally:
        pass


def check_winner(url):
    try:
        driver.get(url)
        time.sleep(30)
        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

        url_stats = html[html.find('<iframe _ngcontent-c12="" src="') + 31:
                         html.find('<iframe _ngcontent-c12="" src="') + 120]
        url_stats = url_stats[:url_stats.find('"')]

        html_stats = get_html_stats(url_stats)

        score = html_stats[html_stats.find('<strong class="size-xxxl">') + 26:
                           html_stats.find('<strong class="size-xxxl">') + 40]
        if ':' in score:
            score = score[:score.find("<")]
            score_list = score.split(" : ")
            score_list[0] = int(score_list[0])
            score_list[1] = int(score_list[1])

            if score_list[0] > score_list[1]:
                return 0
            elif score_list[0] == score_list[1]:
                return 1
            elif score_list[0] < score_list[1]:
                return 2
    except Exception as ex:
        logger.warning(ex)
    finally:
        pass


def get_html_stats(url_stats):
    try:
        driver.get(url_stats)
        time.sleep(30)
        return driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    except Exception as ex:
        logger.warning(ex)
    finally:
        pass


def get_bet(coef, lose_money):
    for bet in range(1, 100000000):
        if bet * coef >= bet + lose_money + 107:
            return bet


def main():

    _bank = 100000
    _sum_max_lose = 0
    lose_money = 0
    _list_stats = []

    try:
        while True:
            logger.info("Поиск подходящих матчей...")
            _list_matches = get_list_matches()

            flag = False
            for _dict in _list_matches:
                for coef in _dict['Coefficient']:

                    if coef.replace(".", "").isdigit():
                        coef_str = coef
                        coef = float(coef)
                        if (coef > 1.5) and (coef < 2.1):
                            bet = get_bet(coef, lose_money)

                            _dict['Choose'] = _dict['Coefficient'].index(coef_str)
                            _dict['Bet'] = bet

                            moderator_bot.send_bet_for_premium(_dict)

                            logger.info("Матч выбран...")
                            logger.info("Размер ставки: ")
                            logger.info(bet)
                            logger.info("Информация о матче: ")
                            logger.info(_dict)
                            logger.info("Коэффициент: ")
                            logger.info(coef)

                            while True:
                                time_flag = False
                                _check_list_matches = get_list_matches()
                                _list_players = _dict['Players']

                                time.sleep(3600)

                                for _dict in _check_list_matches:
                                    if _list_players[0] in _dict['Players'] and \
                                        _list_players[1] in _dict['Players']:
                                        time_flag = True

                                if time_flag:
                                    logger.info("Матч еще не закончился, переход в режим ожидания...")
                                else:
                                    time.sleep(7200)
                                    logger.info("Матч закончился, проверка результатов...")
                                    answer = check_winner(_dict['Stats'])
                                    if not (answer is None):
                                        break

                            if answer == _dict['Coefficient'].index(coef_str):
                                _bank -= bet
                                _bank += bet * coef
                                lose_money = 0

                                _dict['Status'] = "Ставка зашла"
                                _dict['Current bank'] = int(_bank)
                                _list_stats.append(_dict)

                                logger.info("Ставка зашла")
                                logger.info("Размер банка бота: ")
                                logger.info(_bank)
                                logger.info("Максимальный выход в минус: ")
                                logger.info(_sum_max_lose)

                            else:
                                _bank -= bet
                                lose_money += bet

                                _dict['Status'] = "Ставка НЕ зашла"
                                _dict['Current bank'] = int(_bank)
                                _list_stats.append(_dict)

                                logger.info("Ставка  НЕ зашла")
                                logger.info("Размер банка бота: ")
                                logger.info(_bank)
                                logger.info("Количество проиранных средств: ")
                                logger.info(lose_money)

                                if lose_money > _sum_max_lose:
                                    _sum_max_lose = lose_money

                            if (len(_list_stats) >= 3) and (lose_money == 0):
                                logger.info("Отправка статистики на канал...")
                                moderator_bot.send_stats_on_channel(_list_stats)
                                _list_stats.clear()

                            flag = True
                            break
                    else:
                        break
                    if flag:
                        break
    except Exception as ex:
        logger.info(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()

