# -*- coding: utf-8 -*-
"""
Bubble Shooter - بازی حباب‌ترکونی
ساخته شده برای شهرام
"""

import math
import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.storage.jsonstore import JsonStore
import os

# ---------- تنظیمات کلی بازی ----------
BUBBLE_RADIUS = 40
ROWS_VISIBLE = 8
COLS = 10
COLORS = [
    (0.9, 0.2, 0.3, 1),   # قرمز
    (0.2, 0.6, 0.9, 1),   # آبی
    (0.95, 0.3, 0.75, 1), # صورتی
    (0.3, 0.85, 0.4, 1),  # سبز
    (0.95, 0.8, 0.2, 1),  # زرد
]
SHOOT_SPEED = 900  # پیکسل بر ثانیه
NEW_ROW_INTERVAL = 12  # هر چند شلیک یک ردیف جدید اضافه شود


class Bubble:
    """هر حباب توی گرید بازی"""
    def __init__(self, row, col, color_idx):
        self.row = row
        self.col = col
        self.color_idx = color_idx
        self.alive = True

    def pixel_pos(self, origin_x, origin_y):
        offset_x = BUBBLE_RADIUS if self.row % 2 == 1 else 0
        x = origin_x + self.col * BUBBLE_RADIUS * 2 + offset_x
        y = origin_y - self.row * BUBBLE_RADIUS * 1.8
        return x, y


