from typing import TypedDict, Literal

import cpat_model.constants as c

### define types:
# TODO: fix better way to define ScenarioType and ShandowPricingScenariosType (using c. throws a warning)
ScenarioType = Literal[
    'Baseline', 'Carbon tax', 'ETS', 'Feebates', 'Energy efficiency regulations',
    'TCP', 'Coal excise', 'Road fuel tax', 'Electricity emissions tax', 'Power feebate',
    'Electricity excise', 'Vehicle fuel economy', 'Residential efficiency regulations',
    'Industrial efficiency regulations'
]
ShandowPricingScenariosType = Literal[
    'Energy efficiency regulations', 'Vehicle fuel economy',
    'Residential efficiency regulations', 'Industrial efficiency regulations', 'Feebates'
]

ElasticititesSourcesType = Literal['Manual', 'Simple']
ElasticititesAdjustmentType = Literal['VHigh', 'High', 'Base', 'Low', 'VLow']

# prices
# TODO: PriceScenarioType add 'EIA', 'AVG', 'Manual', 'IMF-IEA'
PriceScenarioType = Literal['IMF', 'WB', 'IEA', 'IMF-WB']
PriceAdjustmentType = Literal['High', 'Base', 'Low']
GlobalEnergyDemandScenarioType = Literal["Stated Policies", "Announced Pledges", "Net Zero"]

# ntx
# TODO: PigouvianTaxType 'pigouvian' not implemented!
PigouvianTaxType = Literal['pigouvian', 'FFS', 'no tax']


class EnergySectorReform(TypedDict):
    """
    Type for 'Energy sector reform' (v361)
    Keys: the ScenarioDefinition names (NameOfParameter) of the policy inputs. Each key also stands for its baseline
    twin (ProdSubPhaBaseline, FFSProdPhaseoutPeriodBA, ShareOfProdSubPhaBA, ConsSubPhaBaseline, FFSConsPhaseoutPeriodBA,
    ShareofConsSubPhaBA) until the two are split (coded/TODO.md).
    TODO: check input fields again
    CPAT Excel: 230:237
    """
    ProdSubPh: bool # Phase out fossil fuel subsidies (producer)?
    # baseline =MTInputs!F57 -> Dashboard!$V$66; scenario: =MTInputs!F53 -> always True

    FFSProdPhaseoutPeriod: int # FFS (producer) phaseout period?
    # baseline =MTInputs!$F$58 -> Dashboard!$V$67, scenario: =MTInputs!F55 -> Dashboard!$Q$3

    YearProdSubPha: int # Year to begin FFS (producer) phaseout?
    # always =MTInputs!F54 -> Dashboard!$P$3

    ShareofProdSubPha: float # Share of subsidies to phase-out
    # baseline =MTInputs!$F$59 -> Dashboard!$V$68, scenario: =MTInputs!$F$56 -> Dashboard!$V$65


    ConsSubPha: bool # Phase out fossil fuel subsidies (consumer)?
    # always =MTInputs!$F$61 -> always True

    FFPhaseOut: int # FFS (consumer) phaseout period?
    # baseline =MTInputs!$F$66 -> Dashboard!$V$72, scenario: =MTInputs!F63 -> Dashboard!$Q$4

    YearConsSubPha: int # Year to begin FFS (consumer) phaseout?
    # always =MTInputs!F62 -> Dashboard!$P$4

    ShareOfConsSubPha: float # Share of subsidies to phase-out
    # baseline =MTInputs!$F$67 -> Dashboard!$V$73, scenario: =MTInputs!$F$64 -> Dashboard!$V$70


    PrcContPha: bool # Phaseout price control?
    YearPrcContPha: int # Year to introduce price control phaseout
    PrcControlPhaseout: int # Price control phaseout period (years)


