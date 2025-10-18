#[KOR]
# MORSEKEY-A01 ver1.0
#
# 제작자: Airmodeling
# 플랫폼: RP2040-Zero
# 유형: 모스부호 키보드 입력 장치
# 공식 등록: OSHWLab – MORSEKEY-A01
#
# 프로그램 개요
#
# 이 프로그램은 RP2040-Zero 기반의 모스부호 키보드이며,
# 다음과 같은 기능을 제공합니다.
#
# 주요 기능
#
# 모스부호를 한글/영어로 변환하여 키보드 입력
# WPM/IWG 실시간 조정 (로터리 엔코더 사용)
# 매크로 기능 (사용자 정의 단축키)
# 직접 모스부호 입력 모드
# 사운드 설정 (주파수, 볼륨)
# LED 상태 표시 (언어별 색상 구분)
#
# 라이선스 및 저작권
#
# 이 프로젝트는 Adafruit CircuitPython (MIT License) 을 기반으로 제작된
# 오픈소스 하드웨어 및 소프트웨어입니다.
# CircuitPython의 저작권은 © Adafruit Industries에 있으며,
# 해당 라이선스의 모든 조건을 준수합니다.
#
# 본 프로젝트의 코드, 회로도, 3D 모델, 문서는
# 비상업적·개인적 사용에 한해 자유롭게 이용 가능하며,
# 판매·재배포·상업적 활용은 금지됩니다.
#
# 면책 조항
#
# 이 프로젝트의 사용, 개조 또는 응용으로 인해 발생하는
# 손상, 오작동, 데이터 손실, 안전사고 등에 대해
# 제작자는 어떠한 책임도 지지 않습니다.
# 모든 사용 책임은 사용자에게 있습니다.
#
# 문의
#
# Email: airmodel00@gmail.com
# OSHWLab: https://oshwlab.com/airmodeling/morsekey-a01
# YouTube: AIRMODELING 채널
# © 2025 Airmodeling. All Rights Reserved.


#[ENG]
# MORSEKEY-A01 ver1.0
#
# Author: Airmodeling
# Platform: RP2040-Zero
# Type: Morse Code Keyboard Input Device
# Official Registration: OSHWLab – MORSEKEY-A01
#
# Program Overview
#
# This program is a Morse code keyboard based on the RP2040-Zero platform.
# It provides the following features:
#
# Key Features
#
# - Converts Morse code into Korean/English keyboard input  
# - Real-time WPM/IWG adjustment using rotary encoders  
# - Macro function (user-defined shortcuts)  
# - Direct manual Morse input mode  
# - Sound configuration (frequency and volume)  
# - LED status indication (color-coded by language)
#
# License and Copyright
#
# This project is built on Adafruit CircuitPython (MIT License)
# and is released as open-source hardware and software.
# CircuitPython is © Adafruit Industries, and
# all conditions of its license are fully observed.
#
# The code, schematics, 3D models, and documentation
# of this project are freely available for
# non-commercial and personal use only.
# Redistribution, resale, or any commercial use is strictly prohibited.
#
# Disclaimer
#
# The author assumes no responsibility for any damage, malfunction,
# data loss, or safety issues resulting from the use,
# modification, or application of this project.
# All responsibility lies solely with the user.
#
# Contact
#
# Email: airmodel00@gmail.com  
# OSHWLab: https://oshwlab.com/airmodeling/morsekey-a01  
# YouTube: AIRMODELING Channel  
# © 2025 Airmodeling. All Rights Reserved.

# 라이브러리
import time
import json
import supervisor

# CircuitPython
import board
import busio
import digitalio
import pwmio
import displayio
import terminalio
import neopixel
# HID
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
# 디스플레이
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from adafruit_display_shapes import line, roundrect, rect, triangle
from adafruit_bitmap_font import bitmap_font
# 키보드 매핑
# 특수문자 키코드 매핑
special_char_map = {
    '!': (Keycode.SHIFT, Keycode.ONE), '?': (Keycode.SHIFT, Keycode.FORWARD_SLASH), '(': (Keycode.SHIFT, Keycode.NINE), ')': (Keycode.SHIFT, Keycode.ZERO),
    '@': (Keycode.SHIFT, Keycode.TWO), '#': (Keycode.SHIFT, Keycode.THREE), '$': (Keycode.SHIFT, Keycode.FOUR), '%': (Keycode.SHIFT, Keycode.FIVE),
    '^': (Keycode.SHIFT, Keycode.SIX), '&': (Keycode.SHIFT, Keycode.SEVEN), '*': (Keycode.SHIFT, Keycode.EIGHT), '+': (Keycode.SHIFT, Keycode.EQUALS),
    '=': Keycode.EQUALS, '-': Keycode.MINUS, '_': (Keycode.SHIFT, Keycode.MINUS), '[': Keycode.LEFT_BRACKET,
    ']': Keycode.RIGHT_BRACKET, '{': (Keycode.SHIFT, Keycode.LEFT_BRACKET), '}': (Keycode.SHIFT, Keycode.RIGHT_BRACKET), '\\': Keycode.BACKSLASH,
    '|': (Keycode.SHIFT, Keycode.BACKSLASH), ';': Keycode.SEMICOLON, ':': (Keycode.SHIFT, Keycode.SEMICOLON), "'": Keycode.QUOTE,
    '"': (Keycode.SHIFT, Keycode.QUOTE), ',': Keycode.COMMA, '<': (Keycode.SHIFT, Keycode.COMMA), '.': Keycode.PERIOD,
    '>': (Keycode.SHIFT, Keycode.PERIOD), '/': Keycode.FORWARD_SLASH, '`': Keycode.GRAVE_ACCENT, '~': (Keycode.SHIFT, Keycode.GRAVE_ACCENT)
}
# 숫자 키코드 매핑
NUMBER_KEYCODES = ("ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE")
# 화면 표시용 문자열 상수
STR_LANG_EN = "LANG:EN"
STR_LANG_KR = "LANG:KR"
STR_READY = "[ READY ]"
STR_ENTER = "ENTER"
STR_BACKSPACE = "BACKSPACE"
STR_SPACE = "SPACE"
# 한글 된소리 변환 매핑
CAPS_CONVERSION_MAP = {'ㄱ': 'ㄲ', 'ㄷ': 'ㄸ', 'ㅂ': 'ㅃ', 'ㅅ': 'ㅆ', 'ㅈ': 'ㅉ', 'ㅐ': 'ㅒ', 'ㅔ': 'ㅖ'}
# 한글 자모 리스트
CHO_LIST = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
JUNG_LIST = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
JONG_LIST = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
# 한글 복합 자모 분해 매핑
COMPOUND_VOWELS = {'ㅘ': ('ㅗ', 'ㅏ'), 'ㅙ': ('ㅗ', 'ㅐ'), 'ㅚ': ('ㅗ', 'ㅣ'), 'ㅝ': ('ㅜ', 'ㅓ'), 'ㅞ': ('ㅜ', 'ㅔ'), 'ㅟ': ('ㅜ', 'ㅣ'), 'ㅢ': ('ㅡ', 'ㅣ')}
COMPOUND_CONSONANTS = {'ㄳ': ('ㄱ', 'ㅅ'), 'ㄵ': ('ㄴ', 'ㅈ'), 'ㄶ': ('ㄴ', 'ㅎ'), 'ㄺ': ('ㄹ', 'ㄱ'), 'ㄻ': ('ㄹ', 'ㅁ'), 'ㄼ': ('ㄹ', 'ㅂ'), 'ㄽ': ('ㄹ', 'ㅅ'), 'ㄾ': ('ㄹ', 'ㅌ'), 'ㄿ': ('ㄹ', 'ㅍ'), 'ㅀ': ('ㄹ', 'ㅎ'), 'ㅄ': ('ㅂ', 'ㅅ')}
# 한글 자모 키코드 매핑 (자모 → (Keycode, shift))
KOREAN_KEYMAP = {
    'ㄱ': (Keycode.R, False), 'ㄲ': (Keycode.R, True), 'ㄴ': (Keycode.S, False), 
    'ㄷ': (Keycode.E, False), 'ㄸ': (Keycode.E, True), 'ㄹ': (Keycode.F, False), 
    'ㅁ': (Keycode.A, False), 'ㅂ': (Keycode.Q, False), 'ㅃ': (Keycode.Q, True), 
    'ㅅ': (Keycode.T, False), 'ㅆ': (Keycode.T, True), 'ㅇ': (Keycode.D, False), 
    'ㅈ': (Keycode.W, False), 'ㅉ': (Keycode.W, True), 'ㅊ': (Keycode.C, False),
    'ㅋ': (Keycode.Z, False), 'ㅌ': (Keycode.X, False), 'ㅍ': (Keycode.V, False), 
    'ㅎ': (Keycode.G, False), 'ㅏ': (Keycode.K, False), 'ㅐ': (Keycode.O, False), 
    'ㅑ': (Keycode.I, False), 'ㅒ': (Keycode.O, True), 'ㅓ': (Keycode.J, False), 
    'ㅔ': (Keycode.P, False), 'ㅕ': (Keycode.U, False), 'ㅖ': (Keycode.P, True), 
    'ㅗ': (Keycode.H, False), 'ㅛ': (Keycode.Y, False), 'ㅜ': (Keycode.N, False), 
    'ㅠ': (Keycode.B, False), 'ㅡ': (Keycode.M, False), 'ㅣ': (Keycode.L, False)
}


# 유틸리티

def press_release(key1, key2=None):
    if key2:
        keyboard.press(key1, key2)
        keyboard.release(key1, key2)
    else:
        keyboard.press(key1)
        keyboard.release(key1)

def convert_dot_pattern(pattern):
    converted_pattern = ""
    for char in pattern:
        if char in ['·', '•', '∙'] or ord(char) == 0x00B7:  # middle dot (·)
            converted_pattern += '.'
        else:
            converted_pattern += char
    return converted_pattern

def setup_input_pin(pin, pull=digitalio.Pull.UP):
    pin.direction = digitalio.Direction.INPUT
    pin.pull = pull
    return pin

def setup_output_pin(pin, initial_value=False):
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = initial_value
    return pin

# 설정 및 데이터 로드 함수

def load_morse_dict(language="EN"):
    try:
        if language == "KR":
            file_path = '/morse_code/morse_KR.json'
        else:
            file_path = '/morse_code/morse_EN.json'
            
        with open(file_path, 'r') as f:
            morse_data = json.load(f)
        
        morse_dict = {}
        
        # 글자
        for letter, pattern in morse_data['patterns']['letters'].items():
            morse_dict[convert_dot_pattern(pattern)] = letter
        
        # 모음
        if language == "KR" and 'vowels' in morse_data['patterns']:
            for vowel, pattern in morse_data['patterns']['vowels'].items():
                morse_dict[convert_dot_pattern(pattern)] = vowel
        
        # 숫자
        for number, pattern in morse_data['patterns']['numbers'].items():
            morse_dict[convert_dot_pattern(pattern)] = number
        
        # 구두점
        for punct, pattern in morse_data['patterns']['punctuation'].items():
            morse_dict[convert_dot_pattern(pattern)] = punct
        
        return morse_dict
        
    except Exception as e:
        raise

# 메크로 딕셔너리 로드 함수
def load_macro_dict():
    try:
        with open('/macros.json', 'r') as f:
            macro_data = json.load(f)
        return macro_data['macros']
    except Exception as e:
        return {"EN": {}, "KR": {}, "BOTH": {}}

