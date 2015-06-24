#!/usr/bin/env python

import mytools as mt
import E200
import numpy as np

sets      = ['20140629', '13537']
setdate   = sets[0]
setnumber = sets[1]

loadfile = 'nas/nas-li20-pm00/E200/2014/{}/E200_{}'.format(setdate, setnumber)
data     = E200.E200_load_data(loadfile)

wf           = data.write_file
processed_wf = wf['data']['processed']
scalars_wf   = processed_wf['scalars']
vectors_wf   = processed_wf['vectors']
arrays_wf    = processed_wf['arrays']

rf         = data.read_file
raw_rf     = rf['data']['raw']
scalars_rf = raw_rf['scalars']
vectors_rf = raw_rf['vectors']
arrays_rf  = raw_rf['arrays']

# results = E200_get_data_cam(scalars)
# print(results)

# ======================================
# Get UID from analysis output.
# ======================================

camname         = 'ELANEX'
head_str        = 'ss_{}_'.format(camname)
energy_axis_str = vectors_wf['{}energy_axis'.format(head_str)]
uids            = energy_axis_str['UID'].value
uid             = uids[0]

print(type(uid))

elanex_str = raw_rf['images']['ELANEX']
# uid      = elanex_str['UID'][0][0]
elanex     = E200.E200_api_getdat(elanex_str, uid)

setQS_str = scalars_rf['step_value']
setQS_dat = E200.E200_api_getdat(setQS_str)
setQS_unique = np.unique(setQS_dat.dat)
print('Unique setQS: {}'.format(setQS_unique))
for val in setQS_unique:
    setQS  = mt.hardcode.setQS(val)
    ymotor = setQS.elanex_y_motor()
    QS1_BDES = setQS.QS1.BDES
    QS2_BDES = setQS.QS2.BDES

    print('setQS: {val}, ymotor: {ymotor}, QS1 BDES: {QS1_BDES}, QS2 BDES: {QS2_BDES}'.format(
            val      = val,        # noqa
            ymotor   = ymotor,     # noqa
            QS1_BDES = QS1_BDES,   # noqa
            QS2_BDES = QS2_BDES    # noqa
            )
        )

elanex_y_string = 'XPS_LI20_DWFA_M5'

elanex_y_str = scalars_rf[elanex_y_string]
elanex_y = E200.E200_api_getdat(elanex_y_str)
print('Unique elanex_y: {}'.format(np.unique(elanex_y.dat)))

qs1_string = 'LI20_LGPS_3261_BDES'
qs1_str = scalars_rf[qs1_string]
qs1_dat = E200.E200_api_getdat(qs1_str)
print('Unique qs1: {}'.format(np.unique(qs1_dat.dat)))

qs2_string = 'LI20_LGPS_3311_BDES'
qs2_str = scalars_rf[qs2_string]
qs2_dat = E200.E200_api_getdat(qs2_str)
print('Unique qs2: {}'.format(np.unique(qs2_dat.dat)))
