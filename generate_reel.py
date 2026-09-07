#!/usr/bin/env python3
"""Generate a kinetic typography social media marketing reel (9:16)."""

import math
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1080, 1920
FPS = 30
FONT_BOLD = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
ACCENT = (255, 95, 45)
WHITE = (255, 255, 255)
GRAY = (140, 140, 140)
BG = (8, 8, 10)
OUT_DIR = Path("/workspace/video-output/frames")
FINAL = Path("/opt/cursor/artifacts/social-media-revenue-reel.mp4")


def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3


def ease_out_back(t: float) -> float:
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def clamp01(t: float) -> float:
    return max(0.0, min(1.0, t))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        w = draw.textbbox((0, 0), test, font=font)[2]
        if w <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered_multiline(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    y_start: int,
    font,
    fill,
    line_gap: int = 18,
    opacity: float = 1.0,
    x_offset: float = 0.0,
    scale: float = 1.0,
):
    if scale != 1.0:
        # Approximate scale by adjusting y positions only; text size fixed per frame
        pass
    total_h = 0
    sizes = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        sizes.append(h)
        total_h += h + line_gap
    total_h -= line_gap
    y = y_start - total_h // 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (WIDTH - w) // 2 + int(x_offset)
        if opacity < 1.0:
            fill_rgba = (*fill[:3], int(255 * opacity)) if len(fill) == 3 else fill
            overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            od = ImageDraw.Draw(overlay)
            od.text((x, y), line, font=font, fill=fill_rgba)
            return overlay
        draw.text((x, y), line, font=font, fill=fill)
        y += sizes[i] + line_gap
    return None