class DashboardInputsDict(TypedDict):
    """
    Keys are the ScenarioDefinition names (NameOfParameter, legacy MTInputs column H; codes map tab Inputs), v8.4.
    Groups keep a container key: energy_sector_reform, adj_eff_margins_shadow_pricing (SPPEffAdj*) and
    additional_eff_gains (AdditionalEfficiency*). CTaxTrajectoryType also carries ExtendCarbonPriceBeyondOutro.
    Dashboard inputs types defined.
    Based on CPAT Excel (v361) if not stated otherwise
    """
    ScenarioSelected: ScenarioType # Dashboard!$E$3 (v407)

    # elasticities
    ElIncMainSrc: ElasticititesSourcesType # Dashboard!$L$21 (v407)
    ElPrcMainSrc: ElasticititesSourcesType # Dashboard!$L$20 (v407)
    ElastIncAdjustment: ElasticititesAdjustmentType # Dashboard!$Q$21 (v407)
    ElastPriceAdjustment: ElasticititesAdjustmentType # Dashboard!$Q$20 (v407)

    # gdp
    DfSelection: Literal['World', 'Country'] # Dashboard!$G$66
    ResultsYear: int # Dashboard!$G$62 Default 2021
    GdpAdj: Literal['High', 'Base', 'Low'] # Dashboard!$Q$19

    # efs
    EmissionsFactCO2: Literal['IIASA', 'IEA'] # Dashboard!$L$22

    ### Policies
    CTaxComplimentaryToETS: bool # Dashboard!$Q$76
    ExemptPhaseout: bool # MTInputs!$F$49 -> hardcoded True
    YearPha: int # Dashboard!$P$2
    ExemptPhaseoutPeriod: int # Dashboard!$Q$2

    # 'Adjustment to efficiency margins for shadow pricing policies:' (v407)
    # Dashboard!$L$68 Dashboard!$L$69 Dashboard!$L$70 Dashboard!$L$71 Dashboard!$L$72
    adj_eff_margins_shadow_pricing: dict[ShandowPricingScenariosType, float]

    ETSBehavioralAdjustment: float # Dashboard!$Q$78
    NomorReal: Literal['rea', 'nom'] # Dashboard!$G$20 # TODO: 'rea' not implemented
    # Dashboard!$G$19 and Dashboard!$L$78 - they do the same thing but $L$78 overrides $G$19:
    CTaxTrajectoryType: Literal['exp', 'lin', 'cst', 'per']
    CPIntro: int # Dashboard!$I$4 , TODO the same as cp_intro in some parts of the code
    CPOutro: int # Dashboard!$I$7
    CPLevelStart: int # Dashboard!$I$5
    CPLevelTarget: int # Dashboard!$I$6
    CtaxExponentialEscalationRate: float # Dashboard!$L$79

    # Exisiting carbon prices mechanisms
    ExistingCTApply: bool # Dashboard!$Q$71
    ExistingCTGrowth: float # Dashboard!$Q$72
    ExistingETSApply: bool # Dashboard!$Q$74
    ExistingETSGrowth: float # Dashboard!$Q$75

    # Phaseouts
    PrcContPhaBaseline: bool # Dashboard!$V$76
    energy_sector_reform: EnergySectorReform


    ### prices
    IntEnerPricForeSource: PriceScenarioType # Dashboard!$L$18
    IntEnerPricForecastAdjustment: PriceAdjustmentType # Dashboard!$Q$18
    GovPriceControls: Literal['Bucketed', 'Manual', 'None'] # Dashboard!$V$75
    GlobalEnergyDemand: GlobalEnergyDemandScenarioType # Dashboard!$G$73

    # ntx
    AddEfficientTaxesPhaseInYears: int # Dashboard!$V$23
    AddEfficientTaxes: PigouvianTaxType # Dashboard!$V$22
    AdditionalExcise: bool # Dashboard!$V$24


    ### Power
    CFOverrideIfAbove: float # Dashboard!$G$129 CFOverrideIfAbove (v407)
    CFOverrideIfBelowFosOth: float # Dashboard!$G$127 CFOverrideIfBelowFosOth (v407)
    CFOverrideIfBelowWndSol: float # Dashboard!$G$128 CFOverrideIfBelowWndSol (v407)
    MinimumThermalEfficiency: float # Dashboard!G125 MinimumThermalEfficiency (v407)
    kInvestment: float # Dashboard!$L$133 kInvestment (v407)
    kDispatch: float # Dashboard!$G$121 kDispatch (v407)
    MaximumCoalCF: float # Dashboard!$G$123 MaximumCoalCF (v407)
    MaximumGasCF: float # Dashboard!$G$124 MaximumGasCF (v407)
    UseSpotFuelPricesInEngineerModel: bool # Dashboard!$G$122 UseSpotFuelPricesInEngineerModel (v407)

    ### EC
    AlwaysExemptResLPGKer: bool # Dashboard!$V$19 AlwaysExemptResLPGKer (v407)
    additional_eff_gains: dict[ # (v407)
        Literal[
            'pow', # Dashboard!$L$61 AdditionalEfficiencyPower
            'tra', # Dashboard!$L$62 AdditionalEfficiencyRoadVehicle
            'res', # Dashboard!$L$63 AdditionalEfficiencyResidential
            'ind' # Dashboard!$L$64 AdditionalEfficiencyIndustrial
        ],
        float
    ] # Additional policy-induced annual efficiency gains



