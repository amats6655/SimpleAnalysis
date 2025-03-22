import pandas as pd
from colorama import init, Fore, Style
from data_generator import generate_data, prepare_data
from data_statistics import print_statistics
from visualization import plot_all_graphs

def main():
    print(f"\n{Fore.CYAN}Генерация случайных данных...{Style.RESET_ALL}")
    series = generate_data()
    
    print_statistics(series)
    
    print(f"\n{Fore.CYAN}Построение графиков...{Style.RESET_ALL}")
    sorted_asc, sorted_desc, rounded_series = prepare_data(series)
    plot_all_graphs(series, sorted_asc, sorted_desc, rounded_series)
    
    print(f"\n{Fore.CYAN}Сохранение результатов в Excel...{Style.RESET_ALL}")
    df = pd.DataFrame({
        'Исходные данные': series,
        'Сортировка по возрастанию': sorted_asc,
        'Сортировка по убыванию': sorted_desc
    })
    
    with pd.ExcelWriter('results.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Данные')
    print(f"{Fore.LIGHTGREEN_EX}Результаты сохранены в файл 'results.xlsx'{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 