import pcbnew

board = pcbnew.GetBoard()

threshold = 0.9  # mm
threshold_nm = pcbnew.FromMM(threshold)

error_list = []
fix_count = 0

for footprint in board.GetFootprints():
    for pad in footprint.Pads():

        # ✅ chỉ pad có drill (KiCad 9 chuẩn)
        if pad.GetAttribute() not in [pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH]:
            continue

        drill = pad.GetDrillSize()
        pad_size = pad.GetSize()

        # ⚠️ lỗi: drill > pad
        if drill.x > pad_size.x or drill.y > pad_size.y:
            error_list.append((footprint.GetReference(), pad.GetPadName()))
            continue

        # 🔧 fix nếu nhỏ hơn threshold
        if drill.x < threshold_nm or drill.y < threshold_nm:
            new_drill = pcbnew.VECTOR2I(
                max(drill.x, threshold_nm),
                max(drill.y, threshold_nm)
            )
            pad.SetDrillSize(new_drill)
            fix_count += 1

# report
print(f"Fixed {fix_count} pads")

if error_list:
    print("ERROR pads (drill > pad):")
    for ref, name in error_list:
        print(f"{ref} - pad {name}")
else:
    print("No errors")

pcbnew.Refresh()