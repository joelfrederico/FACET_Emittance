import re
import numpy as np

def E200_get_data_cam(group):
	searchlist = group.keys()
	camsearch = re.compile('ss_([a-zA-Z0-9]*)')

	camname_list = np.array([],dtype=object)
	for val in searchlist:
		result = camsearch.match(val)
		if result != None:
			camname = result.groups()[0]

			if camname not in camname_list:
				camname_list = np.append(camname_list,camname)

	return camname_list
