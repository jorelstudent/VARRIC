from flask import Flask, render_template, request
#import pandas as pd

from bokeh import __version__ as BOKEH_VERSION
from bokeh.embed import components
from bokeh.palettes import Spectral6
from bokeh.layouts import column, widgetbox, WidgetBox, layout

# For the button and a hovertool
from bokeh.models import CustomJS, Button, HoverTool, ColumnDataSource, \
                         LinearColorMapper, BasicTicker, PrintfTickFormatter, \
                         ColorBar, OpenURL, TapTool
# For the sliders and dropdown
from bokeh.models.widgets import Paragraph, PreText, CheckboxGroup, Slider, \
                                 Dropdown, Select, RangeSlider
from bokeh.plotting import figure, curdoc, show
# For gridplots
from bokeh.io import gridplot, output_file, show
# For heatmaps
#from bokeh.charts import HeatMap, bins, output_file, show
from bokeh.models import Rect

import numpy as np
import os
from random import random
from load_data import load_hypercube, load_summary_stats, build_data_dict

app = Flask(__name__)
indices = range(100)


@app.route('/')
def home():
    """
    Homepage, which shows summary stats for a given dataset.
    """
    # Define data directories
    PREFIX = "std"
    class_data_root = "%s/data/class/%s" % (os.path.abspath(".."), PREFIX)
    ccl_data_root = "%s/data/ccl/%s" % (os.path.abspath(".."), PREFIX)
    
    # Load sample points
    p = load_hypercube("%s_params.dat" % class_data_root)
    
    # Define binning in (z, k) and threshold values
    thresholds = [5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2]
    scale_ranges = [(1e-4, 1e-2), (1e-2, 1e-1), (1e-1, 1e0)]
    z_vals = [1, 2, 3, 4, 5, 6]
    
    "%s_nl_std"
    
    # Calculate summary stats
    stats_lin = load_summary_stats(p,
                                   "%s_lin" % ccl_data_root, 
                                   "%s_lin_std" % class_data_root,
                                   thresholds=thresholds, z_vals=z_vals,
                                   scale_ranges=scale_ranges, 
                                   cache_name='cache_lin')
    
    # FIXME
    stats_nl = stats_lin
    stats_lin_pre = stats_lin
    stats_nl_pre = stats_lin
    
    """
    stats_nl = load_summary_stats(p, 
                                  "%s_nl" % ccl_data_root, 
                                  "%s_nl_std" % class_data_root,
                                  thresholds=thresholds, z_vals=z_vals,
                                  scale_ranges=scale_ranges, 
                                  cache_name='cache_nl')
    stats_lin_pre = load_summary_stats(p,
                                       "%s_lin" % ccl_data_root, 
                                       "%s_lin_pre" % class_data_root,
                                       thresholds=thresholds, z_vals=z_vals,
                                       scale_ranges=scale_ranges, 
                                       cache_name='cache_lin_pre')
    stats_nl_pre = load_summary_stats(p,
                                      "%s_nl" % ccl_data_root, 
                                      "%s_nl_pre" % class_data_root,
                                      thresholds=thresholds, z_vals=z_vals,
                                      scale_ranges=scale_ranges, 
                                      cache_name='cache_nl_pre')
    """
    
    # Build data dictionaries
    data_lin = build_data_dict(stats_lin, 'lin')
    data_nl = build_data_dict(stats_nl, 'nl')
    data_lin_pre = build_data_dict(stats_lin_pre, 'lin_pre')
    data_nl_pre = build_data_dict(stats_nl_pre, 'nl_pre')
    
    # Package data dictionaries into Bokeh ColumnDataSource objects
    source_lin = ColumnDataSource(data=data_lin)
    source_nl = ColumnDataSource(data=data_nl)
    source_lin_pre = ColumnDataSource(data=data_lin_pre)
    source_nl_pre = ColumnDataSource(data=data_nl_pre)
    
    # Build overall summary statistic for each sample point
    # (use only lin, and the standard threshold value of 1e-4)
    tot_tot_lin = np.sum(stats_lin[:,1], axis=(1,2))
    
    # Create ColumnDataSource with the cosmo params and Delta summary statistic
    src_data = {
        'tot_tot_data':     tot_tot_lin,
        'h_arr':            p['h'], 
        'Omega_b_arr':      p['Omega_b'], 
        'Omega_cdm_arr':    p['Omega_cdm'],
        'A_s_arr':          p['A_s'], 
        'n_s_arr':          p['n_s'], 
        'trial_arr':        ["%05d" % i for i in range(p['h'].size)]
    }
    source_data = ColumnDataSource(data=src_data)

    # Map summary statistic to colors
    colors = ['#fff5ee', '#ffe4e1', '#ffc1c1', '#eeb4b4', '#f08080', 
              '#ee6363', '#d44942', '#cd0000', '#ff0000']
    mapper = LinearColorMapper(palette=colors, low=0.1, high=1000., 
                               low_color='#CCE4FF')

    # Create multiple instances of the hover tool
    hover = [ HoverTool(tooltips=[
                   #('index', '$index'),
                   ('h', '@h_arr'),
                   (u'\u03A9_b', '@Omega_b_arr'),
                   (u'\u03A9_c', '@Omega_cdm_arr'),
                   ('A_s', '@A_s_arr'),
                   ('n_s', '@n_s_arr'),
                   (u'\u0394', '@tot_tot_data')
                   ])
             for i in range(10) ]

    # Selection of tools to enable
    TOOLS = 'hover, pan, wheel_zoom, box_zoom, save, resize, reset'
    WIDTH = 300
    HEIGHT = 300
    
    # Generate the corner plot
    s1 = figure(plot_width=WIDTH, plot_height=HEIGHT,tools=[hover[0], TapTool()])
    s1.grid.grid_line_color = None
    s1_rect = s1.rect('h_arr', 'Omega_b_arr', width=10., height=10., 
                      alpha=0.8, source=source_data, line_color=None,
                      fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                      width_units='screen', height_units='screen')
    s1.yaxis.axis_label = u'\u03A9_b'
    
    s2 = figure(plot_width=WIDTH, plot_height=HEIGHT, tools=[hover[1], TapTool()])
    s2.grid.grid_line_color=None
    s2_rect = s2.rect('h_arr', 'Omega_cdm_arr', width=10., height=10., 
                      alpha=0.8, source=source_data, line_color=None,
                      fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                      width_units='screen', height_units='screen')
    s2.yaxis.axis_label = u'\u03A9_cdm' 

    s3 = figure(plot_width=WIDTH, plot_height=HEIGHT, tools=[hover[2], TapTool()])
    s3.grid.grid_line_color = None
    s3_rect = s3.rect('Omega_b_arr', 'Omega_cdm_arr', width=10., height=10., 
                      alpha=0.8, line_color=None, source=source_data, 
                      fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                      width_units='screen', height_units='screen')
    
    s4 = figure(plot_width=WIDTH, plot_height=HEIGHT, tools=[hover[3], TapTool()])
    s4.grid.grid_line_color = None
    s4_rect = s4.rect('h_arr', 'A_s_arr', width=10., height=10., 
                      alpha=0.8, source=source_data, line_color=None,
                      fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                      width_units='screen', height_units='screen')
    s4.yaxis.axis_label = 'A_s' 

    s5 = figure(plot_width=WIDTH, plot_height=HEIGHT, tools=[hover[4], TapTool()])
    s5.grid.grid_line_color = None
    s5_rect = s5.rect('Omega_b_arr', 'A_s_arr', width=10., height=10., 
                      alpha=0.8, source=source_data, line_color=None,
                      fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                      width_units='screen', height_units='screen')

    s6 = figure(plot_width=WIDTH, plot_height=HEIGHT, tools=[hover[5], TapTool()])
    s6.grid.grid_line_color = None
    s6_rect = s6.rect('Omega_cdm_arr', 'A_s_arr', width=10., height=10., 
                      alpha=0.8, source=source_data, line_color=None,
                      fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                      width_units='screen', height_units='screen')

    s7 = figure(plot_width=WIDTH, plot_height=HEIGHT, tools=[hover[6], TapTool()])
    s7.grid.grid_line_color = None
    s7_rect = s7.rect('h_arr', 'n_s_arr', width=10., height=10., 
                      alpha=0.8, source=source_data, line_color=None,
                      fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                      width_units='screen', height_units='screen')
    s7.yaxis.axis_label = 'n_s'
    s7.xaxis.axis_label = 'h'
   
    s8 = figure(plot_width=WIDTH, plot_height=HEIGHT, tools=[hover[7],TapTool()])
    s8.grid.grid_line_color = None
    s8_rect = s8.rect('Omega_b_arr', 'n_s_arr', width=10., height=10., 
                      alpha=0.8, source=source_data, line_color=None,
                      fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                      width_units='screen', height_units='screen')
    s8.xaxis.axis_label = u'\u03A9_b'

    s9 = figure(plot_width=WIDTH, plot_height=HEIGHT, tools=[hover[8], TapTool()])
    s9.grid.grid_line_color = None
    s9_rect = s9.rect('Omega_cdm_arr', 'n_s_arr', width=10., height=10., 
                      alpha=0.8, source=source_data, line_color=None,
                      fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                      width_units='screen', height_units='screen')
    s9.xaxis.axis_label = u'\u03A9_cdm'

    s10 = figure(plot_width=WIDTH, plot_height=HEIGHT, tools=[hover[9], TapTool()])
    s10.grid.grid_line_color = None
    s10_rect = s10.rect('A_s_arr', 'n_s_arr', width=10., height=10., 
                        alpha=0.8, source=source_data, line_color=None,
                        fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                        width_units='screen', height_units='screen')
    s10.xaxis.axis_label = 'A_s'
    
    # Make lists of rectangles and figures
    rect_list = [ s1_rect, s2_rect, s3_rect, s4_rect, s5_rect, 
                  s6_rect, s7_rect, s8_rect, s9_rect, s10_rect ]
    fig_list = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
   
    # Create glyphs for the highlighting portion, so that when it is tapped
    # the colors don't change
    selected = Rect(fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                    fill_alpha=0.8, line_color=None)
    nonselected = Rect(fill_color={'field':'tot_tot_data', 'transform':mapper}, 
                       fill_alpha=0.8, line_color=None)
    
    # Loop over rectangles, setting selected vs. nonselected glyph
    for rect in rect_list:
        rect.selection_glyph = selected
        rect.nonselection_glyph = nonselected
    
    # Create colorbar for value of Delta
    color_bar = ColorBar( color_mapper=mapper, 
                          major_label_text_font_size='12pt',
                          ticker=BasicTicker(desired_num_ticks=len(colors)),
                          label_standoff=10, border_line_color=None, 
                          location=(0,0) )
    
    s_color = figure(plot_width=WIDTH, plot_height=290)
    s_color.outline_line_color = 'white'
    s_color.grid.grid_line_color = None
    s_color.axis.axis_line_color = None
    s_color.add_layout(color_bar, 'left')
    s_color.toolbar.logo = None
    s_color.toolbar_location = None

    # Create gridplot in the shape of a corner plot
    plot = gridplot([ [s1, None, None, s_color], 
                      [s2, s3, None, None], 
                      [s4,s5,s6, None], 
                      [s7,s8,s9,s10] ])
    
    # Code to be used by the JavaScript in the interface
    code_sliders="""

    // Get the value from our threshold slider
    var thres = thres_slider.value;
    console.log(thres);

    // Get the range of our z_Slider
    var z = z_slider.range;
    var start = z_slider.range[0];
    var end = z_slider.range[1];
    console.log(start);
    console.log(end);

    
    // Get the mode in the dropdown
    var mode_selected = dropdown.value;

    // All of our data
    var tot_data = source_data.data;
    var tot_lin = js_lin.data;
    var tot_nl = js_nl.data;
    var tot_lin_pre = js_lin_pre.data;
    var tot_nl_pre = js_nl_pre.data;
    var sum = 0;
    console.log(mode_selected);

    // Data from the checkbox group
    var k_check = k_checkbox.active;
    console.log(k_check);
    
    if (k_check != []) {
        var k_check_start = k_checkbox.active[0];
        var k_check_end = k_checkbox.active[k_check.length - 1];


        thres_string = String(thres)
        if (mode_selected == "Linear") {
            //Create a loop for the ranges
            for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
                sum = 0;
                for(var j = start; j<=end; j=j+0.5){
                    z_string = String((j*2)+1);
                    for (var l = k_check_start + 1; l<= k_check_end + 1; l++) {
                        k_string = String(l);
                        sum += tot_lin['tot_lin_h' + thres_string + '_k' + k_string + '_z' + z_string][i];
                    } // k_range

                } // z_value

                tot_data['tot_tot_data'][i] = sum;
            } // sum
        }

        if (mode_selected == "Non-Linear") {
            //Create a loop for the ranges
            for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
                sum = 0;
                for(var j = start; j<=end; j=j+0.5){
                    z_string = String((j * 2)+1);
                    for (var l = k_check_start + 1; l<=k_check_end + 1; l++) {
                        k_string = String(l);
                        sum += tot_nl['tot_nl_h' + thres_string + '_k' + k_string + '_z' + z_string][i];
                    } // k_range
                } // z_value

                tot_data['tot_tot_data'][i] = sum;
                
            } // sum
        }

        if (mode_selected == "Linear, Precision"){
            
            //Create a loop for the ranges
            for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
                sum = 0;
                for(var j = start; j<=end; j=j+0.5){
                    z_string = String((j * 2)+1);
                    for (var l = k_check_start + 1; l<=k_check_end + 1; l++) {
                        k_string = String(l);
                        sum += tot_lin_pre['tot_lin_pre_h' + thres_string + '_k' + k_string + '_z' + z_string][i];

                    } // k_range
                
                } // z_value

                tot_data['tot_tot_data'][i] = sum;
            } // sum
        }

        if (mode_selected == "Non-Linear, Precision"){
           
            //Create a loop for the ranges
            for (var i = 0; i <tot_data['tot_tot_data'].length; i++) {
                sum = 0;
                for(var j = start; j<=end; j=j+0.5){
                    z_string = String((j * 2)+1);
                    for (var l = k_check_start + 1; l<=k_check_end + 1; l++) {
                        k_string = String(l);
                        sum += tot_nl_pre['tot_nl_pre_h' + thres_string + '_k' + k_string + '_z' + z_string][i];
                    } // k_range
                
                } // z_value
                tot_data['tot_tot_data'][i] = sum;
            } // sum
        }
    } //else statement
    console.log(tot_data['tot_tot_data']);
    source_data.trigger('change');

    """
    # Attach callback function to ColumnDataSources
    callback_settings = dict( source_data=source_data, 
                              js_lin=source_lin, 
                              js_nl=source_nl, 
                              js_lin_pre=source_lin_pre, 
                              js_nl_pre=source_nl_pre )
    callback_sliders = CustomJS(args=callback_settings, code=code_sliders)
    
    # Create selection menu for power spectrum type
    sel_pstype = [ 'Linear', 'Non-Linear', 
                   'Linear (high-precision)', 'Non-Linear (high-precision)' ]
    pstypes = ['lin', 'nl', 'lin_pre', 'nl_pre']
    dropdown = Select(title='Power spectrum type:', value=sel_pstype[0], 
                      options=sel_pstype, callback=callback_sliders)

    # Create RangeSlider for redshift values
    z_slider = RangeSlider(start=0, end=2.5, range=(0, 2.5), step=0.5, 
                           title='Range of z values', callback=callback_sliders)
    
    # Create slider for accuracy threshold
    thres_slider = Slider(start=1, end=6, value=2, step=1, 
                          title='Accuracy threshold', callback=callback_sliders)

    # Create a checkbox group for the k ranges
    k_lbls = [u'Ultra-Large Scales, 10\u207B\u2074 <= k <= 10\u207B\u00B2', 
              u'Linear Scales, 10\u207B\u00B2 <= k <= 10\u207B\u00B9', 
              u'Quasi-Linear Scales, 10\u207B\u00B9 <= k <= 1']
    k_checkbox = CheckboxGroup(labels=k_lbls, active=[0,1,2], 
                               callback=callback_sliders)
    
    # Attach callback to widgets
    callback_sliders.args['z_slider'] = z_slider
    callback_sliders.args['dropdown'] = dropdown
    callback_sliders.args['thres_slider'] = thres_slider
    callback_sliders.args['k_checkbox'] = k_checkbox
    
    # Code to open new page on click
    code_tap = \
        """
        // Get the value of the item that was tapped
        var index_selected=source.selected['1d'].indices[0];
        console.log(index_selected);
        
        // Get the mode in the dropdown
        var mode_selected = dropdown.value;
        console.log(mode_selected);
        
        // Initialize the starting URL
        //var url = 'http://127.0.0.1:5000/'
        var url = './'
        """
    for i in range(len(sel_pstype)):
        code_tap += "if (mode_selected == \"%s\") {\n" % sel_pstype[i]
        code_tap += "var url_mode = '?mode=%s'\n" % pstypes[i]
        code_tap += "var url_index = '&index=' + String(index_selected)\n"
        code_tap += "url_use = url + 'detail/' + url_mode + url_index\n"
        code_tap += "window.open(url_use)\n}\n"
    
    """
        if (mode_selected == "Linear") {
        var url_mode = 'lin/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }

        if (mode_selected == "Non-Linear") {
        var url_mode = 'nl/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }

        if (mode_selected == "Linear, Precision"){
        var url_mode = 'lin_pre/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }

        if (mode_selected == "Non-Linear, Precision"){
        var url_mode = 'nl_pre/'
        var url_index = '?index=' + String(index_selected)
        url_use = url + url_mode + url_index
        window.open(url_use)
        }
    """
    
    taptool = []
    for i, s in enumerate(fig_list):
        taptool.append( s.select(type=TapTool) )
        
        # Attach taptool to callback
        tt_args = dict(dropdown=dropdown, source=source_data)
        taptool[i].callback = CustomJS(args=tt_args, code=code_tap)
    
    """
    taptool2 = s2.select(type=TapTool)
    taptool2.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool3 = s3.select(type=TapTool)
    taptool3.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool4 = s4.select(type=TapTool)
    taptool4.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool5 = s5.select(type=TapTool)
    taptool5.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool6 = s6.select(type=TapTool)
    taptool6.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool7 = s7.select(type=TapTool)
    taptool7.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool8 = s8.select(type=TapTool)
    taptool8.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool9 = s9.select(type=TapTool)
    taptool9.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))

    taptool10 = s10.select(type=TapTool)
    taptool10.callback = (CustomJS(args=dict(dropdown=dropdown, source=source_data), code=code_tap))
    """
    
    # Build page layout
    l = layout([ [WidgetBox(thres_slider),],
                 [WidgetBox(dropdown),],
                 [WidgetBox(z_slider),], 
                 [WidgetBox(k_checkbox),], 
                 [plot,] ])
    script, div_dict = components(l)
    
    # Render template
    return render_template('homepage.html', 
                           script=script, 
                           div=div_dict, 
                           bokeh_version=BOKEH_VERSION)


