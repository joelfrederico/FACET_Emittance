function emittance_measure_ss(handles)
	gdata=handles.data;
	
	% Get and load the current image
	imgnum=int32(get(handles.imageslider,'Value'));
	img=handles.images{imgnum};
	
	% Get step number
	step_num = int32(get(handles.Stepnumberslider,'Value'))
	if step_num == 0
		step_num = 1
	end

	% Find uid
	uids = E200_api_getUID(gdata.raw.scalars.step_num,step_num);
	uids = intersect(gdata.raw.images.CEGAIN.UID,uids);
	% wanted_UIDs = uids(imgnum);
	
	imgstruct = gdata.raw.images.CEGAIN;
	
	matlab_script(gdata,img)
end
