from yoomoney import YooMoney
from config_data import TOKENS


def getOperationHistory(wallet : str, type = None):    
    target_data = TOKENS[wallet]

    client_id = target_data["client_id"]
    token = target_data["token"]
    proxy = target_data["proxy"]
    redirect_url = target_data["redirect_url"]

    yooMoney = YooMoney(client_id=client_id, token=token, redirect_url=redirect_url, proxy=proxy)
    walletInfo = yooMoney.getHistory(type=1)
    return walletInfo


def dataParsing(data):
    print(type(data))
    for transaction in reversed(data):
        amount = str(transaction['amount'])
        datatime  = str(transaction['datetime'])
        status = str(transaction['status'])
        direction = str(transaction['direction'])
        amount_currency = str(transaction['amount_currency'])
        group_id = str(transaction['group_id'])
        if group_id == 'type_history_p2p_incoming_all':
            sender =  str(transaction['sender'])
            print("\n\nОтправитель " + sender + "\nСумма операции: " + amount + ' ' + amount_currency + "\nВремя: " + datatime + "\nСтатус: " + status + "\nНаправление: " + direction)
        else:
            details = str(transaction['details'])
            print("\n\nОтправитель " + details + "\nСумма операции: " + amount + ' ' + amount_currency + "\nВремя: " + datatime + "\nСтатус: " + status + "\nНаправление: " + direction)


if __name__ == "__main__":
    print("\nПолучение истории сделок\n")
    wallet = str(input("Кошелек: "))
    type_ = input("1 - только приходы, 2 - только расходы: ")
    # 1 - только приходы, 2 - только расходы
    result = getOperationHistory(wallet, type=type_)
    # В случае ошибки
    if result["error"]:
        pass
    # В случае успешной
    else:
        #dataParsing(result)
        dataParsing(result['data']['operations'])
