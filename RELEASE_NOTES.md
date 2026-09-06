# v0.1.0-rc.1 — Air60 V1 Mac/Win Fn tap

Experimental prerelease for **NuPhy Air60 V1 only**. Not an official NuPhy release.

- Physical Win switch: Fn tap sends Right Alt.
- Physical Mac switch: Fn tap sends Control+Space, the configured previous-input-source shortcut.
- Existing Fn chords, Shift+Esc and corrected left OPT/CMD mapping retained.
- Global matrix, report and USB paths unchanged by the customization.

## Download and flash

Download `air60-v1-smk-custom.hex` from Assets. Read the attached **FLASHING.md** for Windows tool installation, two-read backup verification, checksum verification and flashing commands. The source archives are not the firmware image. Stock backups are not distributed.

SHA-256: `31b1cbcf5bc3a60b6add5b4a8abfcaa0bcbaed11de288ea1fd982cfff528721d`

## Verification and limitations

Two builds produced identical HEX files; six source checks passed. Simulator suites were skipped because the patched simulator was unavailable. On 2026-09-06, hardware write/read-back verification and USB re-enumeration succeeded. Actual Mac input switching and this image's typing/2.4 GHz acceptance tests await user confirmation, so this is not a stable release. Bluetooth remains WIP.

Use a verified backup and a viable hardware recovery path before flashing. In macOS, configure Control+Space for previous input source and add English/Korean input sources. This is not a native Apple Globe-key implementation.
