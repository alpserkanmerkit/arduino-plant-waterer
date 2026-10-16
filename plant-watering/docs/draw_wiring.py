"""plant-watering ("Super Fulffy") wiring diagram (Tinkercad/Fritzing style), drawn with ../../tools/wiring_kit.py.

Run:  python draw_wiring.py   -> wiring.svg (+ wiring.pins.json) next to this file
PNG:  python ../../tools/render_png.py

Source of every pin: the owner's Tinkercad design "Super Fulffy" (phone screenshot, cropped copy in
tinkercad-super-fulffy.png). Read from it:
  Uno 5V  -> breadboard + rail (red wire)        Uno GND -> breadboard − rail (black wire)
  Uno A0  -> soil sensor, right pin (green)       + rail -> sensor left pin (yellow), − rail -> sensor middle pin (brown)
  Uno D9  -> servo connector, right pin (purple)  − rail -> servo left pin (grey), + rail -> servo middle pin (orange)
  D9 confidence: medium (the printed "9" is covered by the wire; it is the 9th hole of the 10-pin header).
  Sensor / servo pin labels are not legible in the screenshot: their roles follow the wires above
  (VCC-GND-SIG and GND-+5V-signal, the usual order for these parts).
Layout difference: Tinkercad uses only the bottom rails. Here the Uno feeds the top rails and two jumpers carry
power to the bottom rails, so that no wire crosses another. Electrically identical.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from wiring_kit import Sheet, BY, ROW, P, cx, hole, pin_xy  # noqa: E402

SERVO_SIG = 30                   # servo: brown -> top − (28), red -> top + (29), orange -> column 30 row a
SOIL_VCC_COL = 40                # sensor VCC lead lands in bottom + rail at column 40, GND at 41


def main():
    s = Sheet("plant-watering (\"Super Fulffy\") — breadboard wiring",
              "Arduino Uno + soil moisture sensor + micro servo · dry soil → the servo turns to let water flow · "
              "pins from the owner's Tinkercad design",
              1500)
    s.breadboard()
    s.uno({"5V", "GND", "A0", "D9"})

    # 1-2 Uno power -> top rails (over the top of the Uno), 3-4 top rails -> bottom rails at the right end
    p = pin_xy("5V")
    s.uno_wire("5v", 1, "5V", [(40, p[1]), (40, 140), (cx(2), 140), hole(2, "T+")], (40, 330), "top + rail")
    p = pin_xy("GND")
    s.uno_wire("gnd", 2, "GND", [(26, p[1]), (26, 126), (cx(4) + 10, 126), (cx(4) + 10, ROW["T-"]), hole(4, "T-")],
               (26, 400), "top − rail")
    a, b = hole(61, "T+"), hole(61, "B+")
    s.wire("5v", 3, [a, (a[0] + 10, a[1]), (a[0] + 10, b[1]), b], (a[0] + 10, ROW["h"]))
    a, b = hole(63, "T-"), hole(63, "B-")
    s.wire("gnd", 4, [a, (a[0] + 12, a[1]), (a[0] + 12, b[1]), b], (a[0] + 12, BY + 210))

    # servo (leads drawn by s.servo) + signal from D9
    s.servo(SERVO_SIG, "Servo — turns to let the water flow", sub="Tinkercad micro servo", model="SERVO")
    s.badge(5, (cx(SERVO_SIG - 2) - 14, ROW["T+"] - 12), "gnd")
    s.badge(6, (cx(SERVO_SIG - 1) - 2, BY - 40), "5v")
    s.badge(7, (cx(SERVO_SIG) + 26, ROW["T-"] + 25), "sig")
    s.between_rows("sig", 8, "D9", SERVO_SIG, "d", (cx(18), pin_xy("D9")[1]), "servo signal", ["SERVO_PIN"])

    # soil moisture sensor in a pot below the board
    top = BY + 480
    xv = cx(SOIL_VCC_COL) + 10
    (pv, pg, ps) = s.soil_sensor(xv, top, "Soil moisture sensor")
    s.wire("5v", 9, [pv, (pv[0], ROW["B+"]), hole(SOIL_VCC_COL, "B+")], (pv[0] - 16, top - 22))
    s.wire("gnd", 10, [pg, (pg[0], ROW["B-"]), hole(SOIL_VCC_COL + 1, "B-")], (pg[0] + 2, top - 44))
    # A0 -> SIG: down the left side, under the pot, up the right side (crosses nothing)
    p = pin_xy("A0")
    y_low = top + 124 + 130 + 30
    x_r = pv[0] + P + 160
    s.uno_wire("soil", 11, "A0", [(52, p[1]), (52, y_low), (x_r, y_low), (x_r, top - 24), (ps[0], top - 24), ps],
               (52, 900), "soil sensor SIG", ["SOIL_PIN"])

    s.panel(BY + 820, [
        ("Power", [
            ("1", "Uno 5V → top + rail"), ("2", "Uno GND → top − rail"),
            ("3", "top + rail → bottom + rail (right end)"), ("4", "top − rail → bottom − rail (right end)")]),
        ("Servo (3-wire lead)", [
            ("5", "brown / black (GND) → top − rail"), ("6", "red (+5 V) → top + rail"),
            ("7", "orange / yellow (signal) → column 30"), ("8", "Uno D9 → column 30")]),
        ("Soil moisture sensor (female-male jumpers)", [
            ("9", "VCC → bottom + rail"), ("10", "GND → bottom − rail"), ("11", "SIG → Uno A0")]),
    ], [
        "Pins read from the Tinkercad screenshot of \"Super Fulffy\": sensor → A0, servo → D9 (medium confidence: the printed 9 is "
        "under the wire), power from the Uno 5 V / GND. Sensor and servo pin labels are not legible there;",
        "their roles follow the wires (+ rail, − rail, A0 / D9). Tinkercad uses only the bottom rails; here power goes through "
        "the top rails so no wire crosses another — electrically the same.",
        "Example sketch plant-watering.ino (2026; the original Tinkercad code was not kept): print the A0 value in dry and wet "
        "soil, then set DRY_BELOW. A micro servo runs from the Uno 5 V; a pump would need its own supply.",
    ], colw=600, one_group_per_column=True)
    s.save(HERE / "wiring.svg", ["../plant-watering.ino"],
           unknown=["D9 printed label covered by the wire (9th hole of the 10-pin header -> D9, medium confidence)",
                    "sensor pin labels not legible (roles from the wires: yellow from + rail, brown from − rail, green to A0)",
                    "servo connector labels not legible (roles from the wires: grey from − rail, orange from + rail, purple to D9)",
                    "original Tinkercad code, moisture threshold and the water mechanism (bottle / valve / pump) not known"])


if __name__ == "__main__":
    main()
