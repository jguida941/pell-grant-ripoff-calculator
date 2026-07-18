"""All the math, kept pure: raw input values in, computed numbers out.

Pell model (SNHU Financial Aid Offer Terms and Conditions):
  - Six 8-week terms per year, grouped into three 16-week semesters.
    A semester (two consecutive terms) is the Pell payment period.
  - Full-time is 12 credits per semester. Enrollment intensity scales the
    award: intensity = semester credits / 12, capped at 100%.
  - Pell per semester = (yearly award / 2) x intensity; per term = half that.
  - Year-Round Pell funds a third semester at the same rate (up to 150% of
    the award per year), so more terms never shrinks the per-term amount.
"""

import math

from .constants import MONTHS_PER_TERM, WEEKS_PER_MONTH


def compute(v):
    """v is a dict of raw input values keyed the same as the UI spinboxes."""
    c = {"in": dict(v)}

    for tag in ("o", "n"):
        gross_wk = v[f"{tag}_wage"] * v[f"{tag}_hours"]
        take_wk = gross_wk * (1 - v[f"{tag}_tax"] / 100.0)
        c[f"{tag}_gross_wk"] = gross_wk
        c[f"{tag}_take_wk"] = take_wk
        c[f"{tag}_take_mo"] = take_wk * WEEKS_PER_MONTH

    tuition_term = v["per_credit"] * v["cpt"]
    intensity = min(1.0, (v["cpt"] * 2) / 12.0)
    c["tuition_term"] = tuition_term
    c["intensity"] = intensity
    for tag in ("o", "n"):
        pell_term = (v[f"{tag}_pell"] / 2.0) * intensity / 2.0
        owed_term = max(0.0, tuition_term - pell_term)
        c[f"{tag}_pell_term"] = pell_term
        c[f"{tag}_owed_term"] = owed_term
        c[f"{tag}_school_mo"] = owed_term / MONTHS_PER_TERM

    c["bill_items"] = [
        ("Child support", v["cs"]), ("Rent", v["rent"]), ("Food", v["food"]),
        ("Electric", v["electric"]), ("Internet", v["internet"]), ("Phone", v["phone"]),
        ("Transportation / gas", v["transport"]), ("Medical", v["medical"]),
        ("Other", v["other"]),
    ]
    c["bills"] = sum(val for _, val in c["bill_items"])
    c["o_left_mo"] = c["o_take_mo"] - c["bills"] - c["o_school_mo"]
    c["n_left_mo"] = c["n_take_mo"] - c["bills"] - c["n_school_mo"]
    # True calendar-month average: 52 weeks / 12 months, not 4 paychecks.
    # Bills like rent are per calendar month, so this is the honest average.
    for tag in ("o", "n"):
        c[f"{tag}_take_mo_cal"] = c[f"{tag}_take_wk"] * 52 / 12
        c[f"{tag}_left_mo_cal"] = c[f"{tag}_take_mo_cal"] - c["bills"] - c[f"{tag}_school_mo"]

    c["terms_left"] = int(v["terms_left"])
    c["o_registered_cost"] = c["terms_left"] * c["o_owed_term"]
    # Summer crossover: a term spanning July 1 can be paid from EITHER award
    # year (school's call, per the FSA Handbook). Terms the school assigns to
    # the old award year still cost the OLD Pell rate.
    cross = min(int(v.get("crossover_terms", 0)), c["terms_left"])
    c["crossover_terms"] = cross
    c["n_registered_cost"] = (cross * c["o_owed_term"]
                              + (c["terms_left"] - cross) * c["n_owed_term"])

    # Unscheduled credits (required minus applied), priced term by term.
    unsched = max(0, int(v["req"]) - int(v["applied"]))
    cpt = max(1, int(v["cpt"]))
    c["unsched"] = unsched
    c["unsched_classes"] = math.ceil(unsched / 3)
    c["unsched_terms"] = math.ceil(unsched / cpt) if unsched else 0
    for tag in ("o", "n"):
        left = unsched
        owed = 0.0
        for _ in range(c["unsched_terms"]):
            cr = min(cpt, left)
            left -= cr
            owed += max(0.0, cr * v["per_credit"] - c[f"{tag}_pell_term"])
        c[f"{tag}_final_snhu"] = owed

    c["sophia_cost"] = v["sophia_mo"] * v["sophia_months"]
    c["n_grad_snhu"] = c["n_registered_cost"] + c["n_final_snhu"]
    c["n_grad_sophia"] = c["n_registered_cost"] + c["sophia_cost"]
    c["o_grad_snhu"] = c["o_registered_cost"] + c["o_final_snhu"]
    c["sophia_savings"] = c["n_final_snhu"] - c["sophia_cost"]
    c["pell_cut"] = v["o_pell"] - v["n_pell"]
    return c
