```mermaid
flowchart TD
    subgraph "CLI Layer"
        CLIParser["CLI commands"]
    end

    subgraph "Parsing Layer"
        DirReader["Codebase parser"]
        Codebase["Codebase model"]
    end

    subgraph "Metric Calculators"
        MetricsCalc["Metric calculators"]
        ALOC["Abstract Lines Of Code %"]
        CC["Cyclomatic Complexity"]
        HV["Halstead Volume"]
        MC["Maintainability Cost"]
        LI["Instability"]
    end

    subgraph "Reporting Layer"
        ReportGen["Report generator"]
        BasicReport["Basic terminal report"]
        Diagram["Mermaid diagram output"]
    end

    CLIParser --> DirReader
    DirReader --> Codebase
    Codebase --> MetricsCalc

    MetricsCalc --> ALOC
    MetricsCalc --> CC
    MetricsCalc --> HV
    MetricsCalc --> MC
    MetricsCalc --> LI

    ALOC --> ReportGen
    CC --> ReportGen
    HV --> ReportGen
    MC --> ReportGen
    LI --> ReportGen

    ReportGen --> BasicReport
    DirReader --> Diagram

    %% Notes attached to nodes
    DirReader --- NoteCodebase
    NoteCodebase["Note: Builds a Codebase with root files, top-level layers, and parser stats."]

    MetricsCalc --- NoteMetric
    NoteMetric["Note: Produces Metric objects for ALOC, CC, HV, MC, and instability."]

    ReportGen --- NoteReport
    NoteReport["Note: BASIC_TERMINAL is the only bundled report backend today."]
```