# 설정 파일 로드 함수
def load_settings():
    try:
        with open('/settings.toml', 'r') as f:
            content = f.read()
        
        settings = {}
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # 숫자
                if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                    settings[key] = int(value)
                elif value.replace('.', '').isdigit() or (value.startswith('-') and value[1:].replace('.', '').isdigit()):
                    settings[key] = float(value)
                elif value.startswith('"') and value.endswith('"'):
                    settings[key] = value[1:-1]
                else:
                    settings[key] = value
        
        return settings
    except Exception as e:
        # 기본값
        return {
            'DEFAULT_WPM': 10,
            'DEFAULT_IWG': 0,
            'DEFAULT_HZ': 1000,
            'DEFAULT_DASH_R': 3.00,
            'DEFAULT_IWG_R': 7.00,
            'DEFAULT_ATS': 0,
            'SAVED_TIME': '0'
        }

# 메크로 및 모스부호 처리 함수

def check_macro_match(pattern, current_lang):
    if not macro_visible:
        return None, None, False
    
    # 현재 언어 메크로 확인
    if current_lang in macro_dict:
        if pattern in macro_dict[current_lang]:
            macro_data = macro_dict[current_lang][pattern]
            if isinstance(macro_data, dict):
                display = macro_data.get("display", "")
                input_text = macro_data.get("input", "")
                return display, input_text, False
            else:
                return macro_data, macro_data, False
    
    # BOTH 메크로
    if "BOTH" in macro_dict and pattern in macro_dict["BOTH"]:
        macro_data = macro_dict["BOTH"][pattern]
        if isinstance(macro_data, dict):
            display = macro_data.get("display", "")
            input_text = macro_data.get("input", "")
            return display, input_text, True
        else:
            return macro_data, macro_data, True
    
    return None, None, False

def is_valid_pattern_for_mode(pattern, mode):
    if pattern not in morse_dict:
        return False
    
    character = morse_dict[pattern]
    if len(character) != 1:
        return False
    
    char_code = ord(character)
    
    # 공통 허용 문자
    common_chars = (48 <= char_code <= 57 or  # 0-9
                   char_code in [32, 46, 44, 63, 33, 45, 47, 40, 41, 61, 43, 58, 59, 34, 39])  # 구두점 / punctuation
    
    if mode == "KR":
        # 한글 모드
        return (0x3131 <= char_code <= 0x3163 or common_chars)  # 한글 자모 + 공통 / Korean jamo + common
    else:
        # 영어 모드
        return (65 <= char_code <= 90 or  # A-Z
                97 <= char_code <= 122 or  # a-z
                common_chars)  # 공통 / common

# =============================================================================
# 전역 변수 초기화
# =============================================================================

# 데이터 딕셔너리 및 설정 로드
morse_dict = load_morse_dict("EN")
macro_dict = load_macro_dict()
settings = load_settings()

# 볼륨 레벨 상수 (튜플 사용 - 불변 데이터는 리스트보다 메모리 효율적)
VOL_LEVELS = (0, 1500, 3800, 10922, 32768, 49152)

# 설정값을 전역 변수로 저장
DEFAULT_WPM = settings.get('DEFAULT_WPM', 10)
DEFAULT_IWG = settings.get('DEFAULT_IWG', 0)
DEFAULT_HZ = settings.get('DEFAULT_HZ', 1000)
DEFAULT_VOL_LEVEL = settings.get('DEFAULT_VOL', 4)
DEFAULT_VOL = VOL_LEVELS[min(max(DEFAULT_VOL_LEVEL, 0), 5)]
DEFAULT_LED_ENABLED = settings.get('DEFAULT_LED_ENABLED', 1)
DEFAULT_DASH_R = settings.get('DEFAULT_DASH_R', 3.0)
DEFAULT_IWG_R = settings.get('DEFAULT_IWG_R', 7.0)
SAVED_TIME = settings.get('SAVED_TIME', '0')

# 하드웨어 초기화

# I2C 및 디스플레이 초기화
try:
    i2c = busio.I2C(board.GP1, board.GP0)
    i2c.deinit()
except:
    pass

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# 화면 그룹 초기화 / Display group initialization
splash = displayio.Group()
display.root_group = splash

# UI 요소 초기화

# 폰트 로드 / Font load
small_font = bitmap_font.load_font("/font/5x7.bdf")
try:
    korean_font = bitmap_font.load_font("/font/KR8X8.bdf")
except Exception as e:
    korean_font = terminalio.FONT  # 폴백 / fallback

# 메인 텍스트 영역 / Main text area
text_area = label.Label(terminalio.FONT, text=STR_READY, color=0xFFFF00, x=64, y=33)
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (64, 33)
splash.append(text_area)

# 상단 정보 표시 영역 / Top information display area
wpm_label = label.Label(terminalio.FONT, text="WPM", color=0x00FFFF, x=0, y=4)
splash.append(wpm_label)
wpm_underline = line.Line(x0=0, y0=10, x1=127, y1=10, color=0x00FFFF)
splash.append(wpm_underline)
loading_box = rect.Rect(x=19, y=0, width=30, height=8, outline=0x00FFFF, stroke=1)
splash.append(loading_box)
wpm_value = label.Label(terminalio.FONT, text="00", color=0x00FFFF, x=51, y=4)
splash.append(wpm_value)

# IWG 표시 영역
vertical_line = line.Line(x0=64, y0=0, x1=64, y1=8, color=0x00FFFF)
splash.append(vertical_line)
iwg_label = label.Label(terminalio.FONT, text="IWG", color=0x00FFFF, x=67, y=4)
splash.append(iwg_label)
iwg_box = rect.Rect(x=86, y=0, width=22, height=8, outline=0x00FFFF, stroke=1)
splash.append(iwg_box)
iwg_value = label.Label(terminalio.FONT, text="+00", color=0x00FFFF, x=110, y=4)
splash.append(iwg_value)

# 하단 상태 표시 영역 / Bottom status display area
lang_label = label.Label(small_font, text="LANG:EN", color=0x00FFFF, x=0, y=61)
splash.append(lang_label)
mode_label = label.Label(small_font, text="M:MORSE", color=0x00FFFF, x=0, y=19)
splash.append(mode_label)

# AT-S 상태 표시 (화면 오른쪽 끝에 맞춤, M 모드보다 3픽셀 위)
ats_status_label = label.Label(small_font, text="AT-S:OFF", color=0x00FFFF, x=0, y=16)
ats_status_label.anchor_point = (1.0, 0.0)  # 오른쪽 정렬
ats_status_label.anchored_position = (127, 16)  # 화면 오른쪽 끝, M 모드보다 3픽셀 위
splash.append(ats_status_label)
macro_label = label.Label(small_font, text="MACRO", color=0x00FFFF, x=50, y=61)
caps_label = label.Label(small_font, text="C/LOCK", color=0x00FFFF, x=90, y=61)
splash.append(caps_label)

# 진행바 및 문자 표시 박스 / Progress bar and character display box
additional_box = rect.Rect(x=0, y=10, width=62, height=6, outline=0x00FFFF, stroke=1)
splash.append(additional_box)
# AT-S 진행바 외각 박스
ats_progress_box = rect.Rect(x=66, y=10, width=62, height=6, outline=0x00FFFF, stroke=1)
splash.append(ats_progress_box)
converted_char_box = roundrect.RoundRect(x=2, y=41, width=124, height=16, r=3, outline=0x00FFFF, stroke=1)
splash.append(converted_char_box)

# 진행바 관리 변수 / Progress bar management variables
wpm_progress_lines = []
wpm_last_progress = 0
iwg_progress_lines = []
iwg_last_progress = 0

# =============================================================================
# 하드웨어 핀 설정
# =============================================================================

# 모스부호 입력 스위치
switch_dot = setup_input_pin(digitalio.DigitalInOut(board.GP15))
switch_line = setup_input_pin(digitalio.DigitalInOut(board.GP14))

# 엔코더 1 (WPM 조정용) / Encoder 1 (for WPM adjustment)
encoder_clk = setup_input_pin(digitalio.DigitalInOut(board.GP5))
encoder_data = setup_input_pin(digitalio.DigitalInOut(board.GP6))

# 엔코더 2 (IWG 조정용) / Encoder 2 (for IWG adjustment)
encoder2_clk = setup_input_pin(digitalio.DigitalInOut(board.GP7))
encoder2_data = setup_input_pin(digitalio.DigitalInOut(board.GP8))

# 모스부호 표시 요소

morse_display = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=64, y=33)
morse_display.anchor_point = (0.5, 0.5)
morse_display.anchored_position = (64, 33)

character_display = label.Label(terminalio.FONT, text="", color=0x00FF00, x=64, y=49)
character_display.anchor_point = (0.5, 0.5)
character_display.anchored_position = (64, 49)

# =============================================================================
# 상태 변수
# =============================================================================

# 모스부호 패턴 및 타이머
morse_pattern = ""
last_input_time = time.monotonic()
enter_with_pattern = False
space_pressed = False
enter_via_space = False


# 부저 상태 관리 / Buzzer state management
buzzer_start_time = 0
buzzer_duration = 0
buzzer_active = False

# WPM/IWG 설정
wpm = DEFAULT_WPM
iwg = DEFAULT_IWG

# 엔코더 상태 변수 / Encoder state variables
encoder_last_clk = encoder_last_data = True
encoder_debounce_time = 0
encoder_clk_samples = [True] * 5
encoder_data_samples = [True] * 5
encoder_sample_idx = 0  # 순환 버퍼 인덱스

encoder2_last_clk = encoder2_last_data = True
encoder2_debounce_time = 0
encoder2_clk_samples = [True] * 5
encoder2_data_samples = [True] * 5
encoder2_sample_idx = 0  # 순환 버5퍼 인덱스

# 모스부호 입력 상태 / Morse input state
dot_pressed = False
line_pressed = False
dot_last_press_time = 0
line_last_press_time = 0

# 모스부호 간격 계산 변수 / Morse interval calculation variables
dot_interval = 0
line_interval = 0

# 키 입력 무시를 위한 변수 / Variables for ignoring key input
ignore_input_until = 0

# 스위치 상태 추적 / Switch state tracking
switch_states = {
    'enter': {'value': False},
    'backspace': {'value': False}, 
    'hangul': {'value': False},
    'caps': {'value': False},
    'save': {'value': False}
}

switch_times = {
    'enter': {'value': 0},
    'backspace': {'value': 0},
    'hangul': {'value': 0},
    'caps': {'value': 0},
    'save': {'value': 0}
}

# 동시 누름 감지 / Simultaneous press detection (비활성화)
# both_pressed = False

# 언어 및 모드 상태 / Language and mode state
current_lang = "EN"
macro_visible = False
direct_morse_mode = False

# GP13 스위치 상태 추적
lang_switch_pressed = False
lang_switch_press_time = 0

# AT-S 이전 값 저장 (스위치로 끄고 켤 때 복원용)
ats_previous_value = 1000

# 타이머 관리 / Timer management
ready_timeout = 10.0
last_activity_time = 0
key_display_time = 0
key_display_active = False

# CAPS LOCK 관리
caps_lock_state = False
last_caps_check_time = 0

# 메뉴 상태 관리 / Menu state management
menu_visible = False
menu_selected_item = 0
menu_items = ("HZ", "VOL", "DAS-R", "IWG-R", "AT-S", "DEFAULT", "SAVE", "BACK")  # 튜플 사용 - 메모리 최적화
ms_state = {'value': False}
ms_time = {'value': 0}

