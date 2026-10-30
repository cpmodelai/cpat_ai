"""v0.4.5: the two mapping tables of the distribution module that have no legacy data tab (data/):
  distn_catmap.csv    gtap sector (IO_GTAP code), CPAT consumption category of legacy C.I rows 668-736 (fuel sectors:
                      their fuel group; they reach households through the direct effect only)
  distn_programs.csv  recycling choices of MTInputs: kind, label, data code (legacy Distribution rows 184-189 and
                      195-210: infrastructure access variables; ASPIRE program codes per_<program>.avt_q)
The data tables themselves are legacy's, unchanged: extract_legacy_tables.py (v0.4.4 wrote reshaped copies)."""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', 'data', 'scripts'))
from legacy_csv import legacy_dir, save_to_tidy  # noqa: E402,F401  (data/Public01/tidy/ in the legacy CSV form)
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = legacy_dir()
CATS = {  # legacy Distribution C.I rows 668-736: GTAP sectors (IO_GTAP codes) of each consumption category
    'food': 'b_t c_b cmt ctl fsh gro mil oap ocr ofd omt osd pcr pdr pfb rmk sgr v_f vol wht', 'edu': 'edu',
    'hea': 'hht', 'clo': 'lea tex wap wol', 'hou': 'cns dwe frs i_s nmm omf wtr', 'app': 'eeq ele fmp nfm ome oxt',
    'che': 'chm rpp', 'tpu': 'otp wtp atp whs', 'teq': 'mvh otn trd', 'pap': 'ppp lum', 'com': 'cmn', 'pha': 'bph',
    'ret': 'ros afs', 'oth': 'ins obs ofi osg rsa', 'coa': 'coa', 'ely': 'ely', 'nga': 'nga', 'oil': 'oil',
    'p_c': 'p_c'}
INFRA = [('All Infr.', 'all_acs_share'), ('ICT Infr.', 'ICT_acs_share'), ('Electricity Infr.', 'ely_acs_share'),
         ('Water Infr.', 'wtr_acs_share'), ('Sanitation Infr.', 'sani_acs_share'),
         ('Public Transport Infr.', 'transp_pub_acs_share')]
PROGRAMS = [('Active Labor Market', 'lm_ac'), ('All Labor Market', 'lm_alllm'), ('All Social Assistance', 'sa_allsa'),
            ('All Social Insurance', 'si_allsi'), ('All Social Protection and Labor', 'allsp'),
            ('Cash Transfers', 'sa_ct'), ('Conditional Cash Transfers', 'sa_cc'), ('Contributory Pensions', 'si_cp'),
            ('Fee waivers and targeted subsidies', 'sa_fw'), ('In-Kind', 'sa_ik'), ('Other Social Assistance', 'sa_os'),
            ('Other Social Insurance', 'si_ss'), ('Passive Labor Market', 'lm_pa'), ('Public Works', 'sa_pw'),
            ('School Feeding', 'sa_sf'), ('Social Pensions', 'sa_sp')]


def write(name, header, body):
    with open(os.path.join(DATA, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(body)
    print(f'{name}: {len(body)} rows')


def main():
    write('distn_catmap.csv', ['gtap', 'item'], sorted([[g, c] for c, ss in CATS.items() for g in ss.split()]))
    write('distn_programs.csv', ['key', 'kind', 'label', 'code'],
          [[f'infra|{a}', 'infra', a, b] for a, b in INFRA] + [[f'aspire|{a}', 'aspire', a, f'per_{b}.avt_q'] for a, b in PROGRAMS])


if __name__ == '__main__':
    main()
