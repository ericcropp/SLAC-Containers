import yaml

from UTILITY_linacPhaseAndAmplitude import getLinacMatchStrings, setLinacPhase, setLinacGradientAuto


#This is the all-in-one function that should make any and all changes to the lattice
#This way there's a single place where default values need to be kept
def setLattice(
    tao,
    defaultsFile=None, 
    **overrides
):

    if not defaultsFile:
        defaultsFile = 'setLattice_defaults.yml'
        print(f"No defaults file provided to setLattice(). Using {defaultsFile}")
        
    with open(defaultsFile, 'r') as file:
        defaults = yaml.safe_load(file)
        
    # Combine defaults and overrides, with overrides taking precedence
    latticeSettings = {**defaults, **overrides}


    #Prevent recalculation until changes are made
    tao.cmd("set global lattice_calc_on = F")
    
    setLinacsHelper(tao, 
                    latticeSettings["L1PhaseSet"], 
                    latticeSettings["L2PhaseSet"], 
                    latticeSettings["L2EnergyOffset"], 
                    latticeSettings["L3EnergyOffset"]
                   )

    setAllInjectorQuads(tao, 
                        latticeSettings["QA10361kG"], 
                        latticeSettings["QA10371kG"], 
                        latticeSettings["QE10425kG"], 
                        latticeSettings["QE10441kG"], 
                        latticeSettings["QE10511kG"], 
                        latticeSettings["QE10525kG"]
                       )
    
    setAllFinalFocusQuads(tao, 
                          latticeSettings["Q5FFkG"], 
                          latticeSettings["Q4FFkG"], 
                          latticeSettings["Q3FFkG"], 
                          latticeSettings["Q2FFkG"], 
                          latticeSettings["Q1FFkG"], 
                          latticeSettings["Q0FFkG"], 
                          latticeSettings["Q0DkG"], 
                          latticeSettings["Q1DkG"], 
                          latticeSettings["Q2DkG"]
                         )

    
    setAllWChicaneBends(tao, 
                        latticeSettings["B1EkG"], 
                        latticeSettings["B2EkG"], 
                        latticeSettings["B3EkG"]
                       )
    
    setAllWChicaneQuads(tao, 
                        latticeSettings["Q1EkG"], 
                        latticeSettings["Q2EkG"], 
                        latticeSettings["Q3EkG"], 
                        latticeSettings["Q4EkG"], 
                        latticeSettings["Q5EkG"], 
                        latticeSettings["Q6EkG"]
                       )
    
    setAllWChicaneSextupoles(tao, 
                             latticeSettings["S1ELkG"], 
                             latticeSettings["S2ELkG"], 
                             latticeSettings["S3ELkG"], 
                             latticeSettings["S3ERkG"], 
                             latticeSettings["S2ERkG"], 
                             latticeSettings["S1ERkG"]
                            )
    
    #Reenable lattice calculations
    tao.cmd("set global lattice_calc_on = T")

    return

def setLinacsHelper(tao, L1PhaseSet, L2PhaseSet, L2EnergyOffset, L3EnergyOffset):
    [L1MatchStrings, L2MatchStrings, L3MatchStrings, selectMarkers] = getLinacMatchStrings(tao)
    
    # === Make changes to base lattice ===
    tao.cmd('set ele L0BF PHI0 = 0') #DNT. "loadNominalValues_2Bunch.m" had this set to zero
    tao.cmd('set ele L0BF VOLTAGE = 5.95e7') #DNT. Base value was 7.1067641E+07, new value set to change output energy to 125 MeV (down from 136.5 MeV)
    
    #L1AssertPHI0 = -19 #DNT. "loadNominalValues_2Bunch.m" had this set to -19 degrees
    setLinacPhase(        tao, L1MatchStrings, L1PhaseSet ) 
    setLinacGradientAuto( tao, L1MatchStrings, 0.335e9 - 0.125e9 ) 
    
    #L2AssertPHI0 = -37 #DNT. "loadNominalValues_2Bunch.m" had this set to -37 degrees
    setLinacPhase(        tao, L2MatchStrings, L2PhaseSet ) 
    setLinacGradientAuto( tao, L2MatchStrings, L2EnergyOffset + 4.5e9 - 0.335e9 )
    
    setLinacPhase(        tao, L3MatchStrings, 0 )
    setLinacGradientAuto( tao, L3MatchStrings, L3EnergyOffset + 10.0e9 - 4.5e9 )

def setBendkG(tao, bendName, integratedFieldkG):
    """Set bend based on EPICS-style integrated field. This involves a sign flip!"""
    bendLength = tao.ele_gen_attribs(bendName)["L"]

    desiredGradientkG = integratedFieldkG / bendLength

    #Bmad uses Tesla and opposite sign!
    tao.cmd(f"set ele {bendName} B_FIELD = {-1 * desiredGradientkG/10}")

    return

def getBendkG(tao, bendName):
    """Get bend's present EPICS-style integrated field. This involves a sign flip!"""
    bendLength = tao.ele_gen_attribs(bendName)["L"]
    bendGradientTm = tao.ele_gen_attribs(bendName)["B_FIELD"]
    bendGradientkGm = bendGradientTm*10

    bendIntegratedFieldkG = bendGradientkGm * bendLength

    #Bmad uses opposite sign!
    return -1 * bendIntegratedFieldkG

