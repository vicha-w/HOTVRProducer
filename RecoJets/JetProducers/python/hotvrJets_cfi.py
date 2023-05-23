import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *


hotvrPFJets = cms.EDProducer(
    "HOTVRProducer",
    # PFJetParameters,
    # AnomalousCellParameters,
    src=cms.InputTag("puppi"),
    doRekey = cms.bool(True),       # set True if you want to rekey jet & subjets so that
    rekeyCandidateSrc = cms.InputTag("packedPFCandidates") # constituents point to rekeyCandidateSrc
    )


