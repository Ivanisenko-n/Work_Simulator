import tkinter as tk
import pyautogui
from pynput import mouse
import time
import random
import webbrowser
from threading import Thread

class MouseMoverApp:
    def __init__(self, master):
        self.master = master
        master.title("Work Simulator")
        master.geometry("600x400")

        self.create_ui()

        self.is_running = False
        self.move_thread = None
        self.scroll_thread = None
        self.scroll_enabled = False

    def create_ui(self):
        # Фрейм для кнопок "Start" и "Stop"
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        # Кнопка "Start"
        self.start_button = tk.Button(button_frame, text="Start", command=self.start_moving, width=20, height=2)
        self.start_button.pack(side=tk.LEFT)

        # Кнопка "Stop"
        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_moving, state=tk.DISABLED, width=20, height=2)
        self.stop_button.pack(side=tk.RIGHT)

        # Фрейм для остальных элементов
        content_frame = tk.Frame(self.master)
        content_frame.pack()

        # Элементы в первой строке
        self.label_move_value = tk.Label(content_frame, text="Значение смещения:")
        self.label_move_value.grid(row=0, column=0, pady=5, padx=5, sticky="e")

        self.move_value_entry = tk.Entry(content_frame, width=5)
        self.move_value_entry.grid(row=0, column=1, pady=5, padx=5)

        self.label_delay_value = tk.Label(content_frame, text="Время задержки (сек):")
        self.label_delay_value.grid(row=0, column=2, pady=5, padx=5, sticky="e")

        self.delay_value_entry = tk.Entry(content_frame, width=5)
        self.delay_value_entry.grid(row=0, column=3, pady=5, padx=5)

        # Фрейм для объединенных полей
        margin_frame = tk.Frame(content_frame, bd=2, relief="solid")
        margin_frame.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        # Элементы в первой строке объединенного фрейма
        self.label_top_margin = tk.Label(margin_frame, text="Отступ сверху:")
        self.label_top_margin.grid(row=0, column=0, pady=5, padx=5, sticky="e")

        self.top_margin_entry = tk.Entry(margin_frame, width=5)
        self.top_margin_entry.grid(row=0, column=1, pady=5, padx=5)

        self.label_bottom_margin = tk.Label(margin_frame, text="Отступ снизу:")
        self.label_bottom_margin.grid(row=0, column=2, pady=5, padx=5, sticky="e")

        self.bottom_margin_entry = tk.Entry(margin_frame, width=5)
        self.bottom_margin_entry.grid(row=0, column=3, pady=5, padx=5)

        # Элементы во второй строке объединенного фрейма
        self.label_left_margin = tk.Label(margin_frame, text="Отступ слева:")
        self.label_left_margin.grid(row=1, column=0, pady=5, padx=5, sticky="e")

        self.left_margin_entry = tk.Entry(margin_frame, width=5)
        self.left_margin_entry.grid(row=1, column=1, pady=5, padx=5)

        self.label_right_margin = tk.Label(margin_frame, text="Отступ справа:")
        self.label_right_margin.grid(row=1, column=2, pady=5, padx=5, sticky="e")

        self.right_margin_entry = tk.Entry(margin_frame, width=5)
        self.right_margin_entry.grid(row=1, column=3, pady=5, padx=5)

        self.smooth_movement_var = tk.BooleanVar()
        self.smooth_movement_checkbutton = tk.Checkbutton(content_frame, text="Плавное движение мыши", variable=self.smooth_movement_var)
        self.smooth_movement_checkbutton.grid(row=2, column=0, columnspan=4, pady=5, padx=5)

        # Чекбокс "Использовать скрол"
        self.use_scroll_var = tk.BooleanVar()
        self.use_scroll_checkbutton = tk.Checkbutton(content_frame, text="Использовать скрол", variable=self.use_scroll_var)
        self.use_scroll_checkbutton.grid(row=3, column=0, columnspan=4, pady=5, padx=5)

        # Кнопка "Автору на кофе"
        self.donate_button = tk.Button(content_frame, text="Автору на кофе", command=self.donate_to_author, bg="blue", fg="darkblue", font=("Arial", 12, "bold"), width=40, height=4)
        self.donate_button.grid(row=4, column=0, columnspan=4, pady=15)

    def start_moving(self):
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        move_value = self.get_move_value()
        delay_value = self.get_delay_value()
        smooth_movement = self.smooth_movement_var.get()
        top_margin = self.get_margin_value(self.top_margin_entry.get())
        left_margin = self.get_margin_value(self.left_margin_entry.get())
        bottom_margin = self.get_margin_value(self.bottom_margin_entry.get())
        right_margin = self.get_margin_value(self.right_margin_entry.get())
        use_scroll = self.use_scroll_var.get()

        self.move_thread = Thread(target=self.move_mouse_thread, args=(move_value, delay_value, smooth_movement, top_margin, left_margin, bottom_margin, right_margin, use_scroll))
        self.move_thread.start()

    def stop_moving(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def move_mouse_thread(self, move_value, delay_value, smooth_movement, top_margin, left_margin, bottom_margin, right_margin, use_scroll):
        try:
            screen_width, screen_height = pyautogui.size()

            def move_smoothly():
                while self.is_running:
                    self.move_smoothly_impl(screen_width, screen_height, top_margin, left_margin, bottom_margin, right_margin)
                    time.sleep(delay_value)

            def scroll_smoothly():
                while self.is_running and self.scroll_enabled:
                    scroll_amount = random.randint(-50, 50)
                    with mouse.Controller() as mouse_controller:
                        mouse_controller.scroll(0, scroll_amount)
                    time.sleep(delay_value)

            self.scroll_enabled = use_scroll

            move_thread = Thread(target=move_smoothly)
            move_thread.start()

            if use_scroll:
                scroll_thread = Thread(target=scroll_smoothly)
                scroll_thread.start()

            move_thread.join()

            if use_scroll:
                scroll_thread.join()

        except Exception as e:
            print(f"An error occurred: {e}")

    def move_smoothly_impl(self, screen_width, screen_height, top_margin, left_margin, bottom_margin, right_margin):
        center_x, center_y = screen_width // 2, screen_height // 2

        move_x = random.randint(left_margin, screen_width - right_margin - 1)
        move_y = random.randint(top_margin, screen_height - bottom_margin - 1)

        pyautogui.moveTo(move_x, move_y, duration=0.5)

    def donate_to_author(self):
        webbrowser.open("https://yoomoney.ru/to/410011015748267")

    def get_move_value(self):
        try:
            move_value = int(self.move_value_entry.get())
            return move_value
        except ValueError:
            print("Введите корректное значение смещения.")
            return 10

    def get_delay_value(self):
        try:
            delay_value = float(self.delay_value_entry.get())
            return delay_value
        except ValueError:
            print("Введите корректное значение времени задержки.")
            return 60.0

    def get_margin_value(self, margin):
        try:
            return int(margin) if margin else 0
        except ValueError:
            print("Введите корректное значение отступа.")
            return 0

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.mainloop()
