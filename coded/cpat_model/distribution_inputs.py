from typing import TypedDict, Literal

import cpat_model.constants as c


LaborTaxReductionMethodType = Literal[
    'Proportional Compensation', 'Personal Allowance', 'Targeted Exemption'
]
StatisticType = Literal['mean', 'median', 'p25', 'p75']


class DistributionInputsDict(TypedDict):
    """
    Distribution module inputs.

    Based on the CPAT Excel 'Distribution' sheet, section B (Key assumptions and
    inputs). Kept as its own TypedDict, separate from DashboardInputsDict
    (Mitigation module inputs), because the Distribution sheet has its own
    independent input block in the Excel model -- it *consumes* the Mitigation
    module's results (prices, carbon-price revenue; see
    cpat_model.distribution.distribution.Distribution) rather than
    sharing Dashboard-level scenario config.

    See other/more/CPAT_Distribution_Module_Pseudocode.docx (§4 Inputs)
    for the full input inventory this is progressively implementing.
    """
    # B.I Basic inputs
    YearDistn: int # Distribution!'Analysis Year'
    QuantilesStatistic: StatisticType # Distribution!'Statistic - Outputs', default 'mean'

    # B.I Incidence adjustments (§4.2)
    InferredDist: bool
    behavioral_response_adj_factor: float
    DWLs: bool
    PEDs: bool
    PassthroughDist: bool

    # B.I Exemptions (§4.5)
    ExemptMostCook: bool
    exempt_cooking_fuel_code: str # one of c.DISTN_DIRECT_FUELS, used when exempt_cooking_fuel=True
    exempt_cooking_fuel_share: float
    ExemptCookDeciles: int # exempt the bottom N deciles

    # B.I Revenue recycling (§4.4): % of CP revenue (legacy convention, issue I85: 30 = 30%), should sum to <= 100
    EXPLabortax: float
    EXPTransfers: float
    EXPCapex: float
    EXPGoodsandserv: float

    PITReductionType: LaborTaxReductionMethodType
    DistExcCfDec: int # 'Targeted Exemption' method
    labor_tax_cut_coefficient: float # 'Proportional Compensation' method

    # Targeted transfer design (rules-based synthetic transfer -- Dashboard
    # 'Revenue recycling -> Transfers -> of which'; see recycling.py
    # targeted_transfer_shares, which this configures). Not used when
    # targeted transfers are instead sourced from an ASPIRE program's own
    # incidence (that path isn't wired in yet, see data.load_aspire).
    TargettedPercentile: float # % (legacy, issue I85): e.g. 40 = bottom 40% of the population targeted
    CoverageRate: float # % (legacy, I85) of the targeted population that receives a transfer
    LeakageRate: float # % (legacy, I85) of the untargeted population that also receives one

    # Public investment incidence (§4.4): which HHSurvey infrastructure-
    # access index to weight by (see recycling.py public_investment_shares).
    # One of 'all_acs_share', 'ely_acs_share', 'wtr_acs_share',
    # 'sani_acs_share', 'ICT_acs_share', 'transp_pub_acs_share'.
    PublicInfrastructureInvType: str


class DistributionInputs:
    """
    Contains all Distribution module inputs in d: DistributionInputsDict.
    Mirrors cpat_model.dashboard_inputs.DashboardInputs (default dict + overrides).
    Hardcoded defaults for now -> TODO: UI, same as DashboardInputs.
    """
    d: DistributionInputsDict

    def __init__(self, config_input: dict | None = None) -> None:
        # default
        self.d = {
            'YearDistn': 2030,
            'QuantilesStatistic': 'mean',

            'InferredDist': False,
            'behavioral_response_adj_factor': 1.0,
            'DWLs': False,
            'PEDs': False,
            'PassthroughDist': False,

            'ExemptMostCook': False,
            'exempt_cooking_fuel_code': c.KER,
            'exempt_cooking_fuel_share': 0.0,
            'ExemptCookDeciles': 0,

            'EXPLabortax': 0.0,
            'EXPTransfers': 0.0,
            'EXPCapex': 0.0,
            'EXPGoodsandserv': 0.0,

            'PITReductionType': 'Proportional Compensation',
            'DistExcCfDec': 0,
            'labor_tax_cut_coefficient': 0.0,

            'TargettedPercentile': 100.0,
            'CoverageRate': 100.0,
            'LeakageRate': 0.0,

            'PublicInfrastructureInvType': 'all_acs_share',
        }

        if config_input:
            self.d.update(config_input)