#Index page 
@app.route('/detail/')
def lin():
    index = request.args.get('index')
    if index == None:
        index = '0'
    i = int(index)
    # Create the plot
        # load the data
    i = int(index)

    z_vals = ['1', '2', '3', '4', '5', '6']
    p = figure(toolbar_location="right", title = "CCL vs CLASS mPk, Linear", x_axis_type = "log", y_axis_type = "log",
        tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")

    p2 = figure(toolbar_location="right", title = "Discrepancy mPk, Linear", x_axis_type = "log", y_axis_type = "log",
         tools = "hover, pan, wheel_zoom, box_zoom, save, resize, reset")
    
    #Load the parameter valus
    data = np.loadtxt('../data/par_stan1.csv', skiprows = 1)

    index = float(data[i,0])
    h = float(data[i,1])
    Omega_b = float(data[i,2])
    Omega_cdm = float(data[i,3])
    A_s = float(data[i,4])
    n_s = float(data[i,5])

    for j, color in zip(z_vals, Spectral6):
        z_act = (float(j) - 1) / 2
        z_path = 'z%s_pk.dat' %j
        ccl_path = '../CCL/data_files/lhs_mpk_lin_%05d' % i 
        class_path = '../class/output/lin/lhs_lin_%05d' %i
        ccl_path += z_path
        class_path += z_path

        cclData = np.loadtxt(ccl_path,  skiprows = 1)
        cclK = cclData[:, 0]
        cclPk = cclData[:, 1]

        classData = np.loadtxt(class_path, skiprows = 4);
        classKLin = classData[:, 0]
        classPLin = classData[:, 1]

        #Multiply by factors
        #multiply k by some factor of h, CLASS and CCL use different units, ugh
        
        classKLin *= h
        classPLin /= h**3

        # create a plot and style its properties
        
        p.outline_line_color = None
        p.grid.grid_line_color = None

        p2.outline_line_color = None
        p2.grid.grid_line_color = None

        # plot the data
        #p.circle(ccl_data['k'].values, ccl_data['pk_lin'].values, size = 5, legend = "ccl data")
        p.line(cclK, cclPk, line_width = 2, color=color, legend='ccl data, z=%3.1f' %z_act)
        p.circle(cclK, cclPk, size = 5, color=color, legend = "ccl data, z=%3.1f" %z_act)

        #p.circle(classData['k'].values, classData['P'].values, size = 5, color = "red", legend = "class data")
        p.line(classKLin, classPLin, line_width = 2,color=color, line_dash='dashed', legend='class data, z=%3.1f' %z_act)
        p.square(classKLin, classPLin, size = 5, fill_alpha=0.8,color=color, legend = "class data, z=%3.1f" %z_act)

        # Set the x axis label
        # Set the y axis label
        p.yaxis.axis_label = 'Count (log)'
        comparisonValue = abs(cclPk - classPLin) / classPLin
        p2.line(classKLin, comparisonValue, line_width = 2,color=color, legend='z=%3.1f' %z_act)
        p2.circle(classKLin, abs(cclPk - classPLin) / classPLin, color=color,size = 5, legend='z=%3.1f' %z_act)

    #Adds the interactive legend and the axes
    p.legend.click_policy='hide'
    p.legend.location = 'bottom_left'
    p.yaxis.axis_label = 'P(k)'
    p.xaxis.axis_label = 'k'


    p2.legend.click_policy='hide'
    p2.legend.location = 'bottom_left'
    p2.yaxis.axis_label = '(CCL - CLASS)/CLASS'
    p2.xaxis.axis_label = 'k'
    plot = gridplot([[p2, p]])

    #Also the number for failures can either include clustering regime only or not
    thres = 1.e-4 #Threshold for number of failures
    clustering_only = False #Only counts failures if inside the clustering regime

    ultra_scale_min = 1e-4 #Minimum for the ultra-large scales
    ultra_scale_max = 1e-2 #Maximum for the ultra-large scales
    lin_scale_min = 1e-2 #Min for the linear scales
    lin_scale_max = 1e-1 #Max for the linear scales
    quasi_scale_min = 1e-1 #Min for the quasi-lin scales
    quasi_scale_max = 1.0 #Max for the quasi-lin scales


    cluster_reg_min = 1e-2 #Min for the cluster regime
    cluster_reg_max = 0.2 # Max for the cluster regime
    
    #Create arrays that will be filled in the loop over trials
    #Total of the wights
    tot_tot_lin = []

    #Get the totals for different k_ranges
    #We have 3 k_ranges, denote by 1,2,3
    #1 = Ultra Large Scales
    #2 = Linear scales
    #3 = Nonlinear scales
    #for i in range(len(trial_arr)):
    print("\n\ni is ", i)
    print("\n\nin summary statistic plot")

    trial = data[i,0]
    print ('Performing trial %05d' %trial)

    z_vals = ['1', '2', '3', '4', '5', '6']
    #Gonna generate an array of arrays, with each row corresponding to a different z value
    #Each columns will correspond to a different bins of k_values
    tot_lin = []

    #For list of lists
    tot_lin_ll = []

    for j in range(len(z_vals)):
        z_val = z_vals[j]
        z_path ='_z%s.dat' %z_val
        print ('Performing z_val = ', z_val)

        #For ease in iterating over different z values we use string manipulation
        stats_lin_path = '../stats/lhs_mpk_err_lin_%05d' %trial
#stats_lin_path = '../../stats/lhs/lin/non_pre/lhs_mpk_err_lin_%05d' %trial

        #Adds the z_path
        stats_lin_path += z_path

        #Calls the data
        stats_lin_data = np.loadtxt(stats_lin_path, skiprows=1)

        stats_lin_k = stats_lin_data[:,0]
        stats_lin_err = stats_lin_data[:,1]

        #Create arrays that will be used to fill the complete summary arrays
        tot_lin_z = []

        #For list of lists
        tot_lin_z_ll = []

        #We perform a loop that looks into the bins for k
        #Doing this for lin
        #Much easier than doing a for loop because of list comprehension ALSO FASTER
        tot_ultrasc = 0 #initialize value for ultra large scales
        tot_linsc = 0 #initialize for lin scales
        tot_quasisc = 0 #initialize for quasi lin scales

        #k has to fall in the proper bins
        aux_k_ultra = (stats_lin_k >= ultra_scale_min) & (stats_lin_k < ultra_scale_max)
        aux_k_lin = (stats_lin_k >= lin_scale_min) & (stats_lin_k < lin_scale_max)
        aux_k_quasi = (stats_lin_k >= quasi_scale_min) & (stats_lin_k <= quasi_scale_max)

        #Looks at only the regime where clustering affects it
        if clustering_only == True:
            aux_cluster_ultra = (stats_lin_k[aux_k_ultra] > cluster_reg_min) & (stats_lin_k[aux_k_ultra] < cluster_reg_max)
            aux_cluster_lin = (stats_lin_k[aux_k_lin] > cluster_reg_min) & (stats_lin_k[aux_k_lin] < cluster_reg_max)
            aux_cluster_quasi = (stats_lin_k[aux_k_quasi] > cluster_reg_min) & (stats_lin_k[aux_k_quasi] < cluster_reg_max)

           #Calculate the weights i.e. how badly has this bin failed
            w_ultra = np.log10(np.abs((stats_lin_err[aux_k_ultra])[aux_cluster_ultra]) / thres)
            w_lin = np.log10(np.abs((stats_lin_err[aux_k_lin])[aux_cluster_lin]) / thres)
            w_quasi = np.log10(np.abs((stats_lin_err[aux_k_quasi])[aux_cluster_quasi]) / thres)

            #Make all the negative values = 0, since that means they didn't pass the threshold
            aux_ultra_neg = w_ultra < 0.
            aux_lin_neg = w_lin < 0.
            aux_quasi_neg = w_quasi < 0.

            w_ultra[aux_ultra_neg] = 0
            w_lin[aux_lin_neg] = 0
            w_quasi[aux_quasi_neg] = 0

            tot_ultrasc = np.sum(w_ultra)
            tot_linsc = np.sum(w_lin)
            tot_quasisc = np.sum(w_quasi)
        #calculates imprecision in any regime
        if clustering_only == False:
            #caluclate the weights i.e. how badly has this bin failed
            w_ultra = np.log10(np.abs(stats_lin_err[aux_k_ultra]) / thres)
            w_lin = np.log10(np.abs(stats_lin_err[aux_k_lin]) / thres)
            w_quasi = np.log10(np.abs(stats_lin_err[aux_k_quasi]) / thres)

            #Make all the negative values = 0, since that means they didn't pass the threshold
            aux_ultra_neg = w_ultra < 0.
            aux_lin_neg = w_lin < 0.
            aux_quasi_neg = w_quasi < 0.

            w_ultra[aux_ultra_neg] = 0
            w_lin[aux_lin_neg] = 0
            w_quasi[aux_quasi_neg] = 0

            #calculate the totals
            tot_ultrasc = np.sum(w_ultra)
            tot_linsc = np.sum(w_lin)
            tot_quasisc = np.sum(w_quasi)


        #Append these values to our z summary stat
        #For list only
        tot_lin_z = np.append(tot_lin_z, tot_ultrasc)
        tot_lin_z = np.append(tot_lin_z, tot_ultrasc) # 2 bins
        tot_lin_z = np.append(tot_lin_z, tot_linsc)
        tot_lin_z = np.append(tot_lin_z, tot_quasisc)

        #For list of lists
        tot_lin_z_ll.append(tot_ultrasc)
        tot_lin_z_ll.append(tot_ultrasc) # 2 bins
        tot_lin_z_ll.append(tot_linsc)
        tot_lin_z_ll.append(tot_quasisc)

        #Append these values for the general z stat
        #For list only
        tot_lin = np.append(tot_lin, tot_lin_z)
        #For list of lists
        tot_lin_ll.append(tot_lin_z_ll)



	# Generate our z values for plotting
    z_actual = range(len(z_vals))
    z_arr = np.float_(np.asarray(z_actual))
    z_arr *= 0.5
    z = []
    z_ll = []	# Create a heat map, but makes it red, right now we just mark threshold on the heat map
    for j in range(len(z_actual)):
        z_full = np.full(len(tot_lin_ll[0]), z_arr[j])
        z = np.append(z,z_full)
        z_ll.append(z_full)

	#Generate an array of the midpoints of the bins
    ultra_scale_bin = (np.log10(ultra_scale_max) + np.log10(ultra_scale_min))/2
    ultra_scale_bin_1 = ultra_scale_bin - 0.5
    ultra_scale_bin_2 = ultra_scale_bin + 0.5
    lin_scale_bin = (np.log10(lin_scale_max) + np.log10(lin_scale_min))/2
    quasi_scale_bin = (np.log10(quasi_scale_max) + np.log10(quasi_scale_min))/2

    k_bin = [ultra_scale_bin_1, ultra_scale_bin_2, lin_scale_bin, quasi_scale_bin]
    k_list = k_bin * len(z_vals) 
    k_words = ['Ultra-large', 'Linear', 'Quasi Lin']

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange
    data_lin = {'tot_lin': tot_lin, 'z':z, 'k':k_list}
    source = ColumnDataSource(data=data_lin)

	#Values greater than threshold will be red, values at 0 will be green
	#and values in between will be gradient of orange
	#Trying to brute force colors for me
    colors = ['#fff5ee', '#ffe4e1', '#ffc1c1', '#eeb4b4', '#f08080', '#ee6363', '#d44942', '#cd0000', '#ff0000']
    mapper = LinearColorMapper(palette = colors, low = 0, high = 100)

    TOOLS = 'hover, pan, wheel_zoom, box_zoom, save, resize, reset'
    
    p_sum = figure(title = "Summary Statistic", toolbar_location = "above", tools=TOOLS)
        #tools = tools)

    p_sum.grid.grid_line_color = None
    p_sum.axis.axis_line_color = None
    p_sum.axis.major_tick_line_color = None
    p_sum.axis.major_label_text_font_size = "12pt"
    p_sum.axis.major_label_standoff = 0
    p_sum.xaxis.major_label_orientation = 0.5
    p_sum.rect('k', 'z', source = source, width = (1.0), height = (0.5), fill_color={'field': 'tot_lin', 'transform':mapper}, line_color= None)


    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size='12pt',
                    ticker=BasicTicker(desired_num_ticks=len(colors)),
                    label_standoff=6, border_line_color=None, location=(0,0))

    p_sum.add_layout(color_bar, 'right')
    p_sum.xaxis.axis_label = "log k"
    p_sum.yaxis.axis_label = "z"

    # Make a textarea, so that the html will print out a textbox of the parameter values
    id_val_string = 'Index = %s <br/>' %index
    h_string = 'h = %s <br/>' %h
    Omega_b_string = '&Omega;<sub>b</sub> = %s <br/>' %Omega_b
    Omega_cdm_string = '&Omega;<sub>cdm</sub> = %s <br/>' %Omega_cdm
    A_s_string = 'A<sub>s</sub> = %s <br/>' %A_s
    n_s_string = 'n<sub>s</sub> = %s <br/>' %n_s

    # Textbox html
    textbox = '<div class=\'boxed\'> Parameter values: <br/>' + id_val_string + h_string + Omega_b_string + Omega_cdm_string + A_s_string + n_s_string + '</div>'

    

    # Create a paragraph to tell the users what to do
    readme = Paragraph(text = """Below is the .ini file for CLASS and the code used to run CCL
    on python. For the .ini file, save it under something like mytext.ini, then
    go to your folder with CLASS and simply run ./class myext.ini
    For the CCL one, make sure you have it installed then simply run in Python.
    When you plot these against each other make sure to multiply the CLASS values
    by proper factor of h, since CLASS units are proportional to factors of h
    """, width = 500)

    # Create preformatted text of the .ini file used and the code for CLASS and CCL
    with open('../class/ini_files/lhs_lin_%05d.ini' %i, 'r') as myfile:
        ini_text = myfile.read()
    class_pretext = PreText(text='CLASS .ini file \n' + ini_text)

    h_ccl = 'h = %s \n' %h
    Omega_b_ccl = 'Omega_b = %s \n' %Omega_b
    Omega_cdm_ccl = 'Omega_cdm = %s \n' %Omega_cdm
    A_s_ccl = 'A_s = %s \n' %A_s
    n_s_ccl = 'n_s = %s \n' %n_s

    index_ccl = 'index = %s \n' %index
    
    # Create a textbox that tells the parameters
    parameters = PreText(text="""Parameter values \n""" + index_ccl + h_ccl +
        Omega_b_ccl + Omega_cdm_ccl + A_s_ccl + n_s_ccl)

    # Create a textbox for CCL code
    ccl_pretext = PreText(text=
    """Code for CCL, just simply run in python
Make sure to have the CLASS k values, so it coincides properly
i.e. make sure the class_path_lin is correct

import numpy as np
import pyccl

""" + 
    h_ccl + Omega_b_ccl + Omega_cdm_ccl + A_s_ccl + n_s_ccl + 
    """
cosmo = pyccl.Cosmology(Omega_c=Omega_cdm, Omega_b=Omega_b, h=h, A_s=A_s, n_s=n_s, transfer_function='boltzmann')
z_vals = ['1', '2', '3', '4', '5', '6']
for j in range(len(z_vals)):
    z_val = z_vals[j]
    class_path_lin = '/class/output/lin/lhs_lin_%s' %trial
    z_path = 'z%s_pk.dat' %z_val
    k_lin_data = np.loadtxt(class_path_lin, skiprows=4)
    k_lin = k_lin_data[:,0]
    k_lin *= h
    #Since our z values are like [0, 0.5, 1.,...] with 0.5 steps
    z = j * 0.5
    a = 1. / (1. + z)
    #Matter power spectrum for lin
    pk_lin = pyccl.linear_matter_power(cosmo, k_lin, a)
    """, width=500)

    #ccl_pretext = 
    # Embed plot into HTML via Flask Render

    #Create whitespace to fill between class_pretext and ccl_pretext
    whitespace = PreText(text = """ """, width = 200)
    #l = layout([[p2,p,],[WidgetBox(readme),],[WidgetBox(class_pretext),WidgetBox(whitespace), WidgetBox(ccl_pretext),]])
    l = layout([[p_sum, parameters,],[p2,p,],[WidgetBox(readme),],[WidgetBox(class_pretext),WidgetBox(whitespace), WidgetBox(ccl_pretext),]])
    script, div = components(l)
    #print (script)
    #print(div)

    return render_template("detail.html", script=script, div=div, bokeh_version=BOKEH_VERSION)


if __name__ == '__main__':
    # Set debug to False in a production environment
    app.run(port=5000, debug=True)

