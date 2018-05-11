<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.20.0 -->
<interface>
  <requires lib="gtk+" version="3.20"/>
  <object class="GtkFileFilter" id="filefilter1">
    <patterns>
      <pattern>xlsx</pattern>
      <pattern>csv</pattern>
    </patterns>
  </object>
  <object class="GtkWindow" id="main_window">
    <property name="can_focus">False</property>
    <property name="has_focus">True</property>
    <property name="receives_default">True</property>
    <property name="valign">start</property>
    <property name="urgency_hint">True</property>
    <property name="deletable">False</property>
    <property name="has_resize_grip">True</property>
    <child>
      <object class="GtkBox">
        <property name="width_request">-1</property>
        <property name="height_request">-1</property>
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="vexpand">False</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkMenuBar">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkMenuItem">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">_File</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <child>
                      <object class="GtkImageMenuItem">
                        <property name="label">gtk-new</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem">
                        <property name="label">gtk-open</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem">
                        <property name="label">gtk-save</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem">
                        <property name="label">gtk-save-as</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkSeparatorMenuItem">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem">
                        <property name="label">gtk-quit</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">_Help</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <child>
                      <object class="GtkImageMenuItem">
                        <property name="label">gtk-about</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkNotebook">
            <property name="width_request">-1</property>
            <property name="height_request">-1</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="halign">baseline</property>
            <property name="valign">baseline</property>
            <property name="resize_mode">queue</property>
            <child>
              <object class="GtkBox">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="valign">start</property>
                <property name="vexpand">False</property>
                <property name="resize_mode">queue</property>
                <property name="orientation">vertical</property>
                <property name="baseline_position">bottom</property>
                <child>
                  <object class="GtkBox">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="halign">center</property>
                    <child>
                      <object class="GtkSwitch" id="switch_sectorholdings">
                        <property name="width_request">0</property>
                        <property name="height_request">0</property>
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="halign">start</property>
                        <property name="valign">center</property>
                        <property name="margin_top">6</property>
                        <property name="margin_bottom">6</property>
                        <property name="hexpand">True</property>
                        <property name="vexpand">True</property>
                        <property name="active">True</property>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">True</property>
                        <property name="position">0</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkLabel">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="halign">start</property>
                        <property name="valign">center</property>
                        <property name="xpad">0</property>
                        <property name="label" translatable="yes">Get Sector Holdings</property>
                        <property name="use_underline">True</property>
                        <attributes>
                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Bold Condensed 14"/>
                          <attribute name="weight" value="semibold"/>
                          <attribute name="variant" value="normal"/>
                          <attribute name="foreground" value="#000000000000"/>
                        </attributes>
                      </object>
                      <packing>
                        <property name="expand">True</property>
                        <property name="fill">True</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkBox">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="halign">center</property>
                    <child>
                      <object class="GtkSwitch" id="switch_transactionlog">
                        <property name="width_request">0</property>
                        <property name="height_request">0</property>
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="halign">start</property>
                        <property name="valign">center</property>
                        <property name="margin_top">6</property>
                        <property name="margin_bottom">6</property>
                        <property name="hexpand">True</property>
                        <property name="vexpand">True</property>
                      </object>
                      <packing>
                        <property name="expand">False</property>
                        <property name="fill">True</property>
                        <property name="position">0</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkLabel">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="halign">start</property>
                        <property name="valign">center</property>
                        <property name="xpad">0</property>
                        <property name="label" translatable="yes">Get Transaction Log</property>
                        <property name="use_underline">True</property>
                        <attributes>
                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Bold Condensed 14"/>
                          <attribute name="weight" value="semibold"/>
                          <attribute name="variant" value="normal"/>
                          <attribute name="foreground" value="#000000000000"/>
                        </attributes>
                      </object>
                      <packing>
                        <property name="expand">True</property>
                        <property name="fill">True</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">1</property>
                  </packing>
                </child>
              </object>
            </child>
            <child type="tab">
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">main</property>
              </object>
              <packing>
                <property name="menu_label">main</property>
                <property name="tab_fill">False</property>
              </packing>
            </child>
            <child>
              <object class="GtkScrolledWindow">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="halign">baseline</property>
                <property name="valign">baseline</property>
                <property name="vexpand">False</property>
                <property name="hscrollbar_policy">never</property>
                <property name="shadow_type">in</property>
                <property name="propagate_natural_width">True</property>
                <property name="propagate_natural_height">True</property>
                <child>
                  <object class="GtkViewport">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <child>
                      <object class="GtkBox" id="options_box">
                        <property name="width_request">-1</property>
                        <property name="height_request">-1</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="resize_mode">queue</property>
                        <property name="orientation">vertical</property>
                        <property name="baseline_position">top</property>
                        <child>
                          <object class="GtkFrame">
                            <property name="height_request">-1</property>
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="halign">baseline</property>
                            <property name="valign">baseline</property>
                            <property name="margin_top">5</property>
                            <property name="resize_mode">queue</property>
                            <property name="label_xalign">0</property>
                            <property name="label_yalign">0</property>
                            <child>
                              <object class="GtkBox">
                                <property name="width_request">100</property>
                                <property name="height_request">80</property>
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="resize_mode">queue</property>
                                <property name="baseline_position">top</property>
                                <child>
                                  <object class="GtkEntry" id="transactionLog_txtbox">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="valign">center</property>
                                    <property name="truncate_multiline">True</property>
                                    <property name="shadow_type">none</property>
                                    <property name="placeholder_text" translatable="yes">Transaction Log File/URL</property>
                                  </object>
                                  <packing>
                                    <property name="expand">True</property>
                                    <property name="fill">True</property>
                                    <property name="padding">5</property>
                                    <property name="position">0</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkFileChooserButton" id="file_chooser_button">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <property name="valign">center</property>
                                    <property name="margin_bottom">2</property>
                                    <property name="create_folders">False</property>
                                    <property name="filter">filefilter1</property>
                                    <property name="title" translatable="yes"/>
                                    <signal name="file-set" handler="on_file_chooser_button_file_set" swapped="no"/>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">False</property>
                                    <property name="padding">6</property>
                                    <property name="position">1</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                            <child type="label">
                              <object class="GtkLabel">
                                <property name="visible">True</property>
                                <property name="sensitive">False</property>
                                <property name="can_focus">False</property>
                                <property name="halign">end</property>
                                <property name="margin_left">10</property>
                                <property name="margin_top">5</property>
                                <property name="margin_bottom">2</property>
                                <property name="label" translatable="yes">Transaction Log File</property>
                                <property name="justify">center</property>
                                <property name="track_visited_links">False</property>
                                <attributes>
                                  <attribute name="font-desc" value="Fira Sans Condensed, Semi-Bold Condensed 14"/>
                                  <attribute name="underline" value="True"/>
                                  <attribute name="foreground" value="#000000000000"/>
                                </attributes>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">True</property>
                            <property name="fill">True</property>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkFrame">
                            <property name="height_request">-1</property>
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="valign">baseline</property>
                            <property name="margin_top">5</property>
                            <property name="resize_mode">queue</property>
                            <property name="label_xalign">0</property>
                            <property name="label_yalign">0</property>
                            <child>
                              <object class="GtkBox">
                                <property name="width_request">100</property>
                                <property name="height_request">80</property>
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="resize_mode">queue</property>
                                <property name="baseline_position">top</property>
                                <child>
                                  <object class="GtkEntry" id="outputFolder_txtbox">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="valign">center</property>
                                    <property name="truncate_multiline">True</property>
                                    <property name="shadow_type">none</property>
                                    <property name="placeholder_text" translatable="yes">Save File/s to Output Destination</property>
                                  </object>
                                  <packing>
                                    <property name="expand">True</property>
                                    <property name="fill">True</property>
                                    <property name="padding">5</property>
                                    <property name="position">0</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkFileChooserButton" id="folder_chooser_button">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <property name="valign">center</property>
                                    <property name="margin_bottom">2</property>
                                    <property name="action">select-folder</property>
                                    <property name="filter">filefilter1</property>
                                    <property name="title" translatable="yes">Please Select Output Folder Location</property>
                                    <signal name="file-set" handler="on_folder_chooser_button_file_set" swapped="no"/>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">False</property>
                                    <property name="padding">6</property>
                                    <property name="position">1</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                            <child type="label">
                              <object class="GtkLabel">
                                <property name="visible">True</property>
                                <property name="sensitive">False</property>
                                <property name="can_focus">False</property>
                                <property name="halign">end</property>
                                <property name="margin_left">10</property>
                                <property name="margin_top">5</property>
                                <property name="margin_bottom">2</property>
                                <property name="label" translatable="yes">Output Folder</property>
                                <property name="justify">center</property>
                                <property name="track_visited_links">False</property>
                                <attributes>
                                  <attribute name="font-desc" value="Fira Sans Condensed, Semi-Bold Condensed 14"/>
                                  <attribute name="underline" value="True"/>
                                  <attribute name="foreground" value="#000000000000"/>
                                </attributes>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">True</property>
                            <property name="fill">True</property>
                            <property name="position">1</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkFrame">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label_xalign">0</property>
                            <property name="label_yalign">0</property>
                            <child>
                              <object class="GtkBox">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="orientation">vertical</property>
                                <child>
                                  <object class="GtkLabel">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <property name="halign">start</property>
                                    <property name="margin_left">10</property>
                                    <property name="margin_top">5</property>
                                    <property name="label" translatable="yes">Excel Function Type</property>
                                    <attributes>
                                      <attribute name="font-desc" value="Fira Sans Condensed, Semi-Bold Condensed 14"/>
                                      <attribute name="underline" value="True"/>
                                      <attribute name="foreground" value="#000000000000"/>
                                    </attributes>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">True</property>
                                    <property name="position">0</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkBox">
                                    <property name="width_request">-1</property>
                                    <property name="height_request">-1</property>
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <property name="halign">center</property>
                                    <property name="margin_top">10</property>
                                    <property name="margin_bottom">5</property>
                                    <property name="homogeneous">True</property>
                                    <child>
                                      <object class="GtkRadioButton" id="radiobutton_factset">
                                        <property name="width_request">-1</property>
                                        <property name="height_request">-1</property>
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="receives_default">False</property>
                                        <property name="image_position">right</property>
                                        <property name="active">True</property>
                                        <property name="draw_indicator">True</property>
                                        <child>
                                          <object class="GtkLabel">
                                            <property name="visible">True</property>
                                            <property name="can_focus">False</property>
                                            <property name="halign">center</property>
                                            <property name="label" translatable="yes">Factset</property>
                                            <attributes>
                                              <attribute name="font-desc" value="Fira Sans Condensed, Condensed 12"/>
                                              <attribute name="foreground" value="#000000000000"/>
                                            </attributes>
                                          </object>
                                        </child>
                                      </object>
                                      <packing>
                                        <property name="expand">False</property>
                                        <property name="fill">True</property>
                                        <property name="padding">36</property>
                                        <property name="position">0</property>
                                      </packing>
                                    </child>
                                    <child>
                                      <object class="GtkRadioButton" id="radiobutton_bloomberg">
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="receives_default">False</property>
                                        <property name="draw_indicator">True</property>
                                        <property name="group">radiobutton_factset</property>
                                        <child>
                                          <object class="GtkLabel">
                                            <property name="visible">True</property>
                                            <property name="can_focus">False</property>
                                            <property name="halign">center</property>
                                            <property name="label" translatable="yes">Bloomberg</property>
                                            <property name="wrap">True</property>
                                            <attributes>
                                              <attribute name="font-desc" value="Fira Sans Condensed, Condensed 12"/>
                                              <attribute name="style" value="normal"/>
                                              <attribute name="weight" value="semilight"/>
                                              <attribute name="foreground" value="#000000000000"/>
                                            </attributes>
                                          </object>
                                        </child>
                                      </object>
                                      <packing>
                                        <property name="expand">True</property>
                                        <property name="fill">True</property>
                                        <property name="padding">25</property>
                                        <property name="pack_type">end</property>
                                        <property name="position">2</property>
                                      </packing>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">True</property>
                                    <property name="position">1</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                            <child type="label_item">
                              <placeholder/>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">False</property>
                            <property name="fill">True</property>
                            <property name="position">2</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkFrame">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label_xalign">0</property>
                            <child>
                              <object class="GtkBox">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="orientation">vertical</property>
                                <child>
                                  <object class="GtkLabel">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <property name="halign">start</property>
                                    <property name="margin_left">10</property>
                                    <property name="margin_top">5</property>
                                    <property name="label" translatable="yes">Date Range</property>
                                    <property name="track_visited_links">False</property>
                                    <attributes>
                                      <attribute name="font-desc" value="Fira Sans Condensed, Semi-Bold Condensed 14"/>
                                      <attribute name="weight" value="medium"/>
                                      <attribute name="underline" value="True"/>
                                      <attribute name="foreground" value="#000000000000"/>
                                    </attributes>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">True</property>
                                    <property name="position">0</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkBox">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <property name="homogeneous">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="label" translatable="yes">Start Date:</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                      <packing>
                                        <property name="expand">False</property>
                                        <property name="fill">False</property>
                                        <property name="padding">10</property>
                                        <property name="position">0</property>
                                      </packing>
                                    </child>
                                    <child>
                                      <object class="GtkEntry" id="entry_startdate">
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="halign">end</property>
                                        <property name="margin_bottom">3</property>
                                        <property name="text" translatable="yes">9/25/2010</property>
                                        <property name="placeholder_text" translatable="yes">Start Date</property>
                                      </object>
                                      <packing>
                                        <property name="expand">True</property>
                                        <property name="fill">True</property>
                                        <property name="padding">3</property>
                                        <property name="position">2</property>
                                      </packing>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">True</property>
                                    <property name="position">1</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkSeparator">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">True</property>
                                    <property name="padding">2</property>
                                    <property name="position">2</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkBox">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <property name="homogeneous">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="label" translatable="yes">End Date:</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                      <packing>
                                        <property name="expand">False</property>
                                        <property name="fill">False</property>
                                        <property name="padding">15</property>
                                        <property name="position">0</property>
                                      </packing>
                                    </child>
                                    <child>
                                      <object class="GtkEntry" id="entry_enddate">
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="halign">end</property>
                                        <property name="margin_bottom">3</property>
                                        <property name="placeholder_text" translatable="yes">End Date</property>
                                        <property name="input_purpose">digits</property>
                                      </object>
                                      <packing>
                                        <property name="expand">True</property>
                                        <property name="fill">True</property>
                                        <property name="padding">3</property>
                                        <property name="pack_type">end</property>
                                        <property name="position">2</property>
                                      </packing>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="expand">True</property>
                                    <property name="fill">True</property>
                                    <property name="position">3</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                            <child type="label_item">
                              <placeholder/>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">False</property>
                            <property name="fill">True</property>
                            <property name="position">3</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkFrame">
                            <property name="height_request">-1</property>
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="has_focus">True</property>
                            <property name="double_buffered">False</property>
                            <property name="label_xalign">0</property>
                            <property name="shadow_type">none</property>
                            <child>
                              <object class="GtkGrid" id="sectorGrid">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="halign">center</property>
                                <property name="valign">center</property>
                                <property name="hexpand">False</property>
                                <property name="row_homogeneous">True</property>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_telecom">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">start</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_right">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Telecom</property>
                                        <property name="xalign">0.10000000149011612</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">0</property>
                                    <property name="top_attach">5</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_realestate">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">baseline</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_right">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Real Estate</property>
                                        <property name="xalign">0.10000000149011612</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">0</property>
                                    <property name="top_attach">4</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_industrials">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">baseline</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_right">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Industrials</property>
                                        <property name="xalign">0.10000000149011612</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">0</property>
                                    <property name="top_attach">3</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_financials">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">baseline</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_right">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Financials</property>
                                        <property name="xalign">0.10000000149011612</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">0</property>
                                    <property name="top_attach">2</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_staples">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">baseline</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_right">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Consumer 
