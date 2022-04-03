# Surendoy Bot
  Это инструмент для ставок либо вручную, либо автоматически, состоящий из двух ботов. Далее о них по отдельности...   

## Alert bot
Данный бот парсит страницу букмекерской конторы и создает список словарей(в словарь записывает: название команд, коэффициенты, ссылку на статистику матча). После, обращаясь по отдельности к каждому словарю, выбирает наиболее подходящий коэффицент(от 1.5 до 2.1). Выбрав коэффициент, отправляет оповещение в личный чат(о том сколько ставить и на какую команду), а затем переходит в двух-часовой режим ожидания. 
  
  *Оповещение бота в личном чате*  
  ![Оповещение бота в личном чате](https://github.com/sunrekay/surendoy_bot/blob/main/Screenshots/%D0%BE%D0%BF%D0%BE%D0%B2%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B1%D0%BE%D1%82%D0%B0.png)
  
  Как только время проходит, проверяет результат матча и либо опять переходит в режим ожидания, либо к поиску нового матча для ставки. После ставок на 3 и более матчей, при условии что последний матч был выиграшным, отправляет статистику на канал. На канале со статистикой бота могут ознакомиться подписчики и другие пользователи. 
  
  *Статистика на канале*  
  ![Статистика на канале](https://github.com/sunrekay/surendoy_bot/blob/main/Screenshots/%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0%20%D0%BD%D0%B0%20%D0%BA%D0%B0%D0%BD%D0%B0%D0%BB%D0%B5.png)

Основная задача этого бота - автоматизировать ставки на столько, на сколько это возможно. Дать пользователю возможность заработать не прикладывая при этом особых усилий.

## Telegram bot
