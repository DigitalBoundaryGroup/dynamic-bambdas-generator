# Developed by Kelsey Henton, DBG 2024

from burp import IBurpExtender, IContextMenuFactory, IScopeChangeListener, ITab, IScanIssue
from javax.swing import (
    JFrame,
    JMenuItem,
    GroupLayout,
    JPanel,
    JCheckBox,
    JTextField,
    JLabel,
    JButton,
    JScrollPane,
    JTextArea,
    ScrollPaneConstants
)
from java.util import ArrayList
from urlparse import urlparse
from java.io import PrintWriter, File
from java.awt import Color, Font, Image, Cursor, Desktop
from java.awt.event import KeyListener
from java.net import URL, URI
from java.lang import System
from javax.imageio import ImageIO


# Set the colour for Burp Orange
COLOR_BURP_ORANGE = Color(0xE36B1E)

class BurpExtender(IBurpExtender, IContextMenuFactory, ITab):
    def registerExtenderCallbacks(self, callbacks):
        """
        Registers the extension and initializes
        """
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        # Create the UI part
        self._createUI()

        self.parentTabbedPane = None
        self.tabDefaultColor = None        
              
        # Display welcome message
        print("Dynamic Bambdas Generator - DBG\n")
        print("by @0xKilotel\n")

    def _createUI(self):
        """
        Creates the Java Swing UI 
        """
        # Derive the default font and size
        test = JLabel()
        FONT_FAMILY = test.getFont().getFamily()
        FONT_SIZE = test.getFont().getSize()

        # Create a font for headers and other non standard stuff
        FONT_HEADER = Font(FONT_FAMILY, Font.BOLD, FONT_SIZE + 2)
        FONT_HELP = Font(FONT_FAMILY, Font.BOLD, FONT_SIZE)
        FONT_GAP_MODE = Font(FONT_FAMILY, Font.BOLD, FONT_SIZE)
        FONT_OPTIONS = Font(FONT_FAMILY, Font.BOLD, FONT_SIZE - 2)


        # Potential parameters found section
        self.lblParamList = JLabel("Parameter List:")
        self.lblParamList.setFont(FONT_HEADER)
        self.lblParamList.setForeground(COLOR_BURP_ORANGE)
        self.outParamList = JTextArea(30, 100)
        self.outParamList.setLineWrap(False)
        self.outParamList.setEditable(True)
        self.scroll_outParamList = JScrollPane(self.outParamList)
        self.scroll_outParamList.setVerticalScrollBarPolicy(
            ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED
        )
        self.scroll_outParamList.setHorizontalScrollBarPolicy(
            ScrollPaneConstants.HORIZONTAL_SCROLLBAR_AS_NEEDED
        )

        self.btnFilter = JButton("Generate Bambdas Filter", actionPerformed=self.btnFilter_clicked)
        self.btnFilter.setEnabled(True)        

        self.lblRequestParams = JLabel("FILTER OPTIONS")
        fnt = self.lblRequestParams.getFont()
        self.lblRequestParams.setFont(fnt.deriveFont(fnt.getStyle() | Font.BOLD))
        self.cbParamUrl = self.defineCheckBox("Query string params")
        self.cbParamBody = self.defineCheckBox("Message body params")
        self.cbParamJson = self.defineCheckBox("JSON params")
        self.cbParamCookie = self.defineCheckBox("Cookie params")
        self.cbParamXml = self.defineCheckBox("XML params")
        self.cbHighlight = self.defineCheckBox("Include color highlights")
        self.cbInScope = self.defineCheckBox("Limit results to In-Scope Assets")       
             
        # Potential links found section
        self.lblFilterResult = JLabel("Bambdas Filter Result:")
        self.lblFilterResult.setFont(FONT_HEADER)
        self.lblFilterResult.setForeground(COLOR_BURP_ORANGE)
        self.outFilterResult = JTextArea(30, 100)
        self.outFilterResult.setLineWrap(False)
        self.outFilterResult.setEditable(False)
        self.scroll_outFilterResult = JScrollPane(self.outFilterResult)
        self.scroll_outFilterResult.setVerticalScrollBarPolicy(
            ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED
        )
        self.scroll_outFilterResult.setHorizontalScrollBarPolicy(
            ScrollPaneConstants.HORIZONTAL_SCROLLBAR_AS_NEEDED
        )
        
        self.tab = JPanel()
        layout = GroupLayout(self.tab)
        self.tab.setLayout(layout)
        layout.setAutoCreateGaps(True)
        layout.setAutoCreateContainerGaps(True)


        # Set UI layout
        layout.setHorizontalGroup(
            layout.createParallelGroup()
            .addGroup(
                layout.createSequentialGroup()
                .addGroup(
                    layout.createParallelGroup()
                    .addGroup(
                        layout.createSequentialGroup()
                        .addGroup(
                            layout.createParallelGroup()
                            .addGroup(
                                layout.createSequentialGroup()
                                .addComponent(self.lblParamList)
                            )
                            .addComponent(self.scroll_outParamList)
                        )
                    )                   
                )
                .addGroup(
                    layout.createParallelGroup()
                    .addGroup(
                        layout.createParallelGroup()
                        .addComponent(self.btnFilter)                        
                        .addGroup(
                            layout.createParallelGroup()
                            .addComponent(self.lblRequestParams)
                            .addComponent(self.cbParamUrl)
                            .addComponent(self.cbParamBody)
                            .addComponent(self.cbParamJson)
                            .addComponent(self.cbParamCookie)
                            .addComponent(self.cbParamXml)
                            .addComponent(self.cbHighlight)
                            .addComponent(self.cbInScope)
                        )
                    )
                )
                .addGroup(
                    layout.createParallelGroup()
                    .addComponent(self.lblFilterResult)                
                    .addComponent(self.scroll_outFilterResult)                     
                )
            )
        )

        layout.setVerticalGroup(
            layout.createSequentialGroup()
            .addGroup(
                layout.createParallelGroup()
                .addGroup(
                    layout.createSequentialGroup()
                    .addGroup(
                        layout.createParallelGroup()
                        .addGroup(
                            layout.createSequentialGroup()
                            .addGroup(
                                layout.createParallelGroup()
                                .addComponent(self.lblParamList)
                            )
                            .addComponent(
                                self.scroll_outParamList,
                                GroupLayout.DEFAULT_SIZE,
                                GroupLayout.DEFAULT_SIZE,
                                GroupLayout.DEFAULT_SIZE,
                            )                     
                        )
                    )
                )
                .addGroup(
                    layout.createSequentialGroup()
                    .addComponent(self.lblRequestParams)
                    .addComponent(self.cbParamUrl)
                    .addComponent(self.cbParamBody)
                    .addComponent(self.cbParamJson)
                    .addComponent(self.cbParamCookie)
                    .addComponent(self.cbParamXml)
                    .addComponent(self.cbHighlight)
                    .addComponent(self.cbInScope)
                    .addComponent(self.btnFilter)                                                   
                )
                .addGroup(
                    layout.createSequentialGroup()
                    .addComponent(self.lblFilterResult)     
                    .addComponent(
                        self.scroll_outFilterResult,
                        GroupLayout.DEFAULT_SIZE,
                        GroupLayout.DEFAULT_SIZE,
                        GroupLayout.DEFAULT_SIZE,
                    )                                                       
                )
            )
        )

        self._callbacks.addSuiteTab(self)
   

    def btnFilter_clicked(self, e=None):
        """
        The event called when the "Generate Bambdas Filter" button is clicked
        """
        # Clear the current link list and filtered list
        self.outFilterResult.text = ""

        # Determine which text to process
        txtToProcess = self.outParamList.text

        # Initialize Variables
        filter = []
        urlFilters = []
        bodyFilters = []
        jsonFilters = []
        xmlFilters = []
        cookieFilters = []
        cleanline = ""
        requestFilter = ""
        parameterTypes = ["BODY", "COOKIE", "JSON", "URL", "XML"]
        # Build up the set of links to display
        try:
            # Go through all the lines in the Link text with origin URLs
            for line in txtToProcess.splitlines():
                cleanline = line.replace("\n", "").split(' ',1)[0]
                for parameterType in parameterTypes:
                    requestFilter = 'requestResponse.request().hasParameter("{cleanline}", HttpParameterType.{parameterType})'.format(cleanline=cleanline,parameterType=parameterType)
                    if self.cbParamBody.isSelected() and parameterType == "BODY":
                        bodyFilters.append(requestFilter)
                    elif self.cbParamCookie.isSelected() and parameterType == "COOKIE":
                        cookieFilters.append(requestFilter)
                    elif self.cbParamJson.isSelected() and parameterType == "JSON":
                        jsonFilters.append(requestFilter)
                    elif self.cbParamUrl.isSelected() and parameterType == "URL":
                        urlFilters.append(requestFilter)
                    elif self.cbParamXml.isSelected() and parameterType == "XML":
                        xmlFilters.append(requestFilter)
            

            if self.cbParamUrl.isSelected():
                filterstring = " || \n".join(urlFilters)
                urlFilter = "boolean hasUrlParam = {filterstring};".format(filterstring=filterstring)
            else:
                urlFilter = "boolean hasUrlParam = false;"

            if self.cbParamBody.isSelected():               
                filterstring = " || \n".join(bodyFilters)
                bodyFilter = "boolean hasBodyParam = {filterstring};".format(filterstring=filterstring)
            else:
                bodyFilter = "boolean hasBodyParam = false;"

            if self.cbParamJson.isSelected():    
                filterstring = " || \n".join(jsonFilters)
                jsonFilter = "boolean hasJsonParam = {filterstring};".format(filterstring=filterstring)
            else:
                jsonFilter = "boolean hasJsonParam = false;"

            if self.cbParamXml.isSelected():                
                filterstring = " || \n".join(xmlFilters)
                xmlFilter = "boolean hasXmlParam = {filterstring};".format(filterstring=filterstring)
            else:
                xmlFilter = "boolean hasXmlParam = false;"

            if self.cbParamCookie.isSelected():
                filterstring = " || \n".join(cookieFilters)
                cookieFilter = "boolean hasCookieParam = {filterstring};".format(filterstring=filterstring)     
            else:
                cookieFilter = "boolean hasCookieParam = false;"
            
            if self.cbInScope.isSelected():
                inScopeFilter = "boolean isInScope = requestResponse.request().isInScope();"
            else:
                inScopeFilter = "boolean isInScope = true;"

            filter.append(urlFilter)
            filter.append(bodyFilter)
            filter.append(jsonFilter)
            filter.append(xmlFilter)
            filter.append(cookieFilter)
            filter.append(inScopeFilter)
            if self.cbHighlight.isSelected():
                filter.append("if (hasUrlParam)")
                filter.append("\trequestResponse.annotations().setHighlightColor(HighlightColor.BLUE);")
                filter.append("else if (hasBodyParam)")
                filter.append("\trequestResponse.annotations().setHighlightColor(HighlightColor.GREEN);")
                filter.append("else if (hasJsonParam)")
                filter.append("\trequestResponse.annotations().setHighlightColor(HighlightColor.ORANGE);")
                filter.append("else if (hasXmlParam)")
                filter.append("\trequestResponse.annotations().setHighlightColor(HighlightColor.RED);")
                filter.append("else if (hasCookieParam)")
                filter.append("\trequestResponse.annotations().setHighlightColor(HighlightColor.GRAY);")


            filterstring = "\n".join(filter)
            if not self.cbParamUrl.isSelected() and not self.cbParamBody.isSelected() and not self.cbParamJson.isSelected() and not self.cbParamXml.isSelected() and not self.cbParamCookie.isSelected():
                finalFilter = "{filterstring} \nreturn isInScope;".format(filterstring=filterstring)
            else:
                finalFilter = "{filterstring} \nreturn isInScope && (hasUrlParam || hasBodyParam || hasJsonParam || hasXmlParam || hasCookieParam);".format(filterstring=filterstring)

            self.outFilterResult.text = finalFilter                

        except Exception as e:
            self._stderr.println("btnFilter_clicked 1")
            self._stderr.println(e)
                
    def getTabCaption(self):
        return "DynaBamGen"

    def getUiComponent(self):
        return self.tab
    
    def defineCheckBox(self, caption, selected=True, enabled=True):
        """
        Used when creating check box controls
        """
        checkBox = JCheckBox(caption)
        checkBox.setSelected(selected)
        checkBox.setEnabled(enabled)
        return checkBox    
