from reportbro import Report, ReportBroError
from report.services import ReportService
from .services import ReportDataService
from .reports import pbh, pbp, pbc_H, pbc_P


def _report(prms):
    show_claims = prms.get("showClaims", "false") == 'true'
    group = prms.get("group", "H")
    if show_claims:
        report = "claim_batch_pbc_"+group
        default = pbc_H.template if group == 'H' else pbc_P.template
    elif group == 'H':
        report = "claim_batch_pbh"
        default = pbh.template
    else:
        report = "claim_batch_pbp"
        default = pbp.template
    return report, default


def report(request):
    report_service = ReportService(request.user)
    report, default = _report(request.GET)
    report_data_service = ReportDataService(request.user)
    data = report_data_service.fetch(request.GET)
    return report_service.process(report, {'data': data}, default)
