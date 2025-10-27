# [KOR] MORSEKEY-A01 프로젝트 개요

**프로젝트 소개 영상:**
https://www.youtube.com/shorts/JlrWVxrsSqo


**MORSEKEY-A01**은 **RP2040-Zero** 보드를 기반으로 제작된 **모스부호 키보드 입력 장치**입니다.  
듀얼 키(또는 듀얼 패드) 방식으로 동작하며, 사용자가 점(dot)과 선(dash)을 입력하면 해당 패턴에 맞는 문자가 자동으로 변환되어 입력됩니다.  

매크로 기능을 통해 자주 사용하는 문장을 자동으로 입력할 수 있으며,  
OLED 디스플레이에서는 현재 언어, 속도(WPM), 간격(IWG), 사운드 설정 등을 실시간으로 확인할 수 있습니다.  

누구나 쉽게 제작할 수 있도록 회로와 구조를 단순화했으며,  
기본적인 납땜만으로 조립이 가능하도록 설계되었습니다.  

코드는 **CircuitPython(서킷파이썬)** 으로 작성되었으며,  
PCB 거버 파일, 3D 모델링 데이터, 펌웨어 코드 등 제작에 필요한 모든 자료가 포함되어 있습니다.  
전문 프로그래머가 아니더라도 제작 과정을 따라 하며 학습과 응용이 가능하도록 구성되었습니다.  

조립 관련 매뉴얼은 **한국어 및 영어 버전**으로 제공됩니다.

---

## 완성 사진

<img width="800" alt="MORSEKEY-A01 Real Photo" src="https://github.com/user-attachments/assets/2dfefea7-2b9a-453e-9288-0095c97f78bc" />

---

## 주요 기능

- **모스부호 자동 변환 입력**  
  듀얼 키(점·선)를 이용해 입력한 모스부호 패턴을 문자로 자동 변환하여 PC로 전송합니다.

- **언어 전환 (SYNC)**  
  SYNC 스위치를 통해 입력 언어를 **KR / EN / MO** 모드로 전환할 수 있습니다.  
  - KR : 한글  
  - EN : 영어  
  - MO : 모스부호 직접 입력 모드 (점·선 신호 그대로 입력)

- **대소문자 구분 (CAPS LOCK)**  
  CAPS LOCK 기능을 이용해 대문자와 소문자를 구분할 수 있습니다.

- **매크로 기능 (MACRO)**  
  자주 사용하는 단어나 문장을 JSON 파일에 등록해, 특정 모스 패턴 입력 시 자동으로 문장을 완성합니다.

- **자동 스페이스 (AT-S)**  
  단어 간 자동 간격(스페이스)을 입력하며, 개인 입력 속도에 맞게 딜레이 타이밍을 조정할 수 있습니다.

- **WPM / IWG 실시간 조정**  
  로터리 엔코더를 통해 전송 속도(WPM)와 간격(IWG)을 실시간으로 조정할 수 있습니다.

- **사운드 및 주파수 설정**  
  입력 시 발생하는 비프음의 주파수와 음량을 사용자 취향에 맞게 조절할 수 있습니다.

- **OLED 디스플레이 표시**  
  현재 입력 상태, 언어 모드, WPM/IWG 수치, 매크로 상태 등을 OLED 화면에서 확인할 수 있습니다.

- **설정 저장 및 복원**  
  사용자가 변경한 설정(WPM, IWG, 사운드 등)을 저장하고 재부팅 시 자동으로 불러옵니다.

---

## 회로 구성도 (Circuit Diagram)

<img width="800" alt="MORSEKEY-A01 Circuit" src="https://github.com/user-attachments/assets/f4f3a235-8828-4c03-8761-ed286f14b208" />

위 이미지는 MORSEKEY-A01의 **전자회로 구성도**입니다.

## PCB 거버 데이터

<img width="800" alt="Image" src="https://github.com/user-attachments/assets/33996fed-99c0-443b-923f-121ea926a1dc" />

---

## 옵션 메뉴 설명