# 사운드 설정 / Sound settings
current_hz = DEFAULT_HZ
current_vol = DEFAULT_VOL
hz_adjust_mode = False
temp_hz = current_hz

# AT-S 설정 모드
ats_adjust_mode = False
temp_ats = 0

# 저장 상태 / Save state
save_done_time = 0
save_fail_time = 0
default_done_time = 0


# 모스부호 설정값 / Morse settings values
das_r_value = DEFAULT_DASH_R
iwg_r_value = DEFAULT_IWG_R
led_state = bool(DEFAULT_LED_ENABLED)

# AT-S (Auto Space) 설정값
ats_value = settings.get('DEFAULT_ATS', 0)  # 설정에서 로드, 기본값 0



# 메뉴 화면 그룹 / Menu screen group
option_screen = displayio.Group()
menu_labels = []
selection_triangle = None
menu_page = 0
items_per_page = 5

# 단어 간격 진행바 / Word interval progress bar
word_progress_dots = []
word_progress_start_time = 0
word_progress_active = False
word_progress_last_dots = 0

# AT-S 진행바 / AT-S progress bar
ats_progress_dots = []
ats_progress_start_time = 0
ats_progress_active = False
ats_progress_last_dots = 0
ats_progress_full = True  # 평소에는 꽉 찬 상태

# AT-S 타이머 관리 / AT-S timer management
ats_timer_start = 0
ats_timer_active = False

# 하드웨어 초기화 완료

# WPM/IWG 표시 초기화
wpm_value.text = f"{wpm:02d}"
if iwg < 0:
    iwg_value.text = f"{iwg:03d}"
elif iwg == 0:
    iwg_value.text = " 00"
else:
    iwg_value.text = f"+{iwg:02d}"

# 부저 및 LED 초기화 / Buzzer and LED initialization
buzzer = pwmio.PWMOut(board.GP2, frequency=DEFAULT_HZ, duty_cycle=0)
led = setup_output_pin(digitalio.DigitalInOut(board.GP3), initial_value=led_state)
caps_led = setup_output_pin(digitalio.DigitalInOut(board.GP4))

# RGB LED 초기화
try:
    pixel = neopixel.NeoPixel(board.GP16, 1, brightness=0.2, auto_write=True)
except Exception as e:
    pixel = None

# 키보드 HID 초기화 / Keyboard HID initialization
keyboard = Keyboard(usb_hid.devices)

# =============================================================================
# 스위치 핀 초기화
# =============================================================================
enter_button = setup_input_pin(digitalio.DigitalInOut(board.GP28))
backspace_button = setup_input_pin(digitalio.DigitalInOut(board.A3))
lang_switch = setup_input_pin(digitalio.DigitalInOut(board.GP13))
hangul_switch = setup_input_pin(digitalio.DigitalInOut(board.GP27))
macro_switch = setup_input_pin(digitalio.DigitalInOut(board.GP12))
caps_switch = setup_input_pin(digitalio.DigitalInOut(board.GP26))
save_switch = setup_input_pin(digitalio.DigitalInOut(board.GP9))
menu_switch = setup_input_pin(digitalio.DigitalInOut(board.GP10))
ats_toggle_switch = setup_input_pin(digitalio.DigitalInOut(board.GP11))

# 모스부호 신호 처리 함수

def calculate_intervals():
    global dot_interval, line_interval
    dot_duration = 1.2 / wpm
    line_duration = dot_duration * das_r_value
    dot_interval = dot_duration * 1.5
    line_interval = line_duration + (dot_duration * 0.5)

# 초기 간격 계산 / Initial interval calculation
calculate_intervals()

def start_morse_signal(signal):
    global buzzer_start_time, buzzer_duration, buzzer_active
    
    # 동적 소리 길이
    dot_duration = 1.2 / wpm  # 점 길이 (초) / Dot length (seconds)
    
    if signal == '.':
        buzzer_duration = dot_duration  # 점: WPM에 따라 동적 / Dot: dynamic according to WPM
    elif signal == '-':
        buzzer_duration = dot_duration * das_r_value  # 선: 점의 설정된 배수 / Dash: set multiple of dot
    
    # 언어별 색상
    if current_lang == "KR":
        # 한글: 녹색
        set_rgb_color(0, 255, 0)
    else:
        # 영어: 빨간색
        set_rgb_color(255, 0, 0)
    
    buzzer_start_time = time.monotonic()
    buzzer_active = True
    buzzer.duty_cycle = current_vol  # 현재 설정된 볼륨 사용 / Use currently set volume
    
    # LED 켜기
    if DEFAULT_LED_ENABLED:
        led.value = True

def stop_morse_signal():
    global buzzer_active
    buzzer.duty_cycle = 0
    buzzer_active = False
    # LED 끄기
    if DEFAULT_LED_ENABLED:
        led.value = False
    set_language_led()

def start_new_signal(signal):
    if buzzer_active:
        stop_morse_signal()
        time.sleep((1.2 / wpm) * 0.5)
    if len(morse_pattern) < 20:
        start_morse_signal(signal)
    return add_morse_signal(signal)

def start_direct_signal_with_gap(signal):
    if buzzer_active:
        stop_morse_signal()
        time.sleep((1.2 / wpm) * 0.5)
    start_morse_signal(signal)

def update_buzzer():
    global buzzer_active
    
    if buzzer_active:
        current_time = time.monotonic()
        if current_time - buzzer_start_time >= buzzer_duration:
            buzzer.duty_cycle = 0
            buzzer_active = False
            # LED 끄기
            if DEFAULT_LED_ENABLED:
                led.value = False
            # 언어별 LED 유지
            set_language_led()

def update_buzzer_settings(realtime=False):
    global buzzer
    try:
        # 부저 비활성시만 업데이트
        if not buzzer_active:
            buzzer.deinit()
            buzzer = pwmio.PWMOut(board.GP2, frequency=current_hz, duty_cycle=0)
    except:
        pass

def update_caps_lock_led():
    global caps_lock_state, last_caps_check_time
    
    current_time = time.monotonic()
    
    # CAPS LOCK 상태 확인
    if current_time - last_caps_check_time >= 0.1:
        last_caps_check_time = current_time
        
        # CAPS LOCK 확인
        caps_pressed = keyboard.led_on(Keyboard.LED_CAPS_LOCK)
        
        # 상태 변경시만 LED 업데이트
        if caps_pressed != caps_lock_state:
            caps_lock_state = caps_pressed
            caps_led.value = caps_lock_state
            update_caps_display()

def update_wpm_display():
    """WPM 표시 업데이
"""
    wpm_value.text = f"{wpm:02d}"
    update_progress_bar("wpm")

def update_iwg_display():
    """IWG 표시 업데이트"""
    if iwg < 0:
        iwg_value.text = f"{iwg:03d}"  # 음수는 -01, -02, -03... / Negative: -01, -02, -03...
    elif iwg == 0:
        iwg_value.text = " 00"  # 0일 때는 부호 없이 / No sign when 0
    else:
        iwg_value.text = f"+{iwg:02d}"  # 양수는 +01, +02, +03... / Positive: +01, +02, +03...
    update_progress_bar("iwg")

def switch_language():
    # 언어 전환
    global morse_dict, current_lang, morse_pattern
    
    # 언어 토글
    if current_lang == "EN":
        current_lang = "KR"
    else:
        current_lang = "EN"
    
    # 새 언어 딕셔너리 로드
    morse_dict = load_morse_dict(current_lang)
    
    # 패턴 초기화
    reset_morse_pattern()
    
    # 화면 업데이트
    update_lang_display()
    
    # 언어별 LED 색상
    set_language_led()
    
    # 언어 전환 시 AT-S 진행바 상태 업데이트
    update_ats_progress_on_lang_change()
    
    # 모드 전환 알림
    show_key_action("한글모드" if current_lang == "KR" else "영문모드")

def switch_to_mo_mode():
    """MO(다이렉트 모드)로 전환/해제"""
    global direct_morse_mode, last_input_time, word_progress_active
    
    if not direct_morse_mode:
        # MO 모드로 전환
        direct_morse_mode = True
        update_mode_display()
        update_lang_display()  # LANG 표시도 업데이트
        reset_morse_pattern()
        reset_direct_mode_timer()
        set_rgb_color(0, 0, 255)
        show_key_action("MO모드")
    else:
        # MO 모드에서 일반 모드로 전환
        direct_morse_mode = False
        update_mode_display()
        update_lang_display()  # LANG 표시도 업데이트
        reset_direct_mode_timer()
        set_language_led()  # 언어별 LED 색상으로 복원
        show_key_action("일반모드")

def handle_lang_switch():
    """GP13 스위치 처리: 짧게 누르면 언어 전환, 길게 누르면 MO 모드"""
    global lang_switch_press_time, lang_switch_pressed
    
    current_time = time.monotonic()
    
    if lang_switch.value:  # 스위치가 눌렸을 때
        if not lang_switch_pressed:
            lang_switch_pressed = True
            lang_switch_press_time = current_time
        else:
            # 스위치를 누르고 있는 동안 시간 체크
            press_duration = current_time - lang_switch_press_time
            if press_duration >= 2.0:  # 2초 이상 누르면 MO 모드로 전환
                if not direct_morse_mode:
                    switch_to_mo_mode()
    else:  # 스위치가 떼어졌을 때
        if lang_switch_pressed:
            lang_switch_pressed = False
            press_duration = current_time - lang_switch_press_time
            
            if press_duration < 2.0:  # 2초 미만으로 짧게 누름
                if direct_morse_mode:
                    # MO 모드에서 일반 모드로 복귀
                    switch_to_mo_mode()
                else:
                    # 일반 모드에서 언어 전환
                    switch_language()

def handle_ats_toggle():
    """GP11 스위치 처리: AT-S ON/OFF 토글 (푸시락 방식, 떼어진 상태가 ON)"""
    global ats_value, ats_timer_active, ats_previous_value
    
    if ats_toggle_switch.value:  # 스위치가 떼어진 상태 (ON)
        if ats_value == 0:
            ats_value = ats_previous_value  # 이전 값으로 복원
            show_key_action("AT-S:ON")
            # AT-S 상태 표시 업데이트
            update_ats_status_display()
            # AT-S가 켜지면 현재 모드에 따라 진행바 표시
            update_ats_progress_on_lang_change()
    else:  # 스위치가 눌린 상태 (OFF)
        if ats_value > 0:
            ats_previous_value = ats_value  # 현재 값을 저장
            ats_value = 0  # AT-S 끄기
            ats_timer_active = False  # 타이머 중지
            show_key_action("AT-S:OFF")
            # AT-S 상태 표시 업데이트
            update_ats_status_display()
            # AT-S가 꺼지면 진행바를 빈 상태로 표시
            clear_ats_progress_bars()

def update_lang_display():
    """언어 표시 업데이트"""
    if direct_morse_mode:
        lang_label.text = "LANG:MO"
    else:
        lang_label.text = STR_LANG_KR if current_lang == "KR" else STR_LANG_EN
    update_macro_display()  # 매크로 표시도 함께 업데이트 (언어 변경 시) / Also update macro display (on language change)

def update_caps_display():
    """CAPS LOCK 표시 업데이트"""
    # 대소문자 표시
    caps_indicator = "C/LOCK" if caps_lock_state else "c/lock"
    caps_label.text = caps_indicator

