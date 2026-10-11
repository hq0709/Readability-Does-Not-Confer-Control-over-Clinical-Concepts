"""What the tables show and how they are set, applied to the generated .tex.

The builders decide what is computed; this decides what is printed. It runs after them and the .tex is then
the artefact -- rerunning a builder undoes it, which is why it is one command rather than a hand edit.

It does four things:

  shell      one float policy, one column separation, one type size, and \\fitwidth everywhere. \\fitwidth shrinks a table
             wider than the line and leaves a narrower one alone; a bare \\resizebox magnifies a narrow
             table above body size, which is what made the tables look set at different sizes. Every live
             table spans both columns: measured against the ACL column the narrowest is 1.55 times too
             wide and the widest 2.9 times, so a single-column float would shrink the smallest of them to
             two thirds of body size. A starred float is placed at a column top or on a float page -- `h`
             and `b` are not available to it -- so the appendix policy is [tp], not [htbp].
  intervals  the columns that printed a bootstrap interval. The grades are read from the estimates now, so
             there is no interval to report and a column of them is a column about a method the paper no
             longer uses.
  unresolved the third outcome of the bound rule. Comparing measured effects leaves two, so the column
             group is all zeros and the word is gone from the captions.
  check      every row against its column spec, with a brace-matching reader for the spec, because
             `\\{([^}]*)\\}` stops inside `@{\\hspace{3pt}}` and reads a thirteen-column table as two.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

T = Path(__file__).resolve().parents[1] / "tables"
LIVE = """table_cf_altdir table_cf_ansdir table_cf_attr table_cf_geometry table_cf_main table_cf_models
 table_cf_own table_cf_pairs table_cf_refit table_cf_seed table_cf_semend table_cf_validation
 table_seed_mass""".split()
BODY = {"table_cf_main"}
# Tables that must not take a float page of their own. Each ownership table is 39% of the text
# height, so two of them plus captions fill 87% -- over the 85% a double-column float page needs,
# which is how all three ended up on pages with no prose. [t] keeps them at the top of a text page.
TOP_ONLY = {"table_cf_own"}
# (file, 1-based index of the table environment inside it) that is set in one column instead of two.
# The COCO ownership table is 234 pt wide at 8 pt against a 219 pt column; 1.5 pt of column separation
# brings it to 213 pt, so it fits one column at the same type size as every other table and can sit
# beside the prose rather than spanning the page.
SINGLE_COLUMN = {("table_cf_own", 3): "1.5pt"}


def braced(s: str, i: int) -> tuple[str, int]:
    assert s[i] == "{"
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == "{") - (s[j] == "}")
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError("unbalanced brace")


def ncols(spec: str) -> int:
    n, i = 0, 0
    while i < len(spec):
        c = spec[i]
        if c in "lcr":
            n += 1; i += 1
        elif c == "p" and i + 1 < len(spec) and spec[i + 1] == "{":
            n += 1; _, i = braced(spec, i + 1)
        elif c in "@!>|<" and i + 1 < len(spec) and spec[i + 1] == "{":
            _, i = braced(spec, i + 1)
        elif c == "*" and i + 1 < len(spec) and spec[i + 1] == "{":
            k, i = braced(spec, i + 1); sub, i = braced(spec, i)
            n += int(k) * ncols(sub)
        else:
            i += 1
    return n


def single_column(name: str, s: str) -> str:
    """Put the designated table environments back into one column, with their own column separation.

    A one-column table sits beside the prose instead of spanning the page, which is the only way a
    table interleaves with the text rather than displacing it. It is worth doing only when the table
    fits the column at the shared type size; shrinking the type to force a fit would undo \\cftabsize.
    """
    starts = [m.start() for m in re.finditer(r"\\begin\{table\*\}", s)]
    for (f, idx), colsep in sorted(SINGLE_COLUMN.items(), reverse=True):
        if f != name or idx > len(starts):
            continue
        a = starts[idx - 1]
        b = s.index("\\end{table*}", a) + len("\\end{table*}")
        block = s[a:b]
        block = block.replace("\\begin{table*}", "\\begin{table}", 1)
        block = block.replace("\\end{table*}", "\\end{table}")
        block = re.sub(r"\\setlength\{\\tabcolsep\}\{[0-9.]+pt\}",
                       "\\\\setlength{\\\\tabcolsep}{" + colsep + "}", block)
        s = s[:a] + block + s[b:]
    return s


def shell(name: str) -> None:
    p = T / f"{name}.tex"; s = p.read_text()
    where = "[t]" if name in BODY or name in TOP_ONLY else "[tp]"
    s = re.sub(r"\\begin\{table\*?\}(\[[^\]]*\])?", "\\\\begin{table*}" + where, s)
    s = s.replace("\\end{table}", "\\end{table*}")
    s = re.sub(r"\\setlength\{\\tabcolsep\}\{[0-9.]+pt\}", r"\\setlength{\\tabcolsep}{3pt}", s)
    if "tabcolsep" not in s:
        s = s.replace("\\centering\n", "\\centering\n\\setlength{\\tabcolsep}{3pt}\n", 1)
    for raw in (r"\resizebox{\linewidth}{!}{%", r"\resizebox{\textwidth}{!}{%",
                r"\adjustbox{max width=\linewidth}{%"):
        s = s.replace(raw, "\\fitwidth{%")
    # the size goes inside \fitwidth, which is a group, so it reaches the tabular and not the caption
    # the pass runs more than once over the same file, so collapse any size already inserted
    # before inserting it: a plain replace is not idempotent and stacked a copy per run.
    s = re.sub(r"(?:\\cftabsize\n)+", "", s)
    s = s.replace("\\fitwidth{%\n", "\\fitwidth{%\n\\cftabsize\n")
    s = single_column(name, s)        # last: it sets its own column separation
    p.write_text(s)


def drop_pairs_interval() -> bool:
    """table_cf_pairs counted, per pair, how many of six concepts had an interval clear of zero."""
    p = T / "table_cf_pairs.tex"; s = p.read_text()
    if r"\Delta O_q$ CI" not in s:
        return False
    s = s.replace(r"\begin{tabular}{llcrrrrr}", r"\begin{tabular}{llcrrrr}")
    s = s.replace(r" & \multicolumn{1}{c}{$\Delta O_q$ CI} & \multicolumn{2}{c}{$|\Delta O_q|$}",
                  r" & \multicolumn{2}{c}{$|\Delta O_q|$}")
    s = s.replace(r"\cmidrule(lr){5-6}\cmidrule(lr){7-8}", r"\cmidrule(lr){4-5}\cmidrule(lr){6-7}")
    s = s.replace(r"&  &  & \multicolumn{1}{c}{$\not\ni 0$} & \multicolumn{1}{c}{median}",
                  r"&  &  & \multicolumn{1}{c}{median}")
    s = re.sub(r"(& (?:bit-identical|bf16-equal)) & \d/\d & ", r"\1 & ", s)
    s = s.replace(r", with paired patient-bootstrap 95\% intervals;", r";")
    p.write_text(s); return True


def drop_seed_interval() -> bool:
    """table_cf_seed printed the interval beside O_q inside the same cell."""
    p = T / "table_cf_seed.tex"; s = p.read_text()
    out = s.replace(r"$O_q$ [95\% CI]", r"$O_q$")
    out = re.sub(r"(-?[\d.]+) \[-?[\d.]+, *-?[\d.]+\]", r"\1", out)
    if out == s:
        return False
    p.write_text(out); return True


def drop_seed_mass_columns() -> bool:
    """table_seed_mass carried a 95% CI column in its top panel and a lower-bound column in its bottom one."""
    p = T / "table_seed_mass.tex"; s = p.read_text()
    if r"95\% CI" not in s and "Minimum LCB" not in s:
        return False
    s = s.replace(r"\begin{tabular}{lrrrrr}", r"\begin{tabular}{lrrrr}")
    s = s.replace(r"Prompt & Clinical margin & 95\% CI & Mass effect", r"Prompt & Clinical margin & Mass effect")
    s = re.sub(r"^((?:Standard yes/no|A-present|B-present) & \$[-\d.]+\$) & \$\[[^\]]*\]\$ & ", r"\1 & ", s, flags=re.M)
    s = s.replace(r"Condition & Clinical margin & Minimum LCB & Mass effect & Random max & \\",
                  r"Condition & Clinical margin & Mass effect & Random max & \\")
    s = re.sub(r"^(\\textit\{\w+\}/[AB]-present & \$?-?[\d.]+\$?) & \$?-?[\d.]+\$? & ", r"\1 & ", s, flags=re.M)
    p.write_text(s); return True


def drop_refit_unresolved() -> bool:
    """The bound rule's third outcome. Its three columns are all zeros now."""
    p = T / "table_cf_refit.tex"; s = p.read_text()
    if r"\multicolumn{3}{c}{unresolved}" not in s:
        return False
    s = s.replace(r"\begin{tabular}{lrrrrrrrrrrrrrrr}", r"\begin{tabular}{lrrrrrrrrrrrr}")
    s = s.replace(r" & \multicolumn{3}{c}{unresolved}", "")
    s = s.replace(r"\cmidrule(lr){4-7}\cmidrule(lr){8-10}\cmidrule(lr){11-13}\cmidrule(lr){14-15}",
                  r"\cmidrule(lr){4-7}\cmidrule(lr){8-10}\cmidrule(lr){11-12}")
    # the second header row and every body row lose the three cells at positions 11-13
    def cut(line: str) -> str:
        cells = line.split(" & ")
        return " & ".join(cells[:10] + cells[13:]) if len(cells) >= 14 else line
    out = []
    for line in s.splitlines():
        out.append(cut(line) if line.count("&") >= 13 and "multicolumn{3}" not in line else line)
    s = "\n".join(out) + "\n"
    s = s.replace("(owned, stronger competitor, unresolved, fixed-family advantage without the reference)",
                  "(owned, stronger competitor, advantage without the reference)")
    p.write_text(s); return True


