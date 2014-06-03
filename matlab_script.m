function out = matlab_script(data,camname,imgnum)
	% Save for python loading
	display(camname)
	display(imgnum)
	save('forpython.mat','data','camname','imgnum','-v7.3');

	% setenv('DYLD_LIBRARY_PATH', '/usr/local/bin:/opt/local/lib:');
	% unix('source ~/.profile; ./analyze_matlab.py forpython.mat -v');
	LD_LIBRARY_PATH_command ='export LD_LIBRARY_PATH=/home/fphysics/joelfred/opt-base/lib:/usr/local/lcls/package/intel/fc/10.1.015/lib:/usr/X11R6/lib:/usr/local/lcls/package/oracle/product/11.1.0.6/client/lib:/usr/local/lcls/package/oracle/product/11.1.0.6/client::/usr/local/facet/package/java/jdk1.7.0_05/jre/lib/i386:/usr/local/facet/package/java/jdk1.7.0_05/jre/lib/i386/server:/usr/local/facet/package/python/tcltk/lib:/usr/local/facet/epics/base/base-R3-14-8-2-lcls6_p1/lib/linux-x86:/usr/local/facet/epics/extensions/extensions-R3-14-8-2/lib/linux-x86:/usr/local/facet/tools/lib/linux-x86;' 
	PYTHONPATH_command = 'export PYTHONPATH=/home/fphysics/joelfred/opt-base/lib/python2.7/site-packages:/home/fphysics/joelfred/SDDSTOOLS:/usr/local/lcls/package/python/python2.7.4/lib/python2.7/site-packages:$PYTHONPATH;'
	unix([LD_LIBRARY_PATH_command PYTHONPATH_command ' ./runGUI.py']);
end
