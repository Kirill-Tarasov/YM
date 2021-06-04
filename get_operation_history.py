from yoomoney import YooMoney
from config_data import TOKENS


def getOperationHistory(wallet : str, records : int,  operation_type = None):    
    target_data = TOKENS[wallet]

    client_id = target_data["client_id"]
    token = target_data["token"]
    proxy = target_data["proxy"]
    redirect_url = target_data["redirect_url"]

    yooMoney = YooMoney(client_id=client_id, token=token, redirect_url=redirect_url, proxy=proxy)
    walletInfo = yooMoney.getHistory(operation_type=operation_type, records=records)
    return walletInfo


def dataParsing(data):
    for transaction in reversed(data):
        amount = str(transaction['amount'])
        datatime  = str(transaction['datetime'])
        status = str(transaction['status'])
        direction = str(transaction['direction'])
        amount_currency = str(transaction['amount_currency'])
        group_id = str(transaction['group_id'])
        opertion_type = str(transaction['type'])
        if group_id == 'type_history_p2p_incoming_all':
            sender =  str(transaction['sender'])
            print("\n\nОтправитель " + sender + "\nСумма операции: " + amount + ' ' + amount_currency + "\nВремя: " + datatime + "\nСтатус: " + status + "\nНаправление: " + direction)
        else:
            title = str(transaction['title'])
            print("\n\nОтправитель " + title + "\nСумма операции: " + amount + ' ' + amount_currency + "\nВремя: " + datatime + "\nСтатус: " + status + "\nНаправление: " + direction)


if __name__ == "__main__":
    print("\nПолучение истории сделок\n")
    wallet = str(input("Кошелек: "))
    records = int(input("Кол-во записей min=1, max=100: "))
    operation_type = int(input("1 - только приходы, 2 - только расходы: "))
    print("""===============================================================================================""")
    # 1 - только приходы, 2 - только расходы
    result = getOperationHistory(wallet, operation_type=operation_type, records=records)
    # В случае ошибки
    if result["error"]:
        pass
    # В случае успешной
    else:
        dataParsing(result['data']['operations'])
