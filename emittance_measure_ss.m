function emittance_measure_ss(handles)
	cam_contents = get(handles.Cams,'String')
	camname = cam_contents{get(handles.Cams,'Value')}



	matlab_script(handles.data);
end
