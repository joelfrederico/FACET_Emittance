function out = matlab_script(c,x_min,x_max,y_min,y_max)
	global data
	camname = 'ELANEX';
	
	% Usual data
	day = '20140422';
	data_set = 'E200_12561';

	if isempty(data)
	
		% day = '20130429';
		% data_set = 'E200_10911';
		pathstr=['/nas/nas-li20-pm00/E200/2014/' day '/' data_set '/' data_set '.mat']
		
		data=E200_load_data(pathstr);
	end

	
	% Save for python loading
	save('forpython.mat','data','-v7.3');

	% setenv('DYLD_LIBRARY_PATH', '/usr/local/bin:/opt/local/lib:');
	% unix('source ~/.profile; ./analyze_matlab.py forpython.mat -v');
	out=data;
end
