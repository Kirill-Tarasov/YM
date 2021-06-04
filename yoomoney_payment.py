from yoomoney import YooMoney
from config_data import TOKENS


if __name__ == "__main__":
    print('\n')
    my_wallet = str(input("Мой кошелек: "))
    payee = int(input("Кошелек получателя: "))
    amount = float(input("Сумма платежа: "))
    comment = str(input("Сообщение для получателя: "))

    confirmation = input("\nПроверьте введенные данные, если все верно нажмите Y, если нет N: ")
    print('\n')
    if confirmation == "Y":
        # Получаем информацию по кошлельку 
        target_data = TOKENS[my_wallet]
        client_id = target_data["client_id"]
        token = target_data["token"]
        proxy = target_data["proxy"]
        redirect_url = target_data["redirect_url"]

        yooMoney = YooMoney(client_id=client_id, token=token, redirect_url=redirect_url, proxy=proxy)
        response = yooMoney.makePayment(to=payee, amount=amount, message=comment)
        print(response)

    elif confirmation == "N":
        pass
    



