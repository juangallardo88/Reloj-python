import math
import time
import tkinter as tk


BACKGROUND_COLOR = "#e8edf2"
FACE_COLOR = "#ffffff"
OUTLINE_COLOR = "#263238"
HOUR_HAND_COLOR = "#263238"
MINUTE_HAND_COLOR = "#455a64"
SECOND_HAND_COLOR = "#d84343"


class AnalogClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analog Clock and Stopwatch")
        self.root.configure(background=BACKGROUND_COLOR)
        self.root.minsize(420, 560)

        self.stopwatch_elapsed = 0.0
        self.stopwatch_started_at = None
        self.clock_job = None
        self.stopwatch_job = None

        self.time_label = tk.Label(
            root,
            text="",
            font=("Segoe UI", 18, "bold"),
            foreground=OUTLINE_COLOR,
            background=BACKGROUND_COLOR,
        )
        self.time_label.pack(pady=(18, 8))

        self.canvas = tk.Canvas(
            root,
            background=BACKGROUND_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)
        self.canvas.bind("<Configure>", self.draw_clock)

        stopwatch = tk.Frame(root, background=BACKGROUND_COLOR)
        stopwatch.pack(fill=tk.X, padx=24, pady=(8, 20))

        tk.Label(
            stopwatch,
            text="Stopwatch",
            font=("Segoe UI", 13, "bold"),
            foreground=OUTLINE_COLOR,
            background=BACKGROUND_COLOR,
        ).pack(pady=(0, 4))

        self.stopwatch_label = tk.Label(
            stopwatch,
            text="00:00.0",
            font=("Segoe UI", 24),
            foreground=OUTLINE_COLOR,
            background=BACKGROUND_COLOR,
        )
        self.stopwatch_label.pack(pady=(0, 8))

        buttons = tk.Frame(stopwatch, background=BACKGROUND_COLOR)
        buttons.pack()

        tk.Button(buttons, text="Start", width=9, command=self.start_stopwatch).pack(
            side=tk.LEFT, padx=4
        )
        tk.Button(buttons, text="Pause", width=9, command=self.pause_stopwatch).pack(
            side=tk.LEFT, padx=4
        )
        tk.Button(buttons, text="Reset", width=9, command=self.reset_stopwatch).pack(
            side=tk.LEFT, padx=4
        )

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.update_clock()
        self.update_stopwatch()

    def draw_clock(self, event=None):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        radius = max(10, min(width, height) * 0.44)

        self.canvas.delete("all")
        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill=FACE_COLOR,
            outline=OUTLINE_COLOR,
            width=max(2, radius * 0.025),
        )

        for mark in range(60):
            angle = math.radians(mark * 6 - 90)
            is_hour_mark = mark % 5 == 0
            outer_radius = radius * 0.91
            inner_radius = radius * (0.81 if is_hour_mark else 0.86)
            self.canvas.create_line(
                center_x + math.cos(angle) * inner_radius,
                center_y + math.sin(angle) * inner_radius,
                center_x + math.cos(angle) * outer_radius,
                center_y + math.sin(angle) * outer_radius,
                fill=OUTLINE_COLOR,
                width=max(2, radius * (0.022 if is_hour_mark else 0.008)),
                capstyle=tk.ROUND,
            )

        for number in range(1, 13):
            angle = math.radians(number * 30 - 90)
            number_radius = radius * 0.70
            self.canvas.create_text(
                center_x + math.cos(angle) * number_radius,
                center_y + math.sin(angle) * number_radius,
                text=str(number),
                fill=OUTLINE_COLOR,
                font=("Segoe UI", max(10, int(radius * 0.105)), "bold"),
            )

        local_time = time.localtime()
        hour_position = (local_time.tm_hour % 12) + local_time.tm_min / 60
        minute_position = local_time.tm_min + local_time.tm_sec / 60
        second_position = local_time.tm_sec

        self.draw_hand(
            center_x,
            center_y,
            radius * 0.48,
            math.radians(hour_position * 30 - 90),
            HOUR_HAND_COLOR,
            max(4, radius * 0.055),
        )
        self.draw_hand(
            center_x,
            center_y,
            radius * 0.69,
            math.radians(minute_position * 6 - 90),
            MINUTE_HAND_COLOR,
            max(3, radius * 0.035),
        )
        self.draw_hand(
            center_x,
            center_y,
            radius * 0.78,
            math.radians(second_position * 6 - 90),
            SECOND_HAND_COLOR,
            max(1, radius * 0.012),
        )

        center_radius = max(5, radius * 0.045)
        self.canvas.create_oval(
            center_x - center_radius,
            center_y - center_radius,
            center_x + center_radius,
            center_y + center_radius,
            fill=SECOND_HAND_COLOR,
            outline=OUTLINE_COLOR,
            width=1,
        )

    def draw_hand(self, center_x, center_y, length, angle, color, width):
        end_x = center_x + math.cos(angle) * length
        end_y = center_y + math.sin(angle) * length
        self.canvas.create_line(
            center_x,
            center_y,
            end_x,
            end_y,
            fill=color,
            width=width,
            capstyle=tk.ROUND,
        )

    def update_clock(self):
        local_time = time.localtime()
        self.time_label.config(text=time.strftime("%Y-%m-%d  |  %H:%M:%S", local_time))
        self.draw_clock()
        self.clock_job = self.root.after(1000, self.update_clock)

    def start_stopwatch(self):
        if self.stopwatch_started_at is None:
            self.stopwatch_started_at = time.monotonic()

    def pause_stopwatch(self):
        if self.stopwatch_started_at is not None:
            self.stopwatch_elapsed += time.monotonic() - self.stopwatch_started_at
            self.stopwatch_started_at = None
            self.show_stopwatch_time()

    def reset_stopwatch(self):
        self.stopwatch_elapsed = 0.0
        if self.stopwatch_started_at is not None:
            self.stopwatch_started_at = time.monotonic()
        self.show_stopwatch_time()

    def show_stopwatch_time(self):
        elapsed = self.stopwatch_elapsed
        if self.stopwatch_started_at is not None:
            elapsed += time.monotonic() - self.stopwatch_started_at

        tenths = int(elapsed * 10)
        minutes, remainder = divmod(tenths, 600)
        seconds, tenths = divmod(remainder, 10)
        self.stopwatch_label.config(text=f"{minutes:02d}:{seconds:02d}.{tenths}")

    def update_stopwatch(self):
        self.show_stopwatch_time()
        self.stopwatch_job = self.root.after(50, self.update_stopwatch)

    def close(self):
        if self.clock_job is not None:
            self.root.after_cancel(self.clock_job)
        if self.stopwatch_job is not None:
            self.root.after_cancel(self.stopwatch_job)
        self.root.destroy()


def main():
    root = tk.Tk()
    AnalogClockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
