# Sokoban Worklog

## Current Baseline

- Main playable source: `sokoban/sokoban.bas`
- Turbo experiment source: `sokoban/soturbo.bas`
- Default loader: `fdd/autoexec.bas`
- Default disk image build target: `disk/sokoban-built.dsk`

## What Was Improved In `sokoban.bas`

- Restored visible stage rendering and player rendering on the current SCREEN 1 tile setup.
- Replaced the original placeholder stages with stage data derived from:
  - <https://github.com/begoon/sokoban-maps/blob/master/maps/sokoban-maps-60-plain.txt>
  - Stages 1 through 5 only.
- Expanded the map array to fit larger imported stages:
  - `DIM MAP(12,21)`
- Kept the star-based clear indicator in the upper-left corner.
- Adjusted the ending screen so the player sprite appears to the right of `MSX SOKOBAN V2`.

## HUD / Rendering Notes

- HUD attempts in SCREEN 2/graphics-style handling were removed from the baseline.
- A persistent text HUD caused rendering conflicts and visible black-tile refresh overhead.
- The current baseline keeps the screen simpler and faster by avoiding HUD redraw work.

## BASICKUN / Turbo Investigation

We explored two different things that looked similar but are not identical:

1. `BASICKUN.ROM`
   - Present locally in `bin/BASICKUN.ROM`
   - Cartridge-style BASIC Kun environment

2. `MSX-BASIC Kun Turbo`
   - Documented in:
     - <https://github.com/sndpl/msx-basic-kun-turbo-manual>
   - Appears to be a different environment with stricter rules and disk-based loading flow

### Findings

- The external docs clearly mention:
  - `CALL RUN`
  - `CALL TURBO ON`
  - `CALL TURBO OFF`
- But the documented restrictions are strict:
  - `SCREEN` grammar differs
  - `PLAY` is unsupported in compiled sections
  - `DIM` placement is constrained
  - array handling is sensitive
- In practice, trying to apply the Turbo manual directly to the local `BASICKUN.ROM` setup caused repeated compatibility errors.

### Current Conclusion

- Keep `sokoban.bas` as the stable baseline.
- Keep `soturbo.bas` as an isolated experiment file only.
- Do not treat the current turbo experiment as production-ready yet.
- If turbo work continues later, it should likely follow one of these paths:
  - Find the real `MSX-BASIC Kun Turbo` runtime/binary and test on the correct machine setup
  - Or re-approach optimization specifically for the local `BASICKUN.ROM` behavior instead of the Turbo manual

## Disk Build

The Python builder is available at:

- `python-test/build_sokoban_dsk.py`

It creates a bootable DSK containing:

- `AUTOEXEC.BAS`
- `SOKOBAN.BAS`

Default output:

- `disk/sokoban-built.dsk`

WebMSX launch link:

- <https://webmsx.org/?DISKA_URL=https://raw.githubusercontent.com/honux77/learn-msx-basic/master/disk/sokoban-built.dsk>

## Finish State

- `sokoban.bas` is the baseline to keep using.
- `soturbo.bas` remains in the repo as a separate experimental branch in file form.
- The project can be packaged into a DSK from the baseline source.
