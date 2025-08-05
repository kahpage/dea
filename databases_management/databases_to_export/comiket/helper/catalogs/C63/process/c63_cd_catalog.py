from pathlib import Path
import json
from db_structs import Circle, Source, Medium, ReliabilityTypes, OriginTypes
import re

DECODE_INDEX: dict[bytes, bytes] = { # Map bytes that are not decoded properly to their correct characters
    # b"\x88h": "・".encode('cp932'),
}
GENRES: dict[int, str] = {
    100: "マンガ(創作(少年))",
    101: "マンガ(創作(少女) 動物・ドール・服飾・アクセサリー)",
    102: "マンガ(創作(JUNE) BoysLoveゲーム(オリジナル))",
    105: "マンガ(学漫)",
    106: "マンガ(評論・情報 批評・イベント・飲食物・郵便・医療・育児・体験談(アニメ・ゲーム・特撮に関しては、それぞれのジャンルで))",
    200: "男性向(創作・アニメ・ゲーム(男性向))",
    204: "ゲーム(同人ソフト 自主制作(ソフト&ハード)・CG集・MIDI・音楽CD・ネットワーク・インターネット・コンピュータ・デジタルマスコット(ポスペ等)・伺か。)",
    207: "ゲーム(Leaf & Key (Aquaplus含む)・ToHeart・こみパ・同棲・Moon・ONE・Kanon・AIR・ONE2)",
    208: "ゲーム(ギャルゲー(PC)(初出がパソコン) ソフ倫もの・脱衣麻雀・F&C・アリスソフト(アリスブルー除く)・新生タクティクス・elf・B-room・とらハ・月姫・君が望む永遠)",
    209: "ゲーム(ギャルゲー(CS)(初出が家庭用ゲーム機) 恋愛SLG・育成SLG・シスプリ・デジキャラット・ときメモ・センチ(ジャーニー含む)・サクラ大戦・久遠の絆・プリメ・卒業・ユナ・メモリーズオフ・HAPPYLESSON)",
    302: "ゲーム(ゲーム(格闘) vsシリーズ・スト2・KOF・侍魂・餓狼・ギルティギア・サイキックF・ VF・ヴァーチャロン・鉄拳・DoA・VG・あすか120%・POWER STONE)",
    305: "ゲーム(ゲーム(電源不要&オンライン) ボードゲーム・カードゲーム・テーブルトーク・PBM・MtG・Diablo・Baldur's Gate・UO・PSO・Ragnarok・LFTCG(オリジナルのスターター・エクスパンション含む))",
    308: "ゲーム(ゲーム(その他) 評論・情報・アクション・シューティング・シミュレーション・アドベンチャー・パズル・クイズ・落ち物・プライズ・サウンドノベル・音ゲー・ pop'n music・どこでもいっしょ・バイオハザード・ドラキュラX・ワルキューレ・パワードール・川背・ポヤッチオ・ウィズハー・悠久・エタメロ・デバイスレイン・マリーのアトリエシリーズ・マール王国・ガンパレードマーチ)",
    317: "ゲーム(ゲーム(RPG) 幻想水滸伝・ゼルダ・DQ・FE・オウガバトル・魔人学園・ラングリッサー・シャイニングフォース・スペクトラルフォース・ VP・俺屍・ブラックマトリクス・サーカディア・サモンナイト・ワールドネバーランド)",
    318: "ゲーム(スクウェア&アトラス(RPG) FF全シリーズ(オンライン含む)・ゼノギアス・ゼノサーガ・Saga・聖剣・フロントミッション・女神転生・グローランサー)",
    319: "ゲーム(ゲーム(恋愛) BoysLove(オリジナル除く)・アンジェリークシリーズ・遙かなる時空の中で・王子様Lv.1・ときめきメモリアルGirl’sSide)",
    400: "マンガ(FC(ジャンプ) スーパージャンプ・コミックバンチ・車田・C翼・男塾・キン肉マン)",
    410: "マンガ(SLAMDUNK 井上雄彦)",
    411: "マンガ(冨樫義博 幽遊白書・レベルE・HUNTER×HUNTER)",
    412: "マンガ(封神演義 サクラテツ)",
    413: "マンガ(ワンピース)",
    414: "マンガ(NARUTO)",
    415: "マンガ(テニスの王子様)",
    501: "アニメ(アニメ(少女) 魔法少女・レイアース・CCさくら・エンジェリックレイヤー・ちょびっツ・セーラームーン・守護月天・コレクターユイ)",
    505: "アニメ(アニメ(その他) 声優・評論・情報・海外アニメ・NHK・藤子・藤島康介・麻宮騎亜・ガイナックス・ルパン・スレイヤーズ・まほろまてぃっく・ギャラクシーエンジェル・おねがい☆ティーチャー)",
    506: "アニメ(アニメ(サンライズ) FSS・スーパーロボット大戦(魔装機神))",
    517: "アニメ(ガンダム 全シリーズ・ゲーム全シリーズ(ギレンの野望など))",
    600: "その他(歴史 歌舞伎)",
    603: "その他(創作(文芸・小説) オリジナルの創作物(詩・俳句・短歌・替え歌・放送劇など))",
    607: "その他(SF・ファンタジー ハヤカワ・創元)",
    608: "その他(特撮(その他) 評論・情報・アメコミ)",
    609: "その他(鉄道・旅行・メカミリ バス・モータースポーツ・おもちゃ・ガレキ・車・バイク・先行者)",
    701: "その他(音楽(洋楽・邦楽) T.M.R・及川・野猿・DAPUMP・アジア系男性アイドル)",
    702: "その他(音楽(男性アイドル))",
    703: "その他(TV・映画・芸能 必殺・大河ドラマ・舞台・演劇・ミュージカル・宝塚・吉本・女性アイドル・女性アーティスト・お笑い番組・アジア系映画)",
    704: "その他(特撮(補則参照) 平成ウルトラマン・ライダー(クウガ以降)・戦隊もの(評論・情報除く))",
    705: "その他(スポーツ F1・相撲・ギャンブル・競馬・パチンコ・パチスロ)",
    800: "その他(FC(小説) 児童文学・フジミ・トールキン・銀河の荒鷲シーフォート)",
    810: "マンガ(FC(少年) 少年サンデー・少年マガジン・少年チャンピオン・ボンボン・GAO・手塚治虫・高橋留美子・石ノ森・超人ロック・メダロット・009)",
    811: "マンガ(FC(少女) CLAMP・闇の末裔・フルーツバスケット)",
    812: "マンガ(FC(青年) Yキング・Yマガジン・Yアニマル・Yサンデー・Yジャンプ・Bジャンプ・Uジャンプ・アフタヌーン・モーニング・バーズ・ガム・電撃大王・高田裕三・トライガン・頭文字D・藍より青し・あずまんが)",
    813: "マンガ(FC(コロコロ) デジモン含む・ポケモン・Let's & Go!・ゾイド・ビックリマン)",
    814: "マンガ(FC(ガンガン) コミックブレイド・コミックゼロサム・柴田亜美・いがらしみきお・最遊記)",
    900: 'その他(その他 (作品名、作家名、雑誌名などが特定できる場合と、ジャンル複合の場合は"その他"以外で申し込んで下さい))',
    999: "()", # see '薬缶本舗'
}

DATE_INDEX = {
    "土": "12.28",
    "日": "12.29",
    "月": "12.30",
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
    NUM = 63
    circles_raw = []
    raw_entries: list[list[str]] = []
    
    # =====================================
    # Other circles
    # =====================================

    # ===== Load csv like data ======
    with open(Path(__file__).parent / 'CDATA' / 'C63ROM1.txt', 'rb') as file:
        lines = file.readlines()
    with open(Path(__file__).parent / 'CDATA' / 'C63ROM2.txt', 'rb') as file:
        lines.extend(file.readlines())
    with open(Path(__file__).parent / 'CDATA' / 'C63ROM3.txt', 'rb') as file:
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
    with open(Path(__file__).parent / 'CDATA' / 'C63ROM0.txt', 'rb') as file:
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