import sys
import os
import json
import math
import subprocess
import re
import psutil
import atexit
import random
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup, QSize
from PyQt5.QtGui import *

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_data_dir():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return base_dir

def log_message(msg):
    """Запись сообщения в лог-файл"""
    try:
        log_file = Path(get_data_dir()) / "deepshell_launcher.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {msg}\n")
    except:
        pass

class CustomMessageBox(QDialog):
    def __init__(self, parent=None, title="", message="", icon_type="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 200)
        
        if icon_type == "error":
            border_color = "#ff0000"
            gradient_start = "#330000"
            gradient_end = "#220000"
            icon_text = "❌"
        elif icon_type == "warning":
            border_color = "#ffff00"
            gradient_start = "#333300"
            gradient_end = "#222200"
            icon_text = "⚠️"
        else:  # info
            border_color = "#00ff00"
            gradient_start = "#003300"
            gradient_end = "#002200"
            icon_text = "ℹ️"
        
        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {gradient_start}, stop:1 {gradient_end});
                border: 2px solid {border_color};
                border-radius: 15px;
            }}
        """)
        
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(35)
        self.title_bar.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {gradient_start}, stop:1 {gradient_end});
                border-top-left-radius: 13px;
                border-top-right-radius: 13px;
                border-bottom: 1px solid {border_color};
            }}
        """)
        
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        title_layout.setSpacing(10)
        
        self.title_icon = QLabel(icon_text)
        self.title_icon.setStyleSheet(f"font-size: 16px; color: {border_color};")
        title_layout.addWidget(self.title_icon)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"color: {border_color}; font-weight: bold; font-size: 12px;")
        title_layout.addWidget(self.title_label)
        
        title_layout.addStretch()
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(22, 22)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: #880000;
                color: #ffffff;
                border: 1px solid #aa0000;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover { background: #aa0000; }
            QPushButton:pressed { background: #660000; }
        """)
        self.close_btn.clicked.connect(self.accept)
        title_layout.addWidget(self.close_btn)
        
        self.content_area = QWidget(self)
        self.content_area.setGeometry(0, 35, 400, 165)
        
        layout = QVBoxLayout(self.content_area)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet(f"color: {border_color}; font-size: 11px;")
        layout.addWidget(self.message_label)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setFixedSize(80, 30)
        self.ok_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00aa00, stop:1 #006600);
                color: #000000;
                font-weight: bold;
                border: 2px solid {border_color};
                border-radius: 8px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00cc00, stop:1 #008800);
            }}
        """)
        self.ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_btn)
        
        layout.addLayout(button_layout)
        
        self.drag_pos = None

    def showEvent(self, event):
        if self.parent():
            parent_center = self.parent().frameGeometry().center()
            new_x = parent_center.x() - self.width() // 2
            new_y = parent_center.y() - self.height() // 2
            desktop = QApplication.desktop().availableGeometry()
            if new_x < desktop.left(): new_x = desktop.left()
            if new_y < desktop.top(): new_y = desktop.top()
            if new_x + self.width() > desktop.right(): new_x = desktop.right() - self.width()
            if new_y + self.height() > desktop.bottom(): new_y = desktop.bottom() - self.height()
            self.move(new_x, new_y)
        self.raise_()
        self.activateWindow()
        super().showEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 35:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos is not None:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = None

