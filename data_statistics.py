from colorama import init, Fore, Style

# Инициализация colorama для вывода в консоль
init()

def print_statistics(series):
    """Вывод статистических характеристик с форматированием"""
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}СТАТИСТИЧЕСКИЙ АНАЛИЗ ДАННЫХ{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}\n")
    
    stats = {
        "Минимальное значение": series.min(),
        "Максимальное значение": series.max(),
        "Сумма всех чисел": series.sum(),
        "Среднеквадратическое отклонение": series.std(),
        "Количество повторяющихся значений": series.value_counts()[series.value_counts() > 1].count()
    }
    
    max_length = max(len(key) for key in stats.keys())
    for key, value in stats.items():
        print(f"{Fore.YELLOW}{key:<{max_length}}: {Fore.WHITE}{value:,.2f}{Style.RESET_ALL}") 