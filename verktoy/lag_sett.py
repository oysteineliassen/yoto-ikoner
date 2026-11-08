#!/usr/bin/env python3
"""Lag et ikonsett fra en tekstfil med 16x16 pikselrutenett.

Bruk:
  python3 verktoy/lag_sett.py ikoner.txt --id sett-03 --navn "Musikk 2 (låt 19–21)" --cardId abc12

Format i ikoner.txt (én blokk per ikon, 16 linjer à 16 tegn):
  # 19_Tittel_paa_laaten
  ................
  ...
Tegnene er nøklene i PALETT under. '.' er gjennomsiktig.
Lager sett/<id>/*.png, oppdaterer sett.json og skriver forhåndsvisning til /tmp/<id>.png.
"""
import argparse, json, os, sys
from PIL import Image, ImageDraw, ImageFont

PALETT = {
 '.': None,
 'k': '#2b2b2b',  # nesten svart (øyne, detaljer)
 'W': '#ffffff', 'w': '#c9d3de',            # hvit / lys grå (kontur på hvitt)
 'Y': '#ffcc33', 'y': '#d98e00', 'C': '#ffe9a8',  # gul / mørk gul / blek gul (glød)
 'O': '#ff8c1a',
 'R': '#e53935', 'r': '#a8231f', 'P': '#ff8fb1',  # rød / mørk rød / rosa
 'G': '#5cbf4f', 'g': '#2e7d32',            # grønn / mørk grønn
 'B': '#5aa9f0', 'b': '#2a6fb8',            # blå / mørk blå
 'V': '#9c6ade', 'v': '#6b3fa0',            # lilla / mørk lilla
 'N': '#a0673f', 'n': '#5d3a22',            # brun / mørk brun
 'S': '#ffd2a8', 's': '#d9956a',            # hud / mørkere hud
 'H': '#f5d76e',                            # blondt hår
}

def les(fil):
    ikoner, navn, rader = {}, None, []
    for linje in open(fil, encoding='utf-8'):
        linje = linje.rstrip('\n')
        if linje.startswith('#'):
            if navn: ikoner[navn] = rader
            navn, rader = linje[1:].strip(), []
        elif linje.strip():
            rader.append(linje)
    if navn: ikoner[navn] = rader
    return ikoner

def main():
    a = argparse.ArgumentParser()
    a.add_argument('fil'); a.add_argument('--id', required=True); a.add_argument('--navn', required=True)
    a.add_argument('--cardId', default=None)
    a = a.parse_args()
    rot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ut = os.path.join(rot, 'sett', a.id); os.makedirs(ut, exist_ok=True)
    ikoner = les(a.fil); feil = False; bilder = []
    for navn, rader in ikoner.items():
        if len(rader) != 16 or any(len(r) != 16 for r in rader):
            print(f'FEIL: {navn} må være 16x16, fikk {len(rader)} rader med lengder {[len(r) for r in rader]}'); feil = True; continue
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        for y, r in enumerate(rader):
            for x, c in enumerate(r):
                if c not in PALETT: print(f'FEIL: ukjent tegn {c!r} i {navn} rad {y}'); feil = True; continue
                if PALETT[c]:
                    h = PALETT[c].lstrip('#'); im.putpixel((x, y), tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,))
        im.save(os.path.join(ut, navn + '.png')); bilder.append((navn, im))
    if feil: sys.exit(1)
    sj = os.path.join(rot, 'sett.json')
    sett = json.load(open(sj, encoding='utf-8'))
    sett = [s for s in sett if s['id'] != a.id]
    nytt = {'id': a.id, 'navn': a.navn, 'filer': [f'sett/{a.id}/{f}' for f in sorted(os.listdir(ut)) if f.endswith('.png')]}
    if a.cardId: nytt['cardId'] = a.cardId
    sett.append(nytt)
    json.dump(sett, open(sj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # forhåndsvisning
    S = 160; n = len(bilder); kol = min(n, 5); rad = (n + kol - 1) // kol
    ark = Image.new('RGB', (kol * (S + 30) + 30, rad * (S + 60) + 30), '#121212'); d = ImageDraw.Draw(ark)
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    except Exception: f = None
    for i, (navn, im) in enumerate(bilder):
        x = 30 + (i % kol) * (S + 30); y = 30 + (i // kol) * (S + 60)
        d.rounded_rectangle([x - 5, y - 5, x + S + 5, y + S + 5], 10, fill='#2a2a2a')
        st = im.resize((S, S), Image.NEAREST); ark.paste(st, (x, y), st)
        d.text((x, y + S + 12), navn.replace('_', ' ')[:22], fill='white', font=f)
    ark.save(f'/tmp/{a.id}.png')
    print(f'OK: {len(bilder)} ikoner i sett/{a.id}, forhåndsvisning /tmp/{a.id}.png')

if __name__ == '__main__': main()
