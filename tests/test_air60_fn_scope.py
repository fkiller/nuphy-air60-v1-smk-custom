from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent
LAYOUT = ROOT / "src" / "keyboards" / "nuphy-air60" / "layouts" / "default" / "layout.c"
KEYBOARD = ROOT / "src" / "keyboards" / "nuphy-air60" / "kb.c"


class TestAir60FnScope(unittest.TestCase):
    def test_mac_shortcut_is_scoped_to_uninterrupted_fn_release(self) -> None:
        source = KEYBOARD.read_text(encoding="utf-8")
        tap = source.split("if (!fn_interrupted) {", 1)[1].split('dprintf(', 1)[0]
        mac, windows = tap.split("} else {", 1)
        self.assertIn("user_keyboard_state.os_mode == KEYBOARD_OS_MODE_MAC", mac)
        operations = (
            "add_mods(MOD_BIT(KC_LCTL));", "add_key(KC_SPC);",
            "send_keyboard_report();", "del_key(KC_SPC);",
            "send_keyboard_report();", "del_mods(MOD_BIT(KC_LCTL));",
            "send_keyboard_report();",
        )
        remaining = mac
        for operation in operations:
            self.assertIn(operation, remaining)
            remaining = remaining.split(operation, 1)[1]
        self.assertIn("add_mods(MOD_BIT(KC_RALT));", windows)
        self.assertIn("del_mods(MOD_BIT(KC_RALT));", windows)
        self.assertNotIn("KC_SPC", windows)

    def test_left_opt_and_cmd_are_correct_on_the_active_base_layer(self) -> None:
        # Given: the Air60 base layer used for every host OS.
        source = LAYOUT.read_text(encoding="utf-8")
        active_base = source.split("[_MAC_BL]", 1)[1].split("[_WIN_BL]", 1)[0]

        # When: the physical bottom-row keycodes are inspected.
        left_bottom = "KC_LCTL, KC_LALT, KC_LGUI"

        # Then: left OPT is Alt/Option and left CMD is GUI/Command.
        self.assertIn(left_bottom, active_base)

    def test_right_bottom_mapping_is_unchanged(self) -> None:
        # Given: the Air60 base layer used for every host OS.
        source = LAYOUT.read_text(encoding="utf-8")
        active_base = source.split("[_MAC_BL]", 1)[1].split("[_WIN_BL]", 1)[0]

        # When: the right side of the bottom row is inspected.
        right_bottom = "KC_LGUI, FN_TAP, KC_LEFT, KC_DOWN, KC_RGHT"

        # Then: the working right-side mapping remains intact.
        self.assertIn(right_bottom, active_base)

    def test_fn_tap_is_only_on_the_active_base_layer(self) -> None:
        # Given: the Air60 default keymap.
        source = LAYOUT.read_text(encoding="utf-8")

        # When: the always-active layer zero and inactive layer one are isolated.
        active_base = source.split("[_MAC_BL]", 1)[1].split("[_WIN_BL]", 1)[0]
        inactive_base = source.split("[_WIN_BL]", 1)[1].split("[_MAC_FL]", 1)[0]

        # Then: only the base layer actually read by matrix.c receives Fn tap.
        self.assertIn("FN_TAP", active_base)
        self.assertIn("MO(_WIN_FL)", inactive_base)
        self.assertEqual(source.count("FN_TAP"), 1)

    def test_fn_tap_does_not_enter_core_input_paths(self) -> None:
        # Given: SMK's global matrix, report, and USB paths.
        core_paths = (
            ROOT / "src" / "smk" / "matrix.c",
            ROOT / "src" / "smk" / "report.c",
            ROOT / "src" / "platform" / "sh68f90a" / "usb.c",
        )

        # When: their source is inspected.
        sources = tuple(path.read_text(encoding="utf-8") for path in core_paths)

        # Then: none of the global paths know about the Air60 Fn tap keycode.
        for source in sources:
            self.assertNotIn("FN_TAP", source)
            self.assertNotIn("active_keycodes", source)

    def test_other_keys_only_mark_an_active_fn_chord(self) -> None:
        # Given: the Air60-specific key event handler.
        source = KEYBOARD.read_text(encoding="utf-8")

        # When: its Fn tap state boundary is inspected.
        interruption_guard = "fn_pressed && key_pressed && keycode != FN_TAP"

        # Then: other keys are observed only while Fn is active.
        self.assertIn(interruption_guard, source)
        self.assertIn("case FN_TAP:", source)
        self.assertNotIn("kb_get_base_layer", source)
        self.assertNotIn("matrix_has_multiple_keys_pressed", source)


if __name__ == "__main__":
    unittest.main()
