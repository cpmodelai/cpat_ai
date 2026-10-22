# CPAT legacy data export

Created 2026-10-21 by data/scripts/export_to_legacy.py
Source folder: dummy
Countries: all in the source files
EnergyCons year column: 2022 (energy_consumption.csv has no year)


## How to paste into legacy CPAT (CPAT 1.0pre_456 .xlsb)

Each sheet here has the same name, header rows and cell positions as the legacy data sheet. Copy the data block below and Paste Special > Values onto the legacy sheet at the same top-left cell. Clear the old data rows first if the new block is shorter.
  EnergyCons: data A2:X4048 (4047 rows); header row 1 as in legacy
  Prices_dom: data A9:EL888 (880 rows); header rows 1-8 as in legacy
  HHSurvey: data A2:BP133 (132 rows); header row 1 as in legacy
  IO_GTAP: data A2:BP12 (11 rows); header row 1 as in legacy


## Legacy settings and checks

EnergyCons is read by legacy Mitigation rows 583-601 only when the Dashboard switch BalancesOrConsumption is not "Balances" (Mitigation C578). The IEA flow-level Balances sheet cannot be built from energy_consumption.csv (already aggregated to CPAT sectors).
In the NoPropData workbook some lookups into the stripped sheets were shrunk to row 1 (e.g. Mitigation AA583 =MATCH(B583,EnergyCons!$A$1:$A$1,0)). Pasting into that file needs those ranges widened to the data rows; the full (proprietary) workbook has them.
EnergyCons keys are LOWER(country)&".mit.enc."&fuel (Mitigation B583); heat uses "heat". Prices_dom countrycode_weo is set to the ISO code; check it for countries whose WEO code differs.


## Gaps in the source files

EnergyCons: sector columns wav, neu are not in energy_consumption.csv; left blank (legacy Mitigation does not read them in Consumption mode).
Prices_dom: 48 legacy columns are not in prices_dom.csv and are left blank: mit.spsrc.coa.pow, mit.rprel.coa.pow, mit.rpsrc.coa.pow, mit.spsrc.coa.ind, mit.rprel.coa.ind, mit.rpsrc.coa.ind, mit.spsrc.coa.res, mit.rprel.coa.res, mit.rpsrc.coa.res, mit.spsrc.nga.pow, mit.rprel.nga.pow, mit.rpsrc.nga.pow, mit.spsrc.nga.ind, mit.rprel.nga.ind, mit.rpsrc.nga.ind, mit.spsrc.nga.res, mit.rprel.nga.res, mit.rpsrc.nga.res, mit.spsrc.gso.all, mit.rprel.gso.all, mit.rpsrc.gso.all, mit.spsrc.die.all, mit.rprel.die.all, mit.rpsrc.die.all, mit.spsrc.lpg.all, mit.rprel.lpg.all, mit.rpsrc.lpg.all, mit.spsrc.ker.all, mit.rprel.ker.all, mit.rpsrc.ker.all, mit.taxa.ecy.ind, mit.spsrc.ecy.ind, mit.rprel.ecy.ind, mit.rpsrc.ecy.ind, mit.taxa.ecy.res, mit.spsrc.ecy.res, mit.rprel.ecy.res, mit.rpsrc.ecy.res, mit.spsrc.bio.all, mit.rpsrc.bio.all, mit.spsrc.oop.all, mit.rpsrc.oop.all, mit.sub.or.ecy.res, mit.sub.or.ecy.ind, mit.coa.prod, mit.nga.prod, mit.spot.coa, mit.spot.nga.
