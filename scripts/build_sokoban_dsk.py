from __future__ import annotations

import argparse
from pathlib import Path


BYTES_PER_SECTOR = 512
DIR_ENTRY_SIZE = 32


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a bootable MSX DSK image containing AUTOEXEC.BAS and SOKOBAN.BAS."
    )
    parser.add_argument(
        "--template",
        default="disk/basic-sokoban.DSK",
        help="Bootable template DSK to copy system area from.",
    )
    parser.add_argument(
        "--autoexec",
        default="fdd/autoexec.bas",
        help="Path to AUTOEXEC.BAS source file.",
    )
    parser.add_argument(
        "--sokoban",
        default="sokoban.bas",
        help="Path to SOKOBAN.BAS source file.",
    )
    parser.add_argument(
        "--output",
        default="disk/sokoban.dsk",
        help="Output DSK path.",
    )
    return parser.parse_args()


def to_crlf_ascii(data: bytes) -> bytes:
    text = data.decode("ascii")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.replace("\n", "\r\n").encode("ascii")


def format_83(name: str) -> bytes:
    upper = Path(name).name.upper()
    if "." in upper:
        stem, ext = upper.rsplit(".", 1)
    else:
        stem, ext = upper, ""
    if len(stem) > 8 or len(ext) > 3:
        raise ValueError(f"File name is not 8.3 compatible: {name}")
    return stem.ljust(8).encode("ascii") + ext.ljust(3).encode("ascii")


def set_fat12_entry(fat: bytearray, cluster: int, value: int) -> None:
    offset = (cluster * 3) // 2
    value &= 0xFFF
    if cluster & 1:
        fat[offset] = (fat[offset] & 0x0F) | ((value << 4) & 0xF0)
        fat[offset + 1] = (value >> 4) & 0xFF
    else:
        fat[offset] = value & 0xFF
        fat[offset + 1] = (fat[offset + 1] & 0xF0) | ((value >> 8) & 0x0F)


def build_root_entry(filename: str, start_cluster: int, size: int) -> bytes:
    entry = bytearray(32)
    entry[:11] = format_83(filename)
    entry[11] = 0x00
    entry[26:28] = start_cluster.to_bytes(2, "little")
    entry[28:32] = size.to_bytes(4, "little")
    return bytes(entry)


def main() -> None:
    args = parse_args()
    root = Path.cwd()
    template_path = (root / args.template).resolve()
    autoexec_path = (root / args.autoexec).resolve()
    sokoban_path = (root / args.sokoban).resolve()
    output_path = (root / args.output).resolve()

    template = bytearray(template_path.read_bytes())
    autoexec_data = to_crlf_ascii(autoexec_path.read_bytes())
    sokoban_data = to_crlf_ascii(sokoban_path.read_bytes())

    boot = template[:BYTES_PER_SECTOR]
    bytes_per_sector = int.from_bytes(boot[11:13], "little")
    sectors_per_cluster = boot[13]
    reserved_sectors = int.from_bytes(boot[14:16], "little")
    fat_count = boot[16]
    root_entries = int.from_bytes(boot[17:19], "little")
    sectors_per_fat = int.from_bytes(boot[22:24], "little")
    total_sectors = int.from_bytes(boot[19:21], "little")
    total_size = total_sectors * bytes_per_sector

    if bytes_per_sector != BYTES_PER_SECTOR:
        raise ValueError(f"Unsupported bytes/sector: {bytes_per_sector}")

    root_dir_sectors = (root_entries * DIR_ENTRY_SIZE + bytes_per_sector - 1) // bytes_per_sector
    fat_start = reserved_sectors * bytes_per_sector
    fat_size = sectors_per_fat * bytes_per_sector
    root_start = fat_start + fat_count * fat_size
    root_size = root_dir_sectors * bytes_per_sector
    data_start = root_start + root_size
    cluster_size = bytes_per_sector * sectors_per_cluster

    result = bytearray(total_size)
    result[:data_start] = template[:data_start]

    fat = bytearray(fat_size)
    fat[0] = boot[21]
    fat[1] = 0xFF
    fat[2] = 0xFF

    files = [
        ("AUTOEXEC.BAS", autoexec_data),
        ("SOKOBAN.BAS", sokoban_data),
    ]

    current_cluster = 2
    root_entries_data = bytearray(root_size)

    for index, (filename, content) in enumerate(files):
        clusters_needed = max(1, (len(content) + cluster_size - 1) // cluster_size)
        start_cluster = current_cluster

        for i in range(clusters_needed):
            cluster = start_cluster + i
            next_value = 0xFFF if i == clusters_needed - 1 else cluster + 1
            set_fat12_entry(fat, cluster, next_value)

            chunk = content[i * cluster_size : (i + 1) * cluster_size]
            data_offset = data_start + (cluster - 2) * cluster_size
            result[data_offset : data_offset + len(chunk)] = chunk

        entry_offset = index * DIR_ENTRY_SIZE
        root_entries_data[entry_offset : entry_offset + DIR_ENTRY_SIZE] = build_root_entry(
            filename, start_cluster, len(content)
        )
        current_cluster += clusters_needed

    for fat_index in range(fat_count):
        fat_offset = fat_start + fat_index * fat_size
        result[fat_offset : fat_offset + fat_size] = fat

    result[root_start : root_start + root_size] = root_entries_data

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(result)

    print(f"Wrote {output_path}")
    print(f"Included AUTOEXEC.BAS ({len(autoexec_data)} bytes)")
    print(f"Included SOKOBAN.BAS ({len(sokoban_data)} bytes)")


if __name__ == "__main__":
    main()
