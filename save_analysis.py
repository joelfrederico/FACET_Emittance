import logging
logger=logging.getLogger(__name__)
loggerlevel=logging.DEBUG
#  loggerlevel = logging.CRITICAL

import E200
import numpy as np

def save_analysis(
        dataset      ,
        analyze_out  ,
        rect_arr     ,
        camname      ,
        oimg         ,
        uid          ,
        valid = False,
        ):
    # =====================================
    # Extract results and save
    # =====================================
    # Save location
    logger.log(level=loggerlevel,msg='Saving analysis to file...')
    processed = dataset.write_file['data']['processed']
    vectors = processed['vectors']
    scalars = processed['scalars']
    arrays = processed['arrays']

    # Results
    out        = analyze_out
    scanfit    = out.scanfit
    fitresults = scanfit.fitresults

    logger.info('Value for rect_arr: {}'.format(rect_arr))

    result_array = [
        [scalars , 'ss_{}_betastar'.format(camname)         , fitresults.Beam.betastar ] ,
        [scalars , 'ss_{}_emit_n'.format(camname)           , fitresults.emitn         ] ,
        [scalars , 'ss_{}_img_max'.format(camname)          , analyze_out.img.max()    ] ,
        [scalars , 'ss_{}_sstar'.format(camname)            , fitresults.Beam.sstar    ] ,
        [vectors , 'ss_{}_LLS_beta'.format(camname)         , fitresults.beta          ] ,
        [vectors , 'ss_{}_LLS_y_error'.format(camname)      , fitresults.y_error       ] ,
        [vectors , 'ss_{}_energy_axis'.format(camname)      , out.eaxis                ] ,
        [vectors , 'ss_{}_img_eaxis'.format(camname)        , out.imgeaxis             ] ,
        [vectors , 'ss_{}_oimg_eaxis'.format(camname)       , out.oimgeaxis            ] ,
        [vectors , 'ss_{}_rect'.format(camname)             , rect_arr                 ] ,
        [vectors , 'ss_{}_variance'.format(camname)         , out.variance             ] ,
        [arrays  , 'ss_camname'                             , camname                  ] ,
        [arrays  , 'ss_{}_LLS_X_unweighted'.format(camname) , fitresults.X_unweighted  ] ,
        [arrays  , 'ss_{}_image'.format(camname)            , oimg                     ] ,
        [arrays  , 'ss_{}_selected_img'.format(camname)     , out.img                  ] ,
        [scalars , 'ss_{}_valid'.format(camname)            , valid                    ]
        ]

    # Write results to file
    for pair in result_array:
        logger.log(level=loggerlevel,msg='Writing to group {}...'.format(pair[1]))
        try:
            group = pair[0]
            name  = pair[1]
            value = pair[2]

            E200.E200_create_data(group,name)
            E200.E200_api_updateUID(group[name],UID=uid,value=value)

            group.file.flush()
            #  _write_result(pair[0],pair[1],uid,pair[2])
        except:
            logger.critical('Error on saving group {} with value: {}, type: {}'.format(pair[1],pair[2],type(pair[2])))
            raise

    logger.debug('Finished saving')
