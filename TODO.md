## UPCOMING FEATURES

- Add FileReportGenerator
- Add token size to base-stats
- LoD Metric
- Agent configuration export (LLMs)
- Build a grpah/tree for all code nodes (functions/classes) that can later be used by an LLM (or programatically) to generate a high-level conceptual diagram with enough determinism/reproducibility to serve as a good abstraction for software engineering modeling (see Architecture Recovery or Reconstruction)

## BUGS TO FIX

- MC calculates a different value for layers than when you calculate the MC for
  a layer as if it was the 'codebase', these should be the same value ideally
- Correctly exclude "layers" if they are an excluded directory
- Exclude .gitignore directories by default
- Fix layer dependencies when imports are from src dir with pyproject configurable subpackages (see Harle example)
