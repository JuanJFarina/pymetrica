flowchart TD
    subgraph "CLI Layer"
        CLIParser["CLI Parser"]
    end

    subgraph "File Parsing Layer"
        DirReader["Directory Reader"]
    end

    subgraph "Metrics Calculator [Builder Pattern]"
        MetricsCalc["Metrics Calculator"]
        LLOC["LLOC / File ratio"]
        CC["CC / N of Functions"]
        ALOC["Abstract Lines Of Code %"]
        MI["Maintainability Index"]
    end

    subgraph "Report Generator [Strategy Pattern]"
        ReportGen["Report Generator"]
        BasicReport["Basic Terminal Report"]
        PrettyReport["Pretty Terminal Report"]
        JSONReport["JSON Report"]
    end

    CLIParser --> DirReader
    DirReader --> MetricsCalc

    MetricsCalc --> LLOC
    MetricsCalc --> CC
    MetricsCalc --> ALOC
    MetricsCalc --> MI

    LLOC --> ReportGen
    CC --> ReportGen
    ALOC --> ReportGen
    MI --> ReportGen

    ReportGen --> BasicReport
    ReportGen --> PrettyReport
    ReportGen --> JSONReport

    %% Notes attached to nodes
    DirReader --- NoteCodebase
    NoteCodebase["Note: Produces a 'Codebase' structure with Files, Lines, Sourcecode, and raw stats (LLOC, number of files, functions, etc.)"]

    MetricsCalc --- NoteMetric
    NoteMetric["Note: Produces a list of 'Metric' objects. Each metric is a concrete implementation."]

    ReportGen --- NoteReport
    NoteReport["Note: Abstract class for outputting reports. Output type selected via CLI."]
