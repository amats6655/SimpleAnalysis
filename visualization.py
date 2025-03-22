import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
import seaborn as sns
import time

# Настройка стиля графиков
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_theme(style='darkgrid', palette='deep')
sns.set_context("notebook", font_scale=1.1)

class DelayedTooltip:
    def __init__(self, fig, delay=0.5):
        self.fig = fig
        self.delay = delay
        self.hover_time = None
        self.current_annotation = None
        self.last_event = None
        self.last_position = None
        
    def on_hover(self, event):
        if event.inaxes is None:
            self.clear_annotation()
            return
        
        current_position = (event.xdata, event.ydata)
        
        # Если позиция изменилась, сбрасываем таймер и удаляем текущую подсказку
        if (self.last_position is not None and 
            current_position != self.last_position):
            self.clear_annotation()
        
        self.last_event = event
        self.last_position = current_position
        
        if self.hover_time is None:
            self.hover_time = time.time()
    
    def clear_annotation(self):
        if self.current_annotation:
            self.current_annotation.remove()
            self.current_annotation = None
            self.fig.canvas.draw_idle()
        self.hover_time = None
    
    def update(self, frame):
        if self.hover_time is not None and self.last_event is not None:
            current_time = time.time()
            if current_time - self.hover_time >= self.delay:
                x, y = self.last_event.xdata, self.last_event.ydata
                if x is not None and y is not None:
                    self.show_annotation(x, y)
    
    def show_annotation(self, x, y):
        ax = self.last_event.inaxes
        if hasattr(ax, 'get_tooltip_text'):
            text = ax.get_tooltip_text(x, y)
            if text:
                # Если уже есть подсказка, обновляем её текст и позицию
                if self.current_annotation:
                    self.current_annotation.set_text(text)
                    self.current_annotation.xy = (x, y)
                else:
                    # Создаем новую подсказку
                    self.current_annotation = ax.annotate(text,
                        xy=(x, y), xycoords='data',
                        xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
                self.fig.canvas.draw_idle()

def plot_all_graphs(series, sorted_asc, sorted_desc, rounded_series):
    """Построение графиков как отдельных представлений на одной фигуре"""
    # Создаем фигуру с местом для кнопок
    fig = plt.figure(figsize=(12, 7))
    plt.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)
    
    # Создаем обработчик подсказок
    tooltip = DelayedTooltip(fig)
    
    def plot_linear():
        ax.clear()
        line = sns.lineplot(data=series, ax=ax, linewidth=1, alpha=0.7, color='#2E86C1')
        ax.set_title('Линейный график значений', pad=15, fontsize=14)
        ax.set_xlabel('Индекс')
        ax.set_ylabel('Значение')
        
        def get_tooltip_text(x, y):
            index = int(round(x))
            if 0 <= index < len(series):
                return f'Индекс: {index}\nЗначение: {series[index]:,d}'
            return None
        
        ax.get_tooltip_text = get_tooltip_text
        fig.canvas.draw_idle()
    
    def plot_histogram():
        ax.clear()
        hist = sns.histplot(data=rounded_series, bins=50, kde=False, ax=ax, color='#2E86C1')
        ax.set_title('Гистограмма распределения значений', pad=15, fontsize=14)
        ax.set_xlabel('Значение')
        ax.set_ylabel('Частота')
        
        def get_tooltip_text(x, y):
            for patch in hist.patches:
                if patch.get_x() <= x <= patch.get_x() + patch.get_width():
                    return (f'Диапазон: {int(patch.get_x())} / {int(patch.get_x() + patch.get_width())}\n'
                           f'Частота: {int(patch.get_height())}')
            return None
        
        ax.get_tooltip_text = get_tooltip_text
        fig.canvas.draw_idle()
    
    def plot_sorted():
        ax.clear()
        df_sorted = {
            'Индекс': range(len(series)),
            'По возрастанию': sorted_asc,
            'По убыванию': sorted_desc
        }
        sns.lineplot(data=df_sorted, x='Индекс', y='По возрастанию', ax=ax, alpha=0.7, linewidth=2, color='#2E86C1', label='По возрастанию')
        sns.lineplot(data=df_sorted, x='Индекс', y='По убыванию', ax=ax, alpha=0.7, linewidth=2, color='#E74C3C', label='По убыванию')
        ax.set_title('Сравнение отсортированных значений', pad=15, fontsize=14)
        ax.set_xlabel('Индекс')
        ax.set_ylabel('Значение')
        
        def get_tooltip_text(x, y):
            index = int(round(x))
            if 0 <= index < len(series):
                asc_value = sorted_asc[index]
                desc_value = sorted_desc[index]
                closest_value = asc_value if abs(y - asc_value) < abs(y - desc_value) else desc_value
                line_type = "возрастание" if closest_value == asc_value else "убывание"
                return f'Индекс: {index}\nЗначение ({line_type}): {closest_value:,d}'
            return None
        
        ax.get_tooltip_text = get_tooltip_text
        fig.canvas.draw_idle()
    
    # Создаем кнопки
    ax_btn1 = plt.axes([0.2, 0.05, 0.2, 0.075])
    ax_btn2 = plt.axes([0.4, 0.05, 0.2, 0.075])
    ax_btn3 = plt.axes([0.6, 0.05, 0.2, 0.075])
    
    btn1 = Button(ax_btn1, 'Линейный график')
    btn2 = Button(ax_btn2, 'Гистограмма')
    btn3 = Button(ax_btn3, 'График сортировки')
    
    btn1.on_clicked(lambda event: plot_linear())
    btn2.on_clicked(lambda event: plot_histogram())
    btn3.on_clicked(lambda event: plot_sorted())
    
    # Подключаем обработчики событий
    fig.canvas.mpl_connect('motion_notify_event', tooltip.on_hover)
    anim = FuncAnimation(fig, tooltip.update, interval=50, blit=False, cache_frame_data=False)
    
    plot_linear()
    plt.show() 