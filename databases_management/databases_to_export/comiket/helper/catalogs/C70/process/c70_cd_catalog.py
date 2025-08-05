from pathlib import Path
import json
from db_structs import Circle, Source, Medium, ReliabilityTypes, OriginTypes
import re

DECODE_INDEX: dict[bytes, bytes] = { # Map bytes that are not decoded properly to their correct characters
    # b"\x88h": "・".encode('cp932'),
}
GENRES: dict[int, str] = {
    100: "創作(少年)",
    101: "創作(少女)",
    102: "創作(JUNE)",
    105: "学漫",
    106: "評論・情報",
    200: "男性向",
    204: "同人ソフト",
    207: "Leaf & Key",
    208: "ギャルゲー",
    # 209: "ギャルグー(CS)",
    210: "TYPE-MOON",
    302: "ゲーム(格闘)",
    305: "ケーム(電源不要)",
    306: "オンラインケーム",
    308: "ケーム(その他)",
    317: "ケーム(RPG)",
    318: "スクウェア・エニックス(RPG)",
    319: "ケーム(恋愛)",
    400: "FC(ジャンプその他)",
    401: "FC(ジャンプ球技)",
    # 410: "SLAM DUNK",
    # 411: "冨樫義博",
    # 412: "封神演義",
    413: "ワンピース",
    414: "NARUTO",
    415: "テニスの王子様",
    # 501: "アニメ(少女)",
    505: "アニメ(その他)",
    506: "アニメ(サンライズ)",
    517: "ガンダム",
    600: "歴史",
    603: "創作(文芸・小説)",
    # 607: "SF・ファンタジー",
    608: "特撮・SF・ファンタジー",
    609: "鉄道・旅行・メカミリ",
    701: "音楽(洋楽・邦楽)",
    702: "音楽(男性アイドル)",
    703: "TV・映画・芸能",
    # 704: "特撮",
    705: "スポーツ",
    800: "FC(小説)",
    810: "FC(少年)",
    811: "FC(少女)",
    812: "FC(青年)",
    # 813: "FC(コロコロ)",
    814: "FC(ガンガン)",
    820: "鋼の錬金術師",
    900: "その他",
    999: "ノンジャンル",
    802: "UNKNOWN" # see '天嘉'
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

def combine_dakuten_handa_kana(text: str) -> str:
    couples = {
        'ｶﾞ': 'ガ', 'ｷﾞ': 'ギ', 'ｸﾞ': 'グ', 'ｹﾞ': 'ゲ', 'ｺﾞ': 'ゴ',
        'ｻﾞ': 'ザ', 'ｼﾞ': 'ジ', 'ｽﾞ': 'ズ', 'ｾﾞ': 'ゼ', 'ｿﾞ': 'ゾ',
        'ﾀﾞ': 'ダ', 'ﾁﾞ': 'ヂ', 'ﾂﾞ': 'ヅ', 'ﾃﾞ': 'デ', 'ﾄﾞ': 'ド',
        'ﾊﾞ': 'バ', 'ﾋﾞ': 'ビ', 'ﾌﾞ': 'ブ', 'ﾍﾞ': 'ベ', 'ﾎﾞ': 'ボ',
        'ﾊﾟ': 'パ', 'ﾋﾟ': 'ピ', 'ﾌﾟ': 'プ', 'ﾍﾟ': 'ペ', 'ﾎﾟ': 'ポ',
        'ｱﾞ': 'ア゙', 'ｲﾞ': 'イ゙', 'ｳﾞ': 'ヴ', 'ｴﾞ': 'エ゙', 'ｵﾞ': 'オ゙'
    }
    for half, full in couples.items():
        text = text.replace(half, full)
    return text

HALF_WIDTH_TO_FULL = {
    'ｱ': 'ア', 'ｲ': 'イ', 'ｳ': 'ウ', 'ｴ': 'エ', 'ｵ': 'オ',
    'ｶ': 'カ', 'ｷ': 'キ', 'ｸ': 'ク', 'ｹ': 'ケ', 'ｺ': 'コ',
    'ｻ': 'サ', 'ｼ': 'シ', 'ｽ': 'ス', 'ｾ': 'セ', 'ｿ': 'ソ',
    'ﾀ': 'タ', 'ﾁ': 'チ', 'ﾂ': 'ツ', 'ﾃ': 'テ', 'ﾄ': 'ト',
    'ﾅ': 'ナ', 'ﾆ': 'ニ', 'ﾇ': 'ヌ', 'ﾈ': 'ネ', 'ﾉ': 'ノ',
    'ﾊ': 'ハ', 'ﾋ': 'ヒ', 'ﾌ': 'フ', 'ﾍ': 'ヘ', 'ﾎ': 'ホ',
    'ﾏ': 'マ', 'ﾐ': 'ミ', 'ﾑ': 'ム', 'ﾒ': 'メ', 'ﾓ': 'モ',
    'ﾔ': 'ヤ', 'ﾕ': 'ユ', 'ﾖ': 'ヨ',
    'ﾗ': 'ラ', 'ﾘ': 'リ', 'ﾙ': 'ル', 'ﾚ': 'レ', 'ﾛ': 'ロ',
    'ﾜ': 'ワ', 'ｦ': 'ヲ', 'ﾝ': 'ン',
    'ｧ': 'ァ', 'ｨ': 'ィ', 'ｩ': 'ゥ', 'ｪ': 'ェ', 'ｫ': 'ォ',
    'ｬ': 'ャ', 'ｭ': 'ュ', 'ｮ': 'ョ', 'ｯ': 'ッ',
    'ｰ': 'ー' #, '･': '・', '｡': '。', '｢': '「', '｣': '」',
}

def cleanup(text: str) -> str:
    """Cleanup, like convert Japanese full-width alphanumerics to ASCII equivalents."""
    tn = ''.join(JAP_TO_ASCII.get(c, c) for c in text)
    tn = combine_dakuten_handa_kana(tn)
    tn = ''.join(HALF_WIDTH_TO_FULL.get(c, c) for c in tn)
    tn = re.sub(r'\s+', ' ', tn)
    return tn

if __name__ == '__main__':
    NUM = 70
    circles_raw = []
    raw_entries: list[list[str]] = []

    # =====================================
    # Other circles
    # =====================================

    # ===== Load csv like data ======
    with open(Path(__file__).parent / 'CDATA' / 'C70ROM1.txt', 'rb') as file:
        lines = file.readlines()
    with open(Path(__file__).parent / 'CDATA' / 'C70ROM2.txt', 'rb') as file:
        lines.extend(file.readlines())
    with open(Path(__file__).parent / 'CDATA' / 'C70ROM3.txt', 'rb') as file:
        lines.extend(file.readlines())

    # ===== Decode and process lines ======
    for line in lines:
        try:
            linestr = replace_with_index(line).decode('cp932', errors='strict')
            cols = [ col.strip() for col in linestr.split('\t')]
            cols += [''] * (16 - len(cols))  # Ensure there are 13 columns
            raw_entries.append(cols)
            # print(f'{len(cols)=}: {cols}')
            if len(cols) != 16:
                raise ValueError(f'Invalid number of columns: {len(cols)} in line: {linestr}')
            
        except UnicodeDecodeError as e: # Helper to detect decoding issues
            linestr = line.decode('cp932', errors='backslashreplace')
            cols = linestr.split('\t')
            print(linestr)
            print(line)
            raise e
        
    for raw_entry in raw_entries:
        page = cleanup(raw_entry[2])
        index_in_page = cleanup(raw_entry[3])
        event_day = cleanup(raw_entry[4])
        hall = cleanup(raw_entry[5])
        block = cleanup(raw_entry[6])
        booth_numder = cleanup(raw_entry[7])
        name = cleanup(raw_entry[9])
        name_kana = cleanup(raw_entry[10])
        pen_name = cleanup(raw_entry[11])
        product_name = cleanup(raw_entry[12])
        url = cleanup(raw_entry[13])
        mail = cleanup(raw_entry[14])
        description = cleanup(raw_entry[15])

        day_date = DATE_INDEX[event_day]
        if name == "＊＊ 準備会事故用スペース ＊＊": # specific case
            genre = "NONE"
        else:
            try:
                genre = cleanup(GENRES[int(raw_entry[8])])
            except KeyError:
                print(f'ERR (p. {page}-{index_in_page}, i={raw_entry[8]}, {name}): {raw_entry=})')
                exit()
        
        circles_raw.append(Circle(
            aliases=[name],
            pen_names=[pen_name],
            links=[url],
            position=f"{event_day} ({day_date}), {hall}, {block}, {booth_numder}",
            comments='\n'.join(
                ([f'Genre: {genre}'] if genre else []) +
                ([f'Name (kana): {name_kana}'] if name_kana else []) + 
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
    with open(Path(__file__).parent / 'CDATA' / 'C70ROM0.txt', 'rb') as file:
        lines = file.readlines()

    # ===== Decode and process lines ======
    for i, line in enumerate(lines):
        try:
            linestr = replace_with_index(line).decode('cp932', errors='strict')
            cols = [ col.strip() for col in linestr.split('\t')]
            raw_entries.append(cols)
            # print(f'{len(cols)=}: {cols}')
            if len(cols) != 14:
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
        except KeyError:
            print(f"Unknown genre code at line {i} (key={raw_entry[6]}, {raw_entry[7]}): {raw_entry=}")
            exit()
        name = cleanup(raw_entry[7])
        name_kana = cleanup(raw_entry[8])
        pen_name = cleanup(raw_entry[9])
        product_name = cleanup(raw_entry[10])
        url = cleanup(raw_entry[11])
        mail = cleanup(raw_entry[12])
        description = cleanup(raw_entry[13])
    
        circles_raw.append(Circle(
            aliases=[name],
            pen_names=[pen_name],
            position="抽選漏れサークル (Lost lottery)",
            links=[url],
            comments='\n'.join(
                ([f'Genre: {genre}'] if genre else []) +
                ([f'Name (kana): {name_kana}'] if name_kana else []) + 
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