# -*- coding: utf-8 -*-
"""Ocean Freight Demurrage OSRA-22 Dispute Generator for GenPark Agentic Commerce."""
import json
from typing import Dict, Any, List

class FreightDemurrageDisputeDismissalGenerator:
    @staticmethod
    def audit_demurrage_appointment_unavailability(container_num: str, terminal_appointment_attempts: List[Dict[str, Any]], billed_demurrage_usd: float) -> Dict[str, Any]:
        # Under FMC Rule 46 C.F.R. Part 541, carriers cannot bill demurrage if cargo is unavailable or appointment slots are closed
        blocked_days = 0
        for attempt in terminal_appointment_attempts:
            if not attempt.get("appointment_available", False) or attempt.get("terminal_dual_transaction_lock", False):
                blocked_days += 1

        unlawful_ratio = min(1.0, blocked_days / max(1, len(terminal_appointment_attempts)))
        refundable_usd = round(billed_demurrage_usd * unlawful_ratio, 2)
        return {
            "container_number": container_num,
            "total_days_logged": len(terminal_appointment_attempts),
            "documented_terminal_lockout_days": blocked_days,
            "unlawful_demurrage_amount_usd": refundable_usd,
            "osra22_violation": blocked_days > 0,
            "statutory_status": "CHARGE_UNENFORCEABLE_PER_FMC_FINAL_RULE" if blocked_days > 0 else "TERMINAL_AVAILABLE"
        }

    @staticmethod
    def generate_fmc_inaccurate_invoice_charge_complaint(carrier_scac: str, container_num: str, invoice_amount_usd: float, dispute_reasons: List[str]) -> Dict[str, Any]:
        memo = f"""FORMAL CHARGE COMPLAINT (FMC OSRA-22 / 46 U.S.C. § 41104)

To: Ocean Common Carrier [{carrier_scac}] Billing Escalations
Re: Container {container_num}
Disputed Invoiced Charge: ${invoice_amount_usd:.2f}

DEMAND FOR IMMEDIATE DISMISSAL OF IMPROPER INVOICE

The demurrage charges billed under this invoice violate 46 C.F.R. Part 541 due to:
{'; '.join(dispute_reasons)}.

Pursuant to federal law, if a billing party fails to comply with statutory billing rules, the invoiced party is not required to pay the charge. Demand is hereby made to dismiss this invoice within 30 days.
"""
        return {
            "carrier": carrier_scac,
            "container": container_num,
            "disputed_sum_usd": invoice_amount_usd,
            "charge_complaint_dossier": memo,
            "regulatory_recourse": "Submit to FMC Office of Consumer Affairs and Dispute Resolution Services (CADRS)."
        }
