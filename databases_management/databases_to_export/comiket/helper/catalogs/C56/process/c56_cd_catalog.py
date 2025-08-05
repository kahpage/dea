from pathlib import Path
import json
from db_structs import Circle, Source, Medium, ReliabilityTypes, OriginTypes
import re

DECODE_INDEX: dict[bytes, bytes] = { # Map bytes that are not decoded properly to their correct characters
    b'\x98x': '・'.encode('cp932'),
    b'\x88c': '・'.encode('cp932'),
    b'\x88[': '・'.encode('cp932'),
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

GENRES: dict[int, str] = {
    1: "創作(少年)①",
    2: "創作(少年)②",
    3: "創作(少女)①",
    4: "創作(少女)②",
    5: "創作(JUNE)",
    6: "学漫",
    7: "評論・情報・その他",
    8: "FC(少女)①",
    9: "FC(少女)②",
    10: "男性向(創作・アニメグーム)①",
    11: "男性向(創作・アニメグーム)②",
    12: "男性向(創作・アニメグーム)③",
    13: "男性向(創作・アニメグーム)④",
    14: "男性向(創作・アニメグーム)⑤",
    15: "男性向(創作・アニメグーム)⑥",
    16: "男性向(創作・アニメグーム)⑦",
    17: "男性向(創作・アニメグーム)⑧",
    18: "男性向(創作・アニメグーム)⑨",
    19: "男性向(創作・アニメグーム)⑩",
    20: 'アニメ(少女)①',
    21: 'アニメ(少女)②',
    22: 'アニメ(その他)①',
    23: 'アニメ(その他)②',
    24: 'アニメ(その他)③',
    25: 'アニメ(その他)④',
    26: 'ギャルゲー①',
    27: 'ギャルゲー②',
    28: 'ケーム(格聞)①',
    29: 'ケーム(格聞)②',
    30: 'SNK(格聞)①',
    31: 'SNK(格聞)②',
    32: '同人ソフト①',
    33: '同人ソフト②',
    34: 'ケーム(電源不要)①',
    35: 'ケーム(電源不要)②',
    36: 'ケーム(その他)①',
    37: 'ケーム(その他)②',
    38: 'ケーム(RPG)①',
    39: 'ケーム(RPG)②',
    40: 'スクウェア(RPG)①',
    41: 'スクウェア(RPG)②',
    42: 'グーム(育成)①',
    43: 'グーム(育成)②',
    44: 'C翼①',
    45: 'C翼②',
    46: 'C翼③',
    47: 'トルーパー',
    48: '幽遊白書①',
    49: '幽遊白書②',
    50: 'SLAM DUNK ①',
    51: 'SLAM DUNK ②',
    52: 'SLAM DUNK ③',
    53: 'アニメ(少年)①',
    54: 'アニメ(少年)②',
    55: 'アニメ(少年)③',
    56: 'アニメ(少年)④',
    57: 'アニメ(少年)⑤',
    58: 'アニメ(少年)⑥',
    59: 'アニメ(少年)⑦',
    60: 'アニメ(少年)⑧',
    61: 'アニメ(少年)⑨',
    62: 'ガンダム①',
    63: 'ガンダム②',
    64: 'ガンダム③',
    65: '歷史①',
    66: '歴史②',
    67: '創作(文芸)①',
    68: '創作(文芸)②',
    69: '創作(文芸)③',
    70: 'SF・ファンタジー①',
    71: 'SF・ファンタジー②',
    72: '特撮①',
    73: '特撮②',
    74: 'メカ・ミリタリー',
    75: '音楽(洋楽・邦楽)',
    76: '音楽(男性アイドル)',
    77: 'TV・映画・芸能①',
    78: 'TV・映画・芸能②',
    79: 'スポーツ',
    80: 'FC(小説)①',
    81: 'FC(小説)②',
    82: 'FC(小説)③',
    83: '炎の蜜気楼①',
    84: '炎の蜜気楼②',
    85: 'FC(少年)①',
    86: 'FC(少年)②',
    87: 'FC(ジャンプ)①',
    88: 'FC(ジャンプ)②',
    89: 'FC(ジャンプ)③',
    90: '不明(90)',
}

DATE_INDEX = {
    "金": "08.13",
    "土": "08.14",
    "日": "08.15",
}

if __name__ == '__main__':
    circles_raw = []
    
    # =====================================
    # Other circles
    # =====================================
    raw_entries: list[list[str]] = []

    # ===== Load csv like data ======
    with open(Path(__file__).parent / 'cdata' / 'C56rom1.txt', 'rb') as file:
        lines = file.readlines()
    with open(Path(__file__).parent / 'cdata' / 'C56rom2.txt', 'rb') as file:
        lines.extend(file.readlines())
    with open(Path(__file__).parent / 'cdata' / 'C56rom3.txt', 'rb') as file:
        lines.extend(file.readlines())

    # ===== Decode and process lines ======
    for line in lines:
        try:
            linestr = replace_with_index(line).decode('cp932', errors='strict')
            cols = [ col.strip() for col in linestr.split('\t')]
            cols += [''] * (13 - len(cols))  # Ensure there are 13 columns
            raw_entries.append(cols)
            # print(f'{len(cols)=}: {cols}')
            if len(cols) != 13:
                raise ValueError(f'Invalid number of columns: {len(cols)} in line: {linestr}')
            
        except UnicodeDecodeError as e: # Helper to detect decoding issues
            linestr = line.decode('cp932', errors='backslashreplace')
            cols = linestr.split('\t')
            print(linestr)
            print(line)
            raise e
        
    for raw_entry in raw_entries:
        try:
            page = cleanup(raw_entry[0])
            index_in_page = cleanup(raw_entry[1])
            event_day = cleanup(raw_entry[2])
            hall = cleanup(raw_entry[3])
            block = cleanup(raw_entry[4])
            booth_numder = cleanup(raw_entry[5])
            genre = cleanup(GENRES[int(raw_entry[6])])
            name = cleanup(raw_entry[7])
            pen_name = cleanup(raw_entry[8])
            product_name = cleanup(raw_entry[9])
            url = cleanup(raw_entry[10])
            mail = cleanup(raw_entry[11])
            description = cleanup(raw_entry[12])

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
                Medium(f"{page}.jpg", # TODO: to host
                       [Source("C56 catalog CD.", (ReliabilityTypes.Reliable, OriginTypes.Official))]
                       , comments=f"{index_in_page=}"),
            ]
        ).get_json())

    # =====================================
    # 抽選漏れサークル (circles that were not selected in the lottery)
    # =====================================
    raw_entries: list[list[str]] = []

    # ===== Load csv like data ======
    with open(Path(__file__).parent / 'cdata' / 'C56rom0.txt', 'rb') as file:
        lines = file.readlines()

    # ===== Decode and process lines ======
    for line in lines:
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
            raise e
        
    for raw_entry in raw_entries:
        genre = cleanup(GENRES[int(raw_entry[6])])
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
    with open(Path(__file__).parent / 'c56_circles.json', 'w+', encoding='utf-8') as f:
        json.dump(circles_raw, f, indent=4, ensure_ascii=False)

    print(f"{len(circles_raw)} circles data saved to c56_circles.json")