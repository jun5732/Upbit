
import pyupbit
upbit = pyupbit.Upbit("C0Az21yejT3prbheZAUdZMCUGi9Tr1R0OlSNgIp3","ZRozlBWm55cYlLjSmf9eBzYjhpuxUWeXKPFNzf4Q")
balances = upbit.get_balances()
print(balances)