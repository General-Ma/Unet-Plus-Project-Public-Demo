#inspired by https://github.com/PySimpleGUI/PySimpleGUI/issues/2437
import PySimpleGUI as sg

def change_theme_dynamic(window, theme):
                current_theme = sg.LOOK_AND_FEEL_TABLE[theme]
                try:
                    window_bkg = current_theme.get('BACKGROUND')
                    window.TKroot.config(background=window_bkg)
                except Exception as e:
                        print(e)

                # iterate over all widgets:
                for v, element in window.AllKeysDict.items():
                # for child in window.TKroot.frame.children.values():
                    
                    try:
                        color = current_theme.get(element.Type.upper())
                        if color:
                            if element.Type == 'button':
                                element.Widget.config(foreground=color[0], background=color[1])
                            else:
                                element.Widget.config(background=color)

                            element.update()
                    except Exception as error:
                        print(error)

def set_new_theme(window, theme):
    global CURRENT_THEME
    CURRENT_THEME = theme
    sg.theme(theme)
    window.TKroot.config(background=sg.theme_background_color())
    for element in window.element_list():
        element.Widget.config(background=sg.theme_background_color())
        element.ParentRowFrame.config(background=sg.theme_background_color())
        if 'text' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_text_color())
            element.Widget.config(background=sg.theme_text_element_background_color())
        if 'input' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_input_text_color())
            element.Widget.config(background=sg.theme_input_background_color())
        if 'progress' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_progress_bar_color()[0])
            element.Widget.config(background=sg.theme_progress_bar_color()[1])
        if 'slider' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_slider_color())
        if 'button' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_button_color()[0])
            element.Widget.config(background=sg.theme_button_color()[1])
        if 'radio' in str(type(element)).lower():
            #element.Widget.config(foreground=sg.theme_text_color())
            element.Widget.config(background=sg.theme_text_element_background_color())
        if 'input' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_text_color())
            element.Widget.config(background=sg.theme_text_element_background_color())
        if 'frame' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_text_color())
            element.Widget.config(background=sg.theme_text_element_background_color())
        if 'multiline' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_text_color())
            element.Widget.config(background=sg.theme_text_element_background_color())
    window.Refresh()

def main():
    themes = sg.ListOfLookAndFeelValues()
    selected_theme = 'Reds'
    current_them = sg.LOOK_AND_FEEL_TABLE[selected_theme]
    sg.theme(selected_theme)

    layout = [
            [sg.T('User Setting:')],
            [sg.Text('Select Theme:'), 
            sg.Combo(values=themes, default_value=selected_theme, size=(15, 1), enable_events=True, key='select_theme')],
            [sg.I('this is input')], 
            [sg.B('Hello'), sg.Button(' about ', key='about')]
    ]

    window = sg.Window('', layout=layout)

    while True:
        e, v= window()
        if e is None:
            break
        
        elif e == 'select_theme':
            set_new_theme(window, v['select_theme'])

if __name__ == "__main__":
    main()