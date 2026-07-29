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
                coordinates=(35.0960914, 136.9241402),
                address="5 Chome-1-16 Higashimatabeecho, Minami Ward, Nagoya, Aichi 457-0833, Japan",
                description="日本ガイシフォーラム（旧称：名古屋市総合体育館 サン笠寺）",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWmj8MzT8MDc2f6y-m4HKbW409CgcjzT-W5sICqc_6FGCydMMyIdsr37ZfspiGt3FF4_viq4XCwlLXeK4sHeI428n6LGylj2FGApSjctQAT_dR0dwUcv0i9FQt7mKQ5a4YH401m5Ig=s0?imgmax=0",
                url="https://maps.app.goo.gl/UY9XC3cm89b4qD8g7",
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
                coordinates=(35.1708859, 136.8837218),
                address="4-chōme-4-38 Meieki, Nakamura Ward, Nagoya, Aichi 450-0002, Japan",
                description="愛知県産業労働センター７階展示場",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://streetviewpixels-pa.googleapis.com/v1/thumbnail?output=thumbnail&cb_client=maps_sv.tactile.gps&panoid=plEI7dd2WTUE58egOJKX3g&w=1177&h=1300&yaw=170&pitch=-40",
                url="https://maps.app.goo.gl/6F2N7Dtys66bRMQQ9",
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
                coordinates=(35.01365, 135.7809429),
                address="9-1 Okazaki Seishojicho, Sakyo Ward, Kyoto, 606-8343, Japan",
                description="京都市勧業館（みやこめっせ）",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWlur6oWztq77DaOuTZLw5MRyj3iDVD1CD-wl9_7wkEXC7e9JYhls5YX8XY6_936CE_RWP6CozLolZI73Mh7gleO-PgU9DJro4VpNaq7nQSPaHd9rChZ-VVge7urD47mbsVOMZ6B-A=s870-k-no",
                url="https://maps.app.goo.gl/8MjxYFEFKBxjhyTT8",
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
                coordinates=(35.1708859, 136.8837218),
                address="4-chōme-4-38 Meieki, Nakamura Ward, Nagoya, Aichi 450-0002, Japan",
                description="愛知県産業労働センター（ウインクあいち） ６階展示場",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://streetviewpixels-pa.googleapis.com/v1/thumbnail?output=thumbnail&cb_client=maps_sv.tactile.gps&panoid=plEI7dd2WTUE58egOJKX3g&w=1177&h=1300&yaw=170&pitch=-40",
                url="https://maps.app.goo.gl/6F2N7Dtys66bRMQQ9",
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
                coordinates=(35.01365, 135.7809429),
                address="9-1 Okazaki Seishojicho, Sakyo Ward, Kyoto, 606-8343, Japan",
                description="京都市勧業館（みやこめっせ）第３展示場全面",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWlur6oWztq77DaOuTZLw5MRyj3iDVD1CD-wl9_7wkEXC7e9JYhls5YX8XY6_936CE_RWP6CozLolZI73Mh7gleO-PgU9DJro4VpNaq7nQSPaHd9rChZ-VVge7urD47mbsVOMZ6B-A=s870-k-no",
                url="https://maps.app.goo.gl/8MjxYFEFKBxjhyTT8",
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
                coordinates=(35.1708859, 136.8837218),
                address="4-chōme-4-38 Meieki, Nakamura Ward, Nagoya, Aichi 450-0002, Japan",
                description="愛知県産業労働センター（ウインクあいち）６階・７階展示場",
                sources=[
                    Source(
                        vopara_main_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://streetviewpixels-pa.googleapis.com/v1/thumbnail?output=thumbnail&cb_client=maps_sv.tactile.gps&panoid=plEI7dd2WTUE58egOJKX3g&w=1177&h=1300&yaw=170&pitch=-40",
                url="https://maps.app.goo.gl/6F2N7Dtys66bRMQQ9",
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
                coordinates=(35.1708859, 136.8837218),
                address="4-chōme-4-38 Meieki, Nakamura Ward, Nagoya, Aichi 450-0002, Japan",
                description="愛知県産業労働センター（ウインクあいち） ６階展示場",
                sources=[
                    Source(
                        "https://web.archive.org/web/20120309003013/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://streetviewpixels-pa.googleapis.com/v1/thumbnail?output=thumbnail&cb_client=maps_sv.tactile.gps&panoid=plEI7dd2WTUE58egOJKX3g&w=1177&h=1300&yaw=170&pitch=-40",
                url="https://maps.app.goo.gl/6F2N7Dtys66bRMQQ9",
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
                coordinates=(35.1313699, 136.8980176),
                address="1-1 Atsuta Nishimachi, Atsuta Ward, Nagoya, Aichi 456-0036, Japan",
                description="名古屋国際会議場 白鳥（しろとり）ホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20130423043601/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn7Lqm9_Q0NEdha1ASXnQ5vdfjHbPJAbiquEME-dTc0IQlVMwwldl4PgCGmoqwXy7f1H0VzeeQ34Sfh31dwy-yLo6SG1i6J7RxOt2LCAXGM3sea6CVPSdGtLv8BqQvcjQ9wGbdq8g=s0?imgmax=0",
                url="https://maps.app.goo.gl/WvWpsu1s7P6fTsdj9",
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
                coordinates=(35.1708859, 136.8837218),
                address="4-chōme-4-38 Meieki, Nakamura Ward, Nagoya, Aichi 450-0002, Japan",
                description="愛知県名古屋市熱田区熱田西町1番1号名古屋国際会議場 イベントホール",
                sources=[
                    Source(
                        "https://www.pixiv.net/event_detail.php?event_id=4162",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://streetviewpixels-pa.googleapis.com/v1/thumbnail?output=thumbnail&cb_client=maps_sv.tactile.gps&panoid=plEI7dd2WTUE58egOJKX3g&w=1177&h=1300&yaw=170&pitch=-40",
                url="https://maps.app.goo.gl/6F2N7Dtys66bRMQQ9",
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
                coordinates=(35.1313699, 136.8980176),
                address="1-1 Atsuta Nishimachi, Atsuta Ward, Nagoya, Aichi 456-0036, Japan",
                description="愛知県愛知県名古屋市熱田区熱田西町1番1号名古屋国際会議場 白鳥ホール",
                sources=[
                    Source(
                        "https://www.pixiv.net/event_detail.php?event_id=4948",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn7Lqm9_Q0NEdha1ASXnQ5vdfjHbPJAbiquEME-dTc0IQlVMwwldl4PgCGmoqwXy7f1H0VzeeQ34Sfh31dwy-yLo6SG1i6J7RxOt2LCAXGM3sea6CVPSdGtLv8BqQvcjQ9wGbdq8g=s0?imgmax=0",
                url="https://maps.app.goo.gl/WvWpsu1s7P6fTsdj9",
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
                coordinates=(35.1316493, 136.895784),
                address="1-1 Atsuta Nishimachi, Atsuta Ward, Nagoya, Aichi 456-0036, Japan",
                description="名古屋国際会議場 イベントホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20160219102424/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWktkJOUF1Dj75m5uf1NOu4f4ZSJqePSniPmQ-lFQLZKHHxYlMXIXqwIYRDL1Pz6uwvqNAVoxKFi8CsA2ShNX_STmUZUEoRQOhzKg37OkNQAgQS_TmjI_P2eocrZPK8YLDcj5hIMRA=s0?imgmax=0",
                url="https://maps.app.goo.gl/ZKEKnswpsBoZELkp6",
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
                coordinates=(35.1316493, 136.895784),
                address="1-1 Atsuta Nishimachi, Atsuta Ward, Nagoya, Aichi 456-0036, Japan",
                description="名古屋国際会議場 イベントホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20171003002242/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWktkJOUF1Dj75m5uf1NOu4f4ZSJqePSniPmQ-lFQLZKHHxYlMXIXqwIYRDL1Pz6uwvqNAVoxKFi8CsA2ShNX_STmUZUEoRQOhzKg37OkNQAgQS_TmjI_P2eocrZPK8YLDcj5hIMRA=s0?imgmax=0",
                url="https://maps.app.goo.gl/ZKEKnswpsBoZELkp6",
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
                coordinates=(35.1313699, 136.8980176),
                address="1-1 Atsuta Nishimachi, Atsuta Ward, Nagoya, Aichi 456-0036, Japan",
                description="名古屋国際会議場 白鳥ホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20180925180443/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn7Lqm9_Q0NEdha1ASXnQ5vdfjHbPJAbiquEME-dTc0IQlVMwwldl4PgCGmoqwXy7f1H0VzeeQ34Sfh31dwy-yLo6SG1i6J7RxOt2LCAXGM3sea6CVPSdGtLv8BqQvcjQ9wGbdq8g=s0?imgmax=0",
                url="https://maps.app.goo.gl/WvWpsu1s7P6fTsdj9",
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
                coordinates=(35.334103, 137.1288233),
                address="Japan, 〒507-0831 Gifu, Tajimi, Shinmachi, 1 Chome−２３",
                description="多治見市産業文化センター ５階ホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20240714193723/http://ttc.ninja-web.net/vo-para/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWkSZuwNxFhmlk_wbB5TDxN1XQ33eBXjMchn6XpudPnnmfnYGW-1Ik4UqKwx05HvOK3hm7_ry8bDbf8ZrrO3pZXIgd_0FAnI-WPdGWIfhiv8vRSXNboVBmnbFgP0FXuO62tPYsg8GQ=s812-k-no",
                url="https://maps.app.goo.gl/vQXSpphcMZdTU78u5",
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
