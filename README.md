My pet-project, parser from .data file, which you will get if use financePM

http://finance.uramaks.com

https://play.google.com/store/apps/details?id=com.finperssaver&hl=ru

***

**Install:**

For using you should have python (>=2.7).

Install all dependecies:

    pip install -r requirements.txt
    
After that, put your `financePM.data` file into `tmp` directory and run script first time 
(every time, then you will have new copy your transactions, you should repeat this step)

    python money.py --fill

***

**Running:**

    python money.py [OPTIONS]

***

**Options:**

    --all                 Report by all month
    -rm REPORT_BY_MONTH, --report_by_month REPORT_BY_MONTH
                        Report by one month. Key works only with --year
    -y YEAR, --year YEAR
    -t TYPE, --type TYPE  1: full category, 0: only parent, default=0
    -f, --fill

***

**Example:**

Report by all year:

    python money.py --all

    Year: 2015 summary: 10000.00
    Year: 2016 summary: 11000.00
    Year: 2017 summary: 12000.00

Report by one month:

    python  money.py -rm september -y 2016

                     Обед 1200.0
                      Дом 1100.0
                 Аквариум 1000.0
           Одежда и обувь 900.0
                   Другое 800.0
                  Топливо 700.0
                     Клуб 600.0
       Накопительный счет 500.0
                  Подарки 400.0
                    Такси 300.0
          Мобильная связь 200.0
              Электроника 100.0

Report by one month with full category:

    python money.py -rm october --year 2018 -t 1
    Долг 30000
                     Продукты 3500
                    Кварплата 3400
                         Обед 3300
                      Топливо 3200
                         Кафе 3100
                     Поездки  3000
                        Хобби 2900
                       Друзья 2800
                        Гараж 2700
                       Другое 2600
                   Английский 2500
               Одежда и обувь 2400
                     Запчасти 2300
                  Расхождение 2200
                      Бассейн 2100
                        Штраф 2000
                    Лекарства 1900
                     Консьерж 1800
                         Кино 1700
                     Аквариум 1600
       Общественный транспорт 1500
              Еда с доставкой 1400
                         Кофе 1300
                      Перекус 1200
                      Подарки 1100
                   Расходники 1000
                       Кошка  900
                    Капремонт 800
                        Мойка 700
              Мобильная связь 600
                      Телефон 500
                     Завтрак  400
                     Парковка 300
                  Развлечение 200
                       Музыка 100
    
If your database is empty, or it doesn't has any transactions by selected month, you will have error:

    python  money.py -rm september
    Didn't found any transactions by this date: may 2019.
