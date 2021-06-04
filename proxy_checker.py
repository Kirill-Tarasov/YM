import urllib.request , socket

socket.setdefaulttimeout(8)

def is_bad_proxy(proxy):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)        
        sock=urllib.request.urlopen('http://www.google.com')  # change the url address here
        #sock=urllib.urlopen(req)
    except urllib.error.HTTPError as e:        
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:

        print( "ERROR:", detail)
        return 1
    return 0


proxy = str(input('Введите прокси для проверки в формате login:password@ip:http(s)_port: '))
print()
if is_bad_proxy(proxy):
    print (proxy, " - 'этот стаффчик ПОЛНАЯ ШЛЯПА")
else:
    print (proxy, " - этот стаффичик ПРУЩИЙ")
print()
