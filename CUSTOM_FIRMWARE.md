# NuPhy Air60 V1 custom firmware

This repository is a focused SMK fork for the NuPhy Air60 V1. It keeps the upstream keyboard matrix and transport paths unchanged and limits custom behavior to the Air60-specific keymap and keyboard handler.

## Custom behavior

- `Esc` sends Escape; `Shift + Esc` sends `~` on a US ANSI host layout.
- With the physical switch set to **Win**, tapping `Fn` alone sends Right Alt, which the Windows Korean IME can use for Korean/English switching.
- With the switch set to **Mac**, tapping `Fn` alone sends Control+Space (previous input source). Space is released before Control. This is a shortcut, not an Apple Globe/Fn HID key, and does not detect the host OS automatically.
- Holding `Fn` and pressing another key keeps the existing Windows Fn layer behavior.
- Left `OPT` sends Left Alt/Option and left `CMD` sends Left GUI/Command on both Windows and macOS.
- The right-bottom key mapping remains unchanged.
- USB and 2.4 GHz are the intended transports. Bluetooth support remains work in progress upstream.

## Ready-to-flash image

`firmware/air60-v1-smk-custom.hex`

SHA-256:

```text
31b1cbcf5bc3a60b6add5b4a8abfcaa0bcbaed11de288ea1fd982cfff528721d
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

For release downloads and Windows commands, follow [FLASHING.md](FLASHING.md). No source build is necessary to use the attached HEX image.

SMK is experimental. Preserve a verified full stock-firmware dump outside this repository before flashing. Keep the recovery programmer and stock image available because a broken ISP path can require hardware programming to recover the keyboard.

With the keyboard intentionally placed in its supported ISP mode, flash through the upstream target:

```sh
meson compile -C build nuphy-air60_default_flash
```

Do not use the Bluetooth path as an acceptance criterion for this build. Verify USB first, then the 2.4 GHz receiver.

## macOS setup

Set the keyboard's physical OS switch to **Mac**. Add both English and Korean input sources in macOS Keyboard settings. Under Keyboard Shortcuts > Input Sources, enable **Select the previous input source** and assign **Control+Space**. If another app uses this shortcut, resolve the conflict first. With more than two input sources this selects the previous source, not specifically Korean/English.

This uses Apple's documented [Control+Space input-source shortcut](https://support.apple.com/en-us/102650), not the Globe-key setting. No host-side remapping software is required. The physical switch selects the tap behavior; Fn chords and the base layout are unchanged in both positions.

## Verification status and release checklist

The 2026-09-06 image builds with SDCC, NKRO enabled and `DEBUG=1`, preserving the previously used configuration. Source-level regression checks cover the Fn scope, Mac release order, Windows branch and bottom-row mappings. These checks do not simulate USB timing or prove hardware behavior. Simulator tests require the patched uCsim tool and are skipped when it is unavailable.

The previous image was user-tested for basic input and Windows Fn tapping. **This Mac-shortcut image still needs on-device acceptance testing before a stable release.** Test USB on both operating systems: ordinary fast typing, Backspace release, repeated Fn taps, Fn+number chords, Shift+Esc and left OPT/CMD. Repeat with the 2.4 GHz receiver. Confirm that no key or modifier remains held after a tap or chord. Bluetooth remains unsupported/WIP.

Stock dumps and recovery images are deliberately not distributed. This fork retains the upstream GPL-2.0 license; see [LICENSE](LICENSE). It is an unofficial community project, not a NuPhy release. Intended for **Air60 V1 only**, not Air60 V2 or other models.