def update_macro_display():
    """매크로 표시 업데이트"""
    global macro_visible
    if macro_visible:
        # 매크로 표시
        macro_label.text = "MACRO"
        if macro_label not in splash:
            splash.append(macro_label)
    else:
        # 숨기기
        if macro_label in splash:
            splash.remove(macro_label)

def update_mode_display():
    """모드 표시 업데이트"""
    if direct_morse_mode:
        mode_label.text = "M:MORSE"
        mode_label.color = 0xFFFF00  # 노란색으로 변경 (더 눈에 띄게)
    else:
        mode_label.text = "M:CODE"
        mode_label.color = 0x00FFFF  # 기본 청록색

def update_ats_status_display():
    """AT-S 상태 표시 업데이트"""
    if ats_value == 0:
        ats_status_label.text = "AT-S:OFF"
        # AT-S OFF일 때는 진행바를 빈 상태로 표시
        clear_ats_progress_bars()
    else:
        ats_status_label.text = f"AT-S:{ats_value}ms"
        # AT-S ON일 때는 진행바를 꽉 찬 상태로 표시
        update_ats_progress_on_lang_change()

def ensure_mode_display():
    # MODE 표시
    if mode_label not in splash:
        splash.append(mode_label)
    
    if direct_morse_mode:
        if mode_label.text != "M:MORSE":
            mode_label.text = "M:MORSE"
            mode_label.color = 0xFFFF00
    else:
        if mode_label.text != "M:CODE":
            mode_label.text = "M:CODE"
            mode_label.color = 0x00FFFF

def show_ready():
    """READY 표시"""
    global last_activity_time
    last_activity_time = time.monotonic()
    text_area.text = STR_READY
    if text_area not in splash:
        splash.append(text_area)
    if morse_display in splash:
        splash.remove(morse_display)
    if character_display in splash:
        splash.remove(character_display)

def setup_option_screen():
    """옵션 화면 초기화"""
    global option_screen, menu_labels, selection_triangle
    
    # 요소들 정리
    while len(option_screen) > 0:
        option_screen.pop()
    
    # [ OPTION ] 제목
    option_label = label.Label(terminalio.FONT, text="[ OPTION ] ver1.0", color=0xFFFF00, x=64, y=8)
    option_label.anchor_point = (0.5, 0.5)
    option_label.anchored_position = (64, 8)
    option_screen.append(option_label)
    
    # 메뉴 항목들 생성
    label_x = 28  # 라벨들의 가로 위치
    triangle_x = 15  # 화살표의 가로 위치
    
    menu_labels.clear()
    for i in range(5):  # 5개만 생성
        y_pos = 20 + (i * 10)  # 10픽셀 간격으로 배치
        menu_label = label.Label(terminalio.FONT, text="", color=0x00FFFF, x=label_x, y=y_pos)
        option_screen.append(menu_label)
        menu_labels.append(menu_label)
    
    # 선택 삼각형
    selection_triangle = triangle.Triangle(triangle_x, 17, triangle_x, 23, triangle_x+6, 20, fill=0x00FFFF)
    option_screen.append(selection_triangle)




def update_selection_triangle_unified(menu_type, selected_item):
    """통합된 선택 삼각형 업데이트 함수"""
    global selection_triangle
    
    if menu_type == "menu":
        # 삼각형 제거
        if selection_triangle in option_screen:
            option_screen.remove(selection_triangle)
        
        # 새 삼각형 생성
        triangle_x = 15
        triangle_y = 17 + (selected_item * 10)
        selection_triangle = triangle.Triangle(
            triangle_x, triangle_y, triangle_x, triangle_y+6, triangle_x+6, triangle_y+3, fill=0x00FFFF
        )
        option_screen.append(selection_triangle)
        
        





def read_encoder_unified(encoder_type, callback_func=None):
    # 엔코더 읽기
    global encoder_last_clk, encoder_last_data, encoder_debounce_time, encoder_sample_idx
    global encoder2_last_clk, encoder2_last_data, encoder2_debounce_time, encoder2_sample_idx
    
    current_time = time.monotonic()
    
    # 엔코더 변수 선택
    if encoder_type == "encoder1":
        clk_pin = encoder_clk
        data_pin = encoder_data
        sample_idx = encoder_sample_idx
        last_clk = encoder_last_clk
        last_data = encoder_last_data
        debounce_time = encoder_debounce_time
    else:  # encoder2
        clk_pin = encoder2_clk
        data_pin = encoder2_data
        sample_idx = encoder2_sample_idx
        last_clk = encoder2_last_clk
        last_data = encoder2_last_data
        debounce_time = encoder2_debounce_time
    
    # 디바운싱
    if current_time - debounce_time < 0.01:
        return
    
    # 순환 버퍼 샘플링
    if encoder_type == "encoder1":
        encoder_clk_samples[sample_idx] = clk_pin.value
        encoder_data_samples[sample_idx] = data_pin.value
        encoder_sample_idx = (sample_idx + 1) % 5
        clk_high_count = sum(encoder_clk_samples)
        data_high_count = sum(encoder_data_samples)
    else:
        encoder2_clk_samples[sample_idx] = clk_pin.value
        encoder2_data_samples[sample_idx] = data_pin.value
        encoder2_sample_idx = (sample_idx + 1) % 5
        clk_high_count = sum(encoder2_clk_samples)
        data_high_count = sum(encoder2_data_samples)
    
    # 샘플 인식
    clk_state = clk_high_count >= 3  # 5개 중 3개 이상이 HIGH면 HIGH
    data_state = data_high_count >= 3
    
    # CLK 변화 감지
    if clk_state != last_clk:
        if not clk_state:  # CLK가 LOW로 떨어질 때만 인식
            direction = 1 if data_state != clk_state else -1  # 반시계방향: 1, 시계방향: -1
            if callback_func:
                callback_func(direction)
        
        # 디바운싱 업데이트
        if encoder_type == "encoder1":
            encoder_debounce_time = current_time
        else:
            encoder2_debounce_time = current_time
    
    # 상태 업데이트
    if encoder_type == "encoder1":
        encoder_last_clk = clk_state
        encoder_last_data = data_state
    else:
        encoder2_last_clk = clk_state
        encoder2_last_data = data_state


def update_menu_display():
    # 메뉴 표시
    start_idx = menu_page * items_per_page
    end_idx = min(start_idx + items_per_page, len(menu_items))
    
    # 메뉴 항목들 표시
    for i in range(items_per_page):
        if i < (end_idx - start_idx):
            item_text = menu_items[start_idx + i]
            # HZ 값 표시
            if item_text == "HZ":
                if hz_adjust_mode:
                    menu_labels[i].text = f"Hz   : {temp_hz} SET"
                else:
                    menu_labels[i].text = f"Hz   : {current_hz}"
            # VOL 값 표시
            elif item_text == "VOL":
                try:
                    vol_level = VOL_LEVELS.index(current_vol)
                except ValueError:
                    vol_level = 4
                    for j, level in enumerate(VOL_LEVELS):
                        if current_vol >= level:
                            vol_level = j
                menu_labels[i].text = f"Vol  : {vol_level}"
            # DAS-R 표시
            elif item_text == "DAS-R":
                try:
                    menu_labels[i].text = f"DAS-R: {das_r_value:.1f}"
                except NameError:
                    menu_labels[i].text = "DAS-R: 3.0"
            # IWG-R 표시
            elif item_text == "IWG-R":
                try:
                    menu_labels[i].text = f"IWG-R: {iwg_r_value:.1f}"
                except NameError:
                    menu_labels[i].text = "IWG-R: 7.0"
            # AT-S 표시
            elif item_text == "AT-S":
                if ats_adjust_mode:
                    menu_labels[i].text = f"AT-S : {temp_ats} SET"
                else:
                    menu_labels[i].text = f"AT-S : {ats_value}ms"
            # SAVE 표시
            elif item_text == "SAVE":
                current_time = time.monotonic()
                if save_done_time > 0 and current_time - save_done_time < 3.0:  # 3초간 DONE 표시
                    menu_labels[i].text = "SAVE : DONE"
                elif save_fail_time > 0 and current_time - save_fail_time < 3.0:  # 3초간 FAIL 표시
                    menu_labels[i].text = "SAVE : FAIL"
                else:
                    menu_labels[i].text = "SAVE :"
            # DEFAULT 표시
            elif item_text == "DEFAULT":
                current_time = time.monotonic()
                if default_done_time > 0 and current_time - default_done_time < 3.0:  # 3초간 DONE 표시
                    menu_labels[i].text = "DEFAULT: DONE"
                else:
                    menu_labels[i].text = "DEFAULT:"
            else:
                menu_labels[i].text = item_text
        else:
            menu_labels[i].text = ""  # 빈 항목은 공백으로

def update_selection_triangle():
    """선택 표시 삼각형 위치 업데이트"""
    # 상대적 위치 계산
    relative_pos = menu_selected_item % items_per_page
    update_selection_triangle_unified("menu", relative_pos)


def show_menu():
    """메뉴 표시"""
    global menu_visible
    
    # 옵션 화면 초기화
    if len(option_screen) == 0:
        setup_option_screen()
    
    # 메뉴 상태 업데이트
    update_menu_display()
    update_selection_triangle()
    
    # 화면 전환
    display.root_group = option_screen
    menu_visible = True

def hide_menu():
    """메뉴 숨기기 (기존 화면으로 복원)"""
    global menu_visible
    
    # 화면 복원
    display.root_group = splash
    menu_visible = False
    
    # character_display가 splash에 없으면 추가
    if character_display not in splash:
        splash.append(character_display)


def read_menu_encoder():
    """메뉴 네비게이션용 엔코더 읽기"""
    global menu_selected_item, menu_page, temp_hz, current_hz, temp_ats, ats_value
    global hz_adjust_mode, ats_adjust_mode
    
    def menu_callback(direction):
        global menu_selected_item, menu_page, temp_hz, current_hz, temp_ats, ats_value
        global hz_adjust_mode, ats_adjust_mode
        
        if hz_adjust_mode:
            # HZ 조정
            if direction == 1:  # 반시계방향 (증가)
                if temp_hz < 3000:
                    temp_hz += 50
                    temp_hz = min(3000, temp_hz)
                    current_hz = temp_hz
                    update_buzzer_settings(realtime=True)
                    update_menu_display()
            else:  # 시계방향 (감소)
                if temp_hz > 100:
                    temp_hz -= 50
                    temp_hz = max(100, temp_hz)
                    current_hz = temp_hz
                    update_buzzer_settings(realtime=True)
                    update_menu_display()
        elif ats_adjust_mode:
            # AT-S 조정 (OFF 옵션 제거, 최소 25ms)
            if direction == 1:  # 반시계방향 (증가)
                if temp_ats < 2000:
                    temp_ats += 25
                    temp_ats = min(2000, temp_ats)
                    ats_value = temp_ats
                    ats_previous_value = temp_ats  # 이전 값도 업데이트
                    update_menu_display()
                    update_ats_status_display()  # AT-S 상태 표시 업데이트
            else:  # 시계방향 (감소)
                if temp_ats > 25:
                    temp_ats -= 25
                    temp_ats = max(25, temp_ats)
                    ats_value = temp_ats
                    ats_previous_value = temp_ats  # 이전 값도 업데이트
                    update_menu_display()
                    update_ats_status_display()  # AT-S 상태 표시 업데이트
        else:
            # 메뉴 네비게이션
            if direction == 1:  # 반시계방향 (위로)
                if menu_selected_item > 0:
                    menu_selected_item -= 1
                else:
                    menu_selected_item = len(menu_items) - 1
            else:  # 시계방향 (아래로)
                if menu_selected_item < len(menu_items) - 1:
                    menu_selected_item += 1
                else:
                    menu_selected_item = 0
            
            # 페이지 전환
            new_page = menu_selected_item // items_per_page
            if new_page != menu_page:
                menu_page = new_page
                update_menu_display()
            
            update_selection_triangle()
    
    read_encoder_unified("encoder2", menu_callback)