class DashboardInputs:
    """
    Contains all Dashboard inputs in d: DashboardInputsDict
    Hardcoded here for now -> TODO: UI
    """
    d: DashboardInputsDict

    def __init__(self, config_input: dict | None = None) -> None:
        # default
        self.d = {
            'ScenarioSelected': c.BASELINE,

            'ElIncMainSrc': 'Simple',
            'ElPrcMainSrc': 'Simple',
            'ElastIncAdjustment': 'Base',
            'ElastPriceAdjustment': 'Base',

            'GlobalEnergyDemand': 'Stated Policies',

            'DfSelection': 'World',
            'ResultsYear': 2022,
            'GdpAdj': 'Base',

            'EmissionsFactCO2': 'IIASA',

            'PrcContPhaBaseline': True,
            'energy_sector_reform': {
                'ProdSubPh': True,
                'FFSProdPhaseoutPeriod': 5,
                'YearProdSubPha': 2025,
                'ShareofProdSubPha': 0.5,

                'ConsSubPha': False,
                'FFPhaseOut': 5,
                'YearConsSubPha': 2025,
                'ShareOfConsSubPha': 0.5,

                'PrcContPha': True,
                'PrcControlPhaseout': 5,
                'YearPrcContPha': 2025,
            },

            'ExistingCTApply': True,
            'ExistingCTGrowth': 0.1,
            'ExistingETSApply': True,
            'ExistingETSGrowth': 0.1,

            'GovPriceControls': 'Bucketed',
            'IntEnerPricForeSource': 'IMF-WB',
            'IntEnerPricForecastAdjustment': 'Base',

            'CPIntro': 2025,
            'CPOutro': 2030,
            'CPLevelStart': 0,
            'CPLevelTarget': 25,

            'ExemptPhaseout': True,
            'YearPha': 2025,
            'ExemptPhaseoutPeriod': 5,
            'CTaxComplimentaryToETS': False,

            'adj_eff_margins_shadow_pricing': {
                c.ENERGY_EFFICIENCY_REGULATIONS: 0.7,
                c.VEHICLE_FUEL_ECONOMY: 0.7,
                c.RESIDENTIAL_EFFICIENCY_REGULATIONS: 0.7,
                c.INDUSTRIAL_EFFICIENCY_REGULATIONS: 0.7,
                c.FEEBATES: 1.0
            },

            'AddEfficientTaxesPhaseInYears': 5,
            'AddEfficientTaxes': 'no tax',
            'AdditionalExcise': False,

            'ETSBehavioralAdjustment': 0.9,
            'NomorReal': 'nom',
            'CTaxTrajectoryType': 'lin',
            'CtaxExponentialEscalationRate': 0.00,

            'CFOverrideIfAbove': 1.0,
            'CFOverrideIfBelowFosOth': 0.01,
            'CFOverrideIfBelowWndSol': 0.1,
            'MinimumThermalEfficiency': 0.1,
            'kInvestment': 2.0,
            'kDispatch': 2.0,
            'MaximumCoalCF': 0.9,
            'MaximumGasCF': 0.9,
            # TODO: in Excel False as default, here True as moving prices not implemented:
            'UseSpotFuelPricesInEngineerModel': True,

            'AlwaysExemptResLPGKer': False,
            'additional_eff_gains': {
                'pow': 0.0,
                'tra': 0.0,
                'res': 0.0,
                'ind': 0.0
            }
        }

        if config_input:
            self.d.update(config_input)
