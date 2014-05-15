PYUIC=pyuic4

SOURCES_GUI=mainwindow.ui
OBJECTS_GUI=$(SOURCES_GUI:.ui=_auto.py)


all: $(SOURCES_GUI) $(OBJECTS_GUI)

#  ButterflyGUI_auto.py : ButterflyGUI.ui
#          pyuic4 ButterflyGUI.ui -o ButterflyGUI_auto.py

$(OBJECTS_GUI): $(SOURCES_GUI)
	$(PYUIC) $< -o $@

clean:
	rm -rf *_auto.py