def handle_menu_selection():
    """메뉴 선택 처리"""
    global hz_adjust_mode, ats_adjust_mode
    
    if menu_visible:
        # HZ 조정 모드 종료
        if hz_adjust_mode:
            hz_adjust_mode = False
            update_menu_display()
            return
        
        # AT-S 조정 모드 종료
        if ats_adjust_mode:
            ats_adjust_mode = False
            ats_previous_value = ats_value  # 최종 값을 이전 값으로 저장
            update_menu_display()
            return
        
        
        # 메뉴 선택 처리
        if menu_selected_item == 0:  # HZ
            show_hz_setting()
        elif menu_selected_item == 1:  # VOL
            show_vol_setting()
        elif menu_selected_item == 2:  # DAS-R
            show_das_r_setting()
        elif menu_selected_item == 3:  # IWG-R
            show_iwg_r_setting()
        elif menu_selected_item == 4:  # AT-S
            show_ats_setting()
        elif menu_selected_item == 5:  # DEFAULT
            reset_to_default()
        elif menu_selected_item == 6:  # SAVE
            save_all_settings()
        elif menu_selected_item == 7:  # BACK
            hide_menu()
    else:
        # 메뉴 열기
        show_menu()

# 단순화된 설정 화면 함수들

def show_hz_setting():
    """HZ 설정 화면 표시"""
    global hz_adjust_mode, temp_hz
    hz_adjust_mode = True
    temp_hz = current_hz
    update_menu_display()  # 화면 업데이트 (Hz   : 1500 SET 표시)

def show_vol_setting():
    """VOL 설정 화면 표시 - 버튼식 (최적화)"""
    global current_vol
    # 레벨 순환 (최적화)
    try:
        current_level = VOL_LEVELS.index(current_vol)
    except ValueError:
        current_level = 4  # 기본값
    
    # 다음 레벨 (0~5 순환)
    current_vol = VOL_LEVELS[(current_level + 1) % 6]
    
    update_buzzer_settings()  # 부저 설정 업데이트
    update_menu_display()  # 화면 업데이트

def show_das_r_setting():
    """DAS-R 설정 화면 표시 - 버튼식 (최적화)"""
    global das_r_value
    # 0.5씩 증가 (최적화)
    das_r_values = (1.5, 2.0, 2.5, 3.0, 3.5, 4.0)  # 튜플 사용
    try:
        current_index = das_r_values.index(das_r_value)
        das_r_value = das_r_values[(current_index + 1) % len(das_r_values)]
    except ValueError:
        das_r_value = 1.5  # 기본값 설정
    
    calculate_intervals()  # 모스부호 간격 재계산
    update_menu_display()  # 화면 업데이트

def show_iwg_r_setting():
    """IWG-R 설정 화면 표시 - 버튼식 (최적화)"""
    global iwg_r_value
    # 1.0씩 증가 (최적화)
    iwg_r_value = 3.0 if iwg_r_value >= 10.0 else iwg_r_value + 1.0
    
    calculate_intervals()  # 모스부호 간격 재계산
    update_menu_display()  # 화면 업데이트

def show_ats_setting():
    """AT-S 설정 화면 표시 - HZ처럼 SET 모드"""
    global ats_adjust_mode, temp_ats
    ats_adjust_mode = True
    temp_ats = max(25, ats_value)  # 최소 25ms로 설정
    update_menu_display()  # 화면 업데이트 (AT-S : 500 SET 표시)


def reset_to_default():
    """모든 설정을 기본값으로 리셋"""
    global current_hz, current_vol, temp_hz, das_r_value, iwg_r_value, ats_value, default_done_time
    current_hz = 1000
    current_vol = VOL_LEVELS[4]  # 4단계
    temp_hz = current_hz
    
    # 기본값으로 리셋
    das_r_value = 3.0  # 기본값
    iwg_r_value = 7.0  # 기본값
    ats_value = 0      # 기본값 (OFF)
    
    # DONE 시간 설정
    default_done_time = time.monotonic()
    
    update_buzzer_settings()
    calculate_intervals()  # 모스부호 간격 재계산
    update_menu_display()  # 화면 업데이트
    update_ats_status_display()  # AT-S 상태 표시 업데이트

def save_all_settings():
    # 설정 저장
    global save_done_time, save_fail_time
    
    # 모든 설정 저장
    try:
        # 레벨 변환
        try:
            vol_level = VOL_LEVELS.index(current_vol)
        except ValueError:
            vol_level = 4
            for i, level in enumerate(VOL_LEVELS):
                if current_vol >= level:
                    vol_level = i
        
        settings_content = f"""# Morse Keyboard
DEFAULT_WPM = {wpm}
DEFAULT_IWG = {iwg}
DEFAULT_HZ = {current_hz}
DEFAULT_VOL = {vol_level}
DEFAULT_LED_ENABLED = {DEFAULT_LED_ENABLED}
DEFAULT_DASH_R = {das_r_value}
DEFAULT_IWG_R = {iwg_r_value}
DEFAULT_ATS = {ats_value}
SAVED_TIME = "{time.monotonic():.0f}"
"""
        with open('/settings.toml', 'w') as f:
            f.write(settings_content)
        
        # DONE 표시
        save_done_time = time.monotonic()
        save_fail_time = 0  # FAIL 시간 초기화
        
        # 메뉴가 열려있을 때만 메뉴 표시 업데이트
        if menu_visible:
            update_menu_display()
        
        # 화면에 SAVED 표시
        global key_display_time, key_display_active
        character_display.text = "[SAVED]"
        if character_display not in splash:
            splash.append(character_display)
        key_display_time = time.monotonic()
        key_display_active = True
        
        return True
    except Exception as e:
        # FAIL 표시
        save_fail_time = time.monotonic()
        save_done_time = 0  # DONE 시간 초기화
        
        # 메뉴가 열려있을 때만 메뉴 표시 업데이트
        if menu_visible:
            update_menu_display()
        
        # 화면에 FAILED 표시
        global key_display_time, key_display_active
        character_display.text = "[FAILED]"
        if character_display not in splash:
            splash.append(character_display)
        key_display_time = time.monotonic()
        key_display_active = True
        
        return False

def handle_menu_switch():
    """GP10 메뉴 스위치 처리"""
    current_time = time.monotonic()
    
    # 스위치 상태 확인
    is_pressed = not menu_switch.value
    
    if is_pressed:
        if not ms_state['value']:  # 처음 눌렸을 때
            ms_state['value'] = True
            ms_time['value'] = current_time
            handle_menu_selection()  # 메뉴 선택 처리
    else:
        if ms_state['value']:  # 스위치를 떼었을 때
            ms_state['value'] = False

def hide_ready():
    """READY 숨기기"""
    if text_area in splash:
        splash.remove(text_area)

def update_progress_bar(progress_type):
    # 진행바 업데이트 (최적화)
    global wpm_progress_lines, wpm_last_progress, iwg_progress_lines, iwg_last_progress, wpm, iwg
    
    if progress_type == "wpm":
        # WPM 범위 변환 (5-30 -> 0-28)
        progress_width = max(0, min(28, int((wpm - 5) * 28 / 25)))
        start_x = 20
        progress_lines = wpm_progress_lines
        last_progress = wpm_last_progress
    else:  # iwg
        # IWG 범위 변환 (-40~40 -> 0-20)
        progress_width = max(0, min(20, int((iwg + 40) * 20 / 80)))
        start_x = 87
        progress_lines = iwg_progress_lines
        last_progress = iwg_last_progress
    
    # 진행률 증가시 라인 추가
    if progress_width > last_progress:
        for x in range(start_x + last_progress, start_x + progress_width):
            vertical_line = line.Line(x, 2, x, 5, color=0x00FFFF)
            splash.append(vertical_line)
            progress_lines.append(vertical_line)
    
    # 진행률 감소시 라인 제거
    elif progress_width < last_progress:
        remove_count = last_progress - progress_width
        for _ in range(remove_count):
            if progress_lines:
                last_line = progress_lines.pop()
                splash.remove(last_line)
    
    # 진행률 업데이트
    if progress_type == "wpm":
        global wpm_last_progress
        wpm_last_progress = progress_width
    else:
        global iwg_last_progress
        iwg_last_progress = progress_width

# 진행바 업데이트 함수들은 update_progress_bar()를 직접 호출하도록 변경

def show_key_action(text):
    """키 동작 화면 표시 (중복 제거)"""
    global key_display_time, key_display_active
    character_display.text = text
    if character_display not in splash:
        splash.append(character_display)
    key_display_time = time.monotonic()
    key_display_active = True

def handle_direct_mode_signal(signal):
    """다이렉트 모드 신호 처리 통합 함수"""
    global ats_timer_active
    
    # AT-S 타이머 취소
    if ats_timer_active:
        ats_timer_active = False
        led.value = False  # AT-S 타이머 취소 시 LED 끄기
        clear_ats_progress_bars()  # AT-S 진행바 제거
    
    start_direct_signal_with_gap(signal)
    send_morse_symbol_to_keyboard(signal)
    character_display.text = signal
    if character_display not in splash:
        splash.append(character_display)
    start_direct_mode_timer(signal)

def send_enter_key():
    global morse_pattern, last_input_time, enter_with_pattern, space_pressed, enter_via_space
    if morse_pattern:
        if is_valid_pattern_for_mode(morse_pattern, current_lang):
            character = morse_dict[morse_pattern]
            if current_lang == "KR":
                char_code = ord(character)
                if 0x3131 <= char_code <= 0x3163:
                    display_character = character
                    if caps_lock_state and character in CAPS_CONVERSION_MAP:
                        display_character = CAPS_CONVERSION_MAP[character]
                    
                    create_character_display(display_character, korean_font)
                    send_korean_character_to_keyboard(character)
                else:
                    create_character_display(character)
                    send_character_to_keyboard(character)
            else:
                display_text = character.upper() if caps_lock_state else character.lower()
                create_character_display(display_text)
                send_character_to_keyboard(display_text)
        else:
            create_character_display(f"?({current_lang})")
        
        morse_pattern = ""
        morse_display.text = ""
        display.refresh()
        show_key_action(character)
        enter_with_pattern = True
        space_pressed = True
    else:
        enter_with_pattern = False
        space_pressed = True

def send_backspace_key():
    press_release(Keycode.BACKSPACE)
    show_key_action(STR_BACKSPACE)

def send_space_key():
    press_release(Keycode.SPACE)
    show_key_action(STR_SPACE)

def handle_enter_release():
    global enter_with_pattern, space_pressed, enter_via_space
    space_pressed = False
    if enter_via_space:
        enter_via_space = False
        return
    if not enter_with_pattern:
        press_release(Keycode.SPACE)
        show_key_action("SPACE")


def send_hangul_key():
    press_release(Keycode.RIGHT_ALT)

def send_caps_lock_key():
    press_release(Keycode.CAPS_LOCK)

