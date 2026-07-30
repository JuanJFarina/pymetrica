from pymetrica.models.report_generator import ReportGenerator
from pymetrica.report_generators.basic_hook_report import BasicHookReport

from .basic_terminal_report import BasicTerminalReport
from .json_report import JsonReport

REPORTS_MAPPING: dict[str, type[ReportGenerator]] = {
    "BASIC_TERMINAL": BasicTerminalReport,
    "BASIC_HOOK": BasicHookReport,
    "JSON": JsonReport,
}