class FlyingBubble:
    """توپی که در حال شلیک شدن است"""
    def __init__(self, x, y, vx, vy, color_idx):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color_idx = color_idx


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bubbles = []  # لیست حباب‌های چیده شده در گرید
        self.flying = None  # توپ در حال حرکت
        self.next_color_idx = random.randint(0, len(COLORS) - 1)
        self.score = 0
        self.shots_fired = 0
        self.game_over = False
        self.aim_x = Window.width / 2
        self.aim_y = Window.height / 2

        self.origin_x = 20
        self.origin_y = Window.height - 150

        self.score_label = Label(
            text="امتیاز: 0",
            font_size='28sp',
            pos=(Window.width / 2 - 100, Window.height - 90),
            size=(200, 50),
        )
        self.add_widget(self.score_label)

        self.setup_initial_bubbles()

        Clock.schedule_interval(self.update, 1 / 60)

    def setup_initial_bubbles(self):
        for row in range(4):
            cols_in_row = COLS - 1 if row % 2 == 1 else COLS
            for col in range(cols_in_row):
                color_idx = random.randint(0, len(COLORS) - 1)
                self.bubbles.append(Bubble(row, col, color_idx))

    def get_shooter_pos(self):
        return Window.width / 2, 120

    def on_touch_down(self, touch):
        if self.game_over:
            self.restart()
            return
        if self.flying is not None:
            return
        self.shoot(touch.x, touch.y)

    def on_touch_move(self, touch):
        self.aim_x = touch.x
        self.aim_y = touch.y

    def shoot(self, target_x, target_y):
        sx, sy = self.get_shooter_pos()
        dx = target_x - sx
        dy = target_y - sy
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        vx = dx / dist * SHOOT_SPEED
        vy = dy / dist * SHOOT_SPEED
        self.flying = FlyingBubble(sx, sy, vx, vy, self.next_color_idx)
        self.next_color_idx = random.randint(0, len(COLORS) - 1)
        self.shots_fired += 1

    def update(self, dt):
        self.canvas.clear()
        self.draw_background()
        self.draw_bubbles()
        self.draw_aim_line()
        self.draw_shooter()

        if self.flying is not None:
            self.update_flying(dt)

        if self.game_over:
            return

    def update_flying(self, dt):
        fb = self.flying
        fb.x += fb.vx * dt
        fb.y += fb.vy * dt

        # برخورد با دیوار چپ و راست
        if fb.x - BUBBLE_RADIUS < 0 or fb.x + BUBBLE_RADIUS > Window.width:
            fb.vx *= -1
            fb.x = max(BUBBLE_RADIUS, min(Window.width - BUBBLE_RADIUS, fb.x))

        # برخورد با سقف
        if fb.y > Window.height - 100:
            self.attach_bubble(fb)
            self.flying = None
            return

        # برخورد با حباب‌های موجود
        for b in self.bubbles:
            if not b.alive:
                continue
            bx, by = b.pixel_pos(self.origin_x, self.origin_y)
            dist = math.hypot(fb.x - bx, fb.y - by)
            if dist < BUBBLE_RADIUS * 1.8:
                self.attach_bubble(fb)
                self.flying = None
                return

        self.draw_flying(fb)

    def attach_bubble(self, fb):
        # پیدا کردن نزدیک‌ترین سلول خالی گرید
        best_row, best_col, best_dist = 0, 0, float('inf')
        for row in range(ROWS_VISIBLE + 2):
            cols_in_row = COLS - 1 if row % 2 == 1 else COLS
            for col in range(cols_in_row):
                occupied = any(b.row == row and b.col == col and b.alive for b in self.bubbles)
                if occupied:
                    continue
                temp = Bubble(row, col, fb.color_idx)
                bx, by = temp.pixel_pos(self.origin_x, self.origin_y)
                dist = math.hypot(fb.x - bx, fb.y - by)
                if dist < best_dist:
                    best_dist = dist
                    best_row, best_col = row, col

        new_bubble = Bubble(best_row, best_col, fb.color_idx)
        self.bubbles.append(new_bubble)
        self.check_matches(new_bubble)

        if self.shots_fired % NEW_ROW_INTERVAL == 0:
            self.add_new_row()

        self.check_game_over()

    def check_matches(self, start_bubble):
        visited = set()
        stack = [start_bubble]
        matched = []

        while stack:
            b = stack.pop()
            key = (b.row, b.col)
            if key in visited:
                continue
            visited.add(key)
            matched.append(b)

            for other in self.bubbles:
                if not other.alive or (other.row, other.col) in visited:
                    continue
                if other.color_idx != start_bubble.color_idx:
                    continue
                if self.are_neighbors(b, other):
                    stack.append(other)

        if len(matched) >= 3:
            for b in matched:
                b.alive = False
            self.score += len(matched) * 10
            self.score_label.text = f"امتیاز: {self.score}"
            self.drop_floating_bubbles()

    def are_neighbors(self, b1, b2):
        if b1.row == b2.row and abs(b1.col - b2.col) == 1:
            return True
        if abs(b1.row - b2.row) == 1:
            if b1.row % 2 == 0:
                if b2.col == b1.col or b2.col == b1.col - 1:
                    return True
            else:
                if b2.col == b1.col or b2.col == b1.col + 1:
                    return True
        return False

    def drop_floating_bubbles(self):
        # حباب‌هایی که به سقف (ردیف 0) متصل نیستند سقوط می‌کنند
        alive_bubbles = [b for b in self.bubbles if b.alive]
        connected = set()
        stack = [b for b in alive_bubbles if b.row == 0]
        for b in stack:
            connected.add((b.row, b.col))

        while stack:
            b = stack.pop()
            for other in alive_bubbles:
                key = (other.row, other.col)
                if key in connected:
                    continue
                if self.are_neighbors(b, other):
                    connected.add(key)
                    stack.append(other)

        dropped_count = 0
        for b in alive_bubbles:
            if (b.row, b.col) not in connected:
                b.alive = False
                dropped_count += 1

        if dropped_count:
            self.score += dropped_count * 15
            self.score_label.text = f"امتیاز: {self.score}"

    def add_new_row(self):
        for b in self.bubbles:
            b.row += 1
        new_row_cols = COLS
        for col in range(new_row_cols):
            color_idx = random.randint(0, len(COLORS) - 1)
            self.bubbles.append(Bubble(0, col, color_idx))

    def check_game_over(self):
        for b in self.bubbles:
            if not b.alive:
                continue
            _, by = b.pixel_pos(self.origin_x, self.origin_y)
            if by < 200:
                self.game_over = True
                self.score_label.text = f"باختی! امتیاز نهایی: {self.score} - لمس کن برای شروع مجدد"
                return

    def restart(self):
        self.bubbles = []
        self.score = 0
        self.shots_fired = 0
        self.game_over = False
        self.flying = None
        self.setup_initial_bubbles()
        self.score_label.text = "امتیاز: 0"

    # ---------- توابع رسم ----------
    def draw_background(self):
        with self.canvas:
            Color(0.05, 0.05, 0.2, 1)
            Ellipse(pos=(0, 0), size=(Window.width, Window.height))

    def draw_bubbles(self):
        with self.canvas:
            for b in self.bubbles:
                if not b.alive:
                    continue
                x, y = b.pixel_pos(self.origin_x, self.origin_y)
                Color(*COLORS[b.color_idx])
                Ellipse(pos=(x - BUBBLE_RADIUS, y - BUBBLE_RADIUS),
                         size=(BUBBLE_RADIUS * 2, BUBBLE_RADIUS * 2))

    def draw_shooter(self):
        sx, sy = self.get_shooter_pos()
        with self.canvas:
            Color(*COLORS[self.next_color_idx])
            Ellipse(pos=(sx - BUBBLE_RADIUS, sy - BUBBLE_RADIUS),
                     size=(BUBBLE_RADIUS * 2, BUBBLE_RADIUS * 2))

    def draw_aim_line(self):
        if self.flying is not None:
            return
        sx, sy = self.get_shooter_pos()
        with self.canvas:
            Color(1, 1, 1, 0.5)
            Line(points=[sx, sy, self.aim_x, self.aim_y], width=1.5, dash_length=8, dash_offset=4)

    def draw_flying(self, fb):
        with self.canvas:
            Color(*COLORS[fb.color_idx])
            Ellipse(pos=(fb.x - BUBBLE_RADIUS, fb.y - BUBBLE_RADIUS),
                     size=(BUBBLE_RADIUS * 2, BUBBLE_RADIUS * 2))


class BubbleShooterApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.2, 1)
        return GameWidget()


if __name__ == '__main__':
    BubbleShooterApp().run()
