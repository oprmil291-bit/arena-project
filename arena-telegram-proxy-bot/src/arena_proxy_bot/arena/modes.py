from dataclasses import dataclass


@dataclass(frozen=True)
class ArenaModeDefinition:
    key: str
    label: str
    route_path: str
    model_category: str
    summary: str
    capabilities: str
    purpose: str
    force_model: str | None = None


@dataclass(frozen=True)
class ArenaModelOption:
    label: str
    description: str = ""


@dataclass(frozen=True)
class ArenaModePanel:
    mode: ArenaModeDefinition
    current_model: str
    models: tuple[ArenaModelOption, ...]


DEFAULT_MODE_KEY = "text"
ARENA_MODE_ORDER = ("text", "image", "search", "vip")

ARENA_MODES: dict[str, ArenaModeDefinition] = {
    "text": ArenaModeDefinition(
        key="text",
        label="Text",
        route_path="/text/direct",
        model_category="Text",
        summary="РћР±С‹С‡РЅС‹Р№ С‚РµРєСЃС‚РѕРІС‹Р№ С‡Р°С‚ Arena СЃ СЂСѓС‡РЅС‹Рј РІС‹Р±РѕСЂРѕРј LLM.",
        capabilities="Р”РёР°Р»РѕРі, reasoning, Р°РЅР°Р»РёР·, РєРѕРґ, РґР»РёРЅРЅС‹Рµ РѕС‚РІРµС‚С‹.",
        purpose="РљРѕРіРґР° РЅСѓР¶РµРЅ РѕР±С‹С‡РЅС‹Р№ С‡Р°С‚ Р±РµР· РІРµР±-РїРѕРёСЃРєР° Рё Р±РµР· РіРµРЅРµСЂР°С†РёРё РёР·РѕР±СЂР°Р¶РµРЅРёР№.",
    ),
    "image": ArenaModeDefinition(
        key="image",
        label="Image",
        route_path="/image/direct",
        model_category="Image",
        summary="Р РµР¶РёРј РіРµРЅРµСЂР°С†РёРё РёР·РѕР±СЂР°Р¶РµРЅРёР№ Arena.",
        capabilities="РР»Р»СЋСЃС‚СЂР°С†РёРё, РєРѕРЅС†РµРїС‚С‹, РІРёР·СѓР°Р»СЊРЅС‹Рµ РёРґРµРё, СЂРµС„РµСЂРµРЅСЃС‹.",
        purpose="РљРѕРіРґР° СЂРµР·СѓР»СЊС‚Р°С‚ РЅСѓР¶РµРЅ РІ РІРёРґРµ РєР°СЂС‚РёРЅРєРё, Р° РЅРµ С‚РµРєСЃС‚РѕРІРѕРіРѕ РѕС‚РІРµС‚Р°.",
    ),
    "search": ArenaModeDefinition(
        key="search",
        label="Search",
        route_path="/search/direct",
        model_category="Search",
        summary="Р РµР¶РёРј Arena СЃ РІРµР±-РїРѕРёСЃРєРѕРј Рё search-capable РјРѕРґРµР»СЏРјРё.",
        capabilities="РђРєС‚СѓР°Р»СЊРЅС‹Рµ РґР°РЅРЅС‹Рµ, РїРѕРёСЃРє РїРѕ СЃР°Р№С‚Р°Рј, РЅРѕРІРѕСЃС‚Рё, СЃРІРµР¶РёРµ С„Р°РєС‚С‹.",
        purpose="РљРѕРіРґР° РІР°Р¶РЅР° СЃРІРµР¶Р°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ Рё РѕС‚РІРµС‚С‹ СЃ СѓС‡РµС‚РѕРј РІРµР±-РёСЃС‚РѕС‡РЅРёРєРѕРІ.",
    ),
    "vip": ArenaModeDefinition(
        key="vip",
        label="Vip",
        route_path="/text/direct",
        model_category="Text",
        summary="РџСЂРµСЃРµС‚ Arena Max СЃ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРёРј РІС‹Р±РѕСЂРѕРј СЃРёР»СЊРЅРµР№С€РµР№ РјРѕРґРµР»Рё.",
        capabilities="Р›СѓС‡С€РµРµ РєР°С‡РµСЃС‚РІРѕ РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ Р±РµР· СЂСѓС‡РЅРѕРіРѕ РїРµСЂРµР±РѕСЂР° РјРѕРґРµР»РµР№.",
        purpose="РљРѕРіРґР° РЅСѓР¶РµРЅ РјР°РєСЃРёРјР°Р»СЊРЅРѕ СЃРёР»СЊРЅС‹Р№ СЂРµР¶РёРј РѕРґРЅРёРј РЅР°Р¶Р°С‚РёРµРј.",
        force_model="Max",
    ),
}


def get_mode_definition(mode_key: str | None) -> ArenaModeDefinition:
    if not mode_key:
        return ARENA_MODES[DEFAULT_MODE_KEY]
    return ARENA_MODES.get(mode_key.lower(), ARENA_MODES[DEFAULT_MODE_KEY])