Staples</property>
                                        <property name="xalign">0.10000000149011612</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">0</property>
                                    <property name="top_attach">1</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_all">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">baseline</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_right">10</property>
                                    <property name="image_position">right</property>
                                    <property name="active">True</property>
                                    <property name="draw_indicator">True</property>
                                    <signal name="toggled" handler="on_checkbtn_all_toggled" swapped="no"/>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">All Sectors</property>
                                        <property name="xalign">0.10000000149011612</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">0</property>
                                    <property name="top_attach">0</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_utilites">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">baseline</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_left">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Utilities</property>
                                        <property name="xalign">0.10000000149011612</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">1</property>
                                    <property name="top_attach">5</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_tech">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">baseline</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_left">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Technology</property>
                                        <property name="xalign">0.10000000149011612</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">1</property>
                                    <property name="top_attach">4</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_materials">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">baseline</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_left">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Materials</property>
                                        <property name="xalign">0.10000000149011612</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">1</property>
                                    <property name="top_attach">3</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_healthcare">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">baseline</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_left">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Health Care</property>
                                        <property name="xalign">0.10000000149011612</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">1</property>
                                    <property name="top_attach">2</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_energy">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">baseline</property>
                                    <property name="valign">baseline</property>
                                    <property name="margin_left">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Energy</property>
                                        <property name="track_visited_links">False</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">1</property>
                                    <property name="top_attach">1</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkCheckButton" id="checkbtn_discretionary">
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="halign">center</property>
                                    <property name="valign">center</property>
                                    <property name="margin_left">10</property>
                                    <property name="image_position">right</property>
                                    <property name="draw_indicator">True</property>
                                    <child>
                                      <object class="GtkLabel">
                                        <property name="visible">True</property>
                                        <property name="can_focus">False</property>
                                        <property name="halign">start</property>
                                        <property name="valign">center</property>
                                        <property name="label" translatable="yes">Consumer