def send_morse_symbol_to_keyboard(symbol):
    """모스부호 점/선을 키보드로 바로 입력 전송"""
    try:
        press_release(Keycode.PERIOD if symbol == '.' else Keycode.MINUS)
    except:
        pass

def send_macro_text_to_keyboard(text, force_english=False):
    """메크로 텍스트를 키보드로 입력 전송 (구조 개선)"""
    try:
        if force_english and current_lang == "KR":
            _send_english_text(text)
        else:
            _send_mixed_text(text)
    except:
        pass

def _send_english_text(text):
    """영어 텍스트 전송"""
    send_hangul_key()
    time.sleep(0.05)
    for char in text:
        send_character_to_keyboard(char)
        time.sleep(0.03)
    send_hangul_key()
    time.sleep(0.05)

def _send_mixed_text(text):
    """혼합 텍스트 전송 (한글/영어)"""
    current_mode = "korean" if current_lang == "KR" else "english"
    
    for char in text:
        char_code = ord(char)
        is_korean = (0xAC00 <= char_code <= 0xD7A3 or 0x3131 <= char_code <= 0x3163)
        is_english = (65 <= char_code <= 90 or 97 <= char_code <= 122)
        
        # 언어 모드 전환
        if is_korean and current_mode != "korean":
            send_hangul_key()
            time.sleep(0.05)
            current_mode = "korean"
        elif is_english and current_mode != "english":
            send_hangul_key()
            time.sleep(0.05)
            current_mode = "english"
        
        # 문자 입력
        if is_korean:
            if 0xAC00 <= char_code <= 0xD7A3:
                send_korean_word_to_keyboard(char)
            else:
                korean_key = get_korean_keycode(char)
                if korean_key:
                    press_release(korean_key)
        elif char == ' ':
            press_release(Keycode.SPACE)
            time.sleep(0.03)
        else:
            send_character_to_keyboard(char)
            time.sleep(0.03)
    
    # 마지막 문자가 영어면 한글 모드로 복원
    if text and current_lang == "KR":
        last_char_code = ord(text[-1])
        if 65 <= last_char_code <= 90 or 97 <= last_char_code <= 122:
            send_hangul_key()
            time.sleep(0.05)

def send_character_to_keyboard(character):
    """문자를 키보드로 입력 전송"""
    try:
        # 문자를 키코드로 변환하여 입력
        if len(character) == 1:
            # 단일 문자 입력
            char_code = ord(character)
            
            if 65 <= char_code <= 90:
                keycode = getattr(Keycode, character)
                press_release(keycode) if caps_lock_state else press_release(Keycode.SHIFT, keycode)
            elif 97 <= char_code <= 122:
                keycode = getattr(Keycode, character.upper())
                press_release(Keycode.SHIFT, keycode) if caps_lock_state else press_release(keycode)
            elif 48 <= char_code <= 57:
                press_release(getattr(Keycode, NUMBER_KEYCODES[int(character)]))
            elif character == ' ':
                press_release(Keycode.SPACE)
            elif character in special_char_map:
                keycode = special_char_map[character]
                press_release(keycode[0], keycode[1]) if isinstance(keycode, tuple) else press_release(keycode)
    except:
        pass

def send_korean_character_to_keyboard(character):
    """한글 자모를 키보드로 입력 전송"""
    try:
        if len(character) == 1 and 0x3131 <= ord(character) <= 0x3163:
            korean_key = get_korean_keycode(character)
            if korean_key:
                # KR 모드에서 캡스락이 켜져있으면 모든 입력에 시프트+키
                if caps_lock_state and current_lang == "KR":
                    press_release(Keycode.SHIFT, korean_key)
                else:
                    press_release(korean_key)
    except:
        pass

def get_korean_keycode(korean_char):
    # 한글 자모 변환
    mapping = KOREAN_KEYMAP.get(korean_char)
    return mapping[0] if mapping else None  # (Keycode, shift) 튜플에서 Keycode만 반환

def decompose_korean_to_jamo(korean_char):
    # 한글 자모 분해
    char_code = ord(korean_char)
    if 0xAC00 <= char_code <= 0xD7A3:
        base = char_code - 0xAC00
        cho = base // 588  # 588 = 21 * 28
        jung = (base % 588) // 28
        jong = base % 28
        
        jamo_list = [CHO_LIST[cho]]
        
        # 중성 추가 (복합 모음 분해) - 튜플도 extend 가능
        jung_char = JUNG_LIST[jung]
        if jung_char in COMPOUND_VOWELS:
            jamo_list.extend(COMPOUND_VOWELS[jung_char])
        else:
            jamo_list.append(jung_char)
        
        # 종성 추가 (복합 자음 분해) - 튜플도 extend 가능
        if jong:
            jong_char = JONG_LIST[jong]
            if jong_char in COMPOUND_CONSONANTS:
                jamo_list.extend(COMPOUND_CONSONANTS[jong_char])
            else:
                jamo_list.append(jong_char)
        
        return jamo_list
    return []

def jamo_to_keycode_and_shift(jamo):
    # 자모 키코드 변환
    return KOREAN_KEYMAP.get(jamo, (None, False))

def send_korean_word_to_keyboard(korean_word):
    # 한글 자동 입력
    for char in korean_word:
        if char == ' ':
            press_release(Keycode.SPACE)
        elif 0xAC00 <= ord(char) <= 0xD7A3:
            for jamo in decompose_korean_to_jamo(char):
                keycode, needs_shift = jamo_to_keycode_and_shift(jamo)
                if keycode:
                    press_release(Keycode.SHIFT, keycode) if needs_shift else press_release(keycode)
                    time.sleep(0.05)
        else:
            send_character_to_keyboard(char)
        time.sleep(0.05)

