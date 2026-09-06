# Windows 플래시 안내 / Air60 V1 only

이 펌웨어는 NuPhy Air60 **V1 전용** 실험 버전입니다. V2 또는 다른 모델에 쓰지 마세요. Bluetooth는 WIP이며 Mac 한영 전환과 2.4 GHz 실사용 검증은 아직 남아 있습니다.

## 1. 준비

릴리스 Assets에서 `air60-v1-smk-custom.hex`를 다운로드합니다. [sinowisp 공식 릴리스](https://github.com/carlossless/sinowisp/releases)에서 Windows용 도구를 받아 압축을 풉니다. 도구는 이전에 `sinowealth-kb-tool`이라는 이름이었으며, 이번 플래시는 버전 2.0.0으로 수행했습니다.

아래 예시는 실행 파일을 `sinowisp.exe`라는 이름으로 같은 폴더에 두고 PowerShell을 연 경우입니다. 실제 파일명이 `sinowealth-kb-tool.exe`라면 명령의 실행 파일명만 바꾸세요. `--version`, `read --help`, `write --help`로 버전과 옵션을 확인하세요.

Air60를 데이터 전송 가능한 USB 케이블로 PC에 직접 연결하고 유선 모드로 설정합니다. 다른 Air60는 분리하고 예비 키보드를 준비하세요. 플래시 중에는 케이블을 빼거나 PC를 절전/종료하지 마세요.

```powershell
.\sinowisp.exe list
Get-FileHash .\air60-v1-smk-custom.hex -Algorithm SHA256
```

이 릴리스의 SHA-256:

```text
31b1cbcf5bc3a60b6add5b4a8abfcaa0bcbaed11de288ea1fd982cfff528721d
```

일치하지 않으면 중단하세요. 현재 SMK 설치 장치는 `05ac:024f`, `SMK Keyboard`로 식별됩니다. 이 ID만으로 하드웨어 모델을 판단하지 마세요. 장치를 찾지 못하면 임의의 장치 ID나 플랫폼을 지정하지 말고 연결·모델을 재확인하세요.

## 2. 현재 펌웨어 백업

아래 파일명이 이미 있으면 새 이름을 사용하세요. 각 명령의 성공을 확인하고 다음으로 진행합니다.

```powershell
.\sinowisp.exe read -d nuphy-air60 -s full .\before-flash-full.bin
.\sinowisp.exe read -d nuphy-air60 -s full .\before-flash-full-check.bin
Get-FileHash .\before-flash-full.bin -Algorithm SHA256
Get-FileHash .\before-flash-full-check.bin -Algorithm SHA256
(Get-Item .\before-flash-full.bin).Length
```

두 해시가 같고 파일 크기가 65536바이트인지 확인합니다. 백업을 외부 저장장치에도 복사하세요. 이미 SMK를 사용 중이면 이것은 **순정이 아닌 현재 SMK 백업**입니다. 처음 설치할 때 확보한 순정 백업도 별도로 보관해야 합니다.

USB ISP 덤프는 프로그래머용 원시 메모리 이미지와 같지 않을 수 있습니다. [도구 설명](https://github.com/carlossless/sinowisp#reading)에 주소 재배치 및 읽기 시 펌웨어 활성화 주의사항이 있습니다. 백업만으로 복구가 보장되지 않으며, ISP 진입이 망가지면 하드웨어 프로그래머와 적절히 변환한 이미지가 필요합니다. 복구 수단을 준비하지 못했다면 플래시하지 마세요.

## 3. 플래시

```powershell
.\sinowisp.exe write -d nuphy-air60 --force .\air60-v1-smk-custom.hex
```

`--force`는 이 릴리스의 짧은 Intel HEX를 61440바이트 펌웨어 영역 크기로 패딩하기 위해 사용합니다. 다른 모델이나 잘못된 파일의 오류를 무시하는 용도로 사용하면 안 됩니다. 이번 이미지에서는 21031바이트를 61440바이트로 0 패딩한다는 경고가 예상됩니다.

도구가 지우기, 쓰기, 재읽기 검증, 재부팅을 마치고 `Successfully wrote 61440 bytes`를 출력해야 합니다. 검증 실패 시 성공으로 간주하지 말고 로그를 보존하세요. 이 절차는 정상 USB ISP에 접근 가능한 장치를 전제로 합니다. 실패했다고 임의의 부트로더 파일을 쓰거나 보호 기능을 해제하지 마세요.

## 4. 확인

USB 재인식 후 일반 타이핑과 Backspace를 먼저 확인합니다. Win 스위치에서 Fn 단독 탭은 Right Alt입니다. Mac 스위치에서는 Control+Space이며 macOS에 영어·한국어 입력 소스를 등록하고 해당 단축키를 ‘이전 입력 소스 선택’으로 설정해야 합니다. OS 자동 감지는 하지 않습니다.

Fn+숫자, Shift+Esc, 왼쪽 OPT/CMD도 확인한 뒤 2.4 GHz로 반복합니다. USB 쓰기 검증 성공은 실제 입력 기능의 검증을 대신하지 않습니다.

## 이번 릴리스 검증 기록

2026-09-06: 동일 이미지로 실제 Air60 V1에 61440바이트 쓰기 및 재읽기 검증 성공, 재부팅 후 USB에서 SMK Keyboard 재인식 확인. 플래시 전 65536바이트 백업을 두 번 읽어 일치 확인. Mac 입력 전환·일반 입력·2.4 GHz의 새 이미지 사용자 확인은 대기 중입니다.
