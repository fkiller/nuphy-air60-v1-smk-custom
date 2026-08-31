# NuPhy Air60 V1 custom firmware

This repository is a focused SMK fork for the NuPhy Air60 V1. It keeps the upstream keyboard matrix and transport paths unchanged and limits custom behavior to the Air60-specific keymap and keyboard handler.

## Custom behavior

- `Esc` sends Escape; `Shift + Esc` sends `~` on a US ANSI host layout.
- Tapping `Fn` alone sends Right Alt, which the Windows Korean IME can use for Korean/English switching.
- Holding `Fn` and pressing another key keeps the existing Windows Fn layer behavior.
- Left `OPT` sends Left Alt/Option and left `CMD` sends Left GUI/Command on both Windows and macOS.
- The right-bottom key mapping remains unchanged.
- USB and 2.4 GHz are the intended transports. Bluetooth support remains work in progress upstream.

## Ready-to-flash image

`firmware/air60-v1-smk-custom.hex`

SHA-256:

```text
634060FEF61D042DB32B4713C6F923F54A9411842FBAB95C7B1DB58FB9BE7265
```

## Build

Install Meson, Ninja, SDCC 4.3 or later, and `sinowealth-kb-tool`, then run:

```sh
meson setup build
meson compile -C build nuphy-air60_default_smk.hex
```

The regression suite can be run with:

```sh
python -m unittest discover -s tests
```

## Flash and recovery safety

SMK is experimental. Preserve a verified full stock-firmware dump outside this repository before flashing. Keep the recovery programmer and stock image available because a broken ISP path can require hardware programming to recover the keyboard.

With the keyboard intentionally placed in its supported ISP mode, flash through the upstream target:

```sh
meson compile -C build nuphy-air60_default_flash
```

Do not use the Bluetooth path as an acceptance criterion for this build. Verify USB first, then the 2.4 GHz receiver.
