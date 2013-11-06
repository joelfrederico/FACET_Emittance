% Usage :
%     function Erange = E200_im_get_E_axis(pixelrange, offset)

%% Changelog :
%% E. Adli, Apr 24, 2012 
%%   First version!
% E. Adli, Apr 27, 2013
%   Updated for generic sbend setting
% E. Adli, Sep 10, 2013
%   Bugfixes: FOV correction (3%) for CEGAIN and offset for CELOSS

function [Erange, Eres, Dy] = E200_cher_get_E_axis(datename, camname, visu,  pixelrange, offset, sbend_setting)

if nargin < 3
  visu = 0;
end % if

if nargin < 4
  pixelrange = 1:1392;
end % if


if nargin < 5
  offset = 0;
end % if

if nargin < 6
  sbend_setting = 20.35;
end % if


granularity = 1e-3;
if nargout > 1
  % needed for smooth Dy calc
  granularity = 1e-5;
end % if

if( strcmp(datename, '20130423') ),
%
% date_name = '2013/20130423/';
%
calib_X = 54.4e3 / 1348;
sbend_data = 20.35; % sbend setting when data was taken
B5D36DES = [11.3500   12.3500   13.3500   14.3500   15.3500   16.3500   17.3500   18.3500   19.3500   20.3500   21.3500   22.3500  23.3500   24.3500   25.3500   26.3500   27.3500   28.3500   29.3500   30.3500   31.3500   32.3500  33.3500   34.3500];
cog_Y_CELOSS = [27.3232   26.5266   26.4055   27.2094   26.4605   27.6595   53.6741  53.9436   51.0927   48.1461   45.3044   42.2732   39.4419   36.4143   33.5631   30.4242   27.4541   24.5112   21.4840  18.4459   15.3318   12.2609    9.1166    6.1244];
cog_X_CELOSS = [21.2405   20.4286   22.4629   21.1292   21.1967   22.2190   22.3395 22.2457   22.2742   22.3163   22.4323   22.4264   22.4720   22.4794   22.5229   22.5711   22.5403   22.7056   22.7159   22.7491   22.8003   22.7990   22.8187   22.7670];                
cog_Y_CEGAIN = [40.9637   38.0570   35.1332   32.2354   29.3315   26.4248   23.5381  20.6150   17.7447   14.8687   11.9948    9.0025    6.1825    3.5830   14.0234   27.4109   27.3749   27.4566   27.0755 27.0564   26.4394   26.6816   27.0306   28.4510];
cog_X_CEGAIN = [22.3960   22.4336   22.4933   22.4493   22.4319   22.4874   22.4782  22.4717   22.4773   22.5168   22.6121   22.5888   22.6368   22.5912   21.3678   20.4334   20.8170   21.5229   20.9092  21.5561   21.4583   21.6886   21.2913   21.2042];
% TEMP: compensate FOV difference of 3%
cog_Y_CEGAIN = [40.9637   38.0570   35.1332   32.2354   29.3315   26.4248   23.5381  20.6150   17.7447   14.8687   11.9948    9.0025    6.1825    3.5830   14.0234   27.4109   27.3749   27.4566   27.0755 27.0564   26.4394   26.6816   27.0306   28.4510] * -0.0741/-0.0718;


elseif (strcmp(datename, '20130408') ) 
%
% date_name = '2013/20130408/';
%
calib_X = 54.4e3 / 1348;
sbend_data = 20.35; % sbend setting when data was taken
B5D36DES = [11.3500   12.3500   13.3500   14.3500   15.3500   16.3500   17.3500   18.3500   19.3500   20.3500   21.3500   22.3500  23.3500   24.3500   25.3500   26.3500   27.3500   28.3500   29.3500   30.3500   31.3500   32.3500  33.3500   34.3500];
cog_Y_CEGAIN = [37.7917   34.9273   32.0092   29.0645   26.1395   23.2368   20.2993   17.3923   14.5810   11.6407    8.7575    5.8938    3.0646   28.4838   27.3725   26.5327   28.3731   27.1120   28.4965   27.6412   28.0491   28.1247  28.3756   28.4459];
cog_Y_CELOSS = [   28.3372   27.7983   28.1133   27.1794   28.5226   53.6702   53.6244   50.7250   47.8570   44.9133   41.9727   39.0923   36.1217   33.1782   30.2028   27.2440   24.2440   21.2538   18.2208   15.2098   12.1159    9.1039   6.0705    3.0936];
else
  disp('EA: no calib for this date');
  stop;
end% if

if( strcmp(camname,'CEGAIN') ),
% CEGAIN
n_range = 1:13;
my_meas = [B5D36DES(n_range)' cog_Y_CEGAIN(n_range)'/calib_X*1e3]; % [GeV; pix]
my_meas = [20.3500  cog_Y_CEGAIN(10)/calib_X*1e3; my_meas]; % add nominal at start
[p,y] = E200_cher_E_calib(my_meas, offset, visu, sbend_data, sbend_setting, granularity);
elseif( strcmp(camname,'CELOSS') ),
% CELOSS
n_range = 8:24;
my_meas = [B5D36DES(n_range)' cog_Y_CELOSS(n_range)'/calib_X*1e3]; % [GeV; pix]
my_meas = [20.3500  cog_Y_CELOSS(10)/calib_X*1e3; my_meas]; % add nominal at start
[p,y] = E200_cher_E_calib(my_meas, offset, visu, sbend_data, sbend_setting, granularity);
elseif( strcmp(camname,'CNEAR') ),
  disp('EA: no calib for CNEAR. Returning pixels');
  p=0:1393;
  y=0:1393;
else
  disp('EA: no calib for this cam. Returning pixels');
  p=0:1393;
  y=0:1393;
end% if

% calc E axis
n_count = 0;
for ix=pixelrange,
  n_count = n_count + 1;
  n_index = max(find(y < ix));
   Erange(n_count) = p(n_index);
end% for

% calc Eres
Yres = 300e-6;% [m] - as measured with pencil beam March 2013
%Yres = 70e-6;% [m] - as calculated by stainless steel window, May 20
Nres = round(Yres/calib_X*1e6); % [pix]
n_count = 0;
for ix=pixelrange(1:end-Nres),
  n_count = n_count + 1;
  Eres(n_count) = Erange(n_count+Nres)-Erange(n_count);
end% for
% lin. int. for last steps
n_count = n_count - 1;
for ix=pixelrange(end-Nres:end-1),
  n_count = n_count + 1;
  Eres(n_count+1) = 2*Eres(n_count)-Eres(n_count-1);
end% for


% calc dispersion
n_count = 0;
for ix=pixelrange(1:end-1),
  n_count = n_count + 1;
  dy = calib_X*1e-6; % [m]
  dp = Erange(n_count+1)-Erange(n_count); % [GeV]
  p0 = Erange(n_count); % [GeV]
  %p0_0 = sbend_setting;
  Dy(n_count) = dy / dp * p0;
end% for
% lin. int. for last step
Dy(n_count+1) = 2*Dy(n_count) - Dy(n_count-1);
