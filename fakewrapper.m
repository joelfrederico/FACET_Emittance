global gdata

uids = E200_api_getUID(gdata.raw.scalars.step_num,6);
uids = intersect(gdata.raw.images.CEGAIN.UID,uids);
wanted_UIDs = uids(32);

imgstruct = gdata.raw.images.CEGAIN;

% [imgs,bg]=E200_load_images(imgstruct,wanted_UIDs,data);

% img = imgs{1};

% % Threshold at 3000
% img(img<3000) = 0;

% % ROI
% for j=1:size(img,1)
%         for i=1:size(img,2)
%                 if ~ ( ( i>580 ) && ( i<700 ) && ( j>380 ) && ( j<580 ) )
%                         img(j,i) = 0;
%                 end
%         end
% end
% imagesc(img)
% ximg = sum(img,1);
% xvec = 1:length(ximg);
% xcent = sum(xvec.*ximg)/sum(ximg)

% ximg = transpose(sum(img,2));
% xvec = 1:length(ximg);
% xcent = sum(xvec.*ximg)/sum(ximg)

matlab_script(gdata,wanted_UIDs,imgstruct)
