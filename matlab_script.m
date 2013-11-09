% function out = emittance_measure_ss(c,x_min,x_max,y_min,y_max)
function out = matlab_script(data,wanted_UIDs,imgstruct)
	global data
	
	delE =0;
	
	% ====================================
	% Load the desired image
	% ====================================
	[imgs,bg]=E200_load_images(imgstruct,wanted_UIDs,data);
	% [this,bool] = ismember(wanted_UIDs,imgstruct.UID);
	% res         = imgstruct.RESOLUTION(bool);
	res = E200_api_getdat(imgstruct.RESOLUTION,wanted_UIDs)
	
	% ====================================
	% Manipulate image to plot correctly
	% ====================================
	img_sub=imgs{1}-uint16(bg{1});
	% img_sub=imgs{1};
	img=img_sub;
	% img=rot90(img);
	img=transpose(img);
	img=fliplr(img);
	plotimg=log10(double(img));
	plotimg=img;
	% size(img)
	
	% ====================================
	% Determine spectrometer 
	% bend settings/calibration
	% ====================================
	bend_struct = data.raw.scalars.LI20_LGPS_3330_BDES;
	bool        = ismember(wanted_UIDs,bend_struct.UID);
	% display(bend_struct.UID)
	B5D36 = bend_struct.dat{1};
	% display(B5D36);
	e_axis=E200_cher_get_E_axis('20130423','CELOSS',0,[1:1392],0,B5D36);

	% ====================================
	% Plot Image
	% ====================================
	close('all');
	cmap  = custom_cmap();
	colormap(cmap.wbgyr);
	% colormap(gray)
	immax = max(max(plotimg));
	% size(plotimg)
	fig = imagesc(plotimg,[0,immax]);
	out = fig;

	fig    = imagesc(plotimg(y_min:y_max,x_min:x_max),[0,immax]);
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
	x_meter   = (x_pix-mean(x_pix)) * res * 10^-6;
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
	
	size(processed_data.sum_x)
	for i=1:n_groups
		y_pix_vec = [hist_vec(i):hist_vec(i)+n_rows];
		subimg = transpose(img(y_pix_vec,x_min:x_max));
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
	
	% figure;
	% plot(hist_data(:,1),hist_data(:,2)*(10^3)^2,'-o');
	% tilefigs;
	
	% ====================================
	% Save for python loading
	% ====================================
	save('forpython.mat','img','img_sub','hist_data','B5D36','processed_data','-v7');

	setenv('DYLD_LIBRARY_PATH', '/usr/local/bin:/opt/local/lib:');
	% unix('source ~/.profile; ./analyze_matlab.py forpython.mat -v');
	out=data;
end