def background(frame_idx: int, total_frames: int) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    arr = np.array(img, dtype=np.float32)
    t = frame_idx / max(total_frames - 1, 1)
    # Subtle radial vignette + slow pulse
    cx, cy = WIDTH / 2, HEIGHT * 0.42
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    dist = np.sqrt((xx - cx) ** 2 + ((yy - cy) * 1.2) ** 2)
    vignette = 1 - np.clip(dist / 1200, 0, 0.55)
    pulse = 0.03 * math.sin(t * math.pi * 4)
    arr *= vignette[..., None] * (1 + pulse)
    # Accent glow blob
    glow = np.exp(-((xx - WIDTH * 0.8) ** 2 + (yy - HEIGHT * 0.15) ** 2) / (2 * 280 ** 2))
    arr[..., 0] += glow * 18
    arr[..., 1] += glow * 6
    arr[..., 2] += glow * 2
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def draw_accent_bar(draw: ImageDraw.ImageDraw, progress: float):
    bar_w = int(WIDTH * 0.12 * ease_out_cubic(progress))
    draw.rounded_rectangle(
        [(WIDTH // 2 - bar_w // 2, 120), (WIDTH // 2 + bar_w // 2, 128)],
        radius=4,
        fill=ACCENT,
    )


def render_frame(frame_idx: int, scene_data: dict) -> Image.Image:
    img = background(frame_idx, scene_data["total_frames"])
    draw = ImageDraw.Draw(img)
    scene = scene_data["scene"]
    local_t = scene_data["local_t"]
    p = scene_data["progress"]

    draw_accent_bar(draw, min(1.0, frame_idx / 20))

    if scene == "hook":
        font = load_font(FONT_BOLD, 78)
        lines = wrap_text(draw, "Want to turn social media into a revenue machine?", font, WIDTH - 140)
        alpha = ease_out_cubic(clamp01(local_t / 0.35))
        y_off = int(lerp(60, 0, ease_out_cubic(clamp01(local_t / 0.4))))
        overlay = draw_centered_multiline(draw, lines, HEIGHT // 2 - 40 + y_off, font, WHITE, opacity=alpha)
        if overlay:
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    elif scene == "intro":
        font_top = load_font(FONT_REG, 52)
        font_main = load_font(FONT_BOLD, 88)
        alpha = ease_out_cubic(clamp01(local_t / 0.3))
        top = "Here's what"
        main = "DOESN'T MATTER"
        sub_font = load_font(FONT_REG, 46)
        sub = "if you want real revenue"

        for text, font, y, color in [
            (top, font_top, HEIGHT // 2 - 150, GRAY),
            (main, font_main, HEIGHT // 2 - 20, ACCENT),
            (sub, sub_font, HEIGHT // 2 + 110, WHITE),
        ]:
            a = alpha
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            x = (WIDTH - w) // 2
            slide = int(lerp(40, 0, ease_out_back(clamp01(local_t / 0.45))))
            overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            od = ImageDraw.Draw(overlay)
            od.text((x, y + slide), text, font=font, fill=(*color, int(255 * a)))
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    elif scene == "list_item":
        idx = scene_data["item_idx"]
        items = scene_data["items"]
        font_num = load_font(FONT_BOLD, 120)
        font_item = load_font(FONT_BOLD, 82)
        font_label = load_font(FONT_REG, 40)

        enter = ease_out_back(clamp01(local_t / 0.35))
        exit_p = clamp01((local_t - 0.72) / 0.28)
        alpha = 1 - ease_out_cubic(exit_p)
        y_slide = int(lerp(80, 0, enter)) + int(lerp(0, -60, ease_out_cubic(exit_p)))

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)

        num = f"{idx + 1:02d}"
        nb = od.textbbox((0, 0), num, font=font_num)
        nw = nb[2] - nb[0]
        od.text(((WIDTH - nw) // 2, 280 + y_slide), num, font=font_num, fill=(*ACCENT, int(180 * alpha)))

        item_lines = wrap_text(od, items[idx], font_item, WIDTH - 120)
        y_item = HEIGHT // 2 + y_slide
        total_h = sum(od.textbbox((0, 0), ln, font=font_item)[3] for ln in item_lines) + 20 * (len(item_lines) - 1)
        y = y_item - total_h // 2
        for ln in item_lines:
            bb = od.textbbox((0, 0), ln, font=font_item)
            w = bb[2] - bb[0]
            od.text(((WIDTH - w) // 2, y), ln, font=font_item, fill=(*WHITE, int(255 * alpha)))
            y += bb[3] - bb[1] + 20

        # Strikethrough animates in
        strike_p = ease_out_cubic(clamp01((local_t - 0.45) / 0.25))
        if strike_p > 0:
            line_y = y_item + 20
            half = int((WIDTH - 160) * strike_p / 2)
            cx = WIDTH // 2
            od.line([(cx - half, line_y), (cx + half, line_y)], fill=(*ACCENT, int(255 * alpha)), width=6)

        label = "doesn't matter"
        lb = od.textbbox((0, 0), label, font=font_label)
        lw = lb[2] - lb[0]
        label_alpha = int(255 * alpha * ease_out_cubic(clamp01((local_t - 0.5) / 0.2)))
        od.text(((WIDTH - lw) // 2, HEIGHT - 320 + y_slide), label, font=font_label, fill=(*GRAY, label_alpha))

        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    elif scene == "pivot":
        font = load_font(FONT_BOLD, 76)
        lines = wrap_text(draw, "What actually matters?", font, WIDTH - 120)
        alpha = ease_out_cubic(clamp01(local_t / 0.35))
        scale_push = 1 + 0.04 * math.sin(local_t * math.pi * 2)
        y_off = int(lerp(50, 0, ease_out_cubic(clamp01(local_t / 0.4))))
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        total_h = 0
        for ln in lines:
            bb = od.textbbox((0, 0), ln, font=font)
            total_h += bb[3] - bb[1] + 16
        total_h -= 16
        y = HEIGHT // 2 - total_h // 2 + y_off
        for ln in lines:
            bb = od.textbbox((0, 0), ln, font=font)
            w = bb[2] - bb[0]
            x = (WIDTH - w) // 2
            od.text((x, y), ln, font=font, fill=(*WHITE, int(255 * alpha)))
            y += bb[3] - bb[1] + 16
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    elif scene == "values":
        idx = scene_data["item_idx"]
        values = scene_data["values"]
        font = load_font(FONT_BOLD, 68)
        enter = ease_out_back(clamp01(local_t / 0.32))
        exit_p = clamp01((local_t - 0.7) / 0.3)
        alpha = 1 - ease_out_cubic(exit_p)
        y_off = int(lerp(70, 0, enter)) + int(lerp(0, -50, ease_out_cubic(exit_p)))

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        lines = wrap_text(od, values[idx], font, WIDTH - 100)
        total_h = sum(od.textbbox((0, 0), ln, font=font)[3] for ln in lines) + 18 * (len(lines) - 1)
        y = HEIGHT // 2 - total_h // 2 + y_off
        for i, ln in enumerate(lines):
            color = ACCENT if i == 0 and len(lines) > 1 else WHITE
            bb = od.textbbox((0, 0), ln, font=font)
            w = bb[2] - bb[0]
            od.text(((WIDTH - w) // 2, y), ln, font=font, fill=(*color, int(255 * alpha)))
            y += bb[3] - bb[1] + 18
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    elif scene == "repeat":
        font_big = load_font(FONT_BOLD, 160)
        font_sub = load_font(FONT_REG, 48)
        enter = ease_out_back(clamp01(local_t / 0.4))
        alpha = ease_out_cubic(clamp01(local_t / 0.3))
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        word = "REPEAT."
        bb = od.textbbox((0, 0), word, font=font_big)
        w = bb[2] - bb[0]
        y = HEIGHT // 2 - 60 + int(lerp(40, 0, enter))
        od.text(((WIDTH - w) // 2, y), word, font=font_big, fill=(*ACCENT, int(255 * alpha)))
        sub = "That's the whole game."
        sb = od.textbbox((0, 0), sub, font=font_sub)
        sw = sb[2] - sb[0]
        sub_alpha = int(255 * ease_out_cubic(clamp01((local_t - 0.25) / 0.25)))
        od.text(((WIDTH - sw) // 2, y + 190), sub, font=font_sub, fill=(*WHITE, sub_alpha))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    elif scene == "endcard":
        font = load_font(FONT_BOLD, 56)
        font_sm = load_font(FONT_REG, 36)
        alpha = ease_out_cubic(clamp01(local_t / 0.4))
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        lines = ["Right people.", "Real value.", "Keep going."]
        y = HEIGHT // 2 - 120
        for ln in lines:
            bb = od.textbbox((0, 0), ln, font=font)
            w = bb[2] - bb[0]
            od.text(((WIDTH - w) // 2, y), ln, font=font, fill=(*WHITE, int(255 * alpha)))
            y += 90
        cta = "Turn social into revenue"
        cb = od.textbbox((0, 0), cta, font=font_sm)
        cw = cb[2] - cb[0]
        od.text(((WIDTH - cw) // 2, y + 40), cta, font=font_sm, fill=(*ACCENT, int(255 * alpha)))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    return img


def build_timeline():
    items = [
        "Going viral",
        "Having a huge audience",
        "Trends, hashtags & tactics",
        "Posting every day",
        "Your tech setup",
    ]
    values = [
        "Get in front of the right people.",
        "Provide unmatched value.",
        "Deliver on your promises.",
    ]
    timeline = []
    timeline.append(("hook", 2.8, {}))
    timeline.append(("intro", 2.2, {}))
    for i, item in enumerate(items):
        timeline.append(("list_item", 2.4, {"item_idx": i, "items": items}))
    timeline.append(("pivot", 1.8, {}))
    for i, val in enumerate(values):
        timeline.append(("values", 2.6, {"item_idx": i, "values": values}))
    timeline.append(("repeat", 2.5, {}))
    timeline.append(("endcard", 2.0, {}))
    return timeline


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    timeline = build_timeline()
    total_duration = sum(d for _, d, _ in timeline)
    total_frames = int(total_duration * FPS)

    frame_idx = 0
    for scene_name, duration, extra in timeline:
        scene_frames = int(duration * FPS)
        for f in range(scene_frames):
            local_t = f / max(scene_frames - 1, 1)
            data = {
                "scene": scene_name,
                "local_t": local_t,
                "progress": frame_idx / max(total_frames - 1, 1),
                "total_frames": total_frames,
                **extra,
            }
            img = render_frame(frame_idx, data)
            img.save(OUT_DIR / f"frame_{frame_idx:05d}.png")
            frame_idx += 1

    print(f"Rendered {frame_idx} frames ({total_duration:.1f}s)")

    # Combine frames + generate punchy background beat
    audio_path = Path("/workspace/video-output/beat.wav")
    os.system(
        f'ffmpeg -y -f lavfi -i "sine=frequency=55:duration={total_duration},'
        f'volume=0.15" -f lavfi -i "anoisesrc=d=0.02:c=pink:a=0.08,'
        f'aloop=loop=-1:size=2e+09,atrim=0:{total_duration}" '
        f'-filter_complex "[0][1]amix=inputs=2:duration=first" "{audio_path}" 2>/dev/null'
    )

    # Add beat hits on scene changes
    hit_times = []
    t = 0
    for _, dur, _ in timeline:
        hit_times.append(t)
        t += dur

    hit_filter = ",".join(
        [f"volume=enable='between(t,{max(0,ht-0.01):.3f},{ht+0.08:.3f})':volume=3" for ht in hit_times[:12]]
    )
    audio_enhanced = Path("/workspace/video-output/beat_enhanced.wav")
    os.system(
        f'ffmpeg -y -i "{audio_path}" -af "asetrate=44100*1.0,aresample=44100,{hit_filter}" '
        f'"{audio_enhanced}" 2>/dev/null'
    )

    os.system(
        f'ffmpeg -y -framerate {FPS} -i "{OUT_DIR}/frame_%05d.png" '
        f'-i "{audio_enhanced}" -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium '
        f'-c:a aac -b:a 128k -shortest "{FINAL}"'
    )
    print(f"Video saved to {FINAL}")
    size_mb = FINAL.stat().st_size / (1024 * 1024)
    print(f"File size: {size_mb:.2f} MB")


if __name__ == "__main__":
    main()
