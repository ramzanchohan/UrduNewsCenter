import schedule
import time
import requests


# url = 'http://localhost:8000/run-script'

def execute_urdunews():
    import main
    main.main()
    print('urdu news scrapped successfully.')


def execute_jang():
    import jang
    jang.main()
    print('jang news scrapped successfully.')


def execute_duniayNews():
    import duniyaNews
    duniyaNews.main()
    print('duniyaNews news scrapped successfully.')


def execute_news92():
    import news92
    news92.main()
    print('92News scrapped successfully.')


def run_script():
    execute_news92()
    execute_jang()
    execute_urdunews()
    execute_duniayNews()
    print("All the files Scrapped successfully")
    # requests.get(url)


# Schedule the script to run at 7:00 am daily
schedule.every().day.at('07:00').do(run_script)

# Keep the script running in the background
while True:
    schedule.run_pending()
    time.sleep(1)
