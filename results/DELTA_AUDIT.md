# Delta audit — what moved and why

Variant: `clean`. Heuristic attribution is keyword-overlap only (labelled heuristic; not authoritative).

### llama3_2b/H2/k3 (clean)

- baseline L-GED **162.5** → patched **158.0** (Δ **-4.5**)
- component Δ (weight): v_miss +1.0, v_halluc +0.0, e_diff -5.5 → **driver: e_diff**
- counts: v_miss 63→64, v_halluc 0→0, e_diff 3→1, v_misground 2→2

**Patched misgroundings** (teacher→student citation, verdict of student cite):
- R3→R2: `CO AIA 6-1-1701(7)` vs `NYC LL 144 §20-871` (student *verified*)
- R4→R1: `CO AIA 6-1-1701(9)` vs `CO AIA §6-1-1703(2)(a)` (student *verified*)

### gpt5/M2/k1 (clean)

- baseline L-GED **96.5** → patched **113.0** (Δ **+16.5**)
- component Δ (weight): v_miss +2.5, v_halluc +0.0, e_diff +14.0 → **driver: e_diff**
- counts: v_miss 23→20, v_halluc 0→0, e_diff 16→18, v_misground 6→3

**Recovered teacher rules (2)** (in baseline v_miss, matched after patching):
- **R8** `CO AIA Section 6-1-1703(2)` → *verified*  [heuristic: p_215af45aa260]
- **R9** `CO AIA Section 6-1-1703(6)` → *verified*  [heuristic: p_215af45aa260]

**Newly missed** (matched in baseline, missed after patching): R11, R3, R5

**Patched misgroundings** (teacher→student citation, verdict of student cite):
- R12→R5: `CO AIA Section 6-1-1703(2)(f)-(g)` vs `Colo. Rev. Stat. § 6-1-1703(3)-(4)` (student *verified*)
- R15→R3: `CO AIA Section 6-1-1703(2)(b)(I)` vs `Colo. Rev. Stat. § 6-1-1703(2)(b)` (student *verified*)
- R16→R2: `CO AIA Section 6-1-1703(2)(a)(III)` vs `Colo. Rev. Stat. § 6-1-1703(2)(a)` (student *verified*)

### gpt5/M2/k3 (clean)

- baseline L-GED **96.5** → patched **103.0** (Δ **+6.5**)
- component Δ (weight): v_miss -13.5, v_halluc +7.5, e_diff +12.5 → **driver: v_miss**
- counts: v_miss 23→20, v_halluc 0→3, e_diff 16→16, v_misground 6→0

**Recovered teacher rules (5)** (in baseline v_miss, matched after patching):
- **R10** `CO AIA Section 6-1-1701(8)` → *verified*  [heuristic: p_215af45aa260, p_4b3934a5ecdc, p_b9693e605915]
- **R2** `CO AIA Section 6-1-1701(3)(f)` → *verified*  [heuristic: p_215af45aa260, p_4b3934a5ecdc, p_b9693e605915]
- **R6** `CO AIA Section 6-1-1701(5)` → *verified*  [heuristic: p_215af45aa260, p_4b3934a5ecdc, p_b9693e605915]
- **R8** `CO AIA Section 6-1-1703(2)` → *verified*  [heuristic: p_215af45aa260, p_4b3934a5ecdc, p_b9693e605915]
- **R9** `CO AIA Section 6-1-1703(6)` → *verified*  [heuristic: p_215af45aa260, p_4b3934a5ecdc, p_b9693e605915]

**Newly missed** (matched in baseline, missed after patching): R14

### gpt5/M2/k5 (clean)

- baseline L-GED **96.5** → patched **100.5** (Δ **+4.0**)
- component Δ (weight): v_miss +11.5, v_halluc +5.0, e_diff -12.5 → **driver: e_diff**
- counts: v_miss 23→27, v_halluc 0→2, e_diff 16→10, v_misground 6→6

**Recovered teacher rules (2)** (in baseline v_miss, matched after patching):
- **R8** `CO AIA Section 6-1-1703(2)` → *verified*  [heuristic: p_b6ade26371ca, p_cb80acec9ac0, p_b9693e605915, p_215af45aa260, p_4b3934a5ecdc]
- **R9** `CO AIA Section 6-1-1703(6)` → *verified*  [heuristic: p_b6ade26371ca, p_cb80acec9ac0, p_b9693e605915, p_215af45aa260, p_4b3934a5ecdc]

**Newly missed** (matched in baseline, missed after patching): R11, R14

**Patched misgroundings** (teacher→student citation, verdict of student cite):
- R3→R1: `CO AIA Section 6-1-1701(7)` vs `C.R.S. § 6-1-1701` (student *verified*)
- R5→R6: `CO AIA Section 6-1-1701(6)` vs `C.R.S. § 6-1-1703(2)(d)` (student *verified*)
- R8→R2: `CO AIA Section 6-1-1703(2)` vs `C.R.S. § 6-1-1703(2)(a)` (student *verified*)
- R12→R5: `CO AIA Section 6-1-1703(2)(f)-(g)` vs `C.R.S. § 6-1-1703(2)(c)` (student *verified*)
- R13→R7: `CO AIA Section 6-1-1704` vs `C.R.S. § 6-1-1703(2)(f)` (student *verified*)
- R15→R4: `CO AIA Section 6-1-1703(2)(b)(I)` vs `C.R.S. § 6-1-1703(2)(b)` (student *verified*)
