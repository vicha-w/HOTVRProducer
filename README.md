# HOTVRProducer
From MINI to NANO - HOTVR production

## CMSSW Versions
Suggested CMSSW version:
* Run 2: `CMSSW_10_6_28`
* Run 3: `CMSSW_12_6_0_patch1` (*N.B.:* HOTVR production for Run 3 is still under development!)

## Running CRAB 
The crab submission files are in `crab_mini_to_nano`. The submission files fetch the input files given in `crab_mini_to_nano/input_files.yaml`.
To run the submission:

```
python crab_mini_to_nano/crab_submission.py --year YEAR
```
where YEAR has to be specified. 
For signal samples, use crab_submission_sgn.py. 

N.B.: to test the submission is helpful to specify the option `configTmpl.Data.totalUnits = 1` in the configuration file.