class CustomDialog(QDialog):
    def __init__(self, parent=None, title="Диалог", width=600, height=400):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setFixedSize(width, height)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #001a00, stop:1 #000d00);
                border: 2px solid #00aa00;
                border-radius: 15px;
            }
        """)
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(35)
        self.title_bar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #002200, stop:1 #001100);
                border-top-left-radius: 13px;
                border-top-right-radius: 13px;
                border-bottom: 1px solid #00aa00;
            }
        """)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        title_layout.setSpacing(10)
        self.title_icon = QLabel("🚀")
        self.title_icon.setStyleSheet("font-size: 16px; color: #00ff00;")
        title_layout.addWidget(self.title_icon)
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #00ff00; font-weight: bold; font-size: 12px;")
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(22, 22)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: #880000;
                color: #ffffff;
                border: 1px solid #aa0000;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover { background: #aa0000; }
            QPushButton:pressed { background: #660000; }
        """)
        self.close_btn.clicked.connect(self.close)
        title_layout.addWidget(self.close_btn)
        self.content_area = QWidget(self)
        self.content_area.setGeometry(0, 35, width, height - 35)
        self.content_area.setStyleSheet("background: transparent;")
        self.main_layout = QVBoxLayout(self.content_area)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.drag_pos = None

    def showEvent(self, event):
        if self.parent():
            parent_center = self.parent().frameGeometry().center()
            new_x = parent_center.x() - self.width() // 2
            new_y = parent_center.y() - self.height() // 2
            desktop = QApplication.desktop().availableGeometry()
            if new_x < desktop.left(): new_x = desktop.left()
            if new_y < desktop.top(): new_y = desktop.top()
            if new_x + self.width() > desktop.right(): new_x = desktop.right() - self.width()
            if new_y + self.height() > desktop.bottom(): new_y = desktop.bottom() - self.height()
            self.move(new_x, new_y)
        self.raise_()
        self.activateWindow()
        super().showEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 35:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos is not None:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = None
    def addWidget(self, widget):
        self.main_layout.addWidget(widget)
    def addLayout(self, layout):
        self.main_layout.addLayout(layout)

class AnimatedLaunchButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.animation = QPropertyAnimation(self, b"size")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.default_size = QSize(180, 180)
        self.hover_size = QSize(190, 190)
        self.is_running = False
        self.glow_effect = None

    def set_running(self, running):
        self.is_running = running
        if running:
            self.setText("Запущен")
            self.setStyleSheet("""
                QPushButton {
                    background: qradialgradient(
                        cx: 0.5, cy: 0.5, radius: 1.0,
                        fx: 0.3, fy: 0.3,
                        stop: 0.0 #00ffaa,
                        stop: 0.3 #00dd88,
                        stop: 0.6 #00bb66,
                        stop: 0.9 #009944,
                        stop: 1.0 #007722
                    );
                    color: #001111;
                    border-radius: 90px;
                    font-weight: bold;
                    font-size: 20px;
                    border: 4px solid #00ffaa;
                    padding: 15px;
                }
                QPushButton:hover {
                    background: qradialgradient(
                        cx: 0.5, cy: 0.5, radius: 1.0,
                        fx: 0.3, fy: 0.3,
                        stop: 0.0 #88ffcc,
                        stop: 0.3 #00eeaa,
                        stop: 0.6 #00cc88,
                        stop: 0.9 #00aa66,
                        stop: 1.0 #008844
                    );
                    border: 4px solid #88ffdd;
                    font-size: 22px;
                }
                QPushButton:pressed {
                    background: qradialgradient(
                        cx: 0.5, cy: 0.5, radius: 1.0,
                        fx: 0.3, fy: 0.3,
                        stop: 0.0 #008855,
                        stop: 0.3 #006644,
                        stop: 0.6 #004433,
                        stop: 0.9 #003322,
                        stop: 1.0 #002211
                    );
                    border: 4px solid #00aa88;
                    font-size: 18px;
                }
            """)
            if self.glow_effect:
                self.glow_effect.setColor(QColor(0, 255, 170, 200))
        else:
            self.setText("Запуск")
            self.setStyleSheet("""
                QPushButton {
                    background: qradialgradient(
                        cx: 0.5, cy: 0.5, radius: 1.0,
                        fx: 0.3, fy: 0.3,
                        stop: 0.0 #ff5555,
                        stop: 0.3 #cc0000,
                        stop: 0.6 #990000,
                        stop: 0.9 #660000,
                        stop: 1.0 #330000
                    );
                    color: #ffffff;
                    border-radius: 90px;
                    font-weight: bold;
                    font-size: 20px;
                    border: 4px solid #ff0000;
                    padding: 15px;
                }
                QPushButton:hover {
                    background: qradialgradient(
                        cx: 0.5, cy: 0.5, radius: 1.0,
                        fx: 0.3, fy: 0.3,
                        stop: 0.0 #ff8888,
                        stop: 0.3 #ee0000,
                        stop: 0.6 #aa0000,
                        stop: 0.9 #770000,
                        stop: 1.0 #440000
                    );
                    border: 4px solid #ff8888;
                    font-size: 22px;
                }
                QPushButton:pressed {
                    background: qradialgradient(
                        cx: 0.5, cy: 0.5, radius: 1.0,
                        fx: 0.3, fy: 0.3,
                        stop: 0.0 #aa0000,
                        stop: 0.3 #880000,
                        stop: 0.6 #660000,
                        stop: 0.9 #440000,
                        stop: 1.0 #220000
                    );
                    border: 4px solid #aa0000;
                    font-size: 18px;
                }
            """)
            if self.glow_effect:
                self.glow_effect.setColor(QColor(255, 0, 0, 200))

    def enterEvent(self, event):
        self.animation.setStartValue(self.size())
        self.animation.setEndValue(self.hover_size)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.setStartValue(self.size())
        self.animation.setEndValue(self.default_size)
        self.animation.start()
        super().leaveEvent(event)

class SnowFlake:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(-height, 0)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(2, 5)
        self.opacity = random.uniform(0.3, 0.7)
    def fall(self, height):
        self.y += self.speed
        if self.y > height:
            self.y = -10
            self.x = random.randint(0, 10000)

class DeePsHellLauncher(QMainWindow):
    STRATEGY_STANDARD = "standard"
    STRATEGY_FAKE = "fake"
    STRATEGY_CONFUSION = "confusion"
    STRATEGY_OLD = "old"

    OTHER_FIXES = {
        'goodbyedpi': ['goodbyedpi.exe', 'goodbyedpi_x64.exe', 'goodbyedpi_x86.exe'],
        'zapret': ['winws.exe'],
        'simple_dpi_fix': ['dpifix.exe', 'dpi_fix.exe', 'simple-dpi-fix.exe'],
        'antizapret': ['antizapret.exe', 'antizapret-windows.exe'],
    }

    INDIVIDUAL_PROGRAMS = {
        'Discord': {
            'list_file': 'List-Discord-PsHell.txt',
            'ipset_file': 'Ip-Set-Discord.txt',
            'hostlist_domains': 'discord.media,cdn.discordapp.com,discordapp.net,discord.com,discordapp.com',
            'rules': [
                '--filter-udp=80,443,500-1400,3478-3497,4244,5222-5228,5242-5243,6384-56110 --filter-l7=discord,stun',
                '--filter-tcp=1-65000'
            ]
        },
        'WhatsApp': {
            'list_file': 'List-WhatsApp-PsHell.txt',
            'ipset_file': 'Ip-Set-WahatsApp.txt',
            'hostlist_domains': 'whatsapp.net,whatsapp.com,wa.me,wl.co',
            'rules': [
                '--filter-tcp=1-65000 --filter-l7=discord,stun',
                '--filter-udp=80,443,500-1400,3478-3497,4244,5222-5228,5242-5243,6384-56110 --filter-l7=discord,stun'
            ]
        },
        'Telegram': {
            'list_file': 'List-Telegram-PsHell.txt',
            'ipset_file': 'Ip-Set-Telegram.txt',
            'hostlist_domains': 'telegram.org,t.me',
            'rules': [
                '--filter-tcp=1-65000 --filter-l7=discord,stun',
                '--filter-udp=80,443,500-1400,3478-3497,4244,5222-5228,5242-5243,6384-56110 --filter-l7=discord,stun'
            ]
        },
        'Signal': {
            'list_file': 'List-Signal-PsHell.txt',
            'rules': [
                '--filter-tcp=1-65000 --filter-l7=discord,stun',
                '--filter-udp=80,443,500-1400,3478-3497,4244,5222-5228,5242-5243,6384-56110 --filter-l7=discord,stun'
            ]
        },
        'Snapchat': {
            'list_file': 'List-Snapchat-PsHell.txt',
            'rules': [
                '--filter-tcp=1-65000 --filter-l7=discord,stun',
                '--filter-udp=80,443,500-1400,3478-3497,4244,5222-5228,5242-5243,6384-56110 --filter-l7=discord,stun'
            ]
        },
        'FaceTime': {
            'list_file': 'List-FaceTime-PsHell.txt',
            'rules': [
                '--filter-tcp=1-65000 --filter-l7=discord,stun',
                '--filter-udp=80,443,500-1400,3478-3497,4244,5222-5228,5242-5243,6384-56110 --filter-l7=discord,stun'
            ]
        },
        'Viber': {
            'list_file': 'List-Viber-PsHell.txt',
            'ipset_file': 'Ip-Set-Viber.txt',
            'rules': [
                '--filter-tcp=1-65000 --filter-l7=discord,stun',
                '--filter-udp=80,443,500-1400,3478-3497,4244,5222-5228,5242-5243,6384-56110 --filter-l7=discord,stun'
            ]
        },
        'Google Meet': {
            'list_file': 'List-Google-Mete-PsHell.txt',
            'ipset_file': 'Ip-Set-Google-mete.txt',
            'rules': [
                '--filter-tcp=1-65000 --filter-l7=discord,stun',
                '--filter-udp=80,443,500-1400,3478-3497,4244,5222-5228,5242-5243,6384-56110 --filter-l7=discord,stun'
            ]
        },
        'Steam': {
            'list_file': 'List-Steam-PsHell.txt',
            'ipset_file': 'Ip-Set-Steam.txt',
            'rules': [
                '--filter-tcp=80,443,1024-1124,2099,3724,3074-3479,4000,5060-5062,5222-5223,6112-6120,6250,8088,8393-8400,9960-9969,12000-65000',
                '--filter-udp=80,443,1119-1120,1024-1124,3724,3478-4380,5060-5062,6112-6119,6250,7000-8000,8088,8180-8181,12000-65535'
            ]
        },
        'Battlefield': {
            'list_file': 'List-BF-PsHell.txt',
            'ipset_file': 'Ip-Set-BF.txt',
            'rules': [
                '--filter-tcp=80,443,1024-1124,2099,3724,3074-3479,4000,5060-5062,5222-5223,6112-6120,6250,8088,8393-8400,9960-9969,12000-65000',
                '--filter-udp=80,443,1119-1120,1024-1124,3724,3478-4380,5060-5062,6112-6119,6250,7000-8000,8088,8180-8181,12000-65535'
            ]
        },
        'Roblox': {
            'list_file': 'List-Roblox-PsHell.txt',
            'ipset_file': 'Ip-Set-Roblox.txt',
            'rules': [
                '--filter-tcp=80,443,1024-1124,2099,3724,3074-3479,4000,5060-5062,5222-5223,6112-6120,6250,8088,8393-8400,9960-9969,12000-65000',
                '--filter-udp=80,443,1119-1120,1024-1124,3724,3478-4380,5060-5062,6112-6119,6250,7000-8000,8088,8180-8181,12000-65535'
            ]
        },
        'Ubisoft': {
            'list_file': 'List-Ubisoft-PsHell.txt',
            'rules': ['--filter-tcp=80,443,1024-1124,2099,3724,3074-3479,4000,5060-5062,5222-5223,6112-6120,6250,8088,8393-8400,9960-9969,12000-65000']
        },
        'BattlEye': {
            'list_file': 'List-Battleye-PsHell.txt',
            'rules': ['--filter-tcp=80,443,1024-1124,2099,3724,3074-3479,4000,5060-5062,5222-5223,6112-6120,6250,8088,8393-8400,9960-9969,12000-65000']
        },
        'Riot': {
            'list_file': 'List-Riot-PsHell.txt',
            'rules': ['--filter-tcp=80,443,1024-1124,2099,3724,3074-3479,4000,5060-5062,5222-5223,6112-6120,6250,8088,8393-8400,9960-9969,12000-65000']
        },
        'Electronic Arts': {
            'list_file': 'List-Electronicarts-PsHell.txt',
            'ipset_file': 'Ip-Set-Elecronicarts.txt',
            'rules': ['--filter-tcp=80,443,1024-1124,2099,3724,3074-3479,4000,5060-5062,5222-5223,6112-6120,6250,8088,8393-8400,9960-9969,12000-65000']
        },
        'Epic Games': {
            'list_file': 'List-EpicGames-PsHell.txt',
            'rules': ['--filter-tcp=80,443,1024-1124,2099,3724,3074-3479,4000,5060-5062,5222-5223,6112-6120,6250,8088,8393-8400,9960-9969,12000-65000']
        },
        'Apex Legends': {
            'list_file': 'List-ApexLegends-PsHell.txt',
            'ipset_file': 'Ip-Set-ApexLegends.txt',
            'rules': [
                '--filter-tcp=80,443,1024-1124,2099,3724,3074-3479,4000,5060-5062,5222-5223,6112-6120,6250,8088,8393-8400,9960-9969,12000-65000',
                '--filter-udp=80,443,1119-1120,1024-1124,3724,3478-4380,5060-5062,6112-6119,6250,7000-8000,8088,8180-8181,12000-65535'
            ]
        },
        'Battle.net': {
            'list_file': 'List-Battlenet-PsHell.txt',
            'ipset_file': 'Ip-Set-Battlenet.txt',
            'rules': [
                '--filter-tcp=80,443,1024-1124,2099,3724,3074-3479,4000,5060-5062,5222-5223,6112-6120,6250,8088,8393-8400,9960-9969,12000-65000',
                '--filter-udp=80,443,1119-1120,1024-1124,3724,3478-4380,5060-5062,6112-6119,6250,7000-8000,8088,8180-8181,12000-65535'
            ]
        },
        'YouTube': {
            'list_file': 'List-Youtube-PsHell.txt',
            'ipset_file': 'Ip-Set-Youtube.txt',
            'ipset_file_none': 'Ip-Set-YoutubeNone.txt',
            'hostlist_domains': 'youtube.com,ytimg.com',
            'rules': [
                '--filter-tcp=80,443,1935',
                '--filter-udp=80,443,3478-3481,19302-19309'
            ]
        },
        'Twitch': {
            'list_file': 'List-Twitch-PsHell.txt',
            'ipset_file': 'Ip-Set-Twitch.txt',
            'hostlist_domains': 'twitch.tv',
            'rules': [
                '--filter-tcp=80,443,1935',
                '--filter-udp=80,443,3478-3481,19302-19309'
            ]
        },
        'AnimeGo': {
            'list_file': 'List-Anime-PsHell.txt',
            'rules': ['--filter-tcp=80,443,1935']
        },
        'CurseForge': {
            'list_file': 'List-CurseForge-PsHell.txt',
            'rules': ['--filter-tcp=80,443,21,20,8080']
        },
        'Modrinth': {
            'list_file': 'List-Modrinth-PsHell.txt',
            'rules': ['--filter-tcp=80,443,21,20,8080']
        },
        'Cloudflare': {
            'list_file': 'List-Cloudflare-PsHell.txt',
            'ipset_file': 'Ip-Set-Cloudfare.txt',
            'rules': ['--filter-tcp=80,443,8080', '--filter-udp=80,443,8080']
        },
        'Amazon': {
            'list_file': 'List-Amazon-PsHell.txt',
            'ipset_file': 'Ip-Set-Amazon.txt',
            'rules': ['--filter-tcp=80,443,8080', '--filter-udp=80,443,8080']
        },
        'Akamai': {
            'list_file': 'List-Akamai-PsHell.txt',
            'ipset_file': 'Ip-Set-Akamai.txt',
            'rules': []
        },
        'Facebook': {
            'list_file': 'List-FaceBook-PsHell.txt',
            'rules': []
        },
        'Google': {
            'list_file': 'List-Google-PsHell.txt',
            'ipset_file': 'Ip-Set-GoogleCloud.txt',
            'rules': []
        },
        'Instagram': {
            'list_file': 'List-Instagram-PsHell.txt',
            'rules': ['--filter-tcp=80']
        },
        'Spotify': {
            'list_file': 'List-Spotify-PsHell.txt',
            'rules': ['--filter-tcp=80,4070,57621', '--filter-udp=443,4070']
        },
        'Speedtest': {
            'list_file': 'List-SpeedTest-PsHell.txt',
            'rules': ['--filter-tcp=80']
        },
        'Apple': {
            'list_file': 'List-Apple-PsHell.txt',
            'rules': ['--filter-tcp=80,443,5223']
        },
        'Chess': {
            'list_file': 'List-Chess-PsHell.txt',
            'rules': ['--filter-tcp=80,443']
        },
        'NewGrounds': {
            'list_file': 'List-NewGrounds-PsHell.txt',
            'ipset_file': 'Ip-Set-NewGrounds.txt',
            'rules': ['--filter-tcp=80,443']
        },
        'GitHub': {
            'list_file': 'List-GitHub-PsHell.txt',
            'ipset_file': 'Ip-Set-GitHub.txt',
            'rules': [
                '--filter-tcp=443,80,22,25,9418,122,8080,8443,1336,3033,3037,33064486,5115,5208,6379,8001,8090,8149,8300-8302,9000,9102,9105,9200-9300,11211',
                '--filter-udp=161,8125,8301-8302,25827'
            ]
        }
    }

    REQUIRED_BIN_FILES = [
        'cygwin1.dll',
        'DeePsHell.exe',
        'dht_find_node.bin',
        'dht_get_peers.bin',
        'discord-ip-discovery-without-port.bin',
        'discord-ip-discovery-with-port.bin',
        'dtls_clienthello_w3_org.bin',
        'game_filter.enabled',
        'http_iana_org.bin',
        'isakmp_initiator_request.bin',
        'quic_initial_facebook_com.bin',
        'quic_initial_facebook_com_quiche.bin',
        'quic_initial_rutracker_org.bin',
        'quic_initial_rutracker_org_kyber_1.bin',
        'quic_initial_rutracker_org_kyber_2.bin',
        'quic_initial_vk_com.bin',
        'quic_initial_www_google_com.bin',
        'quic_short_header.bin',
        'stun.bin',
        'tls_clienthello_4pda_to.bin',
        'tls_clienthello_gosuslugi_ru.bin',
        'tls_clienthello_iana_org.bin',
        'tls_clienthello_max_ru.bin',
        'tls_clienthello_rutracker_org_kyber.bin',
        'tls_clienthello_sberbank_ru.bin',
        'tls_clienthello_vk_com.bin',
        'tls_clienthello_vk_com_kyber.bin',
        'tls_clienthello_www_google_com.bin',
        'WinDivert.dll',
        'WinDivert64.sys',
        'wireguard_initiation.bin',
        'wireguard_response.bin',
        'zero_256.bin',
        'zero_512.bin',
        'zero_1024.bin'
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeePsHell Launcher")
        self.setGeometry(100, 100, 950, 700)
        self.setMinimumSize(850, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a1a0a;
                border: 2px solid #00aa00;
                border-radius: 15px;
            }
        """)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.deepshell_process = None
        self.is_running = False
        self.other_deepshell_running = False
        self.other_fixes_running = False
        self.detected_fix_name = ""
        self.detected_fix_key = ""
        self.panel_visible = None
        self.drag_pos = None

        self.central_widget = QWidget()
        self.central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

        self.gradient_phase = 0

        self.bin_path = self.find_bin_directory()
        self.deepshell_exe_path = None
        if self.bin_path:
            self.deepshell_exe_path = self.bin_path / "DeePsHell.exe"

        self.program_categories = {
            'messengers': sorted(['Discord', 'FaceTime', 'Google Meet', 'Signal',
                                 'Snapchat', 'Telegram', 'Viber', 'WhatsApp']),
            'watch': sorted(['AnimeGo', 'Twitch', 'YouTube']),
            'games': sorted(['Apex Legends', 'Battle.net', 'Battlefield', 'BattlEye',
                            'Electronic Arts', 'Epic Games', 'Riot', 'Roblox',
                            'Steam', 'Ubisoft', 'NewGrounds']),
            'minecraft': sorted(['CurseForge', 'Modrinth']),
            'others': sorted(['Akamai', 'Amazon', 'Apple', 'Chess', 'Cloudflare',
                            'Facebook', 'Google', 'Instagram', 'Spotify', 'Speedtest',
                            'GitHub'])
        }

        data_dir = get_data_dir()
        self.config_file = Path(data_dir) / "deepshell_config.json"
        self.load_settings()
        self.panel_width = 300

        self.current_date = datetime.now()
        self.season = self.detect_season()
        self.snowflakes = []
        self.snow_timer = None
        self.pumpkins = []

        self.create_custom_title_bar()
        self.create_launch_button()
        self.create_status_indicator()
        self.create_panels()
        self.create_top_buttons()
        self.apply_enhanced_gradient()

        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_gradient)
        self.animation_timer.start(50)

        self.status_check_timer = QTimer()
        self.status_check_timer.timeout.connect(self.check_deepshell_status)
        self.status_check_timer.start(2000)

        self.set_window_icon()
        self.update_layout()
        self.check_deepshell_status()

        self.setup_seasonal_effects()

        atexit.register(self.cleanup_on_exit)

    def detect_season(self):
        month = self.current_date.month
        day = self.current_date.day
        if month == 1:
            return 'winter'
        elif month == 2 and day == 14:
            return 'valentine'
        elif month == 10 and day == 31:
            return 'halloween'
        else:
            return 'normal'

    def setup_seasonal_effects(self):
        if self.season == 'winter':
            for _ in range(50):
                self.snowflakes.append(SnowFlake(self.width(), self.height()))
            self.snow_timer = QTimer()
            self.snow_timer.timeout.connect(self.update_snow)
            self.snow_timer.start(50)
        elif self.season == 'halloween':
            self.pumpkins = []
            for i in range(5):
                x = random.randint(50, self.width() - 100)
                y = self.height() - 80 + random.randint(-10, 10)
                self.pumpkins.append((x, y))
        elif self.season == 'valentine':
            self.launch_btn.setText("❤️ Запуск")
            self.launch_btn.setStyleSheet(self.launch_btn.styleSheet().replace("🚀", "❤️"))
            self.title_icon.setText("❤️")

    def update_snow(self):
        if not self.snowflakes:
            return
        for flake in self.snowflakes:
            flake.fall(self.height())
        self.central_widget.update()

    def draw_mountains(self, painter, width, height):
        painter.setBrush(QColor(255, 255, 255, 80))
        painter.setPen(Qt.NoPen)
        points = [
            [(0, height), (width*0.2, height*0.6), (width*0.4, height)],
            [(width*0.3, height), (width*0.5, height*0.5), (width*0.7, height)],
            [(width*0.6, height), (width*0.8, height*0.7), (width, height)]
        ]
        for triangle in points:
            polygon = QPolygonF([QPointF(x, y) for x, y in triangle])
            painter.drawPolygon(polygon)

    def draw_snow(self, painter, width, height):
        painter.setPen(Qt.NoPen)
        for flake in self.snowflakes:
            painter.setBrush(QColor(255, 255, 255, int(flake.opacity * 255)))
            painter.drawEllipse(int(flake.x), int(flake.y), flake.size, flake.size)

    def draw_pumpkins(self, painter, width, height):
        painter.setBrush(QColor(255, 140, 0))
        painter.setPen(QPen(Qt.black, 2))
        for x, y in self.pumpkins:
            painter.drawEllipse(x, y, 50, 40)
            painter.setBrush(Qt.black)
            painter.drawEllipse(x+10, y+10, 8, 8)
            painter.drawEllipse(x+32, y+10, 8, 8)
            painter.drawArc(x+15, y+20, 20, 10, 0, 180*16)
            painter.setBrush(QColor(255, 140, 0))

    def update_gradient(self):
        self.gradient_phase = (self.gradient_phase + 0.02) % (2 * 3.14159)
        pixmap = QPixmap(self.central_widget.width(), self.central_widget.height())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        center_x = self.central_widget.width() / 2
        center_y = self.central_widget.height() / 2
        radius = min(center_x, center_y) * 1.5
        wave = (math.sin(self.gradient_phase) + 1) * 0.1
        gradient = QRadialGradient(center_x, center_y, radius)
        gradient.setColorAt(0.0, QColor(0, 50 + int(20 * wave), 0))
        gradient.setColorAt(0.3, QColor(0, 30 + int(15 * wave), 0))
        gradient.setColorAt(0.6, QColor(0, 20 + int(10 * wave), 0))
        gradient.setColorAt(0.8, QColor(0, 10 + int(5 * wave), 0))
        gradient.setColorAt(1.0, QColor(0, 0, 0))
        painter.fillRect(0, 0, self.central_widget.width(), self.central_widget.height(), gradient)
        if self.season == 'winter':
            self.draw_mountains(painter, self.central_widget.width(), self.central_widget.height())
            self.draw_snow(painter, self.central_widget.width(), self.central_widget.height())
        elif self.season == 'halloween':
            self.draw_pumpkins(painter, self.central_widget.width(), self.central_widget.height())
        pen = QPen(QColor(0, 200, 0, 100))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRoundedRect(1, 1, self.central_widget.width() - 2, self.central_widget.height() - 2, 13, 13)
        painter.end()
        palette = self.central_widget.palette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.central_widget.setPalette(palette)
        self.central_widget.update()
        self.update_status_indicator()

    def find_bin_directory(self):
        try:
            possible_paths = [
                "bin",
                "DeePsHell/bin",
                "dist/bin",
                "DeePsHell/dist/bin",
            ]
            for path in possible_paths:
                full_path = get_resource_path(path)
                if os.path.exists(full_path):
                    exe_path = os.path.join(full_path, "DeePsHell.exe")
                    if os.path.exists(exe_path):
                        print(f"Найден DeePsHell.exe в: {full_path}")
                        return Path(full_path)
        except:
            pass

        possible_paths = [
            Path("bin"),
            Path("DeePsHell/bin"),
            Path("dist/bin"),
            Path("DeePsHell/dist/bin"),
            Path(__file__).parent / "bin",
            Path(__file__).parent / "DeePsHell" / "bin",
            Path(__file__).parent.parent / "bin",
            Path.cwd(),
            Path.cwd() / "bin",
        ]
        for path in possible_paths:
            if path.exists():
                exe_path = path / "DeePsHell.exe"
                if exe_path.exists():
                    print(f"Найден DeePsHell.exe в: {path}")
                    return path
                elif path.name == "DeePsHell.exe":
                    return path.parent
        print("Папка bin с DeePsHell.exe не найдена.")
        return None

    def set_window_icon(self):
        icon_paths = [
            "bin/Доп/DeePsHell.ico",
            "DeePsHell/bin/Доп/DeePsHell.ico",
            "bin/Доп/DeePsHell.ico",
            "DeePsHell.ico",
            "dist/bin/Доп/DeePsHell.ico",
            "DeePsHell/dist/bin/Доп/DeePsHell.ico",
        ]
        for icon_path in icon_paths:
            try:
                full_path = get_resource_path(icon_path)
                if os.path.exists(full_path):
                    self.setWindowIcon(QIcon(full_path))
                    print(f"Иконка загружена: {full_path}")
                    return
            except:
                continue
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            local_icon = os.path.join(script_dir, "DeePsHell.ico")
            if os.path.exists(local_icon):
                self.setWindowIcon(QIcon(local_icon))
                print(f"Иконка загружена: {local_icon}")
                return
        except:
            pass
        print("Иконка не найдена. Используется стандартная иконка.")

    def load_settings(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                if isinstance(config_data, dict) and 'selected_programs' in config_data:
                    self.selected_programs = config_data.get('selected_programs', {})
                    settings = config_data.get('settings', {})
                    self.host_fakesplit_mod = settings.get('host_fakesplit_mod', 'www.google.com')
                    self.dpi_desync_repeats = settings.get('dpi_desync_repeats', '6')
                    self.dpi_desync_split_seqovl = settings.get('dpi_desync_split_seqovl', '650-720')
                    self.dpi_desync_autottl = settings.get('dpi_desync_autottl', '2')
                    self.dpi_desync_protocol = settings.get('dpi_desync_protocol', '1')
                    self.dpi_desync_cutoff = settings.get('dpi_desync_cutoff', '2')
                    self.dpi_desync_split_pos = settings.get('dpi_desync_split_pos', '2')
                    self.dpi_desync_split_pos_sniext = settings.get('dpi_desync_split_pos_sniext', '')
                    self.dpi_desync_badseq_increment = settings.get('dpi_desync_badseq_increment', '0')
                    self.strategy = settings.get('strategy', 'standard')
                    self.debug_mode = settings.get('debug_mode', False)
                    self.use_exclude = settings.get('use_exclude', False)
                    self.use_youtube_none = settings.get('use_youtube_none', False)
                    log_message(f"Настройки загружены из {self.config_file}")
                else:
                    self.selected_programs = config_data
                    self.host_fakesplit_mod = 'www.google.com'
                    self.dpi_desync_repeats = '6'
                    self.dpi_desync_split_seqovl = '650-720'
                    self.dpi_desync_autottl = '2'
                    self.dpi_desync_protocol = '1'
                    self.dpi_desync_cutoff = '2'
                    self.dpi_desync_split_pos = '2'
                    self.dpi_desync_split_pos_sniext = ''
                    self.dpi_desync_badseq_increment = '0'
                    self.strategy = 'standard'
                    self.debug_mode = False
                    self.use_exclude = False
                    self.use_youtube_none = False
                    log_message(f"Настройки загружены из {self.config_file} (старый формат)")
                for category in self.program_categories:
                    if category not in self.selected_programs:
                        self.selected_programs[category] = {}
                    for program in self.program_categories[category]:
                        if program not in self.selected_programs[category]:
                            self.selected_programs[category][program] = False
            except Exception as e:
                log_message(f"Ошибка загрузки настроек: {e}")
                self.set_default_settings()
        else:
            self.set_default_settings()

    def set_default_settings(self):
        self.selected_programs = {}
        for category, programs in self.program_categories.items():
            self.selected_programs[category] = {}
            for program in programs:
                self.selected_programs[category][program] = False
        self.host_fakesplit_mod = 'www.google.com'
        self.dpi_desync_repeats = '6'
        self.dpi_desync_split_seqovl = '650-720'
        self.dpi_desync_autottl = '2'
        self.dpi_desync_protocol = '1'
        self.dpi_desync_cutoff = '2'
        self.dpi_desync_split_pos = '2'
        self.dpi_desync_split_pos_sniext = ''
        self.dpi_desync_badseq_increment = '0'
        self.strategy = 'standard'
        self.debug_mode = False
        self.use_exclude = False
        self.use_youtube_none = False
        log_message("Установлены настройки по умолчанию")

    def save_settings(self):
        try:
            for category in self.program_categories:
                if category not in self.selected_programs:
                    self.selected_programs[category] = {}
                for program in self.program_categories[category]:
                    if program not in self.selected_programs[category]:
                        self.selected_programs[category][program] = False
            config = {
                'selected_programs': self.selected_programs,
                'settings': {
                    'host_fakesplit_mod': self.host_fakesplit_mod,
                    'dpi_desync_repeats': self.dpi_desync_repeats,
                    'dpi_desync_split_seqovl': self.dpi_desync_split_seqovl,
                    'dpi_desync_autottl': self.dpi_desync_autottl,
                    'dpi_desync_protocol': self.dpi_desync_protocol,
                    'dpi_desync_cutoff': self.dpi_desync_cutoff,
                    'dpi_desync_split_pos': self.dpi_desync_split_pos,
                    'dpi_desync_split_pos_sniext': self.dpi_desync_split_pos_sniext,
                    'dpi_desync_badseq_increment': self.dpi_desync_badseq_increment,
                    'strategy': self.strategy,
                    'debug_mode': self.debug_mode,
                    'use_exclude': self.use_exclude,
                    'use_youtube_none': self.use_youtube_none,
                }
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            log_message(f"Настройки сохранены в {self.config_file}")
        except Exception as e:
            log_message(f"Ошибка сохранения настроек: {e}")

    def normalize_url(self, url):
        url = re.sub(r'^https?://', '', url)
        url = re.sub(r'\/.*$', '', url)
        return url.strip()

    def create_custom_title_bar(self):
        self.title_bar = QWidget(self)
        self.title_bar.setFixedHeight(35)
        self.title_bar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #002200, stop:1 #001100);
                border-top-left-radius: 13px;
                border-top-right-radius: 13px;
                border-bottom: 1px solid #00aa00;
            }
        """)
        layout = QHBoxLayout(self.title_bar)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)
        self.title_icon = QLabel("🚀")
        self.title_icon.setStyleSheet("font-size: 16px; color: #00ff00;")
        layout.addWidget(self.title_icon)
        self.title_label = QLabel("DeePsHell Launcher v2.0")
        self.title_label.setStyleSheet("color: #00ff00; font-weight: bold; font-size: 12px; background: transparent;")
        layout.addWidget(self.title_label)
        layout.addStretch()
        btn_size = 22
        self.minimize_btn = QPushButton("—")
        self.minimize_btn.setFixedSize(btn_size, btn_size)
        self.minimize_btn.setStyleSheet("""
            QPushButton {
                background: #008800;
                color: #000000;
                border: 1px solid #00aa00;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover { background: #00aa00; }
            QPushButton:pressed { background: #006600; }
        """)
        self.minimize_btn.clicked.connect(self.showMinimized)
        layout.addWidget(self.minimize_btn)
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(btn_size, btn_size)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: #880000;
                color: #ffffff;
                border: 1px solid #aa0000;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover { background: #aa0000; }
            QPushButton:pressed { background: #660000; }
        """)
        self.close_btn.clicked.connect(self.close)
        layout.addWidget(self.close_btn)

    def create_status_indicator(self):
        self.status_label = QLabel("🔴 DeePsHell не запущен", self)
        self.status_label.setFixedSize(350, 40)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setCursor(Qt.ArrowCursor)
        self.indicator_glow = QGraphicsDropShadowEffect()
        self.indicator_glow.setBlurRadius(15)
        self.indicator_glow.setOffset(0, 0)
        self.status_label.setGraphicsEffect(self.indicator_glow)
        self.update_status_indicator()

    def update_status_indicator(self):
        if self.is_running:
            self.status_label.setText("🟢 DeePsHell запущен")
            self.status_label.setStyleSheet("""
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #00ff00, stop:1 #00aa00);
                    color: #000000;
                    font-weight: bold;
                    font-size: 12px;
                    border: 2px solid #00ff00;
                    border-radius: 8px;
                    padding: 5px;
                }
            """)
            self.indicator_glow.setColor(QColor(0, 255, 0, 180))
            self.launch_btn.set_running(True)
        elif self.other_deepshell_running:
            self.status_label.setText("🟡 Другой файл с название DeePsHell запущен")
            self.status_label.setStyleSheet("""
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #ffff00, stop:1 #aaaa00);
                    color: #000000;
                    font-weight: bold;
                    font-size: 12px;
                    border: 2px solid #ffff00;
                    border-radius: 8px;
                    padding: 5px;
                }
            """)
            self.indicator_glow.setColor(QColor(255, 255, 0, 180))
            self.launch_btn.set_running(False)
        elif self.other_fixes_running and self.detected_fix_name:
            if 'goodbyedpi' in self.detected_fix_key:
                self.status_label.setText(f"🔵 {self.detected_fix_name} запущен")
                self.status_label.setStyleSheet("""
                    QLabel {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #00ccff, stop:1 #0088aa);
                        color: #000000;
                        font-weight: bold;
                        font-size: 12px;
                        border: 2px solid #00ccff;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """)
                self.indicator_glow.setColor(QColor(0, 200, 255, 180))
            else:
                self.status_label.setText(f"🟡 {self.detected_fix_name} запущен")
                self.status_label.setStyleSheet("""
                    QLabel {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #ffff00, stop:1 #aaaa00);
                        color: #000000;
                        font-weight: bold;
                        font-size: 12px;
                        border: 2px solid #ffff00;
                        border-radius: 8px;
                        padding: 5px;
                    }
                """)
                self.indicator_glow.setColor(QColor(255, 255, 0, 180))
            self.launch_btn.set_running(False)
        else:
            self.status_label.setText("🔴 DeePsHell не запущен")
            self.status_label.setStyleSheet("""
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #ff4444, stop:1 #aa0000);
                    color: #ffffff;
                    font-weight: bold;
                    font-size: 12px;
                    border: 2px solid #ff0000;
                    border-radius: 8px;
                    padding: 5px;
                }
            """)
            self.indicator_glow.setColor(QColor(255, 0, 0, 180))
            self.launch_btn.set_running(False)

    def check_deepshell_running(self):
        try:
            current_pid = os.getpid()
            our_exe_path = None
            if self.deepshell_exe_path and self.deepshell_exe_path.exists():
                our_exe_path = str(self.deepshell_exe_path.resolve()).lower()
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() == 'deepshell.exe':
                        if proc.info['pid'] != current_pid:
                            is_our_process = False
                            if 'exe' in proc.info and proc.info['exe']:
                                proc_exe_path = str(proc.info['exe']).lower()
                                if our_exe_path and proc_exe_path == our_exe_path:
                                    is_our_process = True
                            if not is_our_process:
                                return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, FileNotFoundError):
                    continue
            return False
        except Exception as e:
            return False

    def check_other_fixes_running(self):
        try:
            for fix_key, process_names in self.OTHER_FIXES.items():
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if proc.info['name'] and proc.info['name'].lower() in process_names:
                            self.detected_fix_key = fix_key
                            self.detected_fix_name = fix_key.replace('_', ' ').title()
                            return True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            self.detected_fix_key = ""
            self.detected_fix_name = ""
            return False
        except Exception as e:
            log_message(f"Ошибка проверки других фиксов: {e}")
            return False

    def check_deepshell_status(self):
        try:
            our_pid = self.get_deepshell_pid()
            if our_pid:
                self.is_running = True
                self.other_deepshell_running = False
                self.other_fixes_running = False
            else:
                self.is_running = False
                self.other_deepshell_running = self.check_deepshell_running()
                if not self.other_deepshell_running:
                    self.other_fixes_running = self.check_other_fixes_running()
                else:
                    self.other_fixes_running = False
            self.update_status_indicator()
        except Exception as e:
            log_message(f"Ошибка проверки статуса: {e}")

    def run_deepshell(self):
        if self.is_running:
            self.stop_deepshell()
        else:
            self.start_deepshell()

    def get_deepshell_pid(self):
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() == 'deepshell.exe':
                        current_pid = os.getpid()
                        if proc.info['pid'] != current_pid:
                            if 'cmdline' in proc.info and proc.info['cmdline']:
                                cmdline = ' '.join(proc.info['cmdline']).lower()
                                if '--daemon' in cmdline or '--wf-tcp' in cmdline:
                                    return proc.info['pid']
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return None
        except Exception as e:
            log_message(f"Ошибка получения PID DeePsHell: {e}")
            return None

    def start_deepshell(self):
        try:
            if self.other_deepshell_running:
                reply = QMessageBox.question(
                    self, 'Другой DeePsHell запущен',
                    'Другой экземпляр DeePsHell уже запущен.\nХотите остановить его и запустить новый?',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.kill_all_deepshell_processes()
                    QTimer.singleShot(1000, lambda: self.continue_deepshell_start())
                else:
                    return
            elif self.other_fixes_running:
                reply = QMessageBox.question(
                    self, 'Другой фикс запущен',
                    f'Обнаружен запущенный фикс: {self.detected_fix_name}\nХотите запустить DeePsHell одновременно?',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
                else:
                    self.continue_deepshell_start()
            else:
                self.continue_deepshell_start()
        except Exception as e:
            self.show_custom_error("Ошибка запуска", f"Не удалось запустить DeePsHell:\n\n{str(e)}")

    def continue_deepshell_start(self):
        try:
            check_result, error_message = self.check_required_files()
            if not check_result:
                self.show_custom_warning("Не найдены файлы", error_message)
                return
            bat_content = self.build_bat_content()
            if not bat_content:
                self.show_custom_error("Ошибка", "Не удалось создать команду запуска.")
                return
            base_path = self.bin_path.parent
            bat_path = base_path / "DeePsHell_Launcher.bat"
            with open(bat_path, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            log_message(f"Создан BAT-файл: {bat_path}")
            if self.debug_mode:
                log_message("Содержимое BAT-файла:\n" + bat_content)
            try:
                if self.debug_mode:
                    log_message("Запуск в режиме отладки (окно видимо)")
                    self.deepshell_process = subprocess.Popen(
                        f'"{bat_path}"',
                        shell=True,
                        cwd=str(base_path)
                    )
                else:
                    log_message("Запуск в фоновом режиме (окно скрыто)")
                    self.deepshell_process = subprocess.Popen(
                        f'"{bat_path}"',
                        shell=True,
                        cwd=str(base_path),
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                self.is_running = True
                self.other_deepshell_running = False
                self.other_fixes_running = False
                self.update_status_indicator()
                QTimer.singleShot(1000, self.check_process_started)
                if not self.debug_mode:
                    QTimer.singleShot(1000, lambda: self.cleanup_bat_file(bat_path))
                log_message("✅ DeePsHell запущен (ожидание подтверждения)")
            except Exception as e:
                log_message(f"Ошибка запуска процесса: {e}")
                self.show_custom_error("Ошибка запуска", f"Не удалось запустить DeePsHell:\n\n{str(e)}")
        except Exception as e:
            log_message(f"Критическая ошибка при запуске: {e}")
            self.show_custom_error("Критическая ошибка", f"Произошла ошибка:\n\n{str(e)}")

    def stop_deepshell(self):
        try:
            if self.deepshell_process:
                try:
                    self.deepshell_process.terminate()
                    self.deepshell_process.wait(timeout=3)
                    log_message("✅ DeePsHell остановлен")
                except:
                    try:
                        self.deepshell_process.kill()
                        log_message("✅ DeePsHell принудительно остановлен")
                    except:
                        log_message("⚠️ Не удалось остановить процесс")
                self.deepshell_process = None
            self.is_running = False
            self.update_status_indicator()
            log_message("✅ DeePsHell остановлен")
        except Exception as e:
            log_message(f"Ошибка остановки: {e}")

    def kill_all_deepshell_processes(self):
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() == 'deepshell.exe':
                        psutil.Process(proc.info['pid']).terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            subprocess.run("taskkill /f /im DeePsHell.exe >nul 2>&1", shell=True)
            log_message("Все процессы DeePsHell остановлены")
        except Exception as e:
            log_message(f"Ошибка остановки процессов: {e}")

    def cleanup_on_exit(self):
        try:
            self.stop_deepshell()
        except:
            pass

    def closeEvent(self, event):
        self.cleanup_on_exit()
        event.accept()

    def create_panels(self):
        self.settings_panel = QWidget(self)
        self.settings_panel.setFixedWidth(self.panel_width)
        self.settings_panel.setFixedHeight(self.height())
        self.settings_panel.move(self.width(), 0)
        self.settings_panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #001a00, stop:1 #000d00);
                border-left: 3px solid #00ff00;
                border-radius: 0px 15px 15px 0px;
            }
            QLabel {
                color: #00ff00;
                font-weight: bold;
                font-size: 14px;
                padding: 5px;
                background: transparent;
            }
            QGroupBox {
                color: #00ff00;
                font-weight: bold;
                border: 2px solid #00aa00;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: rgba(0, 30, 0, 0.3);
                font-size: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                font-size: 12px;
            }
            QRadioButton {
                color: #00ff00;
                spacing: 5px;
                font-size: 11px;
                padding: 5px;
                background: rgba(0, 40, 0, 0.2);
                border-radius: 8px;
                margin: 2px;
            }
            QRadioButton:hover {
                background: rgba(0, 60, 0, 0.4);
                border: 1px solid #00cc00;
            }
            QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px;
                border: 2px solid #00aa00;
                background: #002200;
            }
            QRadioButton::indicator:checked {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.4,
                    fx:0.5, fy:0.5, stop:0 #00ff00, stop:1 #00aa00);
                border: 2px solid #00ff00;
            }
            QCheckBox {
                color: #00ff00;
                spacing: 5px;
                font-size: 11px;
                padding: 5px;
                background: rgba(0, 40, 0, 0.2);
                border-radius: 8px;
            }
            QCheckBox:hover {
                background: rgba(0, 60, 0, 0.4);
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #00aa00;
                border-radius: 4px;
                background: #002200;
            }
            QCheckBox::indicator:checked {
                background: #00ff00;
                border: 2px solid #00ff00;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00aa00, stop:1 #006600);
                color: #000000;
                font-weight: bold;
                padding: 8px;
                border-radius: 8px;
                border: 2px solid #00ff00;
                font-size: 11px;
                margin: 3px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00cc00, stop:1 #008800);
                border: 2px solid #88ff88;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #006600, stop:1 #004400);
            }
            QLineEdit {
                background: #002200;
                color: #00ff00;
                border: 1px solid #00aa00;
                border-radius: 5px;
                padding: 4px;
                font-size: 10px;
                margin: 2px;
            }
            QLineEdit:hover {
                border: 1px solid #00ff00;
            }
        """)
        main_layout = QVBoxLayout(self.settings_panel)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(10, 30, 10, 10)
        main_layout.setSpacing(8)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #003300;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #00aa00;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #00cc00;
            }
        """)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 10, 0)
        layout.setSpacing(8)
        title_layout = QHBoxLayout()
        title_icon = QLabel("⚙️")
        title_icon.setStyleSheet("font-size: 16px;")
        title_label = QLabel("✨ Настройки запуска ✨")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent, stop:0.5 #00ff00, stop:1 transparent);
                height: 1px;
                border: none;
            }
        """)
        layout.addWidget(line)

        self.radio_group = QGroupBox("Стратегия обхода DPI")
        radio_layout = QVBoxLayout()
        self.radio_standard = QRadioButton("Стандарт")
        self.radio_fake = QRadioButton("Фейковый")
        self.radio_confusion = QRadioButton("Полная запутанность")
        self.radio_old = QRadioButton("OLD")
        if self.strategy == 'standard':
            self.radio_standard.setChecked(True)
        elif self.strategy == 'fake':
            self.radio_fake.setChecked(True)
        elif self.strategy == 'confusion':
            self.radio_confusion.setChecked(True)
        else:
            self.radio_old.setChecked(True)
        self.radio_standard.toggled.connect(self.on_strategy_changed)
        self.radio_fake.toggled.connect(self.on_strategy_changed)
        self.radio_confusion.toggled.connect(self.on_strategy_changed)
        self.radio_old.toggled.connect(self.on_strategy_changed)
        radio_layout.addWidget(self.radio_standard)
        radio_layout.addWidget(self.radio_fake)
        radio_layout.addWidget(self.radio_confusion)
        radio_layout.addWidget(self.radio_old)
        self.radio_group.setLayout(radio_layout)
        layout.addWidget(self.radio_group)

        self.debug_cb = QCheckBox("🔧 Дебаг режим")
        self.debug_cb.setChecked(self.debug_mode)
        self.debug_cb.stateChanged.connect(self.on_debug_changed)
        layout.addWidget(self.debug_cb)

        self.exclude_cb = QCheckBox("📁 Использовать Exclude")
        self.exclude_cb.setChecked(self.use_exclude)
        self.exclude_cb.stateChanged.connect(self.on_exclude_changed)
        layout.addWidget(self.exclude_cb)

        self.youtube_none_cb = QCheckBox("🎬 НЕ использовать IP Youtube")
        self.youtube_none_cb.setChecked(self.use_youtube_none)
        self.youtube_none_cb.stateChanged.connect(self.on_youtube_none_changed)
        layout.addWidget(self.youtube_none_cb)

        dpi_group = QGroupBox("Настраиваемые параметры DPI")
        dpi_layout = QVBoxLayout()
        dpi_layout.setSpacing(4)

        host_layout = QHBoxLayout()
        host_label = QLabel("Доп. домен:")
        host_label.setFixedWidth(120)
        host_label.setStyleSheet("font-size: 10px;")
        self.host_edit = QLineEdit()
        self.host_edit.setText(self.host_fakesplit_mod)
        self.host_edit.setPlaceholderText("www.google.com")
        self.host_edit.textChanged.connect(self.on_host_changed)
        host_layout.addWidget(host_label)
        host_layout.addWidget(self.host_edit)
        dpi_layout.addLayout(host_layout)

        repeats_layout = QHBoxLayout()
        repeats_label = QLabel("Repeats (1-12):")
        repeats_label.setFixedWidth(120)
        repeats_label.setStyleSheet("font-size: 10px;")
        self.repeats_edit = QLineEdit()
        self.repeats_edit.setText(self.dpi_desync_repeats)
        self.repeats_edit.setPlaceholderText("6 или 6-12")
        self.repeats_edit.textChanged.connect(self.on_repeats_changed)
        repeats_layout.addWidget(repeats_label)
        repeats_layout.addWidget(self.repeats_edit)
        dpi_layout.addLayout(repeats_layout)

        autottl_layout = QHBoxLayout()
        autottl_label = QLabel("Autottl (1-3):")
        autottl_label.setFixedWidth(120)
        autottl_label.setStyleSheet("font-size: 10px;")
        self.autottl_edit = QLineEdit()
        self.autottl_edit.setText(self.dpi_desync_autottl)
        self.autottl_edit.setPlaceholderText("2")
        self.autottl_edit.textChanged.connect(self.on_autottl_changed)
        autottl_layout.addWidget(autottl_label)
        autottl_layout.addWidget(self.autottl_edit)
        dpi_layout.addLayout(autottl_layout)

        protocol_layout = QHBoxLayout()
        protocol_label = QLabel("Any-protocol (1-3):")
        protocol_label.setFixedWidth(120)
        protocol_label.setStyleSheet("font-size: 10px;")
        self.protocol_edit = QLineEdit()
        self.protocol_edit.setText(self.dpi_desync_protocol)
        self.protocol_edit.setPlaceholderText("1")
        self.protocol_edit.textChanged.connect(self.on_protocol_changed)
        protocol_layout.addWidget(protocol_label)
        protocol_layout.addWidget(self.protocol_edit)
        dpi_layout.addLayout(protocol_layout)

        cutoff_layout = QHBoxLayout()
        cutoff_label = QLabel("Cutoff (1-12):")
        cutoff_label.setFixedWidth(120)
        cutoff_label.setStyleSheet("font-size: 10px;")
        self.cutoff_edit = QLineEdit()
        self.cutoff_edit.setText(self.dpi_desync_cutoff)
        self.cutoff_edit.setPlaceholderText("2")
        self.cutoff_edit.textChanged.connect(self.on_cutoff_changed)
        cutoff_layout.addWidget(cutoff_label)
        cutoff_layout.addWidget(self.cutoff_edit)
        dpi_layout.addLayout(cutoff_layout)

        split_pos_layout = QHBoxLayout()
        split_pos_label = QLabel("Split-pos (1-5):")
        split_pos_label.setFixedWidth(120)
        split_pos_label.setStyleSheet("font-size: 10px;")
        self.split_pos_edit = QLineEdit()
        self.split_pos_edit.setText(self.dpi_desync_split_pos)
        self.split_pos_edit.setPlaceholderText("2")
        self.split_pos_edit.textChanged.connect(self.on_split_pos_changed)
        split_pos_layout.addWidget(split_pos_label)
        split_pos_layout.addWidget(self.split_pos_edit)
        dpi_layout.addLayout(split_pos_layout)

        sniext_layout = QHBoxLayout()
        sniext_label = QLabel("Sniext (+1-3):")
        sniext_label.setFixedWidth(120)
        sniext_label.setStyleSheet("font-size: 10px;")
        self.sniext_edit = QLineEdit()
        self.sniext_edit.setText(self.dpi_desync_split_pos_sniext)
        self.sniext_edit.setPlaceholderText("например 1")
        self.sniext_edit.textChanged.connect(self.on_sniext_changed)
        sniext_layout.addWidget(sniext_label)
        sniext_layout.addWidget(self.sniext_edit)
        dpi_layout.addLayout(sniext_layout)

        badseq_layout = QHBoxLayout()
        badseq_label = QLabel("Badseq-incr (0-100000):")
        badseq_label.setFixedWidth(120)
        badseq_label.setStyleSheet("font-size: 10px;")
        self.badseq_edit = QLineEdit()
        self.badseq_edit.setText(self.dpi_desync_badseq_increment)
        self.badseq_edit.setPlaceholderText("0")
        self.badseq_edit.textChanged.connect(self.on_badseq_changed)
        badseq_layout.addWidget(badseq_label)
        badseq_layout.addWidget(self.badseq_edit)
        dpi_layout.addLayout(badseq_layout)

        seqovl_layout = QHBoxLayout()
        seqovl_label = QLabel("Seqovl (650-720):")
        seqovl_label.setFixedWidth(120)
        seqovl_label.setStyleSheet("font-size: 10px;")
        self.seqovl_edit = QLineEdit()
        self.seqovl_edit.setText(self.dpi_desync_split_seqovl)
        self.seqovl_edit.setPlaceholderText("650-720")
        self.seqovl_edit.textChanged.connect(self.on_seqovl_changed)
        seqovl_layout.addWidget(seqovl_label)
        seqovl_layout.addWidget(self.seqovl_edit)
        dpi_layout.addLayout(seqovl_layout)

        dpi_group.setLayout(dpi_layout)
        layout.addWidget(dpi_group)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent, stop:0.5 #00aa00, stop:1 transparent);
                height: 1px;
                border: none;
                margin: 10px 0;
            }
        """)
        layout.addWidget(line2)
        programs_btn = QPushButton("Выбор программ")
        programs_btn.clicked.connect(self.show_programs_dialog)
        layout.addWidget(programs_btn)
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        close_btn = QPushButton("💾 Сохранить и закрыть")
        close_btn.clicked.connect(self.save_and_hide_settings)
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00aa00, stop:1 #006600);
                border: 2px solid #00ff00;
                font-size: 11px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00cc00, stop:1 #008800);
                border: 2px solid #88ff88;
            }
        """)
        layout.addWidget(close_btn)
        content_widget.setMinimumHeight(1000)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        self.extra_panel = QWidget(self)
        self.extra_panel.setFixedWidth(self.panel_width)
        self.extra_panel.setFixedHeight(self.height())
        self.extra_panel.move(self.width(), 0)
        self.extra_panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #001a00, stop:1 #000d00);
                border-left: 3px solid #00ccff;
                border-radius: 0px 15px 15px 0px;
            }
            QLabel {
                color: #00ccff;
                font-weight: bold;
                font-size: 14px;
                padding: 5px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0088aa, stop:1 #005566);
                color: #000000;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #00ccff;
                font-size: 11px;
                text-align: left;
                margin: 3px 0;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00aacc, stop:1 #007788);
                border: 2px solid #88eeff;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #005566, stop:1 #003344);
            }
        """)
        layout = QVBoxLayout(self.extra_panel)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(10, 30, 10, 10)
        layout.setSpacing(5)
        title_layout = QHBoxLayout()
        title_icon = QLabel("🔧")
        title_icon.setStyleSheet("font-size: 16px;")
        title_label = QLabel("Дополнительные инструменты")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent, stop:0.5 #00ccff, stop:1 transparent);
                height: 1px;
                border: none;
                margin: 5px 0;
            }
        """)
        layout.addWidget(line)
        self.clear_temp_btn = QPushButton("🧹 Очистка временных файлов")
        self.clear_temp_btn.clicked.connect(self.clear_temp)
        layout.addWidget(self.clear_temp_btn)
        self.test_connection_btn = QPushButton("Тест сетевого соединения")
        self.test_connection_btn.clicked.connect(self.test_connection)
        layout.addWidget(self.test_connection_btn)
        self.dns_settings_btn = QPushButton("Настройки DNS серверов")
        self.dns_settings_btn.clicked.connect(self.show_dns_dialog)
        layout.addWidget(self.dns_settings_btn)
        self.log_viewer_btn = QPushButton("Просмотр логов")
        self.log_viewer_btn.clicked.connect(self.show_log_viewer)
        layout.addWidget(self.log_viewer_btn)
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        close_btn = QPushButton("✕ Закрыть меню")
        close_btn.clicked.connect(self.hide_extra_panel)
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #aa0000, stop:1 #660000);
                border: 2px solid #ff0000;
                font-size: 11px;
                padding: 10px;
            }
        """)
        layout.addWidget(close_btn)
        self.settings_panel.hide()
        self.extra_panel.hide()

    def on_strategy_changed(self):
        if self.radio_standard.isChecked():
            self.strategy = 'standard'
        elif self.radio_fake.isChecked():
            self.strategy = 'fake'
        elif self.radio_confusion.isChecked():
            self.strategy = 'confusion'
        else:
            self.strategy = 'old'
        self.save_settings()

    def on_debug_changed(self):
        self.debug_mode = self.debug_cb.isChecked()
        self.save_settings()

    def on_exclude_changed(self):
        self.use_exclude = self.exclude_cb.isChecked()
        self.save_settings()

    def on_youtube_none_changed(self):
        self.use_youtube_none = self.youtube_none_cb.isChecked()
        self.save_settings()

    def on_host_changed(self, text):
        normalized = self.normalize_url(text)
        self.host_fakesplit_mod = normalized
        self.save_settings()

    def on_repeats_changed(self, text):
        if re.match(r'^\d+$', text):
            value = int(text)
            if 1 <= value <= 12:
                self.dpi_desync_repeats = text
                self.save_settings()
        elif re.match(r'^\d+-\d+$', text):
            parts = text.split('-')
            if len(parts) == 2:
                try:
                    start = int(parts[0])
                    end = int(parts[1])
                    if 1 <= start <= 12 and 1 <= end <= 12 and start <= end:
                        self.dpi_desync_repeats = text
                        self.save_settings()
                except:
                    pass

    def on_autottl_changed(self, text):
        if re.match(r'^\d+$', text):
            value = int(text)
            if 1 <= value <= 3:
                self.dpi_desync_autottl = text
                self.save_settings()

    def on_protocol_changed(self, text):
        if re.match(r'^\d+$', text):
            value = int(text)
            if 1 <= value <= 3:
                self.dpi_desync_protocol = text
                self.save_settings()

    def on_cutoff_changed(self, text):
        if re.match(r'^\d+$', text):
            value = int(text)
            if 1 <= value <= 12:
                self.dpi_desync_cutoff = text
                self.save_settings()

    def on_split_pos_changed(self, text):
        if re.match(r'^\d+$', text):
            value = int(text)
            if 1 <= value <= 5:
                self.dpi_desync_split_pos = text
                self.save_settings()

    def on_sniext_changed(self, text):
        if text == '' or (re.match(r'^\d+$', text) and 1 <= int(text) <= 3):
            self.dpi_desync_split_pos_sniext = text
            self.save_settings()

    def on_badseq_changed(self, text):
        if re.match(r'^\d+$', text):
            value = int(text)
            if 0 <= value <= 100000:
                self.dpi_desync_badseq_increment = text
                self.save_settings()

    def on_seqovl_changed(self, text):
        if re.match(r'^\d+$', text):
            value = int(text)
            if 650 <= value <= 720:
                self.dpi_desync_split_seqovl = text
                self.save_settings()
        elif re.match(r'^\d+-\d+$', text):
            parts = text.split('-')
            if len(parts) == 2:
                try:
                    start = int(parts[0])
                    end = int(parts[1])
                    if 650 <= start <= 720 and 650 <= end <= 720 and start <= end:
                        self.dpi_desync_split_seqovl = text
                        self.save_settings()
                except:
                    pass

    def save_and_hide_settings(self):
        self.save_settings()
        self.hide_settings_panel()

    def create_top_buttons(self):
        self.extra_btn = QPushButton("🔧", self)
        self.extra_btn.setFixedSize(40, 40)
        self.extra_btn.setCursor(Qt.PointingHandCursor)
        self.extra_btn.setStyleSheet("""
        QPushButton {
            background: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.8,
                fx: 0.4, fy: 0.4,
                stop: 0 #00ccff,
                stop: 0.7 #0088aa,
                stop: 1 #005566
            );
            color: #001122;
            border: 2px solid #00ccff;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.8,
                fx: 0.4, fy: 0.4,
                stop: 0 #88eeff,
                stop: 0.7 #00aacc,
                stop: 1 #007788
            );
            border: 2px solid #88eeff;
        }
        QPushButton:pressed {
            background: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.8,
                fx: 0.4, fy: 0.4,
                stop: 0 #005566,
                stop: 0.7 #003344,
                stop: 1 #002233
            );
        }
    """)
        self.extra_btn.clicked.connect(self.show_extra_panel)
        self.settings_btn = QPushButton("⚙️", self)
        self.settings_btn.setFixedSize(40, 40)
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.setStyleSheet("""
        QPushButton {
            background: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.8,
                fx: 0.4, fy: 0.4,
                stop: 0 #00ff00,
                stop: 0.7 #00aa00,
                stop: 1 #006600
            );
            color: #001100;
            border: 2px solid #00ff00;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.8,
                fx: 0.4, fy: 0.4,
                stop: 0 #88ff88,
                stop: 0.7 #00cc00,
                stop: 1 #008800
            );
            border: 2px solid #88ff88;
        }
        QPushButton:pressed {
            background: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.8,
                fx: 0.4, fy: 0.4,
                stop: 0 #006600,
                stop: 0.7 #004400,
                stop: 1 #002200
            );
        }
    """)
        self.settings_btn.clicked.connect(self.show_settings_panel)
        self.update_button_positions()

    def create_launch_button(self):
        self.launch_btn = AnimatedLaunchButton("Запуск", self)
        self.launch_btn.setFixedSize(180, 180)
        self.launch_btn.setCursor(Qt.PointingHandCursor)
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(25)
        self.glow_effect.setColor(QColor(255, 0, 0, 200))
        self.glow_effect.setOffset(0, 0)
        self.launch_btn.setGraphicsEffect(self.glow_effect)
        self.launch_btn.glow_effect = self.glow_effect
        self.launch_btn.clicked.connect(self.run_deepshell)
        self.center_launch_button()

    def apply_enhanced_gradient(self):
        self.central_widget.setAutoFillBackground(True)
        self.update_gradient()

    def update_button_positions(self):
        if hasattr(self, 'extra_btn') and hasattr(self, 'settings_btn'):
            title_height = 35 if hasattr(self, 'title_bar') else 0
            self.extra_btn.move(self.width() - 90, title_height + 10)
            self.settings_btn.move(self.width() - 45, title_height + 10)

    def center_launch_button(self):
        if hasattr(self, 'launch_btn'):
            title_height = 35 if hasattr(self, 'title_bar') else 0
            x = (self.width() - self.launch_btn.width()) // 2
            y = title_height + ((self.height() - title_height - self.launch_btn.height()) // 2)
            self.launch_btn.move(x, y)

    def update_layout(self):
        if hasattr(self, 'title_bar'):
            self.title_bar.setGeometry(0, 0, self.width(), 35)
        if hasattr(self, 'status_label'):
            self.status_label.move(20, self.height() - 60)
        self.update_button_positions()
        self.center_launch_button()
        panel_y = 35 if hasattr(self, 'title_bar') else 0
        panel_height = self.height() - panel_y
        self.settings_panel.setFixedHeight(panel_height)
        self.extra_panel.setFixedHeight(panel_height)
        if self.settings_panel.isVisible():
            self.settings_panel.move(self.width() - self.panel_width, panel_y)
        else:
            self.settings_panel.move(self.width(), panel_y)
        if self.extra_panel.isVisible():
            self.extra_panel.move(self.width() - self.panel_width, panel_y)
        else:
            self.extra_panel.move(self.width(), panel_y)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_layout()
        self.update_gradient()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if hasattr(self, 'title_bar') and event.y() < 35:
                self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_pos') and self.drag_pos is not None:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = None

    def show_settings_panel(self):
        if self.extra_panel.isVisible():
            self.hide_extra_panel()
        if not self.settings_panel.isVisible():
            self.settings_panel.show()
            self.settings_panel.raise_()
            self.pos_anim = QPropertyAnimation(self.settings_panel, b"pos")
            self.pos_anim.setDuration(300)
            self.pos_anim.setStartValue(QPoint(self.width(), self.settings_panel.y()))
            self.pos_anim.setEndValue(QPoint(self.width() - self.panel_width, self.settings_panel.y()))
            self.pos_anim.setEasingCurve(QEasingCurve.OutCubic)
            self.opacity_anim = QPropertyAnimation(self.settings_panel, b"windowOpacity")
            self.opacity_anim.setDuration(300)
            self.opacity_anim.setStartValue(0.0)
            self.opacity_anim.setEndValue(1.0)
            self.opacity_anim.setEasingCurve(QEasingCurve.OutCubic)
            self.anim_group = QParallelAnimationGroup()
            self.anim_group.addAnimation(self.pos_anim)
            self.anim_group.addAnimation(self.opacity_anim)
            self.anim_group.start()
            self.panel_visible = 'settings'
        self.update_layout()

    def hide_settings_panel(self):
        if self.settings_panel.isVisible():
            self.pos_anim = QPropertyAnimation(self.settings_panel, b"pos")
            self.pos_anim.setDuration(300)
            self.pos_anim.setStartValue(self.settings_panel.pos())
            self.pos_anim.setEndValue(QPoint(self.width(), self.settings_panel.y()))
            self.pos_anim.setEasingCurve(QEasingCurve.InCubic)
            self.opacity_anim = QPropertyAnimation(self.settings_panel, b"windowOpacity")
            self.opacity_anim.setDuration(300)
            self.opacity_anim.setStartValue(1.0)
            self.opacity_anim.setEndValue(0.0)
            self.opacity_anim.setEasingCurve(QEasingCurve.InCubic)
            self.anim_group = QParallelAnimationGroup()
            self.anim_group.addAnimation(self.pos_anim)
            self.anim_group.addAnimation(self.opacity_anim)
            self.anim_group.finished.connect(lambda: self.settings_panel.hide())
            self.anim_group.start()
            self.panel_visible = None

    def show_extra_panel(self):
        if self.settings_panel.isVisible():
            self.hide_settings_panel()
        if not self.extra_panel.isVisible():
            self.extra_panel.show()
            self.extra_panel.raise_()
            self.pos_anim = QPropertyAnimation(self.extra_panel, b"pos")
            self.pos_anim.setDuration(300)
            self.pos_anim.setStartValue(QPoint(self.width(), self.extra_panel.y()))
            self.pos_anim.setEndValue(QPoint(self.width() - self.panel_width, self.extra_panel.y()))
            self.pos_anim.setEasingCurve(QEasingCurve.OutCubic)
            self.opacity_anim = QPropertyAnimation(self.extra_panel, b"windowOpacity")
            self.opacity_anim.setDuration(300)
            self.opacity_anim.setStartValue(0.0)
            self.opacity_anim.setEndValue(1.0)
            self.opacity_anim.setEasingCurve(QEasingCurve.OutCubic)
            self.anim_group = QParallelAnimationGroup()
            self.anim_group.addAnimation(self.pos_anim)
            self.anim_group.addAnimation(self.opacity_anim)
            self.anim_group.start()
            self.panel_visible = 'extra'
        self.update_layout()

    def hide_extra_panel(self):
        if self.extra_panel.isVisible():
            self.pos_anim = QPropertyAnimation(self.extra_panel, b"pos")
            self.pos_anim.setDuration(300)
            self.pos_anim.setStartValue(self.extra_panel.pos())
            self.pos_anim.setEndValue(QPoint(self.width(), self.extra_panel.y()))
            self.pos_anim.setEasingCurve(QEasingCurve.InCubic)
            self.opacity_anim = QPropertyAnimation(self.extra_panel, b"windowOpacity")
            self.opacity_anim.setDuration(300)
            self.opacity_anim.setStartValue(1.0)
            self.opacity_anim.setEndValue(0.0)
            self.opacity_anim.setEasingCurve(QEasingCurve.InCubic)
            self.anim_group = QParallelAnimationGroup()
            self.anim_group.addAnimation(self.pos_anim)
            self.anim_group.addAnimation(self.opacity_anim)
            self.anim_group.finished.connect(lambda: self.extra_panel.hide())
            self.anim_group.start()
            self.panel_visible = None

    def check_file_exists(self, folder, filename):
        if not filename:
            return False
        try:
            if isinstance(folder, Path):
                try:
                    rel_to_cwd = str(folder.relative_to(Path.cwd()))
                    rel_path = os.path.join(rel_to_cwd, filename)
                except ValueError:
                    rel_path = os.path.join(folder.name, filename)
            else:
                rel_path = os.path.join(folder, filename)
            full_path = get_resource_path(rel_path)
            if os.path.exists(full_path):
                return True
        except:
            pass
        if isinstance(folder, Path):
            file_path = folder / filename
        else:
            file_path = Path(folder) / filename
        return file_path.exists()

    def get_selected_programs_list(self):
        selected = []
        for category in self.selected_programs:
            for program, is_selected in self.selected_programs[category].items():
                if is_selected:
                    selected.append(program)
        log_message(f"Выбраны программы: {selected}")
        return selected

    def build_bat_content(self):
        if not self.bin_path:
            log_message("Ошибка: bin_path не найден")
            return ""

        base_path = self.bin_path.parent
        lists_path = base_path / "Lists"
        ipset_path = base_path / "IpSet"
        exclude_path = base_path / "Exclude"

        service_bat_path = base_path / "service.bat"
        service_bat_exists = service_bat_path.exists()

        bat_lines = []
        bat_lines.append('@echo off')
        bat_lines.append('chcp 65001 >nul')
        bat_lines.append('cd /d "%~dp0"')

        if service_bat_exists:
            bat_lines.append('call service.bat load_game_filter')
        else:
            bat_lines.append('set GameFilter=')

        bat_lines.append('')
        bat_lines.append('set "BIN=%~dp0bin\\"')
        bat_lines.append('set "LISTS=%~dp0Lists\\"')
        bat_lines.append('set "IPSET=%~dp0IpSet\\"')
        bat_lines.append('set "EXCLUDE=%~dp0Exclude\\"')
        bat_lines.append('cd /d %BIN%')
        bat_lines.append('')

        selected_programs = self.get_selected_programs_list()
        if not selected_programs:
            bat_lines.append('echo Внимание: не выбрано ни одной программы. Будут применены только общие правила.')

        start_line = 'start "DeePsHell: %~n0"'
        if not self.debug_mode:
            start_line += ' /min'
            daemon_param = '--daemon '
        else:
            daemon_param = ''

        strategy = self.strategy

        params = []

        if strategy == 'standard':
            tcp_cmd = (f'--wf-tcp=1-65000,%GameFilter% '
                       f'--dpi-desync=fake,multisplit '
                       f'--dpi-desync-hostfakesplit-mod=host={self.host_fakesplit_mod} '
                       f'--dpi-desync-repeats={self.dpi_desync_repeats} '
                       f'--dpi-desync-fooling=ts,badsum '
                       f'--dpi-desync-badseq-increment={self.dpi_desync_badseq_increment} '
                       f'--dpi-desync-fake-tls="%BIN%tls_clienthello_www_google_com.bin" '
                       f'--dpi-desync-fake-http="%BIN%tls_clienthello_www_google_com.bin" '
                       f'--dpi-desync-fake-tls-mod=rnd,dupsid,none,sni=www.google.com')
            udp_cmd = (f'--wf-udp=80,443,500-1400,3724,3478-4380,5060-5062,5222-5243,6112-6119,6250,7000-8000,8088,8180-8181,9000-65535,%GameFilter% '
                       f'--dpi-desync=fake,multisplit '
                       f'--dpi-desync-repeats={self.dpi_desync_repeats} '
                       f'--dpi-desync-any-protocol={self.dpi_desync_protocol} '
                       f'--dpi-desync-cutoff=n{self.dpi_desync_cutoff} '
                       f'--dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" '
                       f'--dpi-desync-fake-unknown-udp="%BIN%quic_initial_www_google_com.bin"')
            params.append(f'{start_line} "%BIN%DeePsHell.exe" {daemon_param}{tcp_cmd} {udp_cmd} ^')
        elif strategy == 'fake':
            params.append(f'{start_line} "%BIN%DeePsHell.exe" {daemon_param}--wf-tcp=1-65000,%GameFilter% --dpi-desync=fake,split2 --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --wf-udp=80,443,500-1400,3724,3478-4380,5060-5062,5222-5243,6112-6119,6250,7000-8000,8088,8180-8181,9000-65535,%GameFilter% --dpi-desync=fake --dpi-desync-repeats={self.dpi_desync_repeats} --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" ^')
        elif strategy == 'confusion':
            split_pos = self.dpi_desync_split_pos
            if self.dpi_desync_split_pos_sniext:
                split_pos += f',sniext+{self.dpi_desync_split_pos_sniext}'
            tcp_cmd = (f'--wf-tcp=1-65000,%GameFilter% '
                       f'--dpi-desync=fake,multidisorder '
                       f'--dpi-desync-split-seqovl={self.dpi_desync_split_seqovl} '
                       f'--dpi-desync-split-pos={split_pos} '
                       f'--dpi-desync-fooling=ts,badsum '
                       f'--dpi-desync-fake-tls=^! '
                       f'--dpi-desync-hostfakesplit-mod=host=rkn.gov.ru '
                       f'--dpi-desync-hostfakesplit-midhost=host-2 '
                       f'--dpi-desync-fake-tls-mod=rnd,dupsid,padencap,none,sni=www.google.com '
                       f'--dpi-desync-badseq-increment={self.dpi_desync_badseq_increment} '
                       f'--dpi-desync-fake-tls="%BIN%tls_clienthello_max_ru.bin" '
                       f'--dpi-desync-fake-http="%BIN%tls_clienthello_max_ru.bin" '
                       f'--dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin"')
            udp_cmd = (f'--wf-udp=80,443,500-1400,3724,3478-4380,5060-5062,5222-5243,6112-6119,6250,7000-8000,8088,8180-8181,9000-65535,%GameFilter% '
                       f'--dpi-desync=fake,multidisorder '
                       f'--dpi-desync-split-pos=1,2,3,sniext+1 '
                       f'--dpi-desync-split-seqovl={self.dpi_desync_split_seqovl} '
                       f'--dpi-desync-repeats={self.dpi_desync_repeats} '
                       f'--dpi-desync=udplen '
                       f'--dpi-desync-repeats=4 '
                       f'--dpi-desync-fake-quic="%BIN%tls_clienthello_max_ru.bin" '
                       f'--dpi-desync-fake-wireguard="%BIN%tls_clienthello_max_ru.bin"')
            params.append(f'{start_line} "%BIN%DeePsHell.exe" {daemon_param}{tcp_cmd} {udp_cmd} ^')
        elif strategy == 'old':
            tcp_cmd = (f'--wf-tcp=1-65000,%GameFilter% '
                       f'--dpi-desync=multisplit '
                       f'--dpi-desync-split-pos=2,sniext+1 '
                       f'--dpi-desync-split-seqovl=679 '
                       f'--dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin"')
            udp_cmd = (f'--wf-udp=80,443,500-1400,3724,3478-4380,5060-5062,5222-5243,6112-6119,6250,7000-8000,8088,8180-8181,9000-65535,%GameFilter% '
                       f'--dpi-desync=multisplit '
                       f'--dpi-desync-repeats=6 '
                       f'--dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin"')
            params.append(f'{start_line} "%BIN%DeePsHell.exe" {daemon_param}{tcp_cmd} {udp_cmd} ^')

        params.append('')

        processed_programs = set()

        for program in selected_programs:
            if program in processed_programs:
                continue

            if program in self.INDIVIDUAL_PROGRAMS:
                program_info = self.INDIVIDUAL_PROGRAMS[program].copy()

                log_message(f"Добавляем правила для: {program}")

                if self.use_youtube_none and program == 'YouTube' and 'ipset_file_none' in program_info:
                    program_info['ipset_file'] = program_info['ipset_file_none']

                if strategy == 'standard' and 'rules_standard' in program_info:
                    program_rules = program_info['rules_standard']
                elif strategy == 'fake' and 'rules_fake' in program_info:
                    program_rules = program_info['rules_fake']
                elif strategy == 'confusion' and 'rules_confusion' in program_info:
                    program_rules = program_info['rules_confusion']
                elif strategy == 'old' and 'rules_old' in program_info:
                    program_rules = program_info['rules_old']
                elif 'rules' in program_info:
                    program_rules = program_info['rules']
                else:
                    program_rules = []

                is_see_program = program in ['YouTube', 'Twitch']

                for rule in program_rules:
                    if '--filter-tcp' in rule:
                        if '=' in rule:
                            ports = rule.split('=')[1].split(' ')[0].strip()
                            l7_param = ' --filter-l7=' + rule.split('--filter-l7=')[1] if '--filter-l7=' in rule else ''
                        else:
                            ports = rule.replace('--filter-tcp', '').strip()
                            l7_param = ''

                        if strategy == 'standard':
                            if is_see_program:
                                desync = (f' --ip-id=zero --dpi-desync=fake,multisplit --dpi-desync-hostfakesplit-mod=host={self.host_fakesplit_mod} '
                                          f'--dpi-desync-repeats={self.dpi_desync_repeats} --dpi-desync-fooling=ts,badsum '
                                          f'--dpi-desync-badseq-increment={self.dpi_desync_badseq_increment} '
                                          f'--dpi-desync-fake-tls-mod=rnd,sni=www.google.com --dpi-desync-fake-tls="%BIN%tls_clienthello_www_google_com.bin"')
                            else:
                                desync = (f' --dpi-desync=fake,multisplit --dpi-desync-hostfakesplit-mod=host={self.host_fakesplit_mod} '
                                          f'--dpi-desync-repeats={self.dpi_desync_repeats} --dpi-desync-fooling=ts,badsum '
                                          f'--dpi-desync-badseq-increment={self.dpi_desync_badseq_increment} '
                                          f'--dpi-desync-fake-tls-mod=rnd,sni=www.google.com --dpi-desync-fake-tls="%BIN%tls_clienthello_www_google_com.bin"')
                        elif strategy == 'fake':
                            if is_see_program:
                                desync = (f' --ip-id=zero --dpi-desync=fake,split2 --dpi-desync=multisplit --dpi-desync-split-seqovl=681 '
                                          f'--dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin"')
                            else:
                                desync = (f' --dpi-desync=fake,split2 --dpi-desync=multisplit --dpi-desync-split-seqovl=681 '
                                          f'--dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin"')
                        elif strategy == 'confusion':
                            if is_see_program:
                                desync = (f' --ip-id=zero --dpi-desync=fake,multidisorder --dpi-desync-split-seqovl={self.dpi_desync_split_seqovl} '
                                          f'--dpi-desync-split-pos=1,midsld --dpi-desync-fooling=ts,badsum --dpi-desync-fake-tls=^! '
                                          f'--dpi-desync-hostfakesplit-mod=host={self.host_fakesplit_mod} --dpi-desync-hostfakesplit-midhost=host-2 '
                                          f'--dpi-desync-fake-tls-mod=rnd,sni=www.google.com --dpi-desync-badseq-increment={self.dpi_desync_badseq_increment} '
                                          f'--dpi-desync-fake-tls="%BIN%tls_clienthello_www_google_com.bin" --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" '
                                          f'--dpi-desync-fake-tls-mod=none')
                            else:
                                desync = (f' --dpi-desync=fake,multidisorder --dpi-desync-split-seqovl={self.dpi_desync_split_seqovl} '
                                          f'--dpi-desync-split-pos=1,midsld --dpi-desync-fooling=ts,badsum --dpi-desync-fake-tls=^! '
                                          f'--dpi-desync-hostfakesplit-mod=host={self.host_fakesplit_mod} --dpi-desync-hostfakesplit-midhost=host-2 '
                                          f'--dpi-desync-fake-tls-mod=rnd,sni=www.google.com --dpi-desync-badseq-increment={self.dpi_desync_badseq_increment} '
                                          f'--dpi-desync-fake-tls="%BIN%tls_clienthello_www_google_com.bin" --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" '
                                          f'--dpi-desync-fake-tls-mod=none')
                        else: 
                            if is_see_program:
                                desync = (f' --ip-id=zero --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 '
                                          f'--dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin"')
                            else:
                                desync = (f' --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 '
                                          f'--dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin"')

                        parts = []
                        if 'hostlist_domains' in program_info and program_info['hostlist_domains']:
                            parts.append(f'--hostlist-domains={program_info["hostlist_domains"]}')
                        if 'list_file' in program_info and self.check_file_exists(lists_path, program_info['list_file']):
                            parts.append(f'--hostlist="%LISTS%{program_info["list_file"]}"')
                        if 'ipset_file' in program_info and self.check_file_exists(ipset_path, program_info['ipset_file']):
                            parts.append(f'--ipset="%IPSET%{program_info["ipset_file"]}"')
                        if self.use_exclude:
                            if self.check_file_exists(exclude_path, 'List-Exclude.txt'):
                                parts.append(f'--hostlist-exclude="%EXCLUDE%List-Exclude.txt"')
                            if self.check_file_exists(lists_path, 'IpSet-Exclude.txt'):
                                parts.append(f'--ipset-exclude="%LISTS%IpSet-Exclude.txt"')
                        parts.append(f'--filter-tcp={ports}{l7_param}')
                        parts.append(desync.strip())
                        parts.append('--new')
                        filter_line = ' '.join(parts) + ' ^'
                        params.append(filter_line)

                    elif '--filter-udp' in rule:
                        if '=' in rule:
                            ports = rule.split('=')[1].split(' ')[0].strip()
                            l7_param = ' --filter-l7=' + rule.split('--filter-l7=')[1] if '--filter-l7=' in rule else ''
                        else:
                            ports = rule.replace('--filter-udp', '').strip()
                            l7_param = ''

                        if strategy == 'standard':
                            if is_see_program:
                                desync = (f' --ip-id=zero --dpi-desync=fake,multisplit --dpi-desync-autottl={self.dpi_desync_autottl} '
                                          f'--dpi-desync-repeats={self.dpi_desync_repeats} '
                                          f'--dpi-desync-any-protocol={self.dpi_desync_protocol} '
                                          f'--dpi-desync-cutoff=n{self.dpi_desync_cutoff} --filter-l7=discord,stun '
                                          f'--dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin"')
                            else:
                                desync = (f' --dpi-desync=fake,multisplit --dpi-desync-autottl={self.dpi_desync_autottl} '
                                          f'--dpi-desync-repeats={self.dpi_desync_repeats} '
                                          f'--dpi-desync-any-protocol={self.dpi_desync_protocol} '
                                          f'--dpi-desync-cutoff=n{self.dpi_desync_cutoff} --filter-l7=discord,stun '
                                          f'--dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin"')
                        elif strategy == 'fake':
                            if is_see_program:
                                desync = f' --ip-id=zero --dpi-desync=fake --dpi-desync-repeats={self.dpi_desync_repeats} --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin"'
                            else:
                                desync = f' --dpi-desync=fake --dpi-desync-repeats={self.dpi_desync_repeats} --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin"'
                        elif strategy == 'confusion':
                            if is_see_program:
                                desync = (f' --ip-id=zero --dpi-desync=fake,multidisorder --dpi-desync-split-pos=1,2,3,sniext+1 '
                                          f'--dpi-desync-split-seqovl={self.dpi_desync_split_seqovl} --dpi-desync-repeats={self.dpi_desync_repeats} '
                                          f'--dpi-desync=udplen --dpi-desync-repeats=4 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin"')
                            else:
                                desync = (f' --dpi-desync=fake,multidisorder --dpi-desync-split-pos=1,2,3,sniext+1 '
                                          f'--dpi-desync-split-seqovl={self.dpi_desync_split_seqovl} --dpi-desync-repeats={self.dpi_desync_repeats} '
                                          f'--dpi-desync=udplen --dpi-desync-repeats=4 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin"')
                        else: 
                            if is_see_program:
                                desync = f' --ip-id=zero --dpi-desync=multisplit --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin"'
                            else:
                                desync = f' --dpi-desync=multisplit --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin"'

                        parts = []
                        if 'hostlist_domains' in program_info and program_info['hostlist_domains']:
                            parts.append(f'--hostlist-domains={program_info["hostlist_domains"]}')
                        if 'list_file' in program_info and self.check_file_exists(lists_path, program_info['list_file']):
                            parts.append(f'--hostlist="%LISTS%{program_info["list_file"]}"')
                        if 'ipset_file' in program_info and self.check_file_exists(ipset_path, program_info['ipset_file']):
                            parts.append(f'--ipset="%IPSET%{program_info["ipset_file"]}"')
                        if self.use_exclude:
                            if self.check_file_exists(exclude_path, 'List-Exclude.txt'):
                                parts.append(f'--hostlist-exclude="%EXCLUDE%List-Exclude.txt"')
                            if self.check_file_exists(lists_path, 'IpSet-Exclude.txt'):
                                parts.append(f'--ipset-exclude="%LISTS%IpSet-Exclude.txt"')
                        parts.append(f'--filter-udp={ports}{l7_param}')
                        parts.append(desync.strip())
                        parts.append('--new')
                        filter_line = ' '.join(parts) + ' ^'
                        params.append(filter_line)

                params.append('')
                processed_programs.add(program)

        bat_lines.extend(params)

        if self.debug_mode:
            bat_lines.append('pause')
            bat_lines.append('echo Нажмите любую клавишу, чтобы закрыть это окно...')

        log_message("=== BAT-файл сгенерирован ===")
        for line in bat_lines:
            log_message(line)
        log_message("==============================")

        return '\n'.join(bat_lines)

    def check_required_files(self):
        if not self.bin_path:
            return False, "Папка bin не найдена. Убедитесь, что папка 'bin' существует рядом с программой."

        base_path = self.bin_path.parent
        lists_path = base_path / "Lists"
        ipset_path = base_path / "IpSet"
        exclude_path = base_path / "Exclude"

        missing = []
        warnings = []

        for fname in self.REQUIRED_BIN_FILES:
            if fname == 'DeePsHell.exe' and self.deepshell_exe_path and self.deepshell_exe_path.exists():
                continue
            if not self.check_file_exists(self.bin_path, fname):
                missing.append(f"[bin] {fname}")

        if not lists_path.exists():
            missing.append("Папка 'Lists' не найдена")
        if not ipset_path.exists():
            missing.append("Папка 'IpSet' не найдена")

        if self.use_exclude:
            if not exclude_path.exists():
                missing.append("Папка 'Exclude' не найдена (необходима для Exclude)")
            else:
                if not self.check_file_exists(exclude_path, 'List-Exclude.txt'):
                    missing.append("[Exclude] List-Exclude.txt (обязателен, т.к. включена опция exclude)")
            if not self.check_file_exists(lists_path, 'IpSet-Exclude.txt'):
                missing.append("[Lists] IpSet-Exclude.txt (обязателен, т.к. включена опция exclude)")
        else:
            if exclude_path.exists() and not self.check_file_exists(exclude_path, 'List-Exclude.txt'):
                warnings.append("Предупреждение: не найден List-Exclude.txt в папке Exclude (опционально)")
            if not self.check_file_exists(lists_path, 'IpSet-Exclude.txt'):
                warnings.append("Предупреждение: не найден IpSet-Exclude.txt в папке Lists (опционально)")

        if self.use_youtube_none:
            if not self.check_file_exists(ipset_path, 'Ip-Set-YoutubeNone.txt'):
                missing.append("[IpSet] Ip-Set-YoutubeNone.txt (обязателен, т.к. включена опция YouTube None)")

        selected = self.get_selected_programs_list()
        for prog in selected:
            info = self.INDIVIDUAL_PROGRAMS.get(prog)
            if not info:
                continue
            if 'list_file' in info and not self.check_file_exists(lists_path, info['list_file']):
                missing.append(f"[Lists] {info['list_file']} (для {prog})")
            if 'ipset_file' in info and not self.check_file_exists(ipset_path, info['ipset_file']):
                missing.append(f"[IpSet] {info['ipset_file']} (для {prog})")

        if missing:
            msg = "Не найдены следующие файлы/папки:\n" + "\n".join(missing)
            if warnings:
                msg += "\n\n" + "\n".join(warnings)
            return False, msg
        elif warnings:
            msg = "Внимание:\n" + "\n".join(warnings)
            self.show_custom_warning("Предупреждение", msg)
            return True, ""
        return True, ""

    def check_process_started(self):
        if self.deepshell_process and self.deepshell_process.poll() is not None:
            self.is_running = False
            self.update_status_indicator()
            log_message("❌ DeePsHell не удалось запустить (процесс завершился)")
        else:
            if self.get_deepshell_pid():
                log_message("✅ DeePsHell подтверждён как работающий")
            else:
                QTimer.singleShot(2000, self.check_process_started)

    def cleanup_bat_file(self, bat_path):
        try:
            if bat_path.exists():
                os.remove(bat_path)
                log_message(f"Удален временный файл: {bat_path}")
        except Exception as e:
            log_message(f"Ошибка удаления временного файла: {e}")

    def show_programs_dialog(self):
        dialog = CustomDialog(self, "Выбор программ", 600, 600)
        tab_widget = QTabWidget()
        self.program_checkboxes = {}
        category_names = {
            'messengers': '💬 Мессенджеры',
            'watch': '🎬 Видео и стриминг',
            'games': '🎮 Игры',
            'minecraft': '⛏️ Майнкрафт',
            'others': '🌐 Прочие сервисы'
        }
        for category, programs in self.program_categories.items():
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            title_label = QLabel(f"Выберите программы в категории:")
            title_label.setStyleSheet("""
                QLabel {
                    color: #00ff00;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 10px;
                    background: rgba(0, 40, 0, 0.3);
                    border-radius: 8px;
                    margin: 3px;
                }
            """)
            tab_layout.addWidget(title_label)
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setSpacing(5)
            self.program_checkboxes[category] = []
            for program in programs:
                cb = QCheckBox(f"   {program}")
                cb.setStyleSheet("""
                    QCheckBox {
                        color: #00ff00;
                        font-size: 11px;
                        padding: 10px 8px;
                        background-color: rgba(0, 40, 0, 0.2);
                        border-radius: 8px;
                        border: 1px solid #005500;
                    }
                    QCheckBox:hover {
                        background-color: rgba(0, 60, 0, 0.4);
                        border: 1px solid #00aa00;
                    }
                    QCheckBox::indicator {
                        width: 18px;
                        height: 18px;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #00ff00;
                        border: 2px solid #005500;
                        border-radius: 4px;
                    }
                    QCheckBox::indicator:unchecked {
                        background-color: #003300;
                        border: 2px solid #005500;
                        border-radius: 4px;
                    }
                """)
                if category in self.selected_programs and program in self.selected_programs[category]:
                    cb.setChecked(self.selected_programs[category].get(program, False))
                else:
                    cb.setChecked(False)
                self.program_checkboxes[category].append((program, cb))
                container_layout.addWidget(cb)
            container_layout.addStretch()
            scroll_area.setWidget(container)
            tab_layout.addWidget(scroll_area)
            btn_layout = QHBoxLayout()
            select_all_btn = QPushButton("✅ Выбрать все")
            select_all_btn.clicked.connect(lambda checked, c=category: self.select_all_programs(c))
            select_all_btn.setStyleSheet("""
                QPushButton {
                    background-color: #00aa00;
                    color: black;
                    font-weight: bold;
                    padding: 8px;
                    border-radius: 8px;
                    border: 2px solid #00ff00;
                    font-size: 11px;
                    margin: 5px 3px;
                }
                QPushButton:hover {
                    background-color: #00cc00;
                }
            """)
            deselect_all_btn = QPushButton("❌ Отменить все")
            deselect_all_btn.clicked.connect(lambda checked, c=category: self.deselect_all_programs(c))
            deselect_all_btn.setStyleSheet("""
                QPushButton {
                    background-color: #aa0000;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                    border-radius: 8px;
                    border: 2px solid #ff0000;
                    font-size: 11px;
                    margin: 5px 3px;
                }
                QPushButton:hover {
                    background-color: #cc0000;
                }
            """)
            btn_layout.addWidget(select_all_btn)
            btn_layout.addWidget(deselect_all_btn)
            tab_layout.addLayout(btn_layout)
            tab_widget.addTab(tab, category_names.get(category, category))
        dialog.addWidget(tab_widget)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setStyleSheet("""
            QPushButton {
                background-color: #00aa00;
                color: black;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
                border: 2px solid #00ff00;
                font-size: 11px;
                margin: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
            QPushButton#cancelButton {
                background-color: #aa0000;
                border: 2px solid #ff0000;
            }
            QPushButton#cancelButton:hover {
                background-color: #cc0000;
            }
        """)
        ok_button = button_box.button(QDialogButtonBox.Ok)
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setObjectName("cancelButton")
        button_box.accepted.connect(lambda: self.save_program_selections(dialog))
        button_box.rejected.connect(dialog.reject)
        dialog.addWidget(button_box)
        dialog.exec_()

    def select_all_programs(self, category):
        for program, checkbox in self.program_checkboxes[category]:
            checkbox.setChecked(True)

    def deselect_all_programs(self, category):
        for program, checkbox in self.program_checkboxes[category]:
            checkbox.setChecked(False)

    def save_program_selections(self, dialog):
        for category, programs in self.program_categories.items():
            if category not in self.selected_programs:
                self.selected_programs[category] = {}
            for i, program in enumerate(programs):
                if i < len(self.program_checkboxes[category]):
                    checkbox = self.program_checkboxes[category][i][1]
                    self.selected_programs[category][program] = checkbox.isChecked()
        self.save_settings()
        total_selected = len(self.get_selected_programs_list())
        log_message(f"Выбрано программ: {total_selected}")
        dialog.accept()

    def clear_temp(self):
        try:
            temp_dir = os.environ.get('TEMP', 'C:\\Windows\\Temp')
            subprocess.run(
                f'@echo off & del /q /f "{temp_dir}\\*.*" 2>nul & ipconfig /flushdns & netsh int ip reset >nul',
                shell=True,
                capture_output=True,
                text=True,
                encoding='cp866'
            )
            self.show_custom_info("Очистка Temp", "Очистка временных файлов выполнена успешно!\n\nВыполнены операции:\n• Удаление временных файлов\n• Очистка DNS кэша\n• Сброс сетевых настроек")
        except Exception as e:
            self.show_custom_error("Ошибка", f"Не удалось выполнить очистку:\n\n{str(e)}")

    def test_connection(self):
        dialog = CustomDialog(self, "Тест сетевого соединения", 600, 400)
        text_output = QTextEdit()
        text_output.setReadOnly(True)
        text_output.setStyleSheet("""
            QTextEdit {
                background-color: #001100;
                color: #00ff00;
                font-family: Consolas, Courier New;
                font-size: 10pt;
                border: 1px solid #00aa00;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        dialog.addWidget(text_output)
        def run_test():
            output_text = "Системная диагностика сети\n"
            output_text += "═" * 40 + "\n\n"
            output_text += "Сетевые интерфейсы:\n"
            output_text += "─" * 25 + "\n"
            ipconfig_result = subprocess.run('ipconfig', shell=True, capture_output=True, text=True, encoding='cp866').stdout
            for line in ipconfig_result.split('\n'):
                if 'адаптер' in line.lower() or 'adapter' in line.lower():
                    output_text += f"  {line.strip()}\n"
            output_text += "\nIP-Адреса:\n"
            output_text += "─" * 25 + "\n"
            ip_result = subprocess.run('ipconfig', shell=True, capture_output=True, text=True, encoding='cp866').stdout
            for line in ip_result.split('\n'):
                if 'IPv4' in line or 'IPv6' in line:
                    output_text += f"  {line.strip()}\n"
            output_text += "\nDNS-серверы:\n"
            output_text += "─" * 25 + "\n"
            dns_result = subprocess.run('ipconfig /all | findstr "DNS серверы"', shell=True, capture_output=True, text=True, encoding='cp866').stdout
            if not dns_result.strip():
                dns_result = subprocess.run('ipconfig /all | findstr "DNS Servers"', shell=True, capture_output=True, text=True, encoding='cp866').stdout
            output_text += dns_result if dns_result.strip() else "  Не найдены\n"
            output_text += "\nТест пропускной способности:\n"
            output_text += "─" * 25 + "\n"
            output_text += "  IPv4 (8.8.8.8): "
            ping_result = subprocess.run('ping -n 2 8.8.8.8 | findstr "Среднее"', shell=True, capture_output=True, text=True, encoding='cp866').stdout
            if not ping_result.strip():
                ping_result = subprocess.run('ping -n 2 8.8.8.8 | findstr "Average"', shell=True, capture_output=True, text=True, encoding='cp866').stdout
            output_text += ping_result.strip() if ping_result.strip() else "Нет ответа\n"
            output_text += "\n" + "═" * 40 + "\n"
            output_text += "Диагностика завершена\n"
            text_output.setText(output_text)
        button_layout = QHBoxLayout()
        test_btn = QPushButton("🔍 Запустить тест")
        test_btn.clicked.connect(run_test)
        button_layout.addWidget(test_btn)
        save_btn = QPushButton("💾 Сохранить отчет")
        save_btn.clicked.connect(lambda: self.save_report(text_output.toPlainText()))
        button_layout.addWidget(save_btn)
        close_btn = QPushButton("✕ Закрыть")
        close_btn.clicked.connect(dialog.close)
        button_layout.addWidget(close_btn)
        dialog.addLayout(button_layout)
        dialog.exec_()

    def save_report(self, report_text):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить отчет", "network_report.txt", "Текстовые файлы (*.txt)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                self.show_custom_info("Сохранение отчета", "Отчет успешно сохранен!")
            except Exception as e:
                self.show_custom_error("Ошибка", f"Не удалось сохранить отчет: {str(e)}")

    def show_dns_dialog(self):
        dialog = CustomDialog(self, "Настройка DNS", 400, 300)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите сетевой адаптер:"))
        adapter_combo = QComboBox()
        adapters = ['Ethernet', 'Wi-Fi', 'Беспроводная сеть']
        for adapter in adapters:
            adapter_combo.addItem(adapter)
        layout.addWidget(adapter_combo)
        def set_dns():
            adapter = adapter_combo.currentText()
            try:
                subprocess.run(f'netsh interface ip set dns name="{adapter}" static 8.8.8.8 primary',
                             shell=True, encoding='cp866')
                subprocess.run(f'netsh interface ip add dns name="{adapter}" 8.8.4.4 index=2',
                             shell=True, encoding='cp866')
                self.show_custom_info("Настройка DNS", f"DNS успешно установлены для адаптера {adapter}!\n\nОсновной DNS: 8.8.8.8\nАльтернативный DNS: 8.8.4.4")
            except Exception as e:
                self.show_custom_error("Ошибка", f"Не удалось установить DNS: {str(e)}")
        def reset_dns():
            adapter = adapter_combo.currentText()
            try:
                subprocess.run(f'netsh interface ip set dns name="{adapter}" dhcp',
                             shell=True, encoding='cp866')
                self.show_custom_info("Сброс DNS", f"Настройки DNS сброшены для адаптера {adapter}!\nВключено автоматическое получение DNS.")
            except Exception as e:
                self.show_custom_error("Ошибка", f"Не удалось сбросить DNS: {str(e)}")
        def show_dns():
            try:
                result = subprocess.run('ipconfig /all | findstr "DNS"', shell=True, capture_output=True, text=True, encoding='cp866').stdout
                self.show_custom_info("Текущие настройки DNS", result)
            except Exception as e:
                self.show_custom_error("Ошибка", f"Не удалось получить настройки DNS: {str(e)}")
        def test_dns():
            try:
                output = "Проверка соединения с DNS серверами:\n\n"
                output += "Пинг 8.8.8.8:\n"
                ping1_result = subprocess.run('ping -n 2 8.8.8.8', shell=True, capture_output=True, text=True, encoding='cp866').stdout
                output += ping1_result + "\n"
                output += "Пинг 8.8.4.4:\n"
                ping2_result = subprocess.run('ping -n 2 8.8.4.4', shell=True, capture_output=True, text=True, encoding='cp866').stdout
                output += ping2_result + "\n"
                output += "🌐 Разрешение имен (google.com):\n"
                nslookup_result = subprocess.run('nslookup google.com 8.8.8.8', shell=True, capture_output=True, text=True, encoding='cp866').stdout
                output += nslookup_result
                self.show_custom_info("Проверка DNS", output)
            except Exception as e:
                self.show_custom_error("Ошибка", f"Не удалось проверить DNS: {str(e)}")
        set_dns_btn = QPushButton("Установить DNS 8.8.8.8 и 8.8.4.4")
        set_dns_btn.clicked.connect(set_dns)
        layout.addWidget(set_dns_btn)
        reset_dns_btn = QPushButton("Восстановить автоматические DNS")
        reset_dns_btn.clicked.connect(reset_dns)
        layout.addWidget(reset_dns_btn)
        show_dns_btn = QPushButton("Показать текущие настройки DNS")
        show_dns_btn.clicked.connect(show_dns)
        layout.addWidget(show_dns_btn)
        test_dns_btn = QPushButton("Проверить соединение с DNS")
        test_dns_btn.clicked.connect(test_dns)
        layout.addWidget(test_dns_btn)
        close_btn = QPushButton("✕ Закрыть")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        dialog.addLayout(layout)
        dialog.exec_()

    def show_log_viewer(self):
        dialog = CustomDialog(self, "Просмотр логов", 800, 600)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #001100;
                color: #00ff00;
                font-family: Consolas, Courier New;
                font-size: 10pt;
                border: 1px solid #00aa00;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        dialog.addWidget(text_edit)
        log_file = Path(get_data_dir()) / "deepshell_launcher.log"
        log_content = self.load_logs(log_file)
        text_edit.setText(log_content)
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(lambda: text_edit.setText(self.load_logs(log_file)))
        button_layout.addWidget(refresh_btn)
        clear_btn = QPushButton("🧹 Очистить логи")
        clear_btn.clicked.connect(lambda: self.clear_logs(log_file, text_edit))
        button_layout.addWidget(clear_btn)
        save_btn = QPushButton("💾 Сохранить")
        save_btn.clicked.connect(lambda: self.save_logs(text_edit.toPlainText()))
        button_layout.addWidget(save_btn)
        close_btn = QPushButton("✕ Закрыть")
        close_btn.clicked.connect(dialog.close)
        button_layout.addWidget(close_btn)
        dialog.addLayout(button_layout)
        dialog.exec_()

    def load_logs(self, log_file):
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                return "⚠️ Не удалось загрузить логи"
        return "📝 Логи отсутствуют"

    def clear_logs(self, log_file, text_edit):
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("")
            text_edit.setText("Логи очищены")
        except:
            text_edit.setText("Не удалось очистить логи")

    def save_logs(self, log_content):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить логи", "deepshell_logs.txt", "Текстовые файлы (*.txt)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                self.show_custom_info("Сохранение логов", "Логи успешно сохранены!")
            except Exception as e:
                self.show_custom_error("Ошибка", f"Не удалось сохранить логи: {str(e)}")

    def show_custom_error(self, title, message):
        dlg = CustomMessageBox(self, title, message, "error")
        dlg.exec_()

    def show_custom_warning(self, title, message):
        dlg = CustomMessageBox(self, title, message, "warning")
        dlg.exec_()

    def show_custom_info(self, title, message):
        dlg = CustomMessageBox(self, title, message, "info")
        dlg.exec_()

    def get_detected_fix_name(self):
        return self.detected_fix_name

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(10, 25, 10))
    dark_palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
    dark_palette.setColor(QPalette.Base, QColor(20, 40, 20))
    dark_palette.setColor(QPalette.AlternateBase, QColor(30, 50, 30))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(20, 40, 20))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(0, 255, 0))
    dark_palette.setColor(QPalette.Button, QColor(30, 60, 30))
    dark_palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Highlight, QColor(0, 180, 0))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(dark_palette)

    app_icon_paths = [
        "bin/Доп/DeePsHell.ico",
        "dist/bin/Доп/DeePsHell.ico",
        "DeePsHell.ico",
        os.path.join(os.path.dirname(__file__), "DeePsHell.ico")
    ]
    app_icon = None
    for icon_path in app_icon_paths:
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            break
    if app_icon:
        app.setWindowIcon(app_icon)

    window = DeePsHellLauncher()
    window.show()
    sys.exit(app.exec_())