| 항목 | 기능 |
|------|------|
| **HZ** | 모스부호 사운드 주파수를 100~3000Hz 범위에서 조절 |
| **VOL** | 사운드 볼륨을 0~5단계로 조절 |
| **DAS-R** | 선(–)의 길이를 1.5~4.0 범위에서 0.5 단위로 조절 |
| **IWG-R** | 문자 간 간격을 3.0~10.0 범위에서 1.0 단위로 조절 |
| **AT-S** | 자동 스페이스 타이밍을 25~3000ms 범위에서 25ms 단위로 조절 |
| **DEFAULT** | 모든 설정을 초기값으로 복원 |
| **SAVE** | 현재 설정을 저장 (성공 시 “DONE”, 실패 시 “FAIL”) |
| **BACK** | 옵션 메뉴를 종료하고 메인 화면으로 복귀 |

---

## 관련 자료 및 다운로드

🔗 **OSHWLab (회로 및 제조 자료)**  
https://oshwlab.com/kimgx05/morsekey-a01  
해당 자료는 실제 출력(3D 프린팅) 또는 가공(CNC, 레이저 컷팅 등)에 바로 사용할 수 있습니다.

🔗 **GitHub (소스코드 및 펌웨어)**  
https://github.com/Airmodeling/MORSEKEY-A01  

### 프로그램 구성
- **MORSEKEY_CODE** – 메인 프로그램 코드 (CircuitPython)  
- **MORSEKEY_Macro_Editor** – 매크로 파일 편집용 PC 프로그램  
- **adafruit-circuitpython-raspberry_pi_pico-en_US-9.2.8** – RP2040-Zero용 CircuitPython 펌웨어  

---

## 프로젝트 의도

MORSEKEY-A01은 ‘누구나 만들 수 있는 모스부호 키보드’를 목표로 설계했습니다.  
단순한 입력 장치를 넘어, 직접 조립하고 설정하며 전자 제작의 과정을 배우고 즐길 수 있도록 구성했습니다.  

이 작품이 여러분의 제작과 학습, 그리고 새로운 아이디어에 도움이 되길 바랍니다.  
다운로드하여 직접 제작해 주신 모든 분들께 진심으로 감사드립니다.

---

## 라이선스 및 저작권 안내

이 프로젝트는 **Adafruit CircuitPython (MIT License)** 을 기반으로 제작된 오픈소스 하드웨어입니다.  

MORSEKEY-A01은 학습, 취미 제작, 개인 연구 목적에 한해 자유롭게 사용할 수 있습니다.  
포함된 회로, 3D 데이터, 펌웨어, 매뉴얼, 디자인 등 모든 자료는 공개 형태로 제공됩니다.

**사용 및 배포 조건**
1. 모든 자료는 **비상업적·비영리적 목적**에 한해 자유롭게 이용할 수 있습니다.  
2. **상업적 판매, 수정 후 재배포, 2차 제작물 판매** 등 영리 목적의 사용은 금지됩니다.  
3. 개인 학습 목적의 수정은 가능하나, 재배포 시 반드시 **원 저작자(Airmodeling)** 를 명시해야 합니다.  
4. 본 프로젝트 사용 중 발생하는 문제·오류·손상·기기 고장 등에 대한 책임은 사용자 본인에게 있습니다.

---

## 참고 및 문의

