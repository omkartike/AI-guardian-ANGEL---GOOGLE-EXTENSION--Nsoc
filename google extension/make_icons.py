"""
Generate TrustLayer AI PNG icons for Chrome extension.
Uses only Python standard library (struct + zlib).
"""
import struct, zlib, os

def make_png(size, color_bg=(0,0,0), color_fg=(255,255,255)):
    """
    Creates a minimal valid PNG: black bg, white 'T' shape.
    Returns raw PNG bytes.
    """
    # Build raw RGBA pixel rows
    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            # Draw a 'T' shape in the center
            cx = size // 2
            # Stem: vertical bar
            stem_x1 = cx - max(1, size // 10)
            stem_x2 = cx + max(1, size // 10)
            stem_y1 = size // 3
            stem_y2 = size - size // 4

            # Cross bar: horizontal bar at top
            bar_x1 = size // 5
            bar_x2 = size - size // 5
            bar_y1 = size // 5
            bar_y2 = size // 3

            in_stem = (stem_x1 <= x <= stem_x2 and stem_y1 <= y <= stem_y2)
            in_bar  = (bar_x1  <= x <= bar_x2  and bar_y1  <= y <= bar_y2)

            if in_stem or in_bar:
                row += list(color_fg) + [255]
            else:
                row += list(color_bg) + [255]
        rows.append(bytes([0] + row))  # filter byte = 0 (None)

    raw = b''.join(rows)
    compressed = zlib.compress(raw, 9)

    def chunk(name, data):
        c = struct.pack('>I', len(data)) + name + data
        return c + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)

    png  = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    # color type 2 = RGB... let's use RGBA (color type 6)
    # Redo IHDR with color type 6 (RGBA)
    png  = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png

out_dir = r"D:\HARSH\New folder\google extension\icons"
os.makedirs(out_dir, exist_ok=True)

for sz in [16, 48, 128]:
    data = make_png(sz)
    path = os.path.join(out_dir, f"icon{sz}.png")
    with open(path, 'wb') as f:
        f.write(data)
    print(f"Created {path} ({len(data)} bytes)")

print("All icons created successfully!")