# RGB LED 제어 함수들
def set_rgb_color(red, green, blue):
    # RGB LED 색상
    if pixel is None:
        return
    try:
        scaled_red = min(red // 5, 50)
        scaled_green = min(green // 5, 50)
        scaled_blue = min(blue // 5, 50)
        pixel[0] = (scaled_red, scaled_green, scaled_blue)
    except:
        pass

def rgb_off():
    """WS2812 RGB LED 끄기"""
    if pixel is None:
        return
    try:
        pixel[0] = (0, 0, 0)
    except:
        pass

def set_language_led():
    """현재 언어에 따른 RGB LED 색상 설정"""
    if direct_morse_mode:
        # 다이렉트 모드: 파란색
        set_rgb_color(0, 0, 255)
    elif current_lang == "KR":
        # 한글 모드: 녹색
        set_rgb_color(0, 255, 0)
    else:
        # 영어 모드: 빨간색
        set_rgb_color(255, 0, 0)


def clear_word_progress_bars():
    """단어 간격 진행바 제거 (중복 제거)"""
    global word_progress_active, word_progress_dots, word_progress_last_dots
    word_progress_active = False
    for progress_bar in word_progress_dots:
        if progress_bar in splash:
            splash.remove(progress_bar)
    word_progress_dots.clear()
    word_progress_last_dots = 0

def update_ats_progress_on_lang_change():
    """언어 전환 시 AT-S 진행바 상태 업데이트"""
    if current_lang == "KR" and not direct_morse_mode:
        clear_ats_progress_bars()
    else:
        if ats_value > 0:
            restore_ats_progress_full()
        else:
            clear_ats_progress_bars()

def clear_ats_progress_bars():
    """AT-S 진행바 제거"""
    global ats_progress_active, ats_progress_dots, ats_progress_last_dots
    ats_progress_active = False
    for progress_bar in ats_progress_dots:
        if progress_bar in splash:
            splash.remove(progress_bar)
    ats_progress_dots.clear()
    ats_progress_last_dots = 0

def restore_ats_progress_full():
    """AT-S 진행바를 꽉 찬 상태로 복원 (메모리 최적화)"""
    global ats_progress_full, ats_progress_active, ats_progress_last_dots
    ats_progress_full = True
    ats_progress_active = False
    ats_progress_last_dots = 10
    
    # 기존 진행바가 있으면 색상만 변경 (깜박임 방지)
    if ats_progress_dots:
        for progress_bar in ats_progress_dots:
            progress_bar.fill = 0x00FF00
    else:
        # 상수로 미리 계산된 값들 사용 (메모리 최적화)
        START_X = 67
        START_Y = 11
        BOX_WIDTH_EACH = 6  # (62-2)/10 = 6
        
        for i in range(10):
            x_pos = START_X + i * BOX_WIDTH_EACH
            progress_bar = rect.Rect(x_pos, START_Y, BOX_WIDTH_EACH, 4, fill=0x00FF00)
            splash.append(progress_bar)
            ats_progress_dots.append(progress_bar)

def start_ats_progress_dots():
    # AT-S 진행바 시작 (메모리 최적화)
    global ats_progress_start_time, ats_progress_active, ats_progress_last_dots, ats_progress_full
    ats_progress_start_time = time.monotonic()
    ats_progress_active = True
    ats_progress_last_dots = 10  # 처음에는 10개 모두 표시
    ats_progress_full = False  # 진행 중이므로 꽉 찬 상태 아님
    
    # 기존 진행바가 있으면 색상만 변경 (깜박임 방지)
    if ats_progress_dots:
        for progress_bar in ats_progress_dots:
            progress_bar.fill = 0x00FF00
    else:
        # 상수로 미리 계산된 값들 사용 (메모리 최적화)
        START_X = 67
        START_Y = 11
        BOX_WIDTH_EACH = 6  # (62-2)/10 = 6
        
        for i in range(10):
            x_pos = START_X + i * BOX_WIDTH_EACH
            progress_bar = rect.Rect(x_pos, START_Y, BOX_WIDTH_EACH, 4, fill=0x00FF00)
            splash.append(progress_bar)
            ats_progress_dots.append(progress_bar)

def update_ats_progress_dots():
    # AT-S 진행바 업데이트
    global ats_progress_active, ats_progress_last_dots, ats_progress_full
    
    if not ats_progress_active:
        return
    
    current_time = time.monotonic()
    elapsed = current_time - ats_progress_start_time
    
    # AT-S 타이머 시간 (실제 AT-S 값에 맞춰 조정)
    total_time = ats_value / 1000.0  # 밀리초를 초로 변환
    
    if elapsed >= total_time:
        # AT-S 타이머 완료 후 바로 꽉 찬 상태로 복원 (깜박임 방지)
        ats_progress_active = False
        ats_progress_full = True
        ats_progress_last_dots = 10
        
        # 진행바가 있으면 색상만 변경, 없으면 새로 생성
        if ats_progress_dots:
            # 기존 진행바를 모두 녹색으로 변경
            for progress_bar in ats_progress_dots:
                progress_bar.fill = 0x00FF00
        else:
            # 진행바가 없으면 새로 생성
            box_count = 10
            box_width = 62
            box_height = 4
            start_x = 67
            start_y = 11
            
            available_width = box_width - 2
            box_width_each = available_width // box_count
            
            for i in range(10):
                x_pos = start_x + i * box_width_each
                progress_bar = rect.Rect(x_pos, start_y, box_width_each, box_height, fill=0x00FF00)
                splash.append(progress_bar)
                ats_progress_dots.append(progress_bar)
        return
    
    # 진행률 계산 (1.0에서 0.0으로 감소)
    progress = 1.0 - (elapsed / total_time)
    dots_count = max(0, int(progress * 10))
    
    # 점이 줄어들어야 하는 경우 (왼쪽에서 오른쪽으로)
    if dots_count < ats_progress_last_dots:
        remove_count = ats_progress_last_dots - dots_count
        for i in range(remove_count):
            if ats_progress_dots:
                # 왼쪽부터 제거 (첫 번째 요소부터)
                first_bar = ats_progress_dots.pop(0)
                if first_bar in splash:
                    splash.remove(first_bar)
        ats_progress_last_dots = dots_count

def start_word_progress_dots():
    """단어 간격 점 진행 시작 (10개 점)"""
    global word_progress_start_time, word_progress_active, word_progress_last_dots
    word_progress_start_time = time.monotonic()
    word_progress_active = True
    word_progress_last_dots = 0
    for dot in word_progress_dots:
        if dot in splash:
            splash.remove(dot)
    word_progress_dots.clear()

def calculate_signal_timer(signal):
    """신호별 타이머 계산 (최적화)"""
    dot_duration = 1.2 / wpm
    signal_duration = dot_duration if signal == '.' else dot_duration * das_r_value
    signal_gap = dot_duration
    word_gap = dot_duration * iwg_r_value
    iwg_offset = iwg * 0.015
    return signal_duration + signal_gap + word_gap + iwg_offset

def start_direct_mode_timer(signal):
    # 직접 입력 타이머
    global last_input_time, last_activity_time
    current_time = time.monotonic()
    total_timer = calculate_signal_timer(signal)
    last_input_time = current_time + total_timer
    last_activity_time = time.monotonic()
    hide_ready()
    start_word_progress_dots()

def handle_direct_mode_timer_complete():
    # 직접 입력 완료
    global last_activity_time, last_input_time, ats_timer_start, ats_timer_active
    clear_word_progress_bars()
    
    # AT-S가 ON이면 AT-S 타이머 시작, OFF면 스페이스 안함
    # KR 모드에서는 AT-S 설정값에 관계없이 자동 스페이스 비활성화 (MO 모드에서는 작동)
    if ats_value > 0 and not (current_lang == "KR" and not direct_morse_mode):
        ats_timer_start = time.monotonic()
        ats_timer_active = True
        # AT-S 타이머 시작 시 LED 켜기 (시각적 표시)
        led.value = True
        # AT-S 진행바 시작
        start_ats_progress_dots()
    # AT-S OFF일 때나 KR 모드일 때는 스페이스 입력 안함 (자동 스페이스 비활성화)
    
    last_input_time = float('inf')
    last_activity_time = time.monotonic()
    display.refresh()

def reset_direct_mode_timer():
    """직접 입력 모드 타이머 초기화 (진행바 제거)"""
    global last_input_time
    last_input_time = float('inf')
    if word_progress_active:
        clear_word_progress_bars()

def update_word_progress_dots():
    """단어 간격 진행바 업데이트 (메모리 최적화)"""
    global word_progress_active, word_progress_last_dots
    
    if not word_progress_active or (not direct_morse_mode and not morse_pattern):
        return
    
    current_time = time.monotonic()
    elapsed = current_time - word_progress_start_time
    remaining_time = last_input_time - current_time
    total_time = last_input_time - word_progress_start_time
    
    if remaining_time <= 0 or total_time <= 0:
        clear_word_progress_bars()
        return
    
    progress = elapsed / total_time
    dots_count = 10 if progress >= 0.9 else int(progress * 10 / 0.9)
    
    if dots_count > word_progress_last_dots:
        # 상수로 미리 계산된 값들 사용 (메모리 최적화)
        BOX_WIDTH = 62
        BOX_HEIGHT = 4
        START_X = 1
        START_Y = 11
        BOX_WIDTH_EACH = 5  # (62-2-9)/10 = 5.1 -> 5
        GAP_WIDTH = 1
        
        for i in range(word_progress_last_dots, dots_count):
            x_pos = START_X + i * (BOX_WIDTH_EACH + GAP_WIDTH)
            progress_bar = rect.Rect(x_pos, START_Y, BOX_WIDTH_EACH, BOX_HEIGHT, fill=0x00FF00)
            splash.append(progress_bar)
            word_progress_dots.append(progress_bar)
        word_progress_last_dots = dots_count


def save_settings():
    """현재 WPM, IWG 값만 settings.toml에 저장"""
    global DEFAULT_WPM, DEFAULT_IWG
    try:
        # 전역 변수 업데이트 (WPM, IWG만)
        DEFAULT_WPM = wpm
        DEFAULT_IWG = iwg
        
        # 기존 설정 파일 읽기
        try:
            with open('/settings.toml', 'r') as f:
                existing_content = f.read()
        except:
            existing_content = ""
        
        # 기존 설정에서 WPM, IWG만 업데이트
        lines = existing_content.split('\n')
        updated_lines = []
        
        for line in lines:
            if line.startswith('DEFAULT_WPM'):
                updated_lines.append(f'DEFAULT_WPM = {wpm}')
            elif line.startswith('DEFAULT_IWG'):
                updated_lines.append(f'DEFAULT_IWG = {iwg}')
            elif line.startswith('SAVED_TIME'):
                updated_lines.append(f'SAVED_TIME = "{time.monotonic():.0f}"')
            else:
                updated_lines.append(line)
        
        # WPM, IWG가 없으면 추가
        if not any(line.startswith('DEFAULT_WPM') for line in updated_lines):
            updated_lines.insert(0, f'DEFAULT_WPM = {wpm}')
        if not any(line.startswith('DEFAULT_IWG') for line in updated_lines):
            updated_lines.insert(1, f'DEFAULT_IWG = {iwg}')
        
        # 파일에 저장
        with open('/settings.toml', 'w') as f:
            f.write('\n'.join(updated_lines))
        
        global key_display_time, key_display_active
        character_display.text = "[SAVED]"
        if character_display not in splash:
            splash.append(character_display)
        key_display_time = time.monotonic()
        key_display_active = True
        return True
    except Exception as e:
        # 저장 실패 시 FAILED 표시
        global key_display_time, key_display_active
        character_display.text = "[FAILED]"
        if character_display not in splash:
            splash.append(character_display)
        key_display_time = time.monotonic()
        key_display_active = True
        return False

def clear_morse_display():
    """모스부호 화면 표시 초기화"""
    global morse_pattern
    morse_pattern = ""
    morse_display.text = ""
    if morse_display in splash:
        splash.remove(morse_display)

def reset_morse_pattern():
    """모스부호 패턴 초기화"""
    clear_morse_display()

# WPM/IWG 엔코더 콜백 함수들
def wpm_callback(direction):
    """WPM 엔코더 콜백"""
    global wpm
    if direction == 1:  # 반시계방향 (증가)
        if wpm < 30:
            wpm += 1
            update_wpm_display()
            calculate_intervals()
    else:  # 시계방향 (감소)
        if wpm > 5:
            wpm -= 1
            update_wpm_display()
            calculate_intervals()

def iwg_callback(direction):
    """IWG 엔코더 콜백"""
    global iwg
    if direction == 1:  # 반시계방향 (증가)
        if iwg < 40:
            iwg += 1
            update_iwg_display()
            calculate_intervals()
    else:  # 시계방향 (감소)
        if iwg > -40:
            iwg -= 1
            update_iwg_display()
            calculate_intervals()

def handle_switch(pin, pressed_state, last_press_time, action_func, name, 
                  inverted=False, repeat_action=None, repeat_delay=1.0, repeat_interval=0.1, release_action=None):
    """통합 스위치 처리 함수"""
    current_time = time.monotonic()
    
    # 스위치 상태 확인 (일반/반전 모두 지원)
    is_pressed = not pin.value if not inverted else pin.value
    
    if is_pressed:
        if not pressed_state['value']:  # 처음 눌렸을 때
            pressed_state['value'] = True
            last_press_time['value'] = current_time
            action_func()
            if repeat_action:
                last_press_time['repeat_time'] = current_time + repeat_delay
                
        elif repeat_action:  # 연속 입력이 있는 경우
            if current_time >= last_press_time.get('repeat_time', float('inf')):
                if current_time - last_press_time['value'] >= repeat_interval:
                    last_press_time['value'] = current_time
                    repeat_action()
    else:
        if pressed_state['value']:
            pressed_state['value'] = False
            # 스위치를 떼는 순간에 release_action 실행
            if release_action:
                release_action()

def handle_hangul_switch():
    """한영 변환 스위치 전용 처리 (키 입력 + 언어 전환)"""
    send_hangul_key()
    switch_language()  # switch_language()에서 AT-S 진행바 업데이트가 이미 처리됨

def handle_macro_switch():
    """매크로 표시 스위치 처리 (토글 방식, 떼어진 상태가 ON)"""
    global macro_visible
    if macro_switch.value:
        if not macro_visible:
            macro_visible = True
            update_macro_display()
    else:
        if macro_visible:
            macro_visible = False
            update_macro_display()


def update_all_systems():
    """모든 시스템 상태 업데이트"""
    global ats_timer_active
    
    update_buzzer()
    update_word_progress_dots()
    update_ats_progress_dots()
    update_caps_lock_led()
    ensure_mode_display()
    
    # AT-S 타이머 체크 (KR 모드에서는 비활성화, MO 모드에서는 작동)
    if ats_timer_active and not (current_lang == "KR" and not direct_morse_mode):
        current_time = time.monotonic()
        elapsed_time = (current_time - ats_timer_start) * 1000  # 초를 밀리초로 변환
        if elapsed_time >= ats_value:
            send_space_key()
            ats_timer_active = False
            # AT-S 타이머 완료 시 LED 끄기
            led.value = False
            # AT-S 타이머 완료 후 바로 꽉 찬 상태로 복원 (깜박임 방지)
            ats_progress_active = False
            ats_progress_full = True
            ats_progress_last_dots = 10
            
            # 진행바가 있으면 색상만 변경, 없으면 새로 생성
            if ats_progress_dots:
                # 기존 진행바를 모두 녹색으로 변경
                for progress_bar in ats_progress_dots:
                    progress_bar.fill = 0x00FF00
            else:
                # 진행바가 없으면 새로 생성
                box_count = 10
                box_width = 62
                box_height = 4
                start_x = 67
                start_y = 11
                
                available_width = box_width - 2
                box_width_each = available_width // box_count
                
                for i in range(10):
                    x_pos = start_x + i * box_width_each
                    progress_bar = rect.Rect(x_pos, start_y, box_width_each, box_height, fill=0x00FF00)
                    splash.append(progress_bar)
                    ats_progress_dots.append(progress_bar)
    
    # 메뉴가 열려있을 때는 메뉴 엔코더 사용, 아니면 일반 엔코더 사용
    if menu_visible:
        read_menu_encoder()
    else:
        read_encoder_unified("encoder1", wpm_callback)
        read_encoder_unified("encoder2", iwg_callback)

def finish_morse_conversion():
    """모스 변환 후 정리 작업"""
    global last_activity_time, ats_timer_start, ats_timer_active
    clear_morse_display()
    clear_word_progress_bars()
    last_activity_time = time.monotonic()
    
    # AT-S 타이머 시작 (AT-S가 ON일 때만, KR 모드에서는 비활성화, MO 모드에서는 작동)
    if ats_value > 0 and not (current_lang == "KR" and not direct_morse_mode):
        ats_timer_start = time.monotonic()
        ats_timer_active = True
        # AT-S 타이머 시작 시 LED 켜기 (시각적 표시)
        led.value = True
        # AT-S 진행바 시작
        start_ats_progress_dots()
    
    display.refresh()

def handle_morse_conversion():
    """모스부호 패턴을 문자로 변환하고 키보드 입력 및 화면에 표시"""
    macro_display, macro_input, is_both_macro = check_macro_match(morse_pattern, current_lang)
    if macro_display and macro_input:
        send_macro_text_to_keyboard(macro_input, force_english=False)
        create_character_display(f"M: {macro_display}", color=0x00FFFF)
        finish_morse_conversion()
        return
    
    # 매크로 매칭 실패 시에도 모스부호 패턴 인식 계속
    if macro_visible:
        # 매크로 매칭 실패 시 모스부호 패턴으로 계속 진행
        pass
    
    if is_valid_pattern_for_mode(morse_pattern, current_lang):
        character = morse_dict[morse_pattern]
        
        # 특수문자/구두점인지 확인 (숫자는 AT-S 적용)
        char_code = ord(character)
        is_special_char = (
            # 구두점 및 특수문자 (숫자 제외)
            char_code in [46, 44, 63, 33, 45, 47, 40, 41, 61, 43, 58, 59, 34, 39, 95, 36, 64] or
            # 한글 특수문자 (한글 모드에서)
            (current_lang == "KR" and char_code in [0x3131, 0x3132, 0x3133, 0x3134, 0x3135, 0x3136, 0x3137, 0x3138, 0x3139, 0x313A, 0x313B, 0x313C, 0x313D, 0x313E, 0x313F, 0x3140, 0x3141, 0x3142, 0x3143, 0x3144, 0x3145, 0x3146, 0x3147, 0x3148, 0x3149, 0x314A, 0x314B, 0x314C, 0x314D, 0x314E, 0x314F, 0x3150, 0x3151, 0x3152, 0x3153, 0x3154, 0x3155, 0x3156, 0x3157, 0x3158, 0x3159, 0x315A, 0x315B, 0x315C, 0x315D, 0x315E, 0x315F, 0x3160, 0x3161, 0x3162, 0x3163])
        )
        
        if current_lang == "KR":
            if 0x3131 <= char_code <= 0x3163:
                # 캡스락이 켜져있으면 화면 표시도 된소리로
                display_character = character
                if caps_lock_state and character in CAPS_CONVERSION_MAP:
                    display_character = CAPS_CONVERSION_MAP[character]
                
                create_character_display(display_character, korean_font)
                send_korean_character_to_keyboard(character)
            else:
                create_character_display(character)
                send_character_to_keyboard(character)
        else:
            display_text = character.upper() if caps_lock_state else character.lower()
            create_character_display(display_text)
            send_character_to_keyboard(display_text)
        
        # 특수문자/구두점이 아닌 경우에만 AT-S 타이머 시작 (숫자는 AT-S 적용)
        if not is_special_char:
            finish_morse_conversion()
        else:
            # 특수문자는 AT-S 없이 정리만 수행
            clear_morse_display()
            clear_word_progress_bars()
            last_activity_time = time.monotonic()
            display.refresh()
    else:
        # 유효하지 않은 패턴일 때는 AT-S 타이머 시작하지 않음
        create_character_display(f"?({current_lang})")
        # AT-S 없이 정리만 수행
        clear_morse_display()
        clear_word_progress_bars()
        last_activity_time = time.monotonic()
        display.refresh()

def create_character_display(text, font=None, color=0x00FF00):
    """character_display를 생성하고 배치하는 통합 함수"""
    global character_display
    if character_display in splash:
        splash.remove(character_display)
    if font is None:
        font = terminalio.FONT
    character_display = label.Label(font, text=text, color=color, x=64, y=49)
    character_display.anchor_point = (0.5, 0.5)
    character_display.anchored_position = (64, 49)
    splash.append(character_display)

def handle_morse_input():
    """통합 모스부호 입력 처리 (구조 개선)"""
    global both_pressed, dot_pressed, line_pressed
    global dot_last_press_time, line_last_press_time, ignore_input_until
    
    current_time = time.monotonic()
    test_mode = menu_visible  # 메뉴가 열려있을 때는 테스트 모드
    
    # 동시 누름 처리 (비활성화)
    # if _handle_simultaneous_press(test_mode):
    #     return True
    
    # 새로운 입력 및 교차 입력 처리
    if _handle_new_inputs(current_time, test_mode):
        return True
    
    # 연속 입력 처리
    if _handle_continuous_inputs(current_time, test_mode):
        return True
    
    return False

def _handle_simultaneous_press(test_mode):
    """동시 누름 처리 (비활성화)"""
    # 동시 누름 기능이 비활성화됨
    return False

def _handle_new_inputs(current_time, test_mode):
    """새로운 입력 및 교차 입력 처리"""
    global dot_pressed, line_pressed, dot_last_press_time, line_last_press_time, ignore_input_until
    
    # 새로운 입력 감지
    new_dot_input = not switch_dot.value and not dot_pressed
    new_line_input = not switch_line.value and not line_pressed
    
    # 교차 입력 감지
    cross_dot_input = not switch_dot.value and line_pressed and switch_line.value
    cross_line_input = not switch_line.value and dot_pressed and switch_dot.value
    
    if new_dot_input or new_line_input or cross_dot_input or cross_line_input:
        signal = '.' if (new_dot_input or cross_dot_input) else '-'
        
        if test_mode:
            start_morse_signal(signal)
        elif direct_morse_mode:
            handle_direct_mode_signal(signal)
        else:
            if start_new_signal(signal):
                display.refresh()
        
        # 상태 업데이트
        if new_dot_input or cross_dot_input:
            dot_pressed = True
            dot_last_press_time = current_time
            ignore_input_until = current_time + dot_interval
            if cross_dot_input:
                line_pressed = False
        else:
            line_pressed = True
            line_last_press_time = current_time
            ignore_input_until = current_time + line_interval
            if cross_line_input:
                dot_pressed = False
        
        if text_area in splash:
            splash.remove(text_area)
        return True
    return False

def _handle_continuous_inputs(current_time, test_mode):
    """연속 입력 처리"""
    global dot_pressed, line_pressed, dot_last_press_time, line_last_press_time, ignore_input_until
    
    # ignore_input_until 확인
    if current_time < ignore_input_until:
        if switch_dot.value:
            dot_pressed = False
        if switch_line.value:
            line_pressed = False
        return True
    
    # 점 스위치 연속 입력
    if not switch_dot.value and dot_pressed:
        if current_time - dot_last_press_time >= dot_interval:
            dot_last_press_time = current_time
            _process_signal('.', test_mode)
            ignore_input_until = current_time + dot_interval
    else:
        if dot_pressed:
            dot_pressed = False
    
    # 선 스위치 연속 입력
    if not switch_line.value and line_pressed:
        if current_time - line_last_press_time >= line_interval:
            line_last_press_time = current_time
            _process_signal('-', test_mode)
            ignore_input_until = current_time + line_interval
    else:
        if line_pressed:
            line_pressed = False
    
    return False

def _process_signal(signal, test_mode):
    """신호 처리"""
    if test_mode:
        start_morse_signal(signal)
    elif direct_morse_mode:
        handle_direct_mode_signal(signal)
    else:
        if start_new_signal(signal):
            display.refresh()

def add_morse_signal(signal):
    global morse_pattern, last_input_time, last_activity_time, ats_timer_active, enter_with_pattern, space_pressed, enter_via_space
    if ats_timer_active:
        ats_timer_active = False
        led.value = False  # AT-S 타이머 취소 시 LED 끄기
        clear_ats_progress_bars()  # AT-S 진행바 제거
    
    if len(morse_pattern) < 20:
        if space_pressed:
            press_release(Keycode.ENTER)
            show_key_action("ENTER")
            enter_via_space = True
            return
        
        morse_pattern += signal
        morse_display.text = morse_pattern
        if morse_display not in splash:
            splash.append(morse_display)
        enter_with_pattern = False
        enter_via_space = False
        
        current_time = time.monotonic()
        total_timer = calculate_signal_timer(signal)
        last_input_time = current_time + total_timer
        last_activity_time = time.monotonic()
        hide_ready()
        start_word_progress_dots()
        return True
    else:
        return False

# 버퍼 초기화
supervisor.runtime.autoreload = False

# WPM 진행바 초기화
update_progress_bar("wpm")
# IWG 진행바 초기화
update_progress_bar("iwg")
# 초기 언어별 LED 설정
set_language_led()
# 초기 모드 표시 업데이트
update_mode_display()
# 초기 AT-S 상태 표시 업데이트
update_ats_status_display()
# 초기 AT-S 진행바 표시
if ats_value > 0:
    # AT-S 진행바를 꽉 찬 상태로 표시 (진행 중이 아닌 상태)
    ats_progress_full = True
    ats_progress_active = False
    ats_progress_last_dots = 10
else:
    # AT-S OFF일 때는 빈 상태로 표시
    ats_progress_full = False
    ats_progress_active = False
    ats_progress_last_dots = 0
    
    # 꽉 찬 상태로 10개 점 생성 (AT-S 외각 박스 안에)
    box_count = 10
    box_width = 62
    box_height = 4
    start_x = 67  # AT-S 외각 박스 시작 위치 (x=66+1=67)
    start_y = 11
    
    # AT-S 진행바는 간격 없이 박스 크기를 크게 (6픽셀씩)
    available_width = box_width - 2
    box_width_each = available_width // box_count  # 간격 없이 6픽셀씩
    
    for i in range(10):
        x_pos = start_x + i * box_width_each  # 간격 없이 붙여서 배치
        progress_bar = rect.Rect(x_pos, start_y, box_width_each, box_height, fill=0x00FF00)
        splash.append(progress_bar)
        ats_progress_dots.append(progress_bar)

# 메인 루프

while True:
    try:
        current_time = time.monotonic()
        
        # 1. 시스템 상태 업데이트
        update_all_systems()
        
        # 2. 모스부호 입력 처리
        if handle_morse_input():
            continue
    
        # 3. 스위치 입력 처리
        handle_switch(enter_button, switch_states['enter'], switch_times['enter'], 
                      send_enter_key, "엔터 버튼", release_action=handle_enter_release)
        
        handle_switch(backspace_button, switch_states['backspace'], switch_times['backspace'], 
                      send_backspace_key, "백스페이스 버튼", repeat_action=send_backspace_key, 
                      repeat_delay=0.5, repeat_interval=0.1)
        
        handle_lang_switch()
        
        handle_switch(hangul_switch, switch_states['hangul'], switch_times['hangul'], 
                      handle_hangul_switch, "한영 변환 스위치")
        
        handle_macro_switch()
        
        handle_ats_toggle()
        
        handle_switch(caps_switch, switch_states['caps'], switch_times['caps'], 
                      send_caps_lock_key, "CAPS LOCK 스위치")
        
        handle_switch(save_switch, switch_states['save'], switch_times['save'], 
                      save_all_settings, "저장 스위치")
        
        handle_menu_switch()
    
        # 5. 모스부호 변환 처리
        if morse_pattern and current_time >= last_input_time and not direct_morse_mode:
            handle_morse_conversion()
        
        if direct_morse_mode and current_time >= last_input_time:
            handle_direct_mode_timer_complete()
        
        # 6. UI 상태 업데이트
        if key_display_active and (current_time - key_display_time) >= 1.0:
            key_display_active = False
            show_ready()
        
        if last_activity_time > 0 and (current_time - last_activity_time) >= ready_timeout:
            show_ready()
            last_activity_time = 0
        
                
    except:
        time.sleep(0.1)