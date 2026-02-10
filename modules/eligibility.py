"""
Eligibility engine for government scheme matching.
Uses rule-based logic to check user eligibility against scheme criteria.
"""

from dataclasses import dataclass, field
from typing import Optional

from app.logging_config import get_logger

logger = get_logger("eligibility")


@dataclass
class UserProfile:
    """User profile for eligibility checking."""

    # Demographics
    age: Optional[int] = None
    gender: Optional[str] = None  # "male" / "female"
    state: str = "maharashtra"

    # Economic
    annual_income: Optional[int] = None
    is_bpl: Optional[bool] = None
    ration_card_type: Optional[str] = None  # "yellow" / "orange" / "white" / "none"

    # Social
    category: Optional[str] = None  # "SC" / "ST" / "OBC" / "NT" / "SBC" / "General"
    marital_status: Optional[str] = None  # "married"/"single"/"widowed"/"divorced"

    # Occupation
    is_farmer: Optional[bool] = None
    has_land: Optional[bool] = None
    land_acres: Optional[float] = None
    is_govt_employee: Optional[bool] = None
    is_income_tax_payer: Optional[bool] = None

    # Housing
    has_pucca_house: Optional[bool] = None
    has_lpg_connection: Optional[bool] = None

    # Documents
    has_aadhaar: Optional[bool] = None
    has_bank_account: Optional[bool] = None
    has_job_card: Optional[bool] = None


@dataclass
class EligibilityResult:
    """Result of an eligibility check for a single scheme."""

    scheme_name: str
    scheme_name_mr: str
    is_eligible: str  # "Yes" / "No" / "Maybe"
    confidence: float  # 0.0 to 1.0
    met_criteria: list[str] = field(default_factory=list)
    unmet_criteria: list[str] = field(default_factory=list)
    missing_info: list[str] = field(default_factory=list)
    benefit_summary: str = ""
    how_to_apply: str = ""
    source_url: str = ""


