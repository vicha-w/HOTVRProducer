from CRABClient.UserUtilities import config, getLumiListInValidFiles
# from WMCore.DataStructs.LumiList import LumiList
import sys,os
import copy
import argparse
import yaml

parser = argparse.ArgumentParser()

parser.add_argument('--recoveryTask', action='store_true', help='True when recoveryTask mode is ON')
parser.add_argument('--year', dest='year', type=str, help='Year')
args = parser.parse_args()

MASS_VALUES = [500, 750]#, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 4000]
WIDTH_VALUES = [4]#, 10, 20, 50]

# requestName = "nanoaodUL"+args.year+"v1_230202"
# requestName = "testNANO18_2"
requestName = "nanoaod_hotvr_UL"+args.year+"v1_230510"

yaml_file_dict = {}
with open('{}/crab_mini_to_nano/input_files.yaml'.format(os.getcwd())) as yaml_f:
    try:
        yaml_file_dict = yaml.safe_load(yaml_f)
    except yaml.YAMLError as exc:
        print(exc)

YAML_KEY = 'sgn'
PROCESS_TAG = yaml_file_dict[YAML_KEY][args.year].keys()[0]
PROCESS = yaml_file_dict[YAML_KEY][args.year][PROCESS_TAG]
print(PROCESS, PROCESS_TAG)


data_tags, datasets = [], []
for mass in MASS_VALUES:
    for width in WIDTH_VALUES:
        process_tag = PROCESS_TAG.replace("MASS", str(mass)).replace("WIDTH", str(width))
        process = PROCESS.replace("MASS", str(mass)).replace("WIDTH", str(width))
        data_tags.append(process_tag)
        datasets.append(process)


myInputFiles = dict()
for data_tag, dataset in zip(data_tags, datasets):

    myInputFiles[data_tag] = [lambda cfg: setattr(cfg.Data,'inputDataset', dataset)]


userName = 'gmilella' #getUsernameFromSiteDB() 
configTmpl = config()
# ----
configTmpl.section_('General')
configTmpl.General.transferOutputs = True
configTmpl.General.transferLogs = False
# ----

# ----
configTmpl.section_('JobType')
configTmpl.JobType.psetName = None
configTmpl.JobType.pluginName = 'Analysis'
configTmpl.JobType.psetName = '{}/mini_to_nano_producer/MiniToNano_producer_{}.py'.format(os.getcwd(), args.year)
configTmpl.JobType.outputFiles = []
configTmpl.JobType.allowUndistributedCMSSW = True
# configTmpl.JobType.maxJobRuntimeMin= 25*60
configTmpl.JobType.maxMemoryMB = 2500
# ----

# ----
configTmpl.section_('Data')
# N.B this part must be active in case of PRIVATE MC!
# configTmpl.Data.inputDBS = 'phys03'
# configTmpl.Data.splitting = 'FileBased'
# configTmpl.Data.unitsPerJob = 1
configTmpl.Data.inputDBS = 'global'
configTmpl.Data.splitting = 'Automatic'
configTmpl.Data.unitsPerJob = 180

# configTmpl.Data.totalUnits = 1  # ACTIVE WHEN TESTING 
configTmpl.Data.publication = True
# ----

# ----
configTmpl.section_('Site')
configTmpl.Site.storageSite = 'T2_DE_DESY'
# configTmpl.Site.blacklist = ['T2_IT_Pisa','T2_US_Vanderbilt','T2_BR_SPRACE','T2_UK_SGrid_RALPP','T2_ES_IFCA']
# ----

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException
    from multiprocessing import Process

    def submit(config):
        try:
            crabCommand('submit',  config = config)
        except HTTPException as hte:
            print("Failed submitting task: %s" % (hte.headers))
        except ClientException as cle:
            print("Failed submitting task: %s" % (cle))


    for i,jobName in enumerate(sorted(myInputFiles.keys())):

        isData = False
        myJob = myInputFiles[jobName]
        i=i+1
        config = copy.deepcopy(configTmpl)

        
        config.General.requestName = jobName+"_"+requestName
        config.General.workArea = "crab/"+requestName+"/"+jobName
        config.Data.outLFNDirBase = "/store/user/"+userName+"/sgn_"+args.year+"/"+requestName
        # config.Data.outputPrimaryDataset = jobName
        config.Data.outputDatasetTag = requestName

        print('outLFNDirBase {}'.format(config.Data.outLFNDirBase))
        for mod in myJob:
            mod(config)
            
        if not os.path.exists(config.JobType.psetName):
            print("\nConfiguration file ", config.JobType.psetName, "does not exist.  Aborting...")
            sys.exit(1)

        if os.path.isdir(os.path.join(os.getcwd(),config.General.workArea)):
            print("Output directory ",os.path.join(os.getcwd(),config.General.workArea)," exists -> skipping")
            print
            continue
            
        print(config)
            
        print("Submitting job ",i," of ",len(myInputFiles.keys()),":",config.General.workArea)
        
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()
            
        #break

        print
        print
        
