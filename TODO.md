## UPCOMING FEATURES

- Add FileReportGenerator
- Add token size to base-stats
- LoD Metric
- Agent configuration export (LLMs)

## BUGS TO FIX

- MC calculates a different value for layers than when you calculate the MC for
  a layer as if it was the 'codebase', these should be the same value ideally
- Correctly exclude "layers" if they are an excluded directory
- Exclude .gitignore directories by default
