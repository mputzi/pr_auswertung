import PySimpleGUI as sg  

maxval = 100

mySlider = sg.Slider(range=(0, maxval),
    default_value=25,
    resolution=1,
    tick_interval=None,
    orientation='h',
    disable_number_display=True,
    border_width=1,
    relief=None,
    change_submits=True,
    enable_events=True,
    disabled=False,
    size=(None, None),
    font=None,
    background_color='blue',
    text_color=None,
    key="_SLIDER_",
    pad=None,
    tooltip=None,
    visible=True,
    metadata=None)



maxInput = sg.InputText(default_text="100",
    size=(4, 1),
    disabled=False,
    password_char="",
    justification="center",
    background_color="white",
    text_color="black",
    font=None,
    tooltip=None,
    change_submits=False,
    enable_events=True,
    do_not_clear=True,
    key="_MAXIN_",
    focus=True,
    pad=None,
    use_readonly_for_disable=True,
    right_click_menu=None,
    visible=True,
    metadata=None)

valuesCanvas = sg.Graph((400,200),
    graph_bottom_left=(0,0),
    graph_top_right=(100,maxval),
    background_color="white",
    pad=(5,5),
    change_submits=False,
    drag_submits=False,
    enable_events=False,
    key="_CANVAS_",
    tooltip=None,
    right_click_menu=None,
    visible=True,
    float_values=False,
    metadata=None)

layout = [[sg.Text('Slider Demonstration'), sg.Text('', key='_OUTPUT_')],
            [sg.T("Maximale Punktzahl:"), maxInput, sg.Button("Setze", key="BMAX")],
            [sg.T('0', size=(4,1), key='_LEFT_'),  
             mySlider,  
             sg.T('0', size=(4,1), key='_RIGHT_')],
             [valuesCanvas],  
            [sg.Button('Show'), sg.Button('Exit')]]  

window = sg.Window('Window Title', layout, finalize=True)  

window["BMAX"].bind("<Return>",None)
window["_MAXIN_"].bind("<Return>",None)
window["_SLIDER_"].bind("<Right>","+RAISE+")
window["_SLIDER_"].expand(expand_x=True)

while True:             # Event Loop  
    event, values = window.read()  
    print(event, values)  
    if event is None or event == 'Exit':  
        break
    elif event == "BMAX" or event=="_MAXIN_":
        oldMaxValue=maxval
        #sg.Print(values["_MAXIN_"])
        newMaxValue = values["_MAXIN_"]
        try:
            newmaxval = int(newMaxValue)
        
        except ValueError:
            
            continue
            
        if not newmaxval == 0:
            maxval = newmaxval
        else:
            pass
        newTickValue = maxval // 4
        window["_SLIDER_"](range=(0,maxval))
        window["_CANVAS_"].change_coordinates((0,0), (maxval,100))

        
    actval = int(values['_SLIDER_'])
    window['_LEFT_'].update(actval)  
    window['_RIGHT_'].update(maxval-actval)
    window["_CANVAS_"].Erase()
    
    w1 = actval
    r1 = window["_CANVAS_"].DrawRectangle((w1,20),(0,40),fill_color="blue")
    c1 = window["_CANVAS_"].DrawPoint((w1,50), size=2, color="black")
    #radius = 5
    #olt = (w1+5, 50-5)
    #obr = (w1-5, 50+5)
    #o1 = window["_CANVAS_"].DrawOval(olt, obr, line_color="red", line_width=2)
    
    l1 = window["_CANVAS_"].DrawLine((w1,10),(w1,90),color="green", width=2)
    
    w2 = maxval-actval
    r2 = window["_CANVAS_"].DrawRectangle((w2,60),(0,80),fill_color="red")
          

window.close()
