import logging
logger=logging.getLogger(__name__)
loggerlevel=logging.DEBUG

import E200
import numpy as np

def save_analysis(
		dataset     ,
		analyze_out ,
		rect_arr    ,
		camname     ,
		oimg        ,
		uid
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

	#  rect_arr = np.array([rect.get_x(),rect.get_y(),rect.get_height(),rect.get_width()])
	# print rect_arr
	logger.info('Value for rect_arr: {}'.format(rect_arr))

	result_array = [
		[arrays  , 'ss_camname'                             , camname                  ] ,
		[scalars , 'ss_{}_emit_n'.format(camname)           , fitresults.emitn         ] ,
		[scalars , 'ss_{}_betastar'.format(camname)         , fitresults.Beam.betastar ] ,
		[scalars , 'ss_{}_sstar'.format(camname)            , fitresults.Beam.sstar    ] ,
		[vectors , 'ss_{}_energy_axis'.format(camname)      , out.eaxis                ] ,
		[vectors , 'ss_{}_variance'.format(camname)         , out.variance             ] ,
		[vectors , 'ss_{}_LLS_beta'.format(camname)         , fitresults.beta          ] ,
		[arrays  , 'ss_{}_LLS_X_unweighted'.format(camname) , fitresults.X_unweighted  ] ,
		[vectors , 'ss_{}_LLS_y_error'.format(camname)      , fitresults.y_error       ] ,
		[vectors , 'ss_{}_rect'.format(camname)             , rect_arr                 ] ,
		[arrays  , 'ss_{}_image'.format(camname)            , oimg                     ]
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
			logger.critical('Error on saving group {} with value: {}'.format(pair[1],pair[2]))
			raise

	logger.debug('Finished saving')
