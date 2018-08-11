My pet-project, parser from .data file, which you will get if use financePM

http://finance.uramaks.com
https://play.google.com/store/apps/details?id=com.finperssaver&hl=ru

***

**Install:**

For using you should have python (>=2.7).

Install all dependecies:

    pip install -r requirements.txt

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

Before first run, you should input all data from your mobile-app to your computer.
Then, before running your report, you must fill local database, like this:

    python money.py --fill

After this 2 steps you may using programm like this:

report by all year:

    python money.py --all

    Year: 2015 summary: 385819.08
    Year: 2016 summary: 1057156.86
    Year: 2017 summary: 1296674.19

report by one month:

    python  money.py -rm september -y 2016

                     Обед 23035.52
                      Дом 13817.75
                 Аквариум 12796
           Одежда и обувь 10338
                   Другое 8024
                  Топливо 3210.05
                     Клуб 2808.09
       Накопительный счет 2256.44
                  Подарки 1782
                    Такси 1298
          Мобильная связь 650
              Электроника 209.2

If in your db don't have any transaction by month which you choise, you will see message like this:

    python  money.py -rm september
    Dont find any transactions by this date: september 2018.