Discretionary</property>
                                        <property name="xalign">0.15000000596046448</property>
                                        <attributes>
                                          <attribute name="font-desc" value="Fira Sans Condensed, Semi-Light Condensed 12"/>
                                          <attribute name="foreground" value="#000000000000"/>
                                        </attributes>
                                      </object>
                                    </child>
                                  </object>
                                  <packing>
                                    <property name="left_attach">1</property>
                                    <property name="top_attach">0</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                            <child type="label">
                              <object class="GtkLabel">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="halign">start</property>
                                <property name="margin_left">10</property>
                                <property name="margin_top">5</property>
                                <property name="label" translatable="yes">Sectors</property>
                                <property name="track_visited_links">False</property>
                                <attributes>
                                  <attribute name="font-desc" value="Fira Sans Condensed, Medium Condensed 14"/>
                                  <attribute name="underline" value="True"/>
                                </attributes>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">True</property>
                            <property name="fill">True</property>
                            <property name="position">4</property>
                          </packing>
                        </child>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
              <packing>
                <property name="position">1</property>
              </packing>
            </child>
            <child type="tab">
              <object class="GtkLabel">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">setup</property>
              </object>
              <packing>
                <property name="menu_label">Setup</property>
                <property name="position">1</property>
                <property name="tab_fill">False</property>
              </packing>
            </child>
            <child>
              <placeholder/>
            </child>
            <child type="tab">
              <placeholder/>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkSeparator">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkStatusbar">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="margin_left">10</property>
            <property name="margin_right">10</property>
            <property name="margin_start">10</property>
            <property name="margin_end">10</property>
            <property name="margin_bottom">4</property>
            <property name="orientation">vertical</property>
            <property name="spacing">2</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="pack_type">end</property>
            <property name="position">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkBox">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="valign">end</property>
            <child>
              <object class="GtkButton" id="button_run">
                <property name="label" translatable="yes">run</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="halign">end</property>
                <property name="valign">center</property>
                <signal name="clicked" handler="on_button_run_clicked" swapped="no"/>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkSeparator">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="padding">10</property>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="button_quit">
                <property name="label" translatable="yes">quit</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="halign">start</property>
                <property name="valign">center</property>
                <signal name="clicked" handler="on_main_window_Destroy" swapped="no"/>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">2</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="pack_type">end</property>
            <property name="position">4</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
  <object class="GtkMessageDialog" id="error_dialogue">
    <property name="can_focus">False</property>
    <property name="type">popup</property>
    <property name="resizable">False</property>
    <property name="modal">True</property>
    <property name="window_position">center-on-parent</property>
    <property name="destroy_with_parent">True</property>
    <property name="type_hint">dialog</property>
    <property name="skip_taskbar_hint">True</property>
    <property name="urgency_hint">True</property>
    <property name="deletable">False</property>
    <property name="gravity">north-east</property>
    <property name="transient_for">main_window</property>
    <property name="message_type">error</property>
    <property name="buttons">close</property>
    <property name="text" translatable="yes">An Error has Occured.</property>
    <child internal-child="vbox">
      <object class="GtkBox">
        <property name="can_focus">False</property>
        <property name="orientation">vertical</property>
        <property name="spacing">2</property>
        <child internal-child="action_area">
          <object class="GtkButtonBox">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="homogeneous">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
  <object class="GtkMessageDialog" id="finished_dialog">
    <property name="can_focus">False</property>
    <property name="resizable">False</property>
    <property name="modal">True</property>
    <property name="destroy_with_parent">True</property>
    <property name="type_hint">dialog</property>
    <property name="urgency_hint">True</property>
    <property name="deletable">False</property>
    <property name="gravity">north-east</property>
    <property name="transient_for">main_window</property>
    <property name="buttons">yes-no</property>
    <property name="text" translatable="yes">Application has finished.</property>
    <property name="secondary_text" translatable="yes">Application will now close. Would you like to display your results?</property>
    <child internal-child="vbox">
      <object class="GtkBox">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="margin_top">10</property>
        <property name="hexpand">False</property>
        <property name="orientation">vertical</property>
        <property name="baseline_position">bottom</property>
        <child internal-child="action_area">
          <object class="GtkButtonBox">
            <property name="can_focus">False</property>
            <property name="homogeneous">True</property>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
    <child type="titlebar">
      <placeholder/>
    </child>
  </object>
</interface>
