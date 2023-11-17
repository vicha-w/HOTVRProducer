from CRABClient.UserUtilities import config, getLumiListInValidFiles
# from WMCore.DataStructs.LumiList import LumiList
import sys,os
import copy
import argparse
import yaml

parser = argparse.ArgumentParser()

parser.add_argument('--isData', action='store_true', help='True when submitting data samples')
parser.add_argument('--recoveryTask', action='store_true', help='True when recoveryTask mode is ON')
parser.add_argument('--year', dest='year', type=str, help='Year')
args = parser.parse_args()


if args.isData:
    goldenJSON_file = ''
    goldenJSON_dir = 'goldenJSON_files/'+args.year
    if args.year == '2016preVFP': goldenJSON_dir = 'goldenJSON_files/2016'
    for goldenJSON_path in os.listdir(goldenJSON_dir):
        if os.path.isfile(os.path.join(goldenJSON_dir, goldenJSON_path)):
            # add filename to list
            goldenJSON_file = goldenJSON_dir + '/' + goldenJSON_path

# requestName = "nanoaodUL"+args.year+"v1_230202"
# requestName = "testNANO18_2"
requestName = "nanoaod_hotvr_UL"+args.year+"v1_230510"

yaml_file_dict = {}
with open('{}/crab_mini_to_nano/input_files.yaml'.format(os.getcwd())) as yaml_f:
    try:
        yaml_file_dict = yaml.safe_load(yaml_f)
    except yaml.YAMLError as exc:
        print(exc)

yaml_key = 'bkg'
if args.isData: yaml_key = 'data'

data_tags = yaml_file_dict[yaml_key][args.year].keys()
datasets = []
for data_tag in yaml_file_dict[yaml_key][args.year].keys():
    datasets.append(yaml_file_dict[yaml_key][args.year][data_tag])

print(data_tags)
print(datasets)

myInputFiles = dict()
for data_tag, dataset in zip(data_tags, datasets):
    myInputFiles[data_tag] = [lambda cfg: setattr(cfg.Data,'inputDataset', dataset)]
print(myInputFiles)

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
if args.isData: 
    configTmpl.JobType.psetName = '{}/mini_to_nano_producer/MiniToNano_producer_data_{}.py'.format(os.getcwd(), args.year) 
else:
    configTmpl.JobType.psetName = '{}/mini_to_nano_producer/MiniToNano_producer_{}.py'.format(os.getcwd(), args.year)
configTmpl.JobType.outputFiles = []
configTmpl.JobType.allowUndistributedCMSSW = True
configTmpl.JobType.maxJobRuntimeMin= 25*60
configTmpl.JobType.maxMemoryMB = 2500
# ----

# ----
configTmpl.section_('Data')
if args.isData:
    configTmpl.Data.inputDBS = 'global'
    configTmpl.Data.splitting = 'LumiBased'
    configTmpl.Data.unitsPerJob = 150
else:
    configTmpl.Data.inputDBS = 'global'
    configTmpl.Data.splitting = 'FileBased'
    configTmpl.Data.unitsPerJob = 20

configTmpl.Data.totalUnits = 1  # ACTIVE WHEN TESTING 
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
        if args.isData: config.Data.outputDatasetTag = requestName+"_era_"+jobName.split('_')[-1]
        else: config.Data.outputDatasetTag = requestName
        
        if args.isData:
            config.Data.outLFNDirBase = "/store/user/"+userName+"/data_"+args.year+"/"+requestName
            config.Data.lumiMask = goldenJSON_file
        else: 
            config.Data.outLFNDirBase = "/store/user/"+userName+"/bkg_"+args.year+"/"+requestName

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
        
        
        # p = Process(target=submit, args=(config,))
        # p.start()
        # p.join()
            
        # #break

        # print
        # print
        