- **YouTube:** [@Airmodeling](https://www.youtube.com/@airmodeling)  
- **Instagram:** [@airmodel00](https://www.instagram.com/airmodel00/)  
- **X (Twitter):** [@airmodel00](https://x.com/airmodel00)  
- **문의:** airmodel00@gmail.com  

© 2025 Airmodeling. All Rights Reserved.  
본 문서는 **CC BY-NC-SA 4.0** 라이선스를 따릅니다.  
이 프로젝트는 **Adafruit CircuitPython (MIT License)** 을 기반으로 제작되었습니다.

---

# [ENG] MORSEKEY-A01 Project Overview

**Project Video:**
https://www.youtube.com/shorts/JlrWVxrsSqo


**MORSEKEY-A01** is a **Morse code keyboard input device** based on the **RP2040-Zero** board.  
It operates with dual keys (or pads), converting dot and dash inputs into corresponding characters automatically.  

Through the macro feature, users can register frequently used sentences for quick automatic input.  
The OLED display shows real-time information such as language mode, WPM, IWG, and sound settings.  

The circuit and structure are simplified for anyone to assemble easily with only basic soldering.  
The firmware is written in **CircuitPython**, and all necessary materials—PCB Gerber files, 3D modeling data, and source code—are included.  
Even without programming experience, users can follow the build process and learn while creating their own device.  

Assembly manuals are provided in **Korean and English**.

---

## Main Features

- **Automatic Morse Code Conversion**  
  Inputs from dual keys (dot/dash) are automatically converted to characters and sent as keyboard input to the PC.

- **Language Switching (SYNC)**  
  Switch between **KR / EN / MO** modes using the SYNC button.  
  - KR: Korean  
  - EN: English  
  - MO: Direct Morse input mode (enter raw dots and dashes)

- **CAPS LOCK Support**  
  Toggle between uppercase and lowercase letters.

- **Macro Function (MACRO)**  
  Register commonly used words or sentences in a JSON file.  
  When a specific Morse pattern is entered, the corresponding text is automatically generated.

- **Auto Space (AT-S)**  
  Automatically inserts spaces between words with adjustable timing.

- **WPM / IWG Adjustment**  
  Use the rotary encoder to adjust transmission speed (WPM) and spacing (IWG) in real time.

- **Sound and Frequency Settings**  
  Customize the beep tone and volume during input.

- **OLED Display Output**  
  View current state, language mode, WPM/IWG values, and macro status.

- **Save and Restore Settings**  
  User-defined configurations (WPM, IWG, sound, etc.) are stored and reloaded after reboot.

---

## Circuit Diagram

<img width="800" alt="MORSEKEY-A01 Circuit" src="https://github.com/user-attachments/assets/f4f3a235-8828-4c03-8761-ed286f14b208" />

The image above shows the electronic circuit diagram of the MORSEKEY-A01.

## PCB Gerber Preview

<img width="800" alt="Image" src="https://github.com/user-attachments/assets/33996fed-99c0-443b-923f-121ea926a1dc" />

---

## Option Menu

| Item | Description |
|------|--------------|
| **HZ** | Adjust beep frequency (100–3000Hz) |
| **VOL** | Adjust sound volume (0–5 levels) |
| **DAS-R** | Adjust dash length (1.5–4.0, step 0.5) |
| **IWG-R** | Adjust inter-word gap (3.0–10.0, step 1.0) |
| **AT-S** | Adjust auto space delay (25–3000ms, step 25ms) |
| **DEFAULT** | Restore all settings to default |
| **SAVE** | Save current settings (shows “DONE” or “FAIL”) |
| **BACK** | Exit option menu and return to main screen |

---

## Resources & Downloads

🔗 **OSHWLab (PCB and design files)**  
https://oshwlab.com/kimgx05/morsekey-a01  
These files can be directly used for fabrication or 3D printing.

🔗 **GitHub (Source & Firmware)**  
https://github.com/Airmodeling/MORSEKEY-A01  

These files can be directly used for fabrication or 3D printing.

### File Structure
- **MORSEKEY_CODE** – Main program (CircuitPython)  
- **MORSEKEY_Macro_Editor** – PC macro editor program  
- **adafruit-circuitpython-raspberry_pi_pico-en_US-9.2.8** – CircuitPython firmware for RP2040-Zero  

---

## Project Concept

MORSEKEY-A01 was designed with the goal of being a **Morse keyboard anyone can build**.  
Beyond being a simple input device, it encourages users to experience and enjoy the process of electronic design and customization.  

We hope this project inspires creativity and helps others learn and experiment.  
Thank you to everyone who downloaded, built, and shared this work.

---

## License & Copyright

This project is based on **Adafruit CircuitPython (MIT License)** and is open-source hardware.  

MORSEKEY-A01 is free to use for educational, hobby, and personal research purposes.  
All included resources—schematics, 3D data, firmware, manuals, and design files—are publicly available.

**Usage & Distribution Rules**
1. All materials are for **non-commercial and non-profit use only**.  
2. **Commercial sales, redistribution, or derivative works for profit** are prohibited.  
3. Personal modifications are allowed, but redistribution must credit **Airmodeling**.  
4. The author is not responsible for any issues, damages, or failures arising from the use of this project.

---

## References & Contact

- **YouTube:** [@Airmodeling](https://www.youtube.com/@airmodeling)  
- **Instagram:** [@airmodel00](https://www.instagram.com/airmodel00/)  
- **X (Twitter):** [@airmodel00](https://x.com/airmodel00)  
- **Email:** airmodel00@gmail.com  

© 2025 Airmodeling. All Rights Reserved.  
This document follows the **CC BY-NC-SA 4.0** license.  
The project is based on **Adafruit CircuitPython (MIT License)**.
