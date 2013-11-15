% function out = emittance_measure_ss(c,x_min,x_max,y_min,y_max)
function out = matlab_script(data,wanted_UIDs,img_sub)
	% close('all');
	
	delE =0;
	
	% ====================================
	% Load the desired image
	% ====================================
	% [imgs,bg]=E200_load_images(imgstruct,wanted_UIDs,data);
	% [this,bool] = ismember(wanted_UIDs,imgstruct.UID);
	% res         = imgstruct.RESOLUTION(bool);
	% res = imgstruct.RESOLUTION(imgstruct.UID==wanted_UIDs);
	res = 10.3934;
	
	% ====================================
	% Manipulate image to plot correctly
	% ====================================
	% img_sub=imgs{1}-uint16(bg{1});
	% img_sub=imgs{1};
	img=img_sub;
	% img=rot90(img);
	% img=transpose(img);
	% img=fliplr(img);
	plotimg=log10(double(img));
	plotimg=img;
	% size(img)

	% ====================================
	% Get yvec for energy
	% ====================================
	[ysize,xsize] = size(img);
	yvec = 1:ysize;
	
	% ====================================
	% Determine spectrometer 
	% bend settings/calibration
	% ====================================
	% bend_struct = data.raw.scalars.LI20_LGPS_3330_BDES;
	% bool        = ismember(wanted_UIDs,bend_struct.UID);
	% display(bend_struct.UID)
	% B5D36 = bend_struct.dat{1};
	% display(B5D36);
	% e_axis=E200_cher_get_E_axis('20130423','CELOSS',0,[1:1392],0,B5D36);
	e_axis = E200_cam_E_cal(data,yvec,res);
	e_axis = fliplr(e_axis);
	% plot(e_axis);

	% ====================================
	% Get zoom region, 2% bandwidth
	% ====================================
	E0 = 20.35;
	bandE = 0.01*E0;
	Emin = E0-bandE;
	Emax = E0+bandE;
	y_min = yvec(sum(e_axis<Emin));
	y_max = yvec(sum(e_axis<Emax));
	x_min = 200;
	x_max = xsize;
	
	% ====================================
	% Plot Image
	% ====================================
	cmap  = custom_cmap();
	colormap(cmap.wbgyr);
	% colormap(gray)
	immax = max(max(plotimg));
	% size(plotimg)
	fig = figure;
	imagesc(plotimg,[0,immax]);

		yticks = 1:round(ysize/5):ysize;
		% yticklabels = (-ymean*res:ysize*res/5:ymean*res)/10^3;
		yticklabels = e_axis(1:round(ysize/5):ysize);
		yticklabelstr = {};
		for i=1:size(yticklabels,2)
			yticklabelstr = [yticklabelstr sprintf('%03.2f',yticklabels(i))];
		end
		% display(yticklabels)
		% display(yticklabelstr)
		set(gca,'YTick',yticks);
		set(gca,'YTickLabel',yticklabelstr);

	% figure;
	% fig    = imagesc(plotimg(y_min:y_max,x_min:x_max),[0,immax]);
	% fig   = surf(double(plotimg(y_min:y_max,x_min:x_max)));
	y_int  = round((y_max-y_min)/10);
	y_vec  = [y_min:y_int:y_max];
	x_int  = round((x_max-x_min)/10);
	x_vec  = [x_min:x_int:x_max];
	x_mean = mean(x_vec);
	x_axis = (x_vec-x_mean)*res*10^-3;

	% set(gca,'YTick',y_vec-y_min,'YTickLabel',e_axis(y_vec),'YDir','normal', ...
	%         'XTick',x_vec-x_min,'XTickLabel', x_axis...
	%         );

	% pcolor([1:size(img,2)],e_axis,img);
	% shading('flat');

	% ====================================
	% Create a histogram of std dev
	% ====================================
	n_rows    = 10;
	hist_vec  = [y_min:n_rows:y_max];
	n_groups  = length(hist_vec);
	hist_data = zeros(n_groups,2);
	% length(hist_vec)
	x_pix     = [x_min:x_max];
	x_meter   = (x_pix-mean(x_pix)) * res * 10^-6 / sqrt(2);
	x_sq      = x_meter.^2;
	% size(x_sq)

	processed_data.x_meter  = x_meter;
	processed_data.e_axis   = e_axis;
	processed_data.img      = img;
	processed_data.x_min    = x_min;
	processed_data.x_max    = x_max;
	processed_data.n_rows   = n_rows;
	processed_data.n_groups = n_groups;
	processed_data.sum_x    = zeros(n_groups,x_max-x_min+1);
	processed_data.sum_y    = zeros(n_groups,11);
	% qs1_bdes = E200_api_getdat(data.raw.scalars.LI20_LGPS_3261_BDES,wanted_UIDs);
	% qs2_bdes = E200_api_getdat(data.raw.scalars.LI20_LGPS_3311_BDES,wanted_UIDs);
	% processed_data.qs1_k_half = BtoK(qs1_bdes,20.35,0.5)
	% processed_data.qs2_k_half = BtoK(qs2_bdes,20.35,0.5)
	processed_data.qs1_k_half = 3.077225846087095e-01;
	processed_data.qs2_k_half = -2.337527121004531e-01;
	
	% size(processed_data.sum_x)
	for i=1:n_groups
		y_pix_vec = [hist_vec(i):hist_vec(i)+n_rows];
		x_pix_vec = x_min:x_max;
		subimg = transpose(img(y_pix_vec,x_pix_vec));
		subimg_x = sum(subimg,2);
		subimg_y = sum(subimg,1);

		hist_data(i,2) = x_sq*subimg_x/sum(subimg_x);
		% size(subimg_x)
		% size(processed_data.sum_x(i,:))
		% size(subimg_y)
		processed_data.sum_x(i,:) = transpose(subimg_x);
		processed_data.sum_y(i,:) = subimg_y;


		% size(subimg_y)
		% size(e_axis(y_pix_vec))
		hist_data(i,1) = subimg_y*transpose(e_axis(y_pix_vec))/sum(subimg_y);
	end
	
	figure;
	imagesc(img(y_pix_vec,x_pix_vec));
	% plot(hist_data(:,1),hist_data(:,2)*(10^3)^2,'-o');
	% tilefigs;
	
	% ====================================
	% Save for python loading
	% ====================================
	curpath = pwd();
	savefile = fullfile(curpath,'tempfiles','forpython.mat');
	save(savefile,'img','img_sub','hist_data','processed_data','-v7');

	% ====================================
	% Run python in unix.
	% ====================================
	env_setup = [set_profile ' joelfred;' set_PYTHONPATH];
	unix([env_setup '~/E200_DRT/aux_functions/FACET_Emittance/analyze_matlab.py ' savefile ' -v']);

	out=data;
end
