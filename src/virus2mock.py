"""Mapping from virus-infected plate IDs to their matched mock-infected controls.

Each key is a plate identifier of the form ``V<virus>_S<set>_R<rep>``
(e.g. ``'V1_S1_R1'``) and the corresponding value is the mock plate ID
(``V0_S<set>_R<rep>``) that was run on the same day and passage and therefore
serves as the appropriate baseline for normalisation.

The mapping encodes the experimental design: up to 5 virus plates were
matched per mock plate, rotating mock-plate assignments within each set
and biological replicate to account for passage variability.
"""

virus2mock = {
    'V1_S1_R1':'V0_S1_R1',
    'V2_S1_R1':'V0_S1_R1',
    'V3_S1_R1':'V0_S1_R1',
    'V4_S1_R1':'V0_S1_R1',
    'V5_S1_R1':'V0_S1_R1',
    
    'V6_S1_R1':'V0_S1_R2',
    'V7_S1_R1':'V0_S1_R2',
    'V1_S1_R2':'V0_S1_R2',
    'V2_S1_R2':'V0_S1_R2',
    'V3_S1_R2':'V0_S1_R2',
    
    'V4_S1_R2':'V0_S1_R3',
    'V5_S1_R2':'V0_S1_R3',
    'V6_S1_R2':'V0_S1_R3',
    'V7_S1_R2':'V0_S1_R3',
    'V1_S1_R3':'V0_S1_R3',
    
    'V2_S1_R3':'V0_S1_R4',
    'V3_S1_R3':'V0_S1_R4',
    'V4_S1_R3':'V0_S1_R4',
    'V5_S1_R3':'V0_S1_R4',
    'V6_S1_R3':'V0_S1_R4',

    'V7_S1_R3':'V0_S1_R5',

    'V1_S2_R1':'V0_S2_R1',
    'V2_S2_R1':'V0_S2_R1',
    'V3_S2_R1':'V0_S2_R1',
    'V4_S2_R1':'V0_S2_R1',
    'V5_S2_R1':'V0_S2_R1',
    
    'V6_S2_R1':'V0_S2_R2',
    'V7_S2_R1':'V0_S2_R2',
    'V1_S2_R2':'V0_S2_R2',
    'V2_S2_R2':'V0_S2_R2',
    'V3_S2_R2':'V0_S2_R2',
    
    'V4_S2_R2':'V0_S2_R3',
    'V5_S2_R2':'V0_S2_R3',
    'V6_S2_R2':'V0_S2_R3',
    'V7_S2_R2':'V0_S2_R3',
    'V1_S2_R3':'V0_S2_R3',

    'V2_S2_R3':'V0_S2_R4',
    'V3_S2_R3':'V0_S2_R4',
    'V4_S2_R3':'V0_S2_R4',
    'V5_S2_R3':'V0_S2_R4',
    'V6_S2_R3':'V0_S2_R4',
    
    'V7_S2_R3':'V0_S2_R5',
    
    'V1_S3_R1':'V0_S3_R1',
    'V2_S3_R1':'V0_S3_R1',
    'V3_S3_R1':'V0_S3_R1',
    'V4_S3_R1':'V0_S3_R1',
    'V5_S3_R1':'V0_S3_R1',
    
    'V6_S3_R1':'V0_S3_R2',
    'V7_S3_R1':'V0_S3_R2',
    'V1_S3_R2':'V0_S3_R2',
    
    'V2_S3_R2':'V0_S3_R3',
    'V3_S3_R2':'V0_S3_R3',
    'V4_S3_R2':'V0_S3_R3',

    'V5_S3_R2':'V0_S3_R4',
    'V6_S3_R2':'V0_S3_R4',
    'V7_S3_R2':'V0_S3_R4',
    'V1_S3_R3':'V0_S3_R4',
    'V2_S3_R3':'V0_S3_R4',

    'V3_S3_R3':'V0_S3_R5',
    'V4_S3_R3':'V0_S3_R5',
    'V5_S3_R3':'V0_S3_R5',
    'V6_S3_R3':'V0_S3_R5',
    'V7_S3_R3':'V0_S3_R5',

    'V1_S4_R1':'V0_S4_R1',
    'V2_S4_R1':'V0_S4_R1',
    'V3_S4_R1':'V0_S4_R1',
    'V4_S4_R1':'V0_S4_R1',
    'V5_S4_R1':'V0_S4_R1',

    'V6_S4_R1':'V0_S4_R2',
    'V7_S4_R1':'V0_S4_R2',
    'V1_S4_R2':'V0_S4_R2',
    'V2_S4_R2':'V0_S4_R2',
    'V3_S4_R2':'V0_S4_R2',

    'V4_S4_R2':'V0_S4_R3',
    'V5_S4_R2':'V0_S4_R3',
    'V6_S4_R2':'V0_S4_R3',
    'V7_S4_R2':'V0_S4_R3',
    'V1_S4_R3':'V0_S4_R3',
    
    'V2_S4_R3':'V0_S4_R4',
    'V3_S4_R3':'V0_S4_R4',
    'V4_S4_R3':'V0_S4_R4',
    'V5_S4_R3':'V0_S4_R4',
    'V6_S4_R3':'V0_S4_R4',

    'V7_S4_R3':'V0_S4_R5',
}