import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.nano_eras_cff import *

from  PhysicsTools.NanoAOD.common_cff import *
from RecoJets.JetProducers.hotvrJets_cfi import hotvrPFJets
from RecoJets.JetProducers.hotvrGenJets_cfi import hotvrGenJets

packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector",
        src=cms.InputTag("packedGenParticles"),
        cut=cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16")
    )

hotvrJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("hotvrPFJets"),
    cut = cms.string(" pt > 30"), #probably already applied in miniaod
    name = cms.string("HOTVRJet"),
    # doc  = cms.string(" "),  #slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        # msoftdrop = Var("groomedMass('SoftDropPuppi')",float, doc="Corrected soft drop mass with PUPPI",precision=10),
        tau1 = Var("userFloat('tau1')",float, doc="Nsubjettiness (1 axis)",precision=10),
        tau2 = Var("userFloat('tau2')",float, doc="Nsubjettiness (2 axis)",precision=10),
        tau3 = Var("userFloat('tau3')",float, doc="Nsubjettiness (3 axis)",precision=10),
        nMuons = Var("?hasOverlaps('muons')?overlaps('muons').size():0", int, doc="number of muons in the jet"),
        muonIdx1 = Var("?overlaps('muons').size()>0?overlaps('muons')[0].key():-1", int, doc="index of first matching muon"),
        muonIdx2 = Var("?overlaps('muons').size()>1?overlaps('muons')[1].key():-1", int, doc="index of second matching muon"),
        electronIdx1 = Var("?overlaps('electrons').size()>0?overlaps('electrons')[0].key():-1", int, doc="index of first matching electron"),
        electronIdx2 = Var("?overlaps('electrons').size()>1?overlaps('electrons')[1].key():-1", int, doc="index of second matching electron"),
        nElectrons = Var("?hasOverlaps('electrons')?overlaps('electrons').size():0", int, doc="number of electrons in the jet"),
        nConstituents = Var("numberOfDaughters()","uint8",doc="Number of particles in the jet"),
        btagDeepB = Var("?(bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb'))>=0?bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb'):-1",float,doc="DeepCSV b+bb tag discriminator",precision=10),
        btagDeepFlavB = Var("bDiscriminator('pfDeepFlavourJetTags:probb')+bDiscriminator('pfDeepFlavourJetTags:probbb')+bDiscriminator('pfDeepFlavourJetTags:problepb')",float,doc="DeepJet b+bb+lepb tag discriminator",precision=10),
        rawFactor = Var("1.",float,doc="1 - Factor to get back to raw pT",precision=6),
        chHEF = Var("chargedHadronEnergyFraction()", float, doc="charged Hadron Energy Fraction", precision= 6),
        neHEF = Var("neutralHadronEnergyFraction()", float, doc="neutral Hadron Energy Fraction", precision= 6),
        chEmEF = Var("chargedEmEnergyFraction()", float, doc="charged Electromagnetic Energy Fraction", precision= 6),
        neEmEF = Var("neutralEmEnergyFraction()", float, doc="neutral Electromagnetic Energy Fraction", precision= 6),
        muEF = Var("muonEnergyFraction()", float, doc="muon Energy Fraction", precision= 6),
        #chFPV0EF = Var("userFloat('chFPV0EF')", float, doc="charged fromPV==0 Energy Fraction (energy excluded from CHS jets). Previously called betastar.", precision= 6),
        subJetIdx1 = Var("?nSubjetCollections()>0 && subjets().size()>0?subjets()[0].key():-1", int, doc="index of first subjet"),
        subJetIdx2 = Var("?nSubjetCollections()>0 && subjets().size()>1?subjets()[1].key():-1", int, doc="index of second subjet"),
        subJetIdx3 = Var("?nSubjetCollections()>0 && subjets().size()>2?subjets()[2].key():-1", int, doc="index of third subjet"),
    ),
)

hotvrSubJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("hotvrPFJets","SubJets"),
    cut = cms.string(""), #probably already applied in miniaod
    name = cms.string("HOTVRSubJet"),
    # doc  = cms.string("slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        nConstituents = Var("numberOfDaughters()","uint8",doc="Number of particles in the jet"),
        rawFactor = Var("1.",float,doc="1 - Factor to get back to raw pT",precision=6),
        chHEF = Var("chargedHadronEnergyFraction()", float, doc="charged Hadron Energy Fraction", precision= 6),
        neHEF = Var("neutralHadronEnergyFraction()", float, doc="neutral Hadron Energy Fraction", precision= 6),
        chEmEF = Var("chargedEmEnergyFraction()", float, doc="charged Electromagnetic Energy Fraction", precision= 6),
        neEmEF = Var("neutralEmEnergyFraction()", float, doc="neutral Electromagnetic Energy Fraction", precision= 6),
        muEF = Var("muonEnergyFraction()", float, doc="muon Energy Fraction", precision= 6),
    )
)

hotvrJetMCTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = hotvrJetTable.src,
    cut = hotvrJetTable.cut,
    name = hotvrJetTable.name,
    # doc  = cms.string(" "),  #slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(True), 
    variables = cms.PSet(P4Vars,
        partonFlavour = Var("partonFlavour()", int, doc="flavour from parton matching"),
        hadronFlavour = Var("hadronFlavour()", int, doc="flavour from hadron ghost clustering"),
        genHOTVRJetIdx = Var("?genJetFwdRef().backRef().isNonnull()?genJetFwdRef().backRef().key():-1", int, doc="index of matched gen jet"),
    ),
)

hotvrSubJetMCTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = hotvrSubJetTable.src,
    cut = hotvrSubJetTable.cut,
    name = hotvrSubJetTable.name,
    # doc  = cms.string("slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(True),
    variables = cms.PSet(P4Vars,
        partonFlavour = Var("partonFlavour()","uint8"),
        hadronFlavour = Var("hadronFlavour()","uint8"),
    )
)

hotvrGenJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("hotvrGenJets"),
    name = cms.string("GenHOTVRJet"),
    cut = cms.string(" pt > 30"), #probably already applied in miniaod
    # doc  = cms.string(" "),  #slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P4Vars,
        # msoftdrop = Var("groomedMass('SoftDropPuppi')",float, doc="Corrected soft drop mass with PUPPI",precision=10),
        partonFlavour = Var("partonFlavour()","uint8"),
        hadronFlavour = Var("hadronFlavour()","uint8"),
    ),
)



hotvrSubGenJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("hotvrGenJets","SubJets"),
    cut = cms.string(""), #probably already applied in miniaod
    name = cms.string("GenHOTVRSubJet"),
    # doc  = cms.string("slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        partonFlavour = Var("partonFlavour()","uint8"),
        hadronFlavour = Var("hadronFlavour()","uint8"),   
    )
)


hotvrjetSequence = cms.Sequence(hotvrPFJets)

hotvrjetTables = cms.Sequence(hotvrJetTable+hotvrSubJetTable)

hotvrjetMC = cms.Sequence(hotvrJetMCTable+hotvrSubJetMCTable+packedGenParticlesForJetsNoNu+hotvrGenJets+hotvrGenJetTable+hotvrSubGenJetTable)