def setQuadkG(tao, quadName, integratedFieldkG):
    """Set quad based on EPICS-style integrated field. This involves a sign flip!"""
    quadLength = tao.ele_gen_attribs(quadName)["L"]

    desiredGradientkG = integratedFieldkG / quadLength

    #Bmad uses Tesla and opposite sign!
    tao.cmd(f"set ele {quadName} B1_GRADIENT = {-1 * desiredGradientkG/10}")

    return

def getQuadkG(tao, quadName):
    """Get quad's present EPICS-style integrated field. This involves a sign flip!"""
    quadLength = tao.ele_gen_attribs(quadName)["L"]
    quadGradientTm = tao.ele_gen_attribs(quadName)["B1_GRADIENT"]
    quadGradientkGm = quadGradientTm*10

    quadIntegratedFieldkG = quadGradientkGm * quadLength

    #Bmad uses opposite sign!
    return -1 * quadIntegratedFieldkG


def setSextkG(tao, sextName, integratedFieldkG):
    """Set sextupole based on EPICS-style integrated field. This involves a sign flip!"""
    sextLength = tao.ele_gen_attribs(sextName)["L"]

    desiredGradientkG = integratedFieldkG / sextLength

    #Bmad uses Tesla and opposite sign!
    tao.cmd(f"set ele {sextName} B2_GRADIENT = {-1 * desiredGradientkG/10}")

    return

def getSextkG(tao, sextName):
    """Get sextupoles's present EPICS-style integrated field. This involves a sign flip!"""
    sextLength = tao.ele_gen_attribs(sextName)["L"]
    sextGradientTm = tao.ele_gen_attribs(sextName)["B2_GRADIENT"]
    sextGradientkGm = sextGradientTm*10

    sextIntegratedFieldkG = sextGradientkGm * sextLength

    #Bmad uses opposite sign!
    return -1 * sextIntegratedFieldkG

def setAllInjectorQuads(tao, QA10361kG, QA10371kG, QE10425kG, QE10441kG, QE10511kG, QE10525kG):
    setQuadkG(tao, "QA10361", QA10361kG)
    setQuadkG(tao, "QA10371", QA10371kG)
    setQuadkG(tao, "QE10425", QE10425kG)
    setQuadkG(tao, "QE10441", QE10441kG)
    setQuadkG(tao, "QE10511", QE10511kG)
    setQuadkG(tao, "QE10525", QE10525kG)

    return

def setAllFinalFocusQuads(tao, Q5FFkG, Q4FFkG, Q3FFkG, Q2FFkG, Q1FFkG, Q0FFkG, Q0DkG, Q1DkG, Q2DkG):

    setQuadkG(tao, "Q5FF", Q5FFkG)
    setQuadkG(tao, "Q4FF", Q4FFkG)
    setQuadkG(tao, "Q3FF", Q3FFkG)
    setQuadkG(tao, "Q2FF", Q2FFkG)
    setQuadkG(tao, "Q1FF", Q1FFkG)
    setQuadkG(tao, "Q0FF", Q0FFkG)
    setQuadkG(tao, "Q0D", Q0DkG)
    setQuadkG(tao, "Q1D", Q1DkG)
    setQuadkG(tao, "Q2D", Q2DkG)

    return

def setAllWChicaneBends(tao, B1EkG, B2EkG, B3EkG):
    
    setBendkG(tao, "B1LE", B1EkG)
    setBendkG(tao, "B2LE", B2EkG)
    setBendkG(tao, "B3LE", B3EkG)
    setBendkG(tao, "B3RE", B3EkG)
    setBendkG(tao, "B2RE", B2EkG)
    setBendkG(tao, "B1RE", B1EkG)

    return

def setAllWChicaneQuads(tao, Q1EkG, Q2EkG, Q3EkG, Q4EkG, Q5EkG, Q6EkG):
    
    setQuadkG(tao, "Q1EL", Q1EkG)
    setQuadkG(tao, "Q2EL", Q2EkG)
    setQuadkG(tao, "Q3EL_1", Q3EkG)
    setQuadkG(tao, "Q3EL_2", Q3EkG)
    setQuadkG(tao, "Q4EL_1", Q4EkG)
    setQuadkG(tao, "Q4EL_2", Q4EkG)
    setQuadkG(tao, "Q4EL_3", Q4EkG)
    setQuadkG(tao, "Q5EL", Q5EkG)
    setQuadkG(tao, "Q6E", Q6EkG)
    setQuadkG(tao, "Q5ER", Q5EkG)
    setQuadkG(tao, "Q4ER_1", Q4EkG)
    setQuadkG(tao, "Q4ER_2", Q4EkG)
    setQuadkG(tao, "Q4ER_3", Q4EkG)
    setQuadkG(tao, "Q3ER_1", Q3EkG)
    setQuadkG(tao, "Q3ER_2", Q3EkG)
    setQuadkG(tao, "Q2ER", Q2EkG)
    setQuadkG(tao, "Q1ER", Q1EkG)
    

    return

def setAllWChicaneSextupoles(tao, S1ELkG, S2ELkG, S3ELkG, S3ERkG, S2ERkG, S1ERkG):
    
    setSextkG(tao, "S1EL",   S1ELkG)
    setSextkG(tao, "S2EL",   S2ELkG)
    setSextkG(tao, "S3EL_1", S3ELkG)
    setSextkG(tao, "S3EL_2", S3ELkG)
    setSextkG(tao, "S3ER_1", S3ERkG)
    setSextkG(tao, "S3ER_2", S3ERkG)
    setSextkG(tao, "S2ER",   S2ERkG)
    setSextkG(tao, "S1ER",   S1ERkG)

    return