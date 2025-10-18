# CircuitPython USB 장치 이름 설정
import usb_hid, board, digitalio, storage, usb_cdc, time

# 편집 모드용 입력 핀들 (2개 이상 스위치 누르면 편집 모드)
pins = [board.GP26, board.GP27, board.GP28]

def is_edit_mode():
    pressed_count = 0
    for p in pins:
        sw = digitalio.DigitalInOut(p)
        sw.switch_to_input(pull=digitalio.Pull.UP)  # 내부 풀업
        val = sw.value
        sw.deinit()
        if not val:  # GND에 눌림 (스위치가 눌린 상태)
            pressed_count += 1
    
    # 2개 이상의 스위치가 눌린 상태면 편집 모드
    return pressed_count >= 2

# 콘솔/데이터 시리얼 둘 다 활성화
usb_cdc.enable(console=True, data=True)

# 핀 안정화 대기(노이즈/스위치 바운싱 대비)
time.sleep(0.02)

if is_edit_mode():
    # 편집 모드: CIRCUITPY 드라이브 보이게 (PC에서 파일 수정)
    pass
else:
    # 실행 모드: CIRCUITPY 드라이브 숨김 (보드가 /settings.toml 등 쓰기 가능)
    storage.disable_usb_drive()

# USB HID 장치 활성화 및 이름 설정
usb_hid.enable(
    (
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.MOUSE,
        usb_hid.Device.CONSUMER_CONTROL,
    ),
    boot_device=1,
    product_name="MORSEKEY-A01",
    manufacturer="Airmodeling",
)
