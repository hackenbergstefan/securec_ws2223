import os

cwpath = None
firmwarepath = None
for cwpath in list(
    os.path.join(os.path.dirname(__file__), p)
    for p in (
        "../..",
        "../../chipwhisperer",
        "../../../chipwhisperer",
    )
) + [r'C:\cw\cw\home\portable\chipwhisperer']:
    firmwarepath = os.path.abspath(os.path.join(cwpath, "hardware/victims/firmware"))
    if os.path.exists(firmwarepath):
        break

if not os.path.exists(firmwarepath):
    raise ValueError("FIRMWAREPATH not found")

print_output = True
"""Print output instead of returning. Looks better in Notebook."""

debug = False
"""Print debug output."""

scope = None
"""ChipWhisperer scope."""

target = None
"""ChipWhisperer target."""
