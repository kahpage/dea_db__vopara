# Notes:
import sys
import json
from pathlib import Path
from typing import Any

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Medium,
    Circle,
    Event,
    EventGroup,
    Source,
    ReliabilityTypes,
    OriginTypes,
    Location,
)

RT, OT = ReliabilityTypes, OriginTypes

PATH_HELPER = Path(__file__).parent
PATH_EVENT_GROUP = PATH_HELPER.parent
PATH_MEDIA = PATH_EVENT_GROUP / "media"


def retrieve_circles(event_name: str) -> list[Circle]:
    """Retrieve circles of given event. In the circle file has not been created, execute the creation script first."""
    circles_json_path = PATH_HELPER / event_name / "circles.json"
    if not circles_json_path.exists():
        print(
            f"Circle file for {event_name} not found, running the creation script ..."
        )
        creation_script_path = PATH_HELPER / event_name / "main.py"
        if not creation_script_path.exists():
            raise FileNotFoundError(
                f"Creation script for {event_name} not found at {creation_script_path}"
            )
        # Import main() from the creation script and execute
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            f"{event_name}.main", creation_script_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()

        if not circles_json_path.exists():
            raise FileNotFoundError(
                f"Creation script {creation_script_path} failed to create {circles_json_path}"
            )

    with circles_json_path.open("r", encoding="utf-8") as f:
        circles_raw = json.load(f)
    return [Circle.load_from_json(c) for c in circles_raw]


