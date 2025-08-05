from pathlib import Path
import json
from db_structs import Circle, Source, Medium, ReliabilityTypes, OriginTypes
import re

DECODE_INDEX: dict[bytes, bytes] = { # Map bytes that are not decoded properly to their correct characters
    b'\x88W': '・'.encode('cp932'),
    b'\x86': '・'.encode('cp932'),
    b'\x81\xb4': '・'.encode('cp932'),
}
GENRES: dict[int, str] = {
    10: "創作(少年)",
    11: "創作(少女)",
    12: "創作(JUNE)",
    15: "学漫",
    16: "評論・情報",
    # 17: "ミスティ",
    20: "創作・アニメ・ケーム(男性向)",
    21: "アニメ(少女)",
    28: "ギャルゲー(PC)",
    29: "ギャルゲー(CS)",
    # 30: "",
    32: "ゲーム(格闘)",
    33: "SNK(格闘)",
    34: "同人ソフト",
    35: "ケーム(電源不要)",
    38: "ケーム(その他)",
    47: "ケーム(RPG)",
    48: "スクウェア&アトラス(RPG)",
    49: 'グーム(育成)',
    # 50: "C翼",
    # 51: "トルーパー",
    53: "SLAM DUNK",
    54: "アニメ(少年)",
    55: "アニメ(その他)",
    57: "ガンダム",
    60: "歴史",
    63: "創作(文芸・小説)",
    67: "SF・ファンタジー",
    68: "特撮",
    69: "メカ・ミリタリー",
    71: "音楽(洋楽・邦楽)",
    72: "音楽(男性アイドル)",
    73: "TV・映画・芸能",
    75: "スポーツ",
    80: "FC(小説)",
    # 81: "炎の蜜気楼",
    82: "FC(少女)",
    85: "FC(青年)",
    86: "FC(少年)",
    87: "FC(ジャンプ)",
    88: "冨樫義博", # (category corrected in C59 catalog CD)
    89: "封神演義",
    90: "その他",
    99: '××××',
}

DATE_INDEX = {
    "金": "08.11",
    "土": "08.12",
    "日": "08.13",
}

def replace_with_index(lineraw: bytes) -> bytes:
    """Replace characters in a string based on DECODE_INDEX."""
    for key, value in DECODE_INDEX.items():
        lineraw = lineraw.replace(key, value)
    return lineraw

JAP_TO_ASCII = {  # replace Japanese full-width letters and numbers with ASCII equivalents
    "ａ": "a", "ｂ": "b", "ｃ": "c", "ｄ": "d", "ｅ": "e", "ｆ": "f", "ｇ": "g", "ｈ": "h", "ｉ": "i", "ｊ": "j",
    "ｋ": "k", "ｌ": "l", "ｍ": "m", "ｎ": "n", "ｏ": "o", "ｐ": "p", "ｑ": "q", "ｒ": "r", "ｓ": "s", "ｔ": "t",
    "ｕ": "u", "ｖ": "v", "ｗ": "w", "ｘ": "x", "ｙ": "y", "ｚ": "z",
    "Ａ": "A", "Ｂ": "B", "Ｃ": "C", "Ｄ": "D", "Ｅ": "E", "Ｆ": "F", "Ｇ": "G", "Ｈ": "H", "Ｉ": "I", "Ｊ": "J",
    "Ｋ": "K", "Ｌ": "L", "Ｍ": "M", "Ｎ": "N", "Ｏ": "O", "Ｐ": "P", "Ｑ": "Q", "Ｒ": "R", "Ｓ": "S", "Ｔ": "T",
    "Ｕ": "U", "Ｖ": "V", "Ｗ": "W", "Ｘ": "X", "Ｙ": "Y", "Ｚ": "Z",
    "０": "0", "１": "1", "２": "2", "３": "3", "４": "4", "５": "5", "６": "6", "７": "7", "８": "8", "９": "9",
}

def cleanup(text: str) -> str:
    """Cleanup, like convert Japanese full-width alphanumerics to ASCII equivalents."""
    tn = ''.join(JAP_TO_ASCII.get(c, c) for c in text)
    tn = re.sub(r'\s+', ' ', tn)
    return tn


