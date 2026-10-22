from cpat_model.constants import BASELINE_SCENARIO

PAGE = {
    "tools": "Tools",
    "CPATPython": "CPAT Python",
    "selectSection": "Select Section",
    "manualInputs": "Manual inputs",
    "scenarios": "Scenarios",
    "rawResults": 'Raw Results',
    "indicators": "Indicators",
    "visualizations": "Visualizations",
    "documentation": "Documentation"
}

SCENARIOS = {
    "load": "Load Scenarios",
    "delete": "Delete all Scenarios",
    "download": "Download Scenarios",
    "run": "Run Scenarios"
}

SCENARIO_CARDS = {
    "removeScenario": "Remove Scenario",
    "countries": "Countries",
    "selectedFuels": "Selected fuels",
    "selectedSectors": "Selected sectors",
    "scenariosEmpty": f"Please load Scenarios or create them in '{PAGE['manualInputs']}'."
}

COMMON = {
    "scenarioName": "Scenario name",
    "selectCountries": "Select countries",
    "startCTYear": "Starting CT policy year",
    "targetCTYear": "Target CT policy year",
    "startCTLevel": "Starting CT level",
    "targetCTLevel": "Target CT level",
    "afterTargetCT": "CT values after target year",
    "selectFuels": "Select fuels",
    "selectSectors": "Select sectors",
    "addScenario": "Add Scenario",
    "pricesSourceSelection": "Prices source selection"
}

RESULTS = {
    "selectIndicators": "Select Indicators",
    "selectVariables": "Select variables to be saved",
    "downloadResults": "Download Raw Results",
    "downloadIndicators": "Download Indicators",
    "createIndicators": "Create Indicators",
    "extractVariables": "Extract variables",
    "resultsEmpty": "Please run Scenarios to generate access to this section.",
    "resultsFileName": "Raw Results file name",
    "indicatorsFileName": "Indicators file name",
    "rawResultsDfSelection": "Select variable to display",
    "rawResultsCountryCode": "CountryCode",
    "rawResultsSectorCode": "SectorCode",
    "rawResultsFuelCode": "FuelCode",
    "rawResultsScenarioName": "ScenarioName",
    "applyFilters": "Apply filters",
    "indicatorsCpatCode": "CPATCode",
    "indicatorsUnit": "Unit",
    "indicatorsHeader": "Indicator header"
}

VISUALIZATIONS = {
    "selectedCountry": "Selected Country",
    "selectedScenario": "Selected Scenario",
    "visualizationsEmpty": "Please run Scenarios and calculate Indicators to generate visualizations.",
}

DOCUMENTATION = {
    'documentationSelection': 'Documentation selection'
}

SERVER = {
    "scenarioCreated": "Scenario created!",
    "runSuccessful": "Run successful!",
    "scenariosInProgress" : "Running Scenarios in progress",
    "resultsSaved": "Results saved!",
    "indicatorsDownloaded": "Indicators downloaded!",
    "indicatorsCreated": "Indicators created!",
    "scenariosDeleted": "All Scenarios deleted!"
}

VALIDATION = {
    "nameEmpty": "Scenario name cannot be empty.",
    "nameTooLong": "Scenario name must be no more than 30 characters long.",
    "baselineName": f"Scenario name cannot be named '{BASELINE_SCENARIO}'.",
    "nameNotUnique": "Scenario name '{scenario_name}' already exists. Please choose a different name.",
    "countriesEmpty": "Selected countries cannot be empty.",
    "countriesNotConsistent": "Provided countries: {c} are not consistent with: {e_c}.",
    "startYearTooLow": f"{COMMON['startCTYear']} cannot be smaller than 2024.",
    "startYearTooHigh": f"{COMMON['startCTYear']} cannot be higher than 2050.",
    "startYearIsFraction": f"{COMMON['startCTYear']} must be a whole number.",
    "startYearType": f"{COMMON['startCTYear']} must be a number.",
    "targetYearTooLow": f"{COMMON['targetCTYear']} cannot be smaller than {COMMON['startCTYear']}.",
    "targetYearTooHigh": f"{COMMON['targetCTYear']} cannot be higher than 2050.",
    "targetYearIsFraction": f"{COMMON['targetCTYear']} must be a whole number.",
    "targetYearType": f"{COMMON['targetCTYear']} must be a number.",

    "startLevelTooLow": f"{COMMON['startCTLevel']} cannot be smaller than 0.",
    "startLevelType": f"{COMMON['startCTLevel']} must be a number.",

    "targetLevelTooLow": f"{COMMON['targetCTLevel']} cannot be smaller than {COMMON['startCTLevel']}.",
    "targetLevelType": f"{COMMON['targetCTLevel']} must be a number.",

    "CTProjectionIncorrect": f"Incorrect value for {COMMON['afterTargetCT']}.",
    "PricesSelectionIncorrect": f"Incorrect value for {COMMON['pricesSourceSelection']}.",

    "fileNameEmpty": "{input_name} cannot be empty.",
    "fileNameIsEmpty": "{input_name} cannot be called 'empty'",
    "fileNameTooLong": "{input_name} must be no more than 30 characters long.",
    "fileNameInvalidChars": "{input_name} contains invalid character(s).",
    "fileNameTrailingWhitespace": "{input_name} has leading or trailing whitespace.",
}