if __name__ == "__main__":
    events: list[Event] = []
    active_events: list[int | str] = list(range(1, 14 + 1))

    i = 1  # ==== vopara1 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para_list.htm"

        media_ = [
            Medium(
                "01_080622_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3264.4252281700215!2d136.9215652758576!3d35.096091372781785!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60037bbf4ac7e49f%3A0x896daa6414e9228d!2sNippon%20Gaishi%20Forum!5e0!3m2!1sfr!2sfr!4v1781202342453!5m2!1sfr!2sfr",
                description="日本ガイシフォーラム（旧称：名古屋市総合体育館 サン笠寺）",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                "VOCALOID PARADISE",
                "VOCALOID PARADISE 1",
                "ボーパラ",
                "ボーパラ1",
            ],
            dates="2008.06.22",
            media=media_,
            sources=[
                Source(
                    f"Date, Participating circles, Notes: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            comments="Notes: 募集数の70スペースを少し上回りましたが、配置上の問題がないため、全サークル全スペース当選とさせていただきます。下記サークルリストのリンクミス・サークル名／ペンネームの誤字脱字などがございましたら、ご連絡願います。",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 2  # ==== vopara2 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = ""

        media_ = [
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3261.437129685104!2d136.8818411804513!3d35.17065601254546!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600376dc4791c681%3A0x862a713c2f107a48!2zSmFwYW4sIOOAkjQ1MC0wMDAyIEFpY2hpLCBOYWdveWEsIE5ha2FtdXJhIFdhcmQsIE1laWVraSwgNC1jaMWNbWXiiJI04oiSMzgg5oSb55-l55yM55Sj5qWt5Yq05YON44K744Oz44K_44O877yI44Km44Kk44Oz44Kv44GC44GE44Gh77yJ!5e0!3m2!1sen!2sfr!4v1781203309542!5m2!1sen!2sfr",
                description="愛知県産業労働センター７階展示場",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2009.11.22",
            circles=[],
            media=media_,
            sources=[
                Source(
                    f"Date, Participating circles, Notes: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            comments="""Notes: 開催日： 2009年11月22日（日）
開催場所： 愛知県産業労働センター７階展示場
同時開催： ツインテールカーニバル６

ＴＴＣ６・ボーパラ２ 館内配置図
A～C … ツインテールカーニバル６
D～H … VOCALOID PARADISE 2""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 3  # ==== vopara3 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para03_list.htm"

        media_ = [
            Medium(
                "03_20120918044032_vo-para03_hyoushi.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20120918044032/http://ttc.ninja-web.net/vo-para/vo-para03_hyoushi.jpg",
                        (RT.Reliable, OT.Official),
                    ),
                    Source(f"Artist: {vopara_main_url}", (RT.Reliable, OT.Official)),
                ],
                comments="tukinan 様 （LUPINASU）",
            ),
            Medium(
                "03_100328_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.751071069338!2d135.7783858758542!3d35.01293597281049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600108e5fdb0fb75%3A0x32f576fbc1dc5042!2sMiyako%20Messe%20(Kyoto%20International%20Exhibition%20Hall)!5e0!3m2!1sen!2sfr!4v1781203776946!5m2!1sen!2sfr",
                description="京都市勧業館（みやこめっせ） ",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2010.03.28",
            circles=[],
            media=media_,
            sources=[
                Source(
                    f"Date, Participating circles, Notes: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            comments="""Notes: 開催日： 2010年3月28日（日）
開催場所： 京都市勧業館（みやこめっせ） 地下１階 第１展示場
同時開催： 乙HiME☆復活祭 Seven

全サークル当選のお知らせ
多くの申込ありがとうございました。
乙HiME☆復活祭側に割り当てられた分をボーパラ側に回して調整を行った結果、二次募集期間に申し込まれたサークルも含めて、全て当選となりました。

館内配置図

第１展示場B面がサークルスペースでいっぱいとなったため、今回の「乙HiME☆復活祭７」「VOCALOID PARADISE 3」では、別途、大会議室をコスプレ撮影エリアとして用意しています。""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 4  # ==== vopara4 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para04_list.htm"

        media_ = [
            Medium(
                "04_20140903032737_vo-para04b.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20140903032737/http://ttc.ninja-web.net/vo-para/vo-para04b.jpg",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="Nacht 様 （シフトライトアリスメティック）",
            ),
            Medium(
                "04_101031_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3261.437129685104!2d136.8818411804513!3d35.17065601254546!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600376dc4791c681%3A0x862a713c2f107a48!2zSmFwYW4sIOOAkjQ1MC0wMDAyIEFpY2hpLCBOYWdveWEsIE5ha2FtdXJhIFdhcmQsIE1laWVraSwgNC1jaMWNbWXiiJI04oiSMzgg5oSb55-l55yM55Sj5qWt5Yq05YON44K744Oz44K_44O877yI44Km44Kk44Oz44Kv44GC44GE44Gh77yJ!5e0!3m2!1sen!2sfr!4v1781203309542!5m2!1sen!2sfr",
                description="愛知県産業労働センター（ウインクあいち） ６階展示場",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2010.10.31",
            circles=[],
            media=media_,
            sources=[
                Source(
                    f"Date, Participating circles, Notes: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            comments="""Notes: 開催日： 2010年10月31日（日）
開催場所： 愛知県産業労働センター（ウインクあいち） ６階展示場
同時開催： 「あンた、背中が透けてるじぇ！！ ２回目」（咲-saki-）

館内配置図（PDFファイル）""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 5  # ==== vopara5 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para05_list.htm"

        media_ = [
            Medium(
                "05_20120918044130_vo-para05.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20120918044130/http://ttc.ninja-web.net/vo-para/vo-para05.jpg",
                        (RT.Reliable, OT.Official),
                    ),
                    Source(f"Artist: {vopara_main_url}", (RT.Reliable, OT.Official)),
                ],
                comments="ボーパラ５チラシ絵　プリンプリン様 （Lachenalia）",
            ),
            Medium(
                "05_110327_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.751071069338!2d135.7783858758542!3d35.01293597281049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600108e5fdb0fb75%3A0x32f576fbc1dc5042!2sMiyako%20Messe%20(Kyoto%20International%20Exhibition%20Hall)!5e0!3m2!1sen!2sfr!4v1781203776946!5m2!1sen!2sfr",
                description="京都市勧業館（みやこめっせ）第３展示場全面",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2011.03.27",
            circles=[],
            media=media_,
            sources=[
                Source(
                    f"Date, Participating circles, Notes: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            comments="""Notes: この度は、ボーパラ５に多くの申込ありがとうございました。
募集数を大幅に上回る285サークル316スペースもの申込がありましたが、３階Ａ面→３階全面へ拡大を行ったため、申込されたサークル様は全て当選となりました。
また、今回はボーパラでは初めての企業出展２社を受け入れました。

ボーパラ５＋同時開催イベントで実施した東日本大震災の義捐金払込報告はこちら。

開催日： 2011年3月27日（日）
開催場所： 京都市勧業館（みやこめっせ） ３階 第３展示場A面 → 第３展示場全面
同時開催：
　・リトバスパーティー４（リトルバスターズ！）
　・AB即売会戦線２（Angel Beats!）
　・Keyパーティー（Key作品総合）
　・MUSIC COMMUNICATION 3（音系）
　・乙HiME☆復活祭 9（舞-HiME/舞-乙HiME）""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 6  # ==== vopara6 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para06_list.htm"

        media_ = [
            Medium(
                "06_20111006041646_vo-para06.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20111006041646/http://ttc.ninja-web.net/vo-para/index.html",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="ボーパラ６チラシ絵　田村ヒロ 様 （stardust）",
            ),
            Medium(
                "06_20111006041646_banner.gif",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
            Medium(
                "06_111030_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3261.437129685104!2d136.8818411804513!3d35.17065601254546!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600376dc4791c681%3A0x862a713c2f107a48!2zSmFwYW4sIOOAkjQ1MC0wMDAyIEFpY2hpLCBOYWdveWEsIE5ha2FtdXJhIFdhcmQsIE1laWVraSwgNC1jaMWNbWXiiJI04oiSMzgg5oSb55-l55yM55Sj5qWt5Yq05YON44K744Oz44K_44O877yI44Km44Kk44Oz44Kv44GC44GE44Gh77yJ!5e0!3m2!1sen!2sfr!4v1781203309542!5m2!1sen!2sfr",
                description="愛知県産業労働センター（ウインクあいち）６階・７階展示場",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2011.10.30",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20111006041646/http://ttc.ninja-web.net/vo-para/index.html",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles, Notes: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            comments="""Notes: この度はボーパラ６に多くの申込ありがとうございました。
おかげさまで、一次締切終了時点で募集数150スペースを越えて満了しましたので、サークル参加受付を終了しました。
7/29までに全ての手続を済ませたサークル様は当選です。
また、館内配置を見直して、7/29までに全ての手続が済んでいない仮受付状態のサークル様も、全て当選としました。

今回、ボーパラ名古屋開催としては、最多の138サークル154スペースの申込がございました。
そして前回同様、「VOCALOID STORE」「（株）インターネット」の企業出展２社の参加がございます。""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 7  # ==== vopara7 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para07_list.htm"

        media_ = [
            Medium(
                "07_20120309003013_vo-para07.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20120309003013/http://ttc.ninja-web.net/vo-para/index.html",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "07_20120309003013_banner.png",
                [
                    Source(
                        "https://web.archive.org/web/20120309003013/http://ttc.ninja-web.net/vo-para/index.html",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "07_121028_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3261.437129685104!2d136.8818411804513!3d35.17065601254546!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600376dc4791c681%3A0x862a713c2f107a48!2zSmFwYW4sIOOAkjQ1MC0wMDAyIEFpY2hpLCBOYWdveWEsIE5ha2FtdXJhIFdhcmQsIE1laWVraSwgNC1jaMWNbWXiiJI04oiSMzgg5oSb55-l55yM55Sj5qWt5Yq05YON44K744Oz44K_44O877yI44Km44Kk44Oz44Kv44GC44GE44Gh77yJ!5e0!3m2!1sen!2sfr!4v1781203309542!5m2!1sen!2sfr",
                description="愛知県産業労働センター（ウインクあいち） ６階展示場",
                sources=[
                    Source(
                        "https://web.archive.org/web/20120309003013/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2012.10.28",
            circles=[],
            media=media_,
            sources=[
                Source(
                    f"Participating circles: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Date: https://web.archive.org/web/20120309003013/http://ttc.ninja-web.net/vo-para/index.html",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # comments="""Notes:""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 8  # ==== vopara8 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para08_list.htm"

        media_ = [
            Medium(
                "08_20130423043601_vo-para08.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20130423043601/http://ttc.ninja-web.net/vo-para/index.html",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "08_20130423043601_bn.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20130423043601/http://ttc.ninja-web.net/vo-para/index.html",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "08_131020_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
            Medium(
                "08_131020_layout2.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d13051.9153575633!2d136.8873299!3d35.1322016!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600379fe829a2f51%3A0x284de675a464956a!2sShirotori%20Hall!5e0!3m2!1sen!2sfr!4v1781209672065!5m2!1sen!2sfr",
                description="名古屋国際会議場 白鳥（しろとり）ホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20130423043601/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2013.10.20",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20130423043601/http://ttc.ninja-web.net/vo-para/index.html",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # comments="""Notes:""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 9  # ==== vopara9 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para09_list.htm"

        media_ = [
            Medium(
                "09_20140716151640_vo-para09_luka-para.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20140716151640/http://ttc.ninja-web.net/vo-para/vo-para09_luka-para.jpg",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "09_141019_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3261.437129685104!2d136.8818411804513!3d35.17065601254546!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600376dc4791c681%3A0x862a713c2f107a48!2zSmFwYW4sIOOAkjQ1MC0wMDAyIEFpY2hpLCBOYWdveWEsIE5ha2FtdXJhIFdhcmQsIE1laWVraSwgNC1jaMWNbWXiiJI04oiSMzgg5oSb55-l55yM55Sj5qWt5Yq05YON44K744Oz44K_44O877yI44Km44Kk44Oz44Kv44GC44GE44Gh77yJ!5e0!3m2!1sen!2sfr!4v1781203309542!5m2!1sen!2sfr",
                description="愛知県名古屋市熱田区熱田西町1番1号名古屋国際会議場 イベントホール",
                sources=[
                    Source(
                        "https://www.pixiv.net/event_detail.php?event_id=4162",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2014.10.19",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date : https://www.pixiv.net/event_detail.php?event_id=4162",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # comments="""Notes:""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 10  # ==== vopara10 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para10_list.htm"

        media_ = [
            Medium(
                "10_20150918005308_vo-para10.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20150918005308/http://ttc.ninja-web.net/vo-para/index.html",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "10_151011_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3261.437129685104!2d136.8818411804513!3d35.17065601254546!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600376dc4791c681%3A0x862a713c2f107a48!2zSmFwYW4sIOOAkjQ1MC0wMDAyIEFpY2hpLCBOYWdveWEsIE5ha2FtdXJhIFdhcmQsIE1laWVraSwgNC1jaMWNbWXiiJI04oiSMzgg5oSb55-l55yM55Sj5qWt5Yq05YON44K744Oz44K_44O877yI44Km44Kk44Oz44Kv44GC44GE44Gh77yJ!5e0!3m2!1sen!2sfr!4v1781203309542!5m2!1sen!2sfr",
                description="愛知県愛知県名古屋市熱田区熱田西町1番1号名古屋国際会議場 白鳥ホール",
                sources=[
                    Source(
                        "https://www.pixiv.net/event_detail.php?event_id=4948",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2015.10.11",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://www.pixiv.net/event_detail.php?event_id=4948",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # comments="""Notes:""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 11  # ==== vopara11 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para11_list.htm"

        media_ = [
            Medium(
                "11_20160219102424_vo-para11.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20160219102424/http://ttc.ninja-web.net/vo-para/index.html",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "11_161002_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3263.000972522528!2d136.8957839758592!3d35.13164927276959!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600379fe92208121%3A0xc830505a7700eaa6!2sNagoya%20Congress%20Center!5e0!3m2!1sen!2sfr!4v1781211470110!5m2!1sen!2sfr",
                description="名古屋国際会議場 イベントホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20160219102424/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2016.10.02",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20160219102424/http://ttc.ninja-web.net/vo-para/index.html",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # comments="""Notes:""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 12  # ==== vopara12 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para12_list.htm"

        media_ = [
            Medium(
                "12_1355.jpg",
                [
                    Source(
                        "https://vocadb.net/E/1355/vocaloid-paradise-12",
                        (RT.Likely, OT.External),
                    )
                ],
            ),
            Medium(
                "12_171015_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3263.000972522528!2d136.8957839758592!3d35.13164927276959!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600379fe92208121%3A0xc830505a7700eaa6!2sNagoya%20Congress%20Center!5e0!3m2!1sen!2sfr!4v1781211470110!5m2!1sen!2sfr",
                description="名古屋国際会議場 イベントホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20171003002242/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2017.10.15",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20171003002242/http://ttc.ninja-web.net/vo-para/index.html",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # comments="""Notes:""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 13  # ==== vopara13 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        vopara_main_url = "https://ttc.ninja-web.net/vo-para/vo-para13_list.htm"

        media_ = [
            Medium(
                "13_20211203064330_vo-para13.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20211203064330/http://ttc.ninja-web.net/vo-para/index.html",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "13_180916_layout.pdf",
                [Source(vopara_main_url, (RT.Reliable, OT.Official))],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d13051.9153575633!2d136.8873299!3d35.1322016!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600379fe829a2f51%3A0x284de675a464956a!2sShirotori%20Hall!5e0!3m2!1sen!2sfr!4v1781209672065!5m2!1sen!2sfr",
                description="名古屋国際会議場 白鳥ホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20180925180443/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2018.09.16",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20180925180443/http://ttc.ninja-web.net/vo-para/index.html",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles: {vopara_main_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # comments="""Notes:""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 14  # ==== vopara14 ====
    if i in active_events:
        event_name = f"vopara{i}"
        print(f"Processing {event_name} ...")
        # vopara_main_url = ""

        media_ = []
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3254.866190194564!2d137.1268545758678!3d35.33414417270119!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60036a70848ce44f%3A0xaea80b3888b9c8db!2sSangyobunka%20Center!5e0!3m2!1sen!2sfr!4v1781213114333!5m2!1sen!2sfr",
                description="多治見市産業文化センター ５階ホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20240714193723/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[f"VOCALOID PARADISE {i}", f"ボーパラ{i}"],
            dates="2019.10.20 -> CANCELLED",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20240714193723/http://ttc.ninja-web.net/vo-para/index.html",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Was cancelled: https://x.com/vo_para/status/1130104714132111360",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            description='Cancelled, the organizing committee suggested to participate in VOCALOID STREET in 多治見 instead (see "Was cancelled" source)',
            # comments="""Notes:""",
            last_edited="2026.06.11",
        )

        # Retrieve circles
        # event.circles = retrieve_circles(event_name)
        events.append(event)

    # ==== event group ====
    media = [
        Medium(
            "banner1_20111006041646_vp-bn01.jpg",
            [
                Source(
                    "https://web.archive.org/web/20131019131152/http://ttc.ninja-web.net/vo-para/vp-bn01.jpg",
                    (RT.Reliable, OT.Official),
                )
            ],
        ),
        Medium(
            "banner2_20080626131159_banner.jpg",
            [
                Source(
                    "https://web.archive.org/web/20111112091158/http://ttc.ninja-web.net/vo-para/vp-bn02.jpg",
                    (RT.Reliable, OT.Official),
                )
            ],
        ),
        Medium(
            "banner3_20100114165308_vp-bn03.jpg",
            [
                Source(
                    "https://web.archive.org/web/20111112085714/http://ttc.ninja-web.net/vo-para/vp-bn03.jpg",
                    (RT.Reliable, OT.Official),
                )
            ],
        ),
        Medium(
            "banner4_20111006041646_vp-bn04.jpg",
            [
                Source(
                    "https://web.archive.org/web/20111112085502/http://ttc.ninja-web.net/vo-para/vp-bn04.jpg",
                    (RT.Reliable, OT.Official),
                )
            ],
        ),
        Medium(
            "banner5_20111006041646_vp-bn05.jpg",
            [
                Source(
                    "https://web.archive.org/web/20111112090115/http://ttc.ninja-web.net/vo-para/vp-bn05.jpg",
                    (RT.Reliable, OT.Official),
                )
            ],
        ),
        Medium(
            "vp-bn06.jpg",
            [
                Source(
                    "https://web.archive.org/web/20130504141410/http://ttc.ninja-web.net/vo-para/vp-bn06.jpg",
                    (RT.Reliable, OT.Official),
                )
            ],
        ),
        Medium(
            "vp-bn07.jpg",
            [
                Source(
                    "https://web.archive.org/web/20130504141410/http://ttc.ninja-web.net/vo-para/vp-bn07.jpg",
                    (RT.Reliable, OT.Official),
                )
            ],
        ),
        Medium(
            "banner6_20130423043601_banner.jpg",
            [
                Source(
                    "https://web.archive.org/web/20131019135636/http://ttc.ninja-web.net/vo-para/vp-bn08.jpg",
                    (RT.Reliable, OT.Official),
                )
            ],
        ),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
    ]
    links = ["http://ttc.ninja-web.net/vo-para/index.html"]

    event_group = EventGroup(
        aliases=["VOCALOID PARADISE", "ボーパラ", "vo-para"],
        events=events,
        media=media,
        links=links,
        sources=[
            # Source(
            #     "",
            #     (ReliabilityTypes.Reliable, OriginTypes.Official),
            # ),
        ],
        comments=None,
        description=None,
        last_edited="2026.06.11",
    )

    print(f"Saving {Path(__file__).stem} database...")
    event_group.save(PATH_EVENT_GROUP, indent=None)
    print("Done")