if __name__ == '__main__':
    NUM = 58
    circles_raw = []
    
    # =====================================
    # Other circles
    # =====================================
    raw_entries: list[list[str]] = []

    # ===== Load csv like data ======
    with open(Path(__file__).parent / 'CDATA' / 'C58ROM1.txt', 'rb') as file:
        lines = file.readlines()
    with open(Path(__file__).parent / 'CDATA' / 'C58ROM2.txt', 'rb') as file:
        lines.extend(file.readlines())
    with open(Path(__file__).parent / 'CDATA' / 'C58ROM3.txt', 'rb') as file:
        lines.extend(file.readlines())

    # ===== Decode and process lines ======
    for line in lines:
        try:
            linestr = replace_with_index(line).decode('cp932', errors='strict')
            cols = [ col.strip() for col in linestr.split('\t')]
            cols += [''] * (15 - len(cols))  # Ensure there are 13 columns
            raw_entries.append(cols)
            # print(f'{len(cols)=}: {cols}')
            if len(cols) != 15:
                raise ValueError(f'Invalid number of columns: {len(cols)} in line: {linestr}')
            
        except UnicodeDecodeError as e: # Helper to detect decoding issues
            linestr = line.decode('cp932', errors='backslashreplace')
            cols = linestr.split('\t')
            print(linestr)
            print(line)
            raise e
        
    for raw_entry in raw_entries:
        try:
            page = cleanup(raw_entry[2])
            index_in_page = cleanup(raw_entry[3])
            event_day = cleanup(raw_entry[4])
            hall = cleanup(raw_entry[5])
            block = cleanup(raw_entry[6])
            booth_numder = cleanup(raw_entry[7])
            genre = cleanup(GENRES[int(raw_entry[8])])
            name = cleanup(raw_entry[9])
            pen_name = cleanup(raw_entry[10])
            product_name = cleanup(raw_entry[11])
            url = cleanup(raw_entry[12])
            mail = cleanup(raw_entry[13])
            description = cleanup(raw_entry[14])

            day_date = DATE_INDEX[event_day]
        except Exception as e:
            print(f'{raw_entry=}')
            raise e
        
        circles_raw.append(Circle(
            aliases=[name],
            pen_names=[pen_name],
            links=[url],
            position=f"{event_day} ({day_date}), {hall}, {block}, {booth_numder}",
            comments='\n'.join(
                ([f'Genre: {genre}'] if genre else []) +
                ([f'Product: {product_name}'] if product_name else []) +
                ([f'email: {mail}'] if mail else []) +
                ([description] if description else [])
            ),
            media=[
                Medium(f"{int(page):04d}.jpg", # TODO: to host
                       [Source(f"C{NUM} catalog CD.", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                       , comments=f"{index_in_page=}"),
            ]
        ).get_json())

    # =====================================
    # 抽選漏れサークル (circles that were not selected in the lottery)
    # =====================================
    raw_entries: list[list[str]] = []

    # ===== Load csv like data ======
    with open(Path(__file__).parent / 'CDATA' / 'C58ROM0.txt', 'rb') as file:
        lines = file.readlines()

    # ===== Decode and process lines ======
    for i, line in enumerate(lines):
        try:
            linestr = replace_with_index(line).decode('cp932', errors='strict')
            cols = [ col.strip() for col in linestr.split('\t')]
            raw_entries.append(cols)
            # print(f'{len(cols)=}: {cols}')
            if len(cols) != 13:
                raise ValueError(f'Invalid number of columns: {len(cols)} in line: {linestr}')
            
        except UnicodeDecodeError as e: # Helper to detect decoding issues
            linestr = line.decode('cp932', errors='backslashreplace')
            cols = linestr.split('\t')
            print(linestr)
            print(line)
            print(f'At line {i}')
            raise e
        
    for i, raw_entry in enumerate(raw_entries):
        try:
            genre = GENRES[int(raw_entry[6])]
        except KeyError as e:
            print(f"Unknown genre code at line {i} (key={raw_entry[6]}): {raw_entry=}")
            raise e
        name = cleanup(raw_entry[7])
        pen_name = cleanup(raw_entry[8])
        product_name = cleanup(raw_entry[9])
        url = cleanup(raw_entry[10])
        mail = cleanup(raw_entry[11])
        description = cleanup(raw_entry[12])
    
        circles_raw.append(Circle(
            aliases=[name],
            pen_names=[pen_name],
            position="抽選漏れサークル (Lost lottery)",
            links=[url],
            comments='\n'.join(
                ([f'Genre: {genre}'] if genre else []) +
                ([f'Product: {product_name}'] if product_name else []) + 
                ([f'email: {mail}'] if mail else []) +
                ([description] if description else [])
                ),
        ).get_json())

    # =====================================
    # Dump circles to JSON
    # =====================================
    with open(Path(__file__).parent / f'c{NUM}_circles.json', 'w+', encoding='utf-8') as f:
        json.dump(circles_raw, f, indent=4, ensure_ascii=False)

    print(f"{len(circles_raw)} circles data saved to c{NUM}_circles.json")