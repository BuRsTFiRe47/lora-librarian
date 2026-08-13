# -*- coding: utf-8 -*-
"""
LoRA Librarian - Base Model Normalizer
Civitai gibi kaynaklardan gelen 'baseModel' etiketi çok sayıda küçük
varyasyonla gelebilir (ör. 'Flux.1 D', 'Flux.1 S', 'Flux.1 Krea').
Bu modül bu varyasyonları temiz, tutarlı klasör isimlerinde toplar ve
yeni/az bilinen teknolojileri (Krea, Anima, Chroma, HiDream, Qwen, Wan,
Hunyuan vb.) de tanır.

Sources like Civitai can return many small variations of the
'baseModel' tag (e.g. 'Flux.1 D', 'Flux.1 S', 'Flux.1 Krea'). This
module groups those variations into clean, consistent folder names and
also recognizes newer/less common technologies (Krea, Anima, Chroma,
HiDream, Qwen, Wan, Hunyuan etc.).
"""

import re

# Order matters: more specific patterns must come before broader ones.
# Sıra önemlidir: daha spesifik kalıplar daha genel olanlardan önce gelmeli.
_RULES = [
    (r"flux.*krea|krea.*flux", "Flux Krea"),
    (r"flux", "Flux"),
    (r"\bkrea\b", "Krea"),
    (r"\banima\b|animagine", "Anima"),
    (r"chroma", "Chroma"),
    (r"hidream", "HiDream"),
    (r"qwen", "Qwen Image"),
    (r"\bwan\b|wan\s*video|wan\s*2", "Wan Video"),
    (r"hunyuan", "Hunyuan Video"),
    (r"\bltx\b", "LTX Video"),
    (r"cascade", "Stable Cascade"),
    (r"pony", "Pony"),
    (r"illustrious", "Illustrious"),
    (r"noobai", "NoobAI"),
    (r"sdxl|sd\s*xl", "SDXL"),
    (r"sd\s*3\.?5|stable\s*diffusion\s*3\.5", "SD 3.5"),
    (r"sd\s*3\b|stable\s*diffusion\s*3\b", "SD 3"),
    (r"sd\s*2|stable\s*diffusion\s*2", "SD 2.1"),
    (r"sd\s*1\.?5|stable\s*diffusion\s*1\.5", "SD 1.5"),
    (r"aura\s*flow", "AuraFlow"),
    (r"kolors", "Kolors"),
    (r"playground", "Playground"),
]

_COMPILED = [(re.compile(pat, re.IGNORECASE), name) for pat, name in _RULES]


def normalize_base_model(raw_name: str, unknown_label: str = "UnknownBase") -> str:
    """
    Map a raw baseModel string (possibly containing version/variation
    suffixes) to a clean canonical family name.

    Ham bir baseModel metnini (sürüm/varyasyon ekleri içerebilir) temiz
    ve kalıcı bir aile ismine dönüştürür.
    """
    if not raw_name:
        return unknown_label

    for pattern, canonical in _COMPILED:
        if pattern.search(raw_name):
            return canonical

    # Not in our known list: fall back to a lightly cleaned version of
    # whatever the source returned, so brand-new/unrecognized base
    # models still get their own sensible folder instead of being lost.
    cleaned = raw_name.strip()
    return cleaned if cleaned else unknown_label
