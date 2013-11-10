function emittance_measure_ss(handles)
	% For debugging, readability
	global data
	data = handles.data;

	camname = getlistsel(handles.Cams);

	% ====================================
	% Get current image & size
	% ====================================
	img_num=int32(get(handles.imageslider,'Value'));
	img = handles.images{img_num};
	imgstruct = get_imgstruct(handles);
	[ysize,xsize] = size(img)
	xvec = 1:xsize;
	yvec = 1:ysize;

	% ====================================
	% Get UID for current GUI selections
	% ====================================
	stepval = get(handles.Stepnumberslider,'Value');
	uid = E200_api_getUID(data.raw.scalars.step_num,stepval);
	uid = intersect(uid,imgstruct.UID);
	uid = uid(img_num)

	ext_fig = figure;

	% ====================================
	% Get BDES's
	% ====================================
	qs1_bdes = E200_api_getdat(data.raw.scalars.LI20_LGPS_3261_BDES,uid);
	qs2_bdes = E200_api_getdat(data.raw.scalars.LI20_LGPS_3311_BDES,uid);

	% ====================================
	% Get Energy Axis and create ticks
	% ====================================
	e_axis = E200_cam_E_cal(data,yvec);
	xticks = 0:xsize/5:xsize

	imagesc(img);
	
	matlab_script(data,uid,imgstruct)
end

function K = BtoK(B,E,l)
	E=20.35;
	Brho=E/0.029979;
	K=bdes/(Brho*l);
end
