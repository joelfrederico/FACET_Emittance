import logging
logger = logging.getLogger(__name__)

import E200
import h5py as h5
import mainwindow_auto as mw
import mytools as mt
import numpy as np
import time

from PyQt4 import QtGui


class ButterflyGUI(QtGui.QMainWindow):
    def __init__(self,
            analyzefcn      ,
            savefcn         ,
            dataset = None  ,
            camname = None  ,
            imgnum  = None  ,
            verbose = False
            ):
        # ======================================
        # Save default info
        # ======================================
        self.verbose    = verbose

        self.analyzefcn = analyzefcn
        self.savefcn    = savefcn
        self.dataset    = dataset
        self.data       = dataset.read_file['data']
        self.infile     = dataset.read_file
        self.camname    = camname
        self.imgnum     = imgnum

        # ======================================
        # Initialize class
        # ======================================
        QtGui.QMainWindow.__init__(self)
    
        # ======================================
        # Use QT Designer window
        # ======================================
        self.ui = mw.Ui_MainWindow()
        self.ui.setupUi(self)

        # ======================================
        # Connect "Redo Analysis" button
        # ======================================
        self.ui.analyzebtn.clicked.connect(self.run_sim)

        # ======================================
        # Load file passed in
        # ======================================
        if camname is None:
            camname = self.data['raw']['images'].keys()
            camname = camname[0]
        if imgnum is None:
            imgnum = 1
        # if verbose:
        #         print 'Camera name is: {}, image number is: {}'.format(camname, imgnum)
        logger.debug('Camera name is: {}, image number is: {}'.format(camname, imgnum))
        self.loadfile(camname, imgnum)

        self.ui.imageview_mpl.setSliderValue(3600)
        self.ui.imageview_mpl._img.rectChanged.connect(self.saverect)

        # ======================================
        # Connect camname_combobox
        # ======================================
        self.ui.camname_combobox.currentIndexChanged.connect(self.camname_combobox_changed)

        # ======================================
        # Connect imagenum_slider
        # ======================================
        # Disable tracking
        self.ui.imagenum_slider.setTracking(False)
        self.ui.imagenum_slider.valueChanged.connect(self.imagenum_slider_changed)

        # ======================================
        # Connect camname_combobox
        # ======================================
        self.ui.imagenum_valid_checkbox.stateChanged.connect(self.updateResults)

        self.ui.saveworld.clicked.connect(self.saveworld)

        # =========================================
        # Configure and Connect plot type selector
        # =========================================
        self.ui.plottype.clear()
        self.plotoptions = np.array([
            ['Normalized Emittance', lambda val:val.scanfit.fitresults.emitn],  # noqa
            ['Beta',                 lambda val:val.scanfit.fitresults.twiss.beta],  # noqa
            ['Beta*',                lambda val:val.scanfit.fitresults.twiss.betastar],  # noqa
            ['Alpha',                lambda val:val.scanfit.fitresults.twiss.alpha],  # noqa
            ['s*',                   lambda val:val.scanfit.fitresults.twiss.sstar],  # noqa
            ['MinSpot',              lambda val:val.scanfit.fitresults.twiss.minspotsize(val.scanfit.fitresults.emit)],  # noqa
            ['Geometric Emittance',  lambda val:val.scanfit.fitresults.emit]  # noqa
            ])
        self.ui.plottype.addItems(self.plotoptions[:, 0])
        # self.ui.plottype.addItems(['emit', 'emitn'])
        self.ui.plottype.currentIndexChanged.connect(self.plotdataset)

        logger.info('UI finished loading, idle...')

    def saverect(self, rect):
        ind = self.ui.imagenum_slider.value-1
        uid = self.allimgs.uid[ind]
        # uid = uid[0]
        # print 'UID to save: {:0.0f}'.format(uid)
        processed = self.dataset.write_file['data']['processed']
        vectors = processed['vectors']
        scalars = processed['scalars']
        rect_xy = np.array(rect.get_xy())
        E200.E200_api_updateUID(vectors['ss_{}_rect_xy'.format(self.camname)], UID=uid, value=rect_xy)
        E200.E200_api_updateUID(scalars['ss_{}_width'.format(self.camname)], UID=uid, value=rect.get_width())
        E200.E200_api_updateUID(scalars['ss_{}_height'.format(self.camname)], UID=uid, value=rect.get_height())
        self.data.file.flush()
        # print 'Saving to index {}, uid {:0.0f}'.format(ind, uid)
        # print 'Image number is {}'.format(self.imgnum)
        # print rect_xy
        # print rect.get_width()
        # print rect.get_height()
        # print 'saved'
        logger.debug('Saving to index {}, uid {:0.0f}'.format(ind, uid))
        logger.debug('Image number is {}'.format(self.imgnum))
        logger.debug('Rect_xy: {}'.format(rect_xy))
        logger.debug('Width: {}'.format(rect.get_width()))
        logger.debug('Height: {}'.format(rect.get_height()))
        logger.debug('saved')

    def plotdataset(self, ind=None):
        if ind is None:
            ind = self.ui.plottype.currentIndex()

        selected_fits = self.fitresults[self.validimg]
        x             = np.vectorize(self.plotoptions[ind, 1])
        self.ui.dataset_mpl.plot(x(selected_fits))
        logger.debug('{}'.format(self.plotoptions[ind, 0]))
        logger.info('Attempted to plot!')
        # print self.plotoptions[ind, 0]
        # print 'Attempted to plot!'

    def saveworld(self):
        try:
            f = h5.File('data.hdf5', 'w-')
        except IOError as e:
            if e.message == 'Unable to create file (File exists)':
                f = h5.File('data-{}.hdf5'.format(time.strftime('%Y-%m-%d-%H:%M:%S')), 'w-')

        mt.picklejar('mydata.pkl', fitresults=self.fitresults, valid=self.validimg, rect=self.rect)

    def imagenum_slider_changed(self, val=None):
        # ======================================
        # Set the new image number
        # ======================================
        if val is not None:
            self.imgnum=val
        logger.debug('Slider changed, image number is: {}'.format(self.imgnum))
        # self.indent.level +=1

        # ======================================
        # Get uid
        # ======================================
        uid = self.allimgs.uid[self.imgnum-1]

        # ======================================
        # Open the right image for viewing
        # ======================================
        imgstr = self.data['raw']['images'][str(self.camname)]
        #  self.oimg   = self.allimgs.images[self.imgnum-1]

        cur_img = E200.E200_load_images(imgstr, uid)
        self.oimg = cur_img.images[0]

        if self.camname=='ELANEX':
            self.oimg = np.rot90(self.oimg)
        self.ui.imageview_mpl.image = self.oimg
        
        # ======================================
        # See if rect info is stored for a UID
        # ======================================
        # Print all UIDs
        # uid = uid[0]
        logger.debug('UID type is: {}'.format(type(uid)))
        logger.debug('Opening UID: {:0.0f}'.format(uid))
        rect = self.ui.imageview_mpl.Rectangle
        processed = self.dataset.write_file['data']['processed']
        vectors = processed['vectors']
        scalars = processed['scalars']
        rect_info_exists = ('ss_{}_rect_xy'.format(self.camname) in vectors.keys() and 'ss_{}_width'.format(self.camname) in scalars.keys() and 'ss_{}_height'.format(self.camname) in scalars.keys())

        # ======================================
        # Try to load rect info from file
        # ======================================
        use_loaded_rect=False
        if rect_info_exists:
            rect_xy = E200.E200_api_getdat(vectors['ss_{}_rect_xy'.format(self.camname)], uid, verbose=self.verbose)
            width   = E200.E200_api_getdat(scalars['ss_{}_width'.format(self.camname)], uid, verbose=self.verbose)
            height  = E200.E200_api_getdat(scalars['ss_{}_height'.format(self.camname)], uid, verbose=self.verbose)
            # One element each for rect_xy, width, height
            if np.size(rect_xy.dat) == 2 and np.size(width.dat) == 1 and np.size(height.dat) == 1:
                logger.info('Loading rect from file...')
                rect_xy = rect_xy.dat[0]
                width   = width.dat[0]
                height  = height.dat[0]
                logger.debug('Width is: {}, Height is: {}'.format(width, height))

                # self.indent.level += 1
                logger.debug('Uid loaded is {:0.0f}'.format(uid))
                logger.debug('Image number is {}'.format(self.imgnum))

                border = np.array([width, height])*0.1
                border_px = None

                use_loaded_rect=True

        # ======================================
        # If unsuccessful, calculate rect info
        # ======================================
        if not use_loaded_rect:
            logger.info('Replacing rect...')
            # self.indent.level += 1
            if self.camname=='CMOS_FAR':
                logger.debug('Using CMOS_FAR default rect')
                x0     = 275
                x1     = 325
                y0     = 1870
                y1     = 1900
                border = None
                border_px = np.array([250, 250])
            elif self.camname=='ELANEX':
                logger.debug('Using ELANEX default rect')
                x0     = 0 + 50
                x1     = self.ui.imageview_mpl.image.shape[0] - 50
                y0     = 0 + 50
                y1     = self.ui.imageview_mpl.image.shape[1] - 50
                border = None
                border_px = np.array([50, 50])
            # self.indent.level -= 1
            rect_xy = np.array([y0, x0])
            width   = (y1 - y0)
            height  = (x1 - x0)

            
            E200.E200_create_data(vectors, 'ss_{}_rect_xy'.format(self.camname))
            E200.E200_create_data(scalars, 'ss_{}_width'.format(self.camname))
            E200.E200_create_data(scalars, 'ss_{}_height'.format(self.camname))

            E200.E200_api_updateUID(vectors['ss_{}_rect_xy'.format(self.camname)], UID=uid, value=rect_xy)
            E200.E200_api_updateUID(scalars['ss_{}_width'.format(self.camname)], UID=uid, value=width)
            E200.E200_api_updateUID(scalars['ss_{}_height'.format(self.camname)], UID=uid, value=height)
            processed.file.flush()

        # ======================================
        # Set and draw rect
        # ======================================
        # self.indent.level += 1
        logger.debug('Rect_xy of rect is {}'.format(rect_xy))
        logger.debug('Width of rect is {}'.format(width))
        logger.debug('Height of rect is {}'.format(height))
        # self.indent.level -= 1

        rect.set_xy(rect_xy)
        rect.set_width(width)
        rect.set_height(height)

        self.ui.imageview_mpl.zoom_rect(border=border, border_px=border_px)
        self.ui.imagenum_valid_checkbox.setChecked(self.validimg[self.imgnum-1])
        self.ui.imageview_mpl.ax.figure.canvas.draw()

        # self.indent.level -=1
        logger.info('Finished updating after slider changed')

    def camname_combobox_changed(self):
        self.camname=self.ui.camname_combobox.currentText()
        self.allimgs=self.loadimages()
        self.imagenum_slider_changed()
        # print 'Tracking is {}'.format(self.ui.imagenum_slider._tracking)

    def loadimages(self):
        logger.info('UI preparing to load images...')

        imgstr=self.data['raw']['images'][str(self.camname)]

        uids = imgstr['UID']
        logger.debug('Number of images requested: {}'.format(uids.shape[0]))

                #  out = E200.E200_load_images(imgstr, uids)
        out = E200.E200_api_getdat(imgstr, UID=uids)

        logger.info('UI finished loading images')
        return out

    def loadfile(self, camname=None, imgnum=1):
        logger.info('Loading file...')
        # self.indent.level += 1
        # ======================================
        # Get and save camname if necessary
        # ======================================
        if camname is None:
            camname=self.ui.camname_combobox.currentText()
        self.camname = camname
    
        # ======================================
        # Save imgnum
        # ======================================
        self.imgnum = imgnum

        # ======================================
        # Load all images and save to array
        # ======================================
        self.allimgs = self.loadimages()

        # ======================================
        # Set the camera names in the GUI
        # ======================================
        self.set_camnames(self.infile, camname=self.camname)

        # ======================================
        # Get the number of images and set gui
        # sliders
        # ======================================
        numimgs = self.infile['data']['raw']['images'][camname]['UID'].shape[0]

        self.ui.imagenum_slider.setMinimum(1)
        self.ui.imagenum_slider.setMaximum(numimgs)
        self.ui.imagenum_slider.setValue(imgnum)

        # =====================================
        # Set arrays for storing fit data
        # =====================================
        self.validimg = np.zeros(numimgs, dtype=np.bool)
        self.fitresults = np.empty(numimgs, dtype=object)

        self.imagenum_slider_changed()

        # self.indent.level -= 1
        logger.info('Finished loading file')

    def set_camnames(self, infile, camname=None):
        camnames = np.array(infile['data']['raw']['images'].keys())
        self.ui.camname_combobox.clear()
        self.ui.camname_combobox.addItems(camnames)
        self.camnames = camnames

        if camname is not None:
            # camname=str(camname)
            camname_index = np.where(self.camnames==camname)
            self.ui.camname_combobox.setCurrentIndex(camname_index[0])

    # def setup_imagenum_slider(self, f, imgnum=1):

    def gaussfit_update(self, val):
        ax=self.ui.gaussfit_mpl.ax
        ax.clear()
        gauss_result = self.out.gaussfits[val-1]
        gauss_result.plot(ax)
        ax.set_title('Gauss Fit, Slice {}'.format(val))

        ax.figure.canvas.draw()

    def run_sim(self):
        try:
            # =====================================
            # Get UID
            # =====================================
            ind = self.ui.imagenum_slider.value-1
            uid = self.allimgs.uid[ind]
            # uid = uid[0]
            logger.debug('UID is {}'.format(uid))

            # =====================================
            # Run the sim
            # =====================================
            # print 'Running sim!'
            logger.info('Running sim!')
            self.ui.fitview_mpl.ax.clear()
            self.ui.roiview_mpl.ax.clear()
            self.rect = self.ui.imageview_mpl.Rectangle

            self.out = self.analyzefcn(
                    data     = self.data,
                    camname  = self.camname,
                    # imgnum   = self.imgnum,
                    oimg     = self.oimg,
                    verbose  = False,
                    roiaxes  = self.ui.roiview_mpl.ax,
                    plotaxes = self.ui.fitview_mpl.ax,
                    rect     = self.rect,
                    uid      = uid
                    )

            # =====================================
            # Redraw results boxes
            # =====================================
            self.ui.fitview_mpl.ax.figure.canvas.draw()
            self.ui.roiview_mpl.ax.figure.canvas.draw()

            # =====================================
            # Update gaussfit slider
            # =====================================
            self.ui.gaussfit_slider.setMinimum(1)
            self.ui.gaussfit_slider.setMaximum(self.out.gaussfits.shape[0])
            self.ui.gaussfit_slider.valueChanged.connect(self.gaussfit_update)
            self.gaussfit_update(1)

            # =====================================
            # Save results locally
            # =====================================
            ind = self.ui.imagenum_slider.value-1
            self.fitresults[ind] = self.out

            # =====================================
            # Update emittance plot
            # =====================================
            self.updateEmitPlot()

            # =====================================
            # Extract results and save
            # =====================================
            rect = self.rect
            rect_arr = np.array([rect.get_x(), rect.get_y(), rect.get_width(), rect.get_height()])
            self.savefcn(
                dataset     = self.dataset ,
                analyze_out = self.out     ,
                rect_arr    = rect_arr     ,
                camname     = self.camname ,
                oimg        = self.oimg    ,
                uid         = uid          ,
                valid       = True
                )
        except:
            pass
            #  from PyQt4.QtCore import pyqtRemoveInputHook
            #  pyqtRemoveInputHook()
            #  traceback.print_exc()
            #  pdb.post_mortem()

    def updateEmitPlot(self):
        validresults = self.fitresults[self.validimg]
        self.emit = np.empty(validresults.shape[0])
        # print validresults
        # print validresults.shape
        # print type(validresults)
        for i, val in enumerate(validresults):
            self.emit[i] = val.scanfit.fitresults.emitn

        ax = self.ui.dataset_mpl.ax
        ax.clear()
        ax.plot(self.emit)
        ax.figure.canvas.draw()

    def updateResults(self, val):
        ind = self.ui.imagenum_slider.value-1
        self.validimg[ind] = np.bool(val)

    # def updateROI(self, rect):
    #     img = self.oimg[xstart:xstop, ystart:ystop]