def drop_own_unresolved() -> bool:
    p = T / "table_cf_own.tex"; s = p.read_text()
    out = s.replace(", unresolved", "").replace("unresolved, ", "")
    if out == s:
        return False
    p.write_text(out); return True


def check() -> int:
    bad = 0
    for name in LIVE:
        s = (T / f"{name}.tex").read_text()
        for m in re.finditer(r"\\begin\{tabular\}", s):
            spec, end = braced(s, s.index("{", m.end()))
            n = ncols(spec)
            body = s[end:s.find(r"\end{tabular}", end)]
            for line in body.splitlines():
                if "&" not in line or line.strip().startswith("%"):
                    continue
                k = line.count("&") + 1 + sum(int(x) - 1 for x in re.findall(r"\\multicolumn\{(\d+)\}", line))
                if k != n:
                    print(f"  COLUMN MISMATCH {name}: spec {n}, row {k}: {line.strip()[:70]}")
                    bad += 1
    return bad


for t in LIVE:
    shell(t)
done = [n for n, f in (("pairs interval", drop_pairs_interval), ("seed interval", drop_seed_interval),
                       ("seed-mass columns", drop_seed_mass_columns),
                       ("refit unresolved", drop_refit_unresolved),
                       ("own unresolved", drop_own_unresolved)) if f()]
print(f"shell normalised in {len(LIVE)} tables; removed: {', '.join(done) if done else 'nothing left to remove'}")
sys.exit(1 if check() else 0)
