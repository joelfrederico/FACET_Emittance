function varargout = FACET_Emittance_GUI(varargin)
% FACET_EMITTANCE_GUI M-file for FACET_Emittance_GUI.fig
%      FACET_EMITTANCE_GUI, by itself, creates a new FACET_EMITTANCE_GUI or raises the existing
%      singleton*.
%
%      H = FACET_EMITTANCE_GUI returns the handle to a new FACET_EMITTANCE_GUI or the handle to
%      the existing singleton*.
%
%      FACET_EMITTANCE_GUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in FACET_EMITTANCE_GUI.M with the given input arguments.
%
%      FACET_EMITTANCE_GUI('Property','Value',...) creates a new FACET_EMITTANCE_GUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before FACET_Emittance_GUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to FACET_Emittance_GUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help FACET_Emittance_GUI

% Last Modified by GUIDE v2.5 08-Nov-2013 23:02:50

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @FACET_Emittance_GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @FACET_Emittance_GUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before FACET_Emittance_GUI is made visible.
function FACET_Emittance_GUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to FACET_Emittance_GUI (see VARARGIN)

% Choose default command line output for FACET_Emittance_GUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes FACET_Emittance_GUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = FACET_Emittance_GUI_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;
