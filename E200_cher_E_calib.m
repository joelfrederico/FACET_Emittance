% Usage :
%     function [p,y] = E200_cher_E_calib(y_meas, offset, visu)

% Changelog :
% E. Adli, Apr 11, 2013
%   First version!
% E. Adli, Apr 27, 2013
%   Updated for generic sbend setting
% E. Adli, Sep 10, 2013
%   Bugfixes: FOV correction (3%) for CEGAIN and offset for CELOSS

function [p,y] = E200_cher_E_calib(y_meas, offset, visu, sbend_data, sbend_setting, granularity)

if nargin < 2
  offset = 0;
end % if

if nargin < 3
  visu = 0;
end % if

if nargin < 4
  sbend_data = 20.35;
end % if

if nargin < 5
  sbend_setting = 20.35;
end % if

if nargin < 6
  granularity = 1e-3;
end % if



% scale B5D36 in case different value from nominal
y_meas(:,1) = y_meas(:,1) * sbend_setting / sbend_data;

% one can add offset here
y_meas(:,2) = y_meas(:,2) + offset;

% fit
P = polyfit(y_meas(:,1), y_meas(:,2), 1);

y_inf = P(2)*1.0; % + offset; 
p_0 = y_meas(1,1); 
% or here, does not matter, except for plotting
%y_0 = y_meas(1,2) + offset;
y_0 = y_meas(1,2);

p_fit = 0:40;
y_fit = P(2) + P(1)*p_fit;

p = 1:granularity:150;
y = y_inf + (y_0 - y_inf)*p_0./p;

if(visu)
  hh = plot(y_meas(:,1), y_meas(:,2), 'xk');
  set(hh, 'LineWidth', 3);
  hold on;
  plot(p_fit, y_fit, '-r');
  hold off;
  grid on;
  xlabel('B5D36_{BDES} [GeV]');
  ylabel('y [pix]');
  pause;

  hh = plot(y, p);
  set(hh, 'LineWidth', 3);
  grid on;
  xlabel('y [pix]');
  ylabel('E [GeV]');
  axis([49 1392 0 60]);
  pause;
end% if