class EligibilityEngine:
    """
    Rule-based eligibility engine for government schemes.

    Checks user profile against predefined scheme rules
    and returns matched schemes with eligibility status.
    """

    def __init__(self):
        self._schemes = self._load_scheme_rules()
        logger.info(f"Eligibility engine loaded with {len(self._schemes)} schemes")

    def check_all(self, profile: UserProfile) -> list[EligibilityResult]:
        """
        Check eligibility for all schemes.

        Args:
            profile: User's profile data.

        Returns:
            List of EligibilityResult sorted by eligibility confidence.
        """
        results = []
        for scheme_id, checker in self._schemes.items():
            result = checker(profile)
            results.append(result)

        # Sort: eligible first, then maybe, then no
        priority = {"Yes": 0, "Maybe": 1, "No": 2}
        results.sort(key=lambda r: (priority.get(r.is_eligible, 2), -r.confidence))

        eligible_count = sum(1 for r in results if r.is_eligible == "Yes")
        maybe_count = sum(1 for r in results if r.is_eligible == "Maybe")
        logger.info(
            f"Eligibility check: {eligible_count} eligible, "
            f"{maybe_count} maybe, profile={profile}"
        )
        return results

    def check_scheme(
        self, profile: UserProfile, scheme_name: str
    ) -> Optional[EligibilityResult]:
        """Check eligibility for a specific scheme."""
        scheme_key = scheme_name.lower().replace(" ", "_")
        checker = self._schemes.get(scheme_key)
        if checker:
            return checker(profile)
        logger.warning(f"Scheme not found: {scheme_name}")
        return None

    def _load_scheme_rules(self) -> dict:
        """Load all scheme eligibility rules."""
        return {
            "pm_kisan": self._check_pm_kisan,
            "shetkari_samman": self._check_shetkari_samman,
            "ayushman_bharat": self._check_ayushman_bharat,
            "mjpjay": self._check_mjpjay,
            "pm_awas": self._check_pm_awas,
            "gharkul": self._check_gharkul,
            "mgnrega": self._check_mgnrega,
            "pm_ujjwala": self._check_pm_ujjwala,
            "ladki_bahin": self._check_ladki_bahin,
        }

    # ------------------------------------------------------------------ #
    #                        Individual Scheme Rules                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _check_pm_kisan(p: UserProfile) -> EligibilityResult:
        r = EligibilityResult(
            scheme_name="PM Kisan Samman Nidhi",
            scheme_name_mr="पीएम किसान सन्मान निधी",
            is_eligible="Maybe",
            confidence=0.0,
            benefit_summary="₹6,000 per year in 3 installments",
            how_to_apply="Register at pmkisan.gov.in or nearest CSC",
            source_url="https://pmkisan.gov.in",
        )
        met, unmet, missing = [], [], []

        if p.is_farmer is True:
            met.append("Is a farmer")
        elif p.is_farmer is False:
            unmet.append("Must be a farmer")
        else:
            missing.append("farming status")

        if p.has_land is True:
            met.append("Has cultivable land")
        elif p.has_land is False:
            unmet.append("Must have cultivable land")
        else:
            missing.append("land ownership")

        if p.is_income_tax_payer is False:
            met.append("Not an income tax payer")
        elif p.is_income_tax_payer is True:
            unmet.append("Income tax payers are not eligible")
        else:
            missing.append("income tax status")

        if p.is_govt_employee is False:
            met.append("Not a government employee")
        elif p.is_govt_employee is True:
            unmet.append("Government employees are not eligible")
        else:
            missing.append("government employee status")

        if p.has_aadhaar is True:
            met.append("Has Aadhaar card")
        else:
            missing.append("Aadhaar card")

        r.met_criteria = met
        r.unmet_criteria = unmet
        r.missing_info = missing
        r.is_eligible, r.confidence = _calculate_eligibility(met, unmet, missing)
        return r

    @staticmethod
    def _check_shetkari_samman(p: UserProfile) -> EligibilityResult:
        r = EligibilityResult(
            scheme_name="Namo Shetkari Mahasanman Nidhi",
            scheme_name_mr="नमो शेतकरी महासन्मान निधी",
            is_eligible="Maybe",
            confidence=0.0,
            benefit_summary="₹6,000/year (additional to PM Kisan = ₹12,000 total)",
            how_to_apply="Auto-enrolled if registered under PM Kisan",
            source_url="https://krishi.maharashtra.gov.in",
        )
        met, unmet, missing = [], [], []

        if p.is_farmer is True:
            met.append("Is a farmer")
        elif p.is_farmer is False:
            unmet.append("Must be a farmer")
        else:
            missing.append("farming status")

        if p.state == "maharashtra":
            met.append("Maharashtra resident")
        else:
            unmet.append("Must be a Maharashtra resident")

        if p.has_land is True:
            met.append("Has land in own name")
        elif p.has_land is False:
            unmet.append("Must have land in own name (7/12 extract)")
        else:
            missing.append("land ownership")

        if p.is_income_tax_payer is False:
            met.append("Not an income tax payer")
        elif p.is_income_tax_payer is True:
            unmet.append("Income tax payers not eligible")
        else:
            missing.append("income tax status")

        r.met_criteria = met
        r.unmet_criteria = unmet
        r.missing_info = missing
        r.is_eligible, r.confidence = _calculate_eligibility(met, unmet, missing)
        return r

    @staticmethod
    def _check_ayushman_bharat(p: UserProfile) -> EligibilityResult:
        r = EligibilityResult(
            scheme_name="Ayushman Bharat PM-JAY",
            scheme_name_mr="आयुष्मान भारत पीएम-जय",
            is_eligible="Maybe",
            confidence=0.0,
            benefit_summary="₹5,00,000 health insurance per family per year",
            how_to_apply="Check eligibility at pmjay.gov.in or visit Ayushman Mitra",
            source_url="https://pmjay.gov.in",
        )
        met, unmet, missing = [], [], []

        if p.is_bpl is True:
            met.append("BPL family")
        elif p.is_bpl is False and p.annual_income and p.annual_income > 300000:
            unmet.append("Not a BPL family (income too high)")
        else:
            missing.append("BPL status")

        if p.category in ("SC", "ST"):
            met.append(f"{p.category} household (auto-eligible)")

        if p.has_aadhaar is True:
            met.append("Has Aadhaar card")
        else:
            missing.append("Aadhaar card")

        r.met_criteria = met
        r.unmet_criteria = unmet
        r.missing_info = missing
        r.is_eligible, r.confidence = _calculate_eligibility(met, unmet, missing)
        return r

    @staticmethod
    def _check_mjpjay(p: UserProfile) -> EligibilityResult:
        r = EligibilityResult(
            scheme_name="Mahatma Jyotirao Phule Jan Arogya Yojana",
            scheme_name_mr="महात्मा ज्योतिराव फुले जन आरोग्य योजना",
            is_eligible="Maybe",
            confidence=0.0,
            benefit_summary="₹1,50,000 health cover (₹5L with Ayushman Bharat)",
            how_to_apply="Visit empaneled hospital with Aadhaar & ration card",
            source_url="https://www.jeevandayee.gov.in",
        )
        met, unmet, missing = [], [], []

        if p.state == "maharashtra":
            met.append("Maharashtra domicile")
        else:
            unmet.append("Must be Maharashtra resident")

        if p.ration_card_type in ("yellow", "orange", "white"):
            met.append(f"Has {p.ration_card_type} ration card")
        elif p.ration_card_type == "none":
            unmet.append("Must have yellow/orange/white ration card")
        else:
            missing.append("ration card type")

        if p.annual_income is not None:
            if p.annual_income <= 100000:
                met.append(f"Annual income ₹{p.annual_income:,} (below ₹1L limit)")
            else:
                unmet.append(f"Income ₹{p.annual_income:,} exceeds ₹1L limit")
        else:
            missing.append("annual income")

        if p.is_farmer is True:
            met.append("Farmer (priority category)")

        r.met_criteria = met
        r.unmet_criteria = unmet
        r.missing_info = missing
        r.is_eligible, r.confidence = _calculate_eligibility(met, unmet, missing)
        return r

    @staticmethod
    def _check_pm_awas(p: UserProfile) -> EligibilityResult:
        r = EligibilityResult(
            scheme_name="PM Awas Yojana - Gramin",
            scheme_name_mr="पीएम आवास योजना - ग्रामीण",
            is_eligible="Maybe",
            confidence=0.0,
            benefit_summary="₹1,20,000 for pucca house construction",
            how_to_apply="Apply through Gram Panchayat",
            source_url="https://pmayg.nic.in",
        )
        met, unmet, missing = [], [], []

        if p.has_pucca_house is False:
            met.append("Does not own a pucca house")
        elif p.has_pucca_house is True:
            unmet.append("Already owns a pucca house")
        else:
            missing.append("housing status")

        if p.is_bpl is True:
            met.append("BPL family")
        else:
            missing.append("BPL status")

        if p.is_govt_employee is False:
            met.append("Not a government employee")
        elif p.is_govt_employee is True:
            unmet.append("Government employees not eligible")
        else:
            missing.append("government employee status")

        if p.is_income_tax_payer is False:
            met.append("Not an income tax payer")
        elif p.is_income_tax_payer is True:
            unmet.append("Income tax payers not eligible")
        else:
            missing.append("income tax status")

        r.met_criteria = met
        r.unmet_criteria = unmet
        r.missing_info = missing
        r.is_eligible, r.confidence = _calculate_eligibility(met, unmet, missing)
        return r

    @staticmethod
    def _check_gharkul(p: UserProfile) -> EligibilityResult:
        r = EligibilityResult(
            scheme_name="Ramai Awas Gharkul Yojana",
            scheme_name_mr="रमाई आवास घरकुल योजना",
            is_eligible="Maybe",
            confidence=0.0,
            benefit_summary="₹2,50,000 for house construction (SC/NT/SBC only)",
            how_to_apply="Apply at Gram Panchayat or Municipal office",
            source_url="https://sjsa.maharashtra.gov.in",
        )
        met, unmet, missing = [], [], []

        if p.state == "maharashtra":
            met.append("Maharashtra resident")
        else:
            unmet.append("Must be Maharashtra resident")

        if p.category in ("SC", "NT", "SBC", "ST"):
            met.append(f"{p.category} category (eligible)")
        elif p.category == "General" or p.category == "OBC":
            unmet.append(f"{p.category} category not eligible (SC/NT/SBC only)")
        else:
            missing.append("caste category")

        if p.has_pucca_house is False:
            met.append("Does not own a pucca house")
        elif p.has_pucca_house is True:
            unmet.append("Already owns a pucca house")
        else:
            missing.append("housing status")

        if p.annual_income is not None:
            if p.annual_income <= 100000:
                met.append(f"Income ₹{p.annual_income:,} within limit")
            else:
                unmet.append(f"Income ₹{p.annual_income:,} may exceed limit")
        else:
            missing.append("annual income")

        r.met_criteria = met
        r.unmet_criteria = unmet
        r.missing_info = missing
        r.is_eligible, r.confidence = _calculate_eligibility(met, unmet, missing)
        return r

    @staticmethod
    def _check_mgnrega(p: UserProfile) -> EligibilityResult:
        r = EligibilityResult(
            scheme_name="MGNREGA",
            scheme_name_mr="मनरेगा",
            is_eligible="Maybe",
            confidence=0.0,
            benefit_summary="100 days guaranteed employment, ₹273/day in Maharashtra",
            how_to_apply="Apply for Job Card at Gram Panchayat",
            source_url="https://nrega.nic.in",
        )
        met, unmet, missing = [], [], []

        # MGNREGA is broadly available to all rural households
        if p.age is not None:
            if p.age >= 18:
                met.append(f"Age {p.age} (above 18)")
            else:
                unmet.append(f"Age {p.age} (must be 18+)")
        else:
            missing.append("age")

        if p.has_job_card is True:
            met.append("Has MGNREGA Job Card")
        else:
            missing.append("Job Card (can be obtained at Gram Panchayat)")

        # No income limit for MGNREGA
        met.append("No income limit (all rural households eligible)")

        r.met_criteria = met
        r.unmet_criteria = unmet
        r.missing_info = missing
        r.is_eligible, r.confidence = _calculate_eligibility(met, unmet, missing)
        return r

    @staticmethod
    def _check_pm_ujjwala(p: UserProfile) -> EligibilityResult:
        r = EligibilityResult(
            scheme_name="PM Ujjwala Yojana",
            scheme_name_mr="पीएम उज्ज्वला योजना",
            is_eligible="Maybe",
            confidence=0.0,
            benefit_summary="Free LPG connection + ₹1,600 subsidy for first refill",
            how_to_apply="Visit nearest LPG distributor (HP/BPCL/IOCL)",
            source_url="https://www.pmuy.gov.in",
        )
        met, unmet, missing = [], [], []

        if p.gender == "female":
            met.append("Female applicant (required)")
        elif p.gender == "male":
            unmet.append("Only women can apply (apply through female family member)")
        else:
            missing.append("gender (women only scheme)")

        if p.age is not None:
            if p.age >= 18:
                met.append(f"Age {p.age} (above 18)")
            else:
                unmet.append(f"Age {p.age} (must be 18+)")
        else:
            missing.append("age")

        if p.is_bpl is True:
            met.append("BPL household")
        elif p.is_bpl is False:
            unmet.append("Must be BPL household")
        else:
            missing.append("BPL status")

        if p.has_lpg_connection is False:
            met.append("No existing LPG connection")
        elif p.has_lpg_connection is True:
            unmet.append("Already has LPG connection")
        else:
            missing.append("LPG connection status")

        r.met_criteria = met
        r.unmet_criteria = unmet
        r.missing_info = missing
        r.is_eligible, r.confidence = _calculate_eligibility(met, unmet, missing)
        return r

    @staticmethod
    def _check_ladki_bahin(p: UserProfile) -> EligibilityResult:
        r = EligibilityResult(
            scheme_name="Mukhyamantri Majhi Ladki Bahin Yojana",
            scheme_name_mr="मुख्यमंत्री माझी लाडकी बहीण योजना",
            is_eligible="Maybe",
            confidence=0.0,
            benefit_summary="₹1,500/month (₹18,000/year) for eligible women",
            how_to_apply="Apply via Nari Shakti Doot app or Gram Panchayat",
            source_url="https://ladkibahin.maharashtra.gov.in",
        )
        met, unmet, missing = [], [], []

        if p.state == "maharashtra":
            met.append("Maharashtra resident")
        else:
            unmet.append("Must be Maharashtra resident")

        if p.gender == "female":
            met.append("Female applicant")
        elif p.gender == "male":
            unmet.append("Only women are eligible")
        else:
            missing.append("gender (women only scheme)")

        if p.age is not None:
            if 21 <= p.age <= 65:
                met.append(f"Age {p.age} (within 21-65 range)")
            else:
                unmet.append(f"Age {p.age} (must be 21-65)")
        else:
            missing.append("age")

        if p.annual_income is not None:
            if p.annual_income <= 250000:
                met.append(f"Family income ₹{p.annual_income:,} (below ₹2.5L)")
            else:
                unmet.append(f"Family income ₹{p.annual_income:,} exceeds ₹2.5L limit")
        else:
            missing.append("annual family income")

        if p.is_govt_employee is False:
            met.append("Not a government employee")
        elif p.is_govt_employee is True:
            unmet.append("Government employees not eligible")
        else:
            missing.append("government employee status")

        if p.is_income_tax_payer is False:
            met.append("Not an income tax payer")
        elif p.is_income_tax_payer is True:
            unmet.append("Income tax payers not eligible")
        else:
            missing.append("income tax status")

        r.met_criteria = met
        r.unmet_criteria = unmet
        r.missing_info = missing
        r.is_eligible, r.confidence = _calculate_eligibility(met, unmet, missing)
        return r


# ------------------------------------------------------------------ #
#                         Helper Functions                             #
# ------------------------------------------------------------------ #


def _calculate_eligibility(
    met: list[str], unmet: list[str], missing: list[str]
) -> tuple[str, float]:
    """
    Calculate eligibility status and confidence from criteria.

    Returns:
        Tuple of (status, confidence) where status is Yes/No/Maybe.
    """
    total = len(met) + len(unmet) + len(missing)
    if total == 0:
        return "Maybe", 0.0

    # Any hard disqualification → Not eligible
    if unmet:
        confidence = len(unmet) / total
        return "No", round(confidence, 2)

    # All criteria met, no missing info → Eligible
    if met and not missing:
        return "Yes", 1.0

    # Some met, some missing → Maybe
    if met:
        confidence = len(met) / total
        return "Maybe", round(confidence, 2)

    return "Maybe", 0.0
