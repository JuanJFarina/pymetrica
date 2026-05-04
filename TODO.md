## UPCOMING FEATURES

- Add FileReportGenerator
- Add JSONReportGenerator
- Metric Primitive Obsesiveness (either full primitive check, or dict/tuple check)
-

## BUGS TO FIX

- MC calculates a different value for layers than when you calculate the MC for
  a layer as if it was the 'codebase', these should be the same value ideally
-

## QUALITY OF LIFE IDEAS

- Convert base-stats in a proper metric so it can be used inside run-all
- Metrics store per-file score, in order to show in threshold failing, configurable through pyproject.toml
- Add settings property flag that checks if threshold is 0 or not, and returns a bool
- 