import re
import shutil

F = r"c:\Users\CVBYW\Documents\Kommune\2026-08-25-queeres-wohnprojekt-design.md"
BAK = F + ".vor-reparatur.bak"

# vor einem oeffnenden Marker darf auch Satzzeichen stehen, danach nur Wortzeichen
BEFORE = re.compile(r"[\w§€%,;:.!?)]", re.UNICODE)
WORD = re.compile(r"[\w§€%]", re.UNICODE)
RUN = re.compile(r"\*+")


def fix_line(line):
    """Repariert fehlende Leerzeichen um Emphase-Marker, richtungsabhängig."""
    if line.lstrip().startswith("```"):
        return line, 0
    bold_open = False
    ital_open = False
    out = []
    pos = 0
    fixes = 0
    for m in RUN.finditer(line):
        run = m.group(0)
        out.append(line[pos:m.start()])
        prev = line[m.start() - 1] if m.start() > 0 else ""
        nxt = line[m.end()] if m.end() < len(line) else ""

        if len(run) == 2:
            opening = not bold_open
            bold_open = not bold_open
        elif len(run) == 1:
            opening = not ital_open
            ital_open = not ital_open
        else:
            out.append(run)
            pos = m.end()
            continue

        if opening and prev and BEFORE.match(prev):
            out.append(" ")
            fixes += 1
        out.append(run)
        if (not opening) and nxt and WORD.match(nxt):
            out.append(" ")
            fixes += 1
        pos = m.end()
    out.append(line[pos:])
    return "".join(out), fixes


def main():
    shutil.copyfile(F, BAK)
    with open(F, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    total = 0
    in_code = False
    new_lines = []
    for line in lines:
        if line.lstrip().startswith("```"):
            in_code = not in_code
            new_lines.append(line)
            continue
        if in_code:
            new_lines.append(line)
            continue
        fixed, n = fix_line(line)
        total += n
        new_lines.append(fixed)

    with open(F, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(new_lines))

    print("Reparaturen:", total)


main()
