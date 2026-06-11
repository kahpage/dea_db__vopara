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
    active_events: list[int | str] = list(range(1, 14))

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

    # i = # ==== vopara ====
    # if i in active_events:
    #     event_name = f"vopara{i}"
    #     print(f"Processing {event_name} ...")

    #     media_ = [
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #     ]
    #     locations = [
    #         # Location(
    #         #     iframe_url="",
    #         #     description="",
    #         #     sources=[
    #         #         Source(, (ReliabilityTypes.Reliable, OriginTypes.Official))
    #         #     ],
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=[""],
    #         dates="",
    #         circles=[],
    #         media=media_,
    #         sources=[
    #             Source(
    #                 f"Date, Participating circles: ",
    #                 (RT.Reliable, OT.Official),
    #             ),
    #         ],
    #         locations=locations,
    #         last_edited="2026.05.30",
    #     )

    #     # Retrieve circles
    #     event.circles = retrieve_circles(event_name)
    #     events.append(event)

    # ==== event group ====
    media = [
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
