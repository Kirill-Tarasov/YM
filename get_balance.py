from yoomoney import YooMoney
from config_data import *


def toFixed(numObj, digits=2):
    return f"{numObj:.{digits}f}"

def getBalanceWallet(wallet : str):
    target_data = TOKENS[wallet]
    client_id = target_data["client_id"]
    token = target_data["token"]
    proxy = target_data["proxy"]
    redirect_url = target_data["redirect_url"]

    yooMoney = YooMoney(client_id=client_id, token=token, redirect_url=redirect_url, proxy=proxy)
    walletInfo = yooMoney.getAccInfo()
    
    return walletInfo
#    print("Кошелек: " + str(walletInfo['data']['account']) + " его баланс: " + str(walletInfo['data']['balance']))

def getBalance():
    # Общий баланс
    totle_balance = []
    response = []
    # Деньг свободных для использования
    free_to_use = []
    # Заблокированых
    blocked = []
    # Показать баланс по каждому кошельку 
    for key in TOKENS.keys():
        walletInfo =  getBalanceWallet(key)
        response.append(walletInfo)
        totle_balance.append(walletInfo['data']['balance'])
        if TOKENS[key]['active']:
            free_to_use.append(walletInfo['data']['balance'])
        else:
            blocked.append(walletInfo['data']['balance'])

    return {"data" : response, "total_balance" : str(sum(totle_balance)), "free_to_use" : toFixed(sum(free_to_use), 2), "blocked" : str(toFixed(sum(blocked), 2))}

if __name__ == "__main__":
    print("\nВ поле вы можете ввести номер кошлька, текущий баланс которого хотите узнать, либо оставить его пустым, в таком случае вы получете информацию по всем своим кошлькам, и нажмите Enter ;)\n")
    input_wallet = input("Введите номер кошелека: ")

    # Если пользователь не ввел никакого значения 
    if input_wallet == '':
        response = getBalance()
        # Парсинг ответа
        for wallet in response['data']:
            account = str(wallet['data']['account'])
            balance = wallet['data']['balance']
            available_to_sending = balance - balance * 0.005
            if TOKENS[account]['active']:
                print("Кошелек: " + account + " его баланс: " + toFixed(balance) + ', доступно к отправке: ' + toFixed(available_to_sending))
            else:
                print("\33[31mКошелек: " + account + " его баланс: " + toFixed(balance) + ', доступно к отправке: ' + toFixed(available_to_sending) + "\033[0m")

        total_balance = float(response['total_balance'])
        total_free_to_use = float(response['free_to_use'])
        free_available_to_sending = total_free_to_use - total_free_to_use * 0.005
        tootal_blocked = response['blocked']

        print("\nДоступно для отправки (без комиссии): " +  str(total_free_to_use))
        print("Доступно для отправки (с комиссией): " + str(toFixed(free_available_to_sending)))
        print("В блоке: " + tootal_blocked)
        print("Итоговый баланс: " + toFixed(total_balance) + '\n')   
    # Если пользователь ввел номер кошелька информацию по которому хочет узнать
    else:
        getBalanceWallet(str(input_wallet))
        # Парсинг ответа

