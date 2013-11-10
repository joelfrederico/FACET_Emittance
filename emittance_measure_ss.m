function emittance_measure_ss(handles)
	% For debugging, readability
	global data
	data = handles.data;

	camname = getlistsel(handles.Cams);

	% ====================================
	% Get current image
	% ====================================
	img_num=int32(get(handles.imageslider,'Value'));
	img = handles.images{img_num};
	imgstruct = get_imgstruct(handles);

	% ====================================
	% Get UID for current GUI selections
	% ====================================
	stepval = get(handles.Stepnumberslider,'Value');
	uid = E200_api_getUID(data.raw.scalars.step_num,stepval);
	uid = intersect(uid,imgstruct.UID);
	uid = uid(img_num);

	ext_fig = figure;
	imagesc(img);

	% ====================================
	% Get BDES's
	% ====================================
	qs1_bdes = E200_api_getdat(data.raw.scalars.LI20_LGPS_3261_BDES,uid);
	qs2_bdes = E200_api_getdat(data.raw.scalars.LI20_LGPS_3311_BDES,uid);

	% matlab_script(handles.data,img);
end
