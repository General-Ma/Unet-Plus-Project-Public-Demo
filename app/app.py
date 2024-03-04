import PySimpleGUI as sg
import cv2
import os
from objects.Log import Log
from elements.change_theme import set_new_theme
from elements.app_utils import init_app, terminate_app
from elements.texts import *
from elements.base64icon import logo_icon as cjel_icon
from elements.train import start_train
from elements.predict import start_predict
from elements.visualise2d import visualise2d_from_dir
from elements.popup_image import popup_image

# initilize the application when start 
working_dir = os.path.dirname(os.path.realpath(__file__))
init_app(working_dir)
init_theme = 'LightGrey3'
sg.theme(init_theme)
init_background_color = sg.LOOK_AND_FEEL_TABLE[init_theme].get('BACKGROUND')
logs = Log()

menu_top = [
    ["Navigation",["Home::redirect_to_home","Train::redirect_to_train","Predict::redirect_to_prediction","Exit"]],
    ["Appearance",["Theme 1","Theme 2", "Theme 3", "Theme 4", "Theme 5"]],
    ["Help",["About","Manual","Support"]]
]

#used as a universal size regulator for UI design 
STD_SIZE = 100

# reformat and load logo when initilized
standard_logo_path = os.path.join(working_dir, 'public', 'logo.png')
resized_logo = cv2.resize(cv2.imread(standard_logo_path),(int(0.5*STD_SIZE),int(0.5*STD_SIZE)))
resized_logo_path = os.path.join(working_dir, '.temp', 'resized_logo.png')

cv2.imwrite(resized_logo_path,resized_logo)

# Start Page UI, i.e home page
start_page_elements = [
    [sg.Text('Nick UNet+ Project')],
    [sg.Button('Trian a new model', key='redirect_to_train')],
    [sg.Button('Make a prediction', key='redirect_to_prediction')],
]

start_page = [
    [sg.Column([[sg.Image(resized_logo_path)]], justification='center')],
    [sg.Column(start_page_elements, vertical_alignment='center', justification='center')],
] 

# Train Page UI
train_page_elements = [
    [sg.Text('Here you train',font=('Default',10,'bold'))],
    [sg.Frame('Choose your Original data directory', layout = 
        [[sg.Input('',key='orig_data_dir', size = (int(0.25*STD_SIZE), None)),
        sg.FolderBrowse('Browse', target='orig_data_dir'),
        sg.Button('Visualize',key='visualize_train_orig')]]
    )],
    [sg.Frame('Choose your True Ground data directory', layout = 
        [[sg.Input('',key='mask_data_dir', size = (int(0.25*STD_SIZE), None)),
        sg.FolderBrowse('Browse', target='mask_data_dir'),
        sg.Button('Visualize',key='visualize_train_mask')]]
    )],
    # assign text tag separately, so that it enables the theme switch
    [sg.Frame('Model Type', layout = 
        [[sg.Radio('', 'model_type', key='b_unet',pad=((0.05*STD_SIZE,0),None)), sg.Text('Basic Unet', pad=((0,0.1*STD_SIZE),None)),
        sg.Radio('', 'model_type', key='resunet',pad=((0.05*STD_SIZE,0),None)), sg.Text('ResUNet', pad=((0,0.1*STD_SIZE),None)),
        sg.Radio('', 'model_type', key='uresnet',pad=((0.05*STD_SIZE,0),None)),sg.Text('U-ResNet', pad=((0,0.1*STD_SIZE),None))]]
    )],
    [sg.Frame('Epoch (integer between 1-200)', layout = 
        [[sg.Input('',key='epoch',size = (int(0.05*STD_SIZE), None))]],
    )],
    [sg.Frame('', border_width=0, layout = 
        [[sg.Button('Start to Train', key='start_to_train'),
        sg.Button('Go Back', key='redirect_to_home_train_pg'),
        sg.Button('Help', key='help_train_pg')]]
    )],
    [sg.Frame('', border_width=0, layout = 
        [[sg.Multiline(logs.content, autoscroll=True, disabled = True,size = (int(0.5*STD_SIZE), int(0.3*STD_SIZE)), key='log_t')]]
    )],
]
train_page = [
    [sg.Column(train_page_elements)]
]

# Predition Page
prediction_page_elements = [
    [sg.Text('Here you predict',font=('Default',10,'bold'))],
    [sg.Frame('Choose your data directory', layout = 
        [[sg.Input('',key='predict_data_dir', size = (int(0.25*STD_SIZE), None)),
        sg.FolderBrowse('Browse', target='predict_data_dir'),
        sg.Button('Visualize',key='visualize_pred_orig')]]
    )],
    [sg.Frame('Choose your model (enter path)', layout = 
        [[sg.Input('',key='model_path', size = (int(0.25*STD_SIZE), None)),
        sg.FolderBrowse('Browse', target='model_path')]]
    )],
    [sg.Frame('Choose your output directory', layout = 
        [[sg.Input('',key='output_mask_dir', size = (int(0.25*STD_SIZE), None)),
        sg.FolderBrowse('Browse', target='output_mask_dir'),
        sg.Button('Visualize',key='visualize_pred_mask')]]
    )],
    [sg.Frame('', border_width=0, layout = 
        [[sg.Button('Predict', key='start_to_predict'),
        sg.Button('Go Back', key='redirect_to_home_pred_pg'),
        sg.Button('Help', key='help_pred_pg')]]
    )],
    [sg.Frame('', border_width=0, layout = 
        [[sg.Multiline(logs.content, autoscroll=True, disabled = True,size = (int(0.5*STD_SIZE), int(0.3*STD_SIZE)), key='log_p')]]
    )]
]
prediction_page = [
    [sg.Column(prediction_page_elements)]
]

# overal layout which wrapped top bar, exit button and different pages
layout = [
    [sg.Menu(menu_top)],
    [sg.Column(start_page, key ="StartPage", visible=True),
    sg.Column(train_page, key ="TrainPage", visible=False),
    sg.Column(prediction_page, key ="PredictionPage", visible=False)
    ]
]

window = sg.Window('Nick UNet+ Project (2D)', icon=cjel_icon, layout=layout ,background_color=init_background_color, \
    size = (4*STD_SIZE,3*STD_SIZE),element_justification='c', resizable=True,finalize=True)   
window.TKroot.minsize(2*STD_SIZE, 2*STD_SIZE) 

# This function uses window and log defined above, it should only be used as a shortcut privately 
def _update_log(string, element='log_t', window=window,log=logs):
    log.update(string)
    window[element].update(log.content)


# Event Listener
while True:
    event, values = window.read() 

    # Menubar Appearance Events
    if event == 'Theme 1':
        set_new_theme(window, init_theme)
    elif event == 'Theme 2':
        set_new_theme(window, 'DarkAmber')
    elif event == 'Theme 3':
        set_new_theme(window, 'LightBlue2')
    elif event == 'Theme 4':
        set_new_theme(window, 'BrightColors') 
    elif event == 'Theme 5':
        set_new_theme(window, 'DarkBlack1')
    
    # Menubar Help Events
    if event == 'About':
        sg.popup_ok(about_text, title='About')
    if event == 'Manual':
        sg.popup_ok('*link to the user manual*', title='Manual')
    if event == 'Support':
        sg.popup_ok(contact_text, title='Contact')

    # Navigation Events
    if event in ['redirect_to_train','Train::redirect_to_train']:
        window['StartPage'].update(visible = False)
        window['TrainPage'].update(visible = True)
        window['PredictionPage'].update(visible = False)
        window.TKroot.minsize(4*STD_SIZE, 4*STD_SIZE)
        _update_log("Navigated to train module. Please train your model.", 'log_t')
    elif event in ['redirect_to_prediction','Predict::redirect_to_prediction']:
        window['StartPage'].update(visible = False)
        window['TrainPage'].update(visible = False)
        window['PredictionPage'].update(visible = True)
        window.TKroot.minsize(4*STD_SIZE, 4*STD_SIZE)
        _update_log("Navigated to prediction module. Please set a prediction task.", 'log_p')
    elif event in ['redirect_to_home', 'Home::redirect_to_home', 'redirect_to_home_train_pg', 'redirect_to_home_pred_pg']:
        window['TrainPage'].update(visible = False)
        window['PredictionPage'].update(visible = False)
        window['StartPage'].update(visible = True)
        window.TKroot.minsize(2*STD_SIZE, 2*STD_SIZE)

    # Train Button events
    if event == 'start_to_train':
        # Get model type from the radio group
        if values['b_unet'] == True:
            model_type = 'b_unet'
        elif values['resunet'] == True:
            model_type = 'resunet'
        elif values['uresnet'] == True:
            model_type = 'uresnet'
        else:
            model_type = None
        _update_log(f"Training Initializing: orig_data_dir->{values['orig_data_dir']},\
            mask_data_dir->{values['mask_data_dir']}, model_type->{model_type}, epoch->{values['epoch']}", 'log_t')
        #THIS WILL BE PUT AS AN ELEMENT IN LATER STAGE OF DEV
        try:
            # There will be a callback to indicate the progress in the future
            will_proceed = sg.popup_ok_cancel('Training may sometimes take long time (usually 3-10 min), please be patient.\n Press OK to start training.')
            if will_proceed=="OK":
                _update_log("Start Training ...", 'log_t')
                trained_model = start_train(orig_data_dir=values['orig_data_dir'], mask_data_dir=values['mask_data_dir'],\
                    model_type=model_type, epoch=values['epoch'] )
                _update_log("Training Finished", 'log_t')
                model_save_dir = sg.popup_get_folder('Save your model', default_path = os.path.join(working_dir, 'models', 'new_model'))
                trained_model.save(model_save_dir)
                _update_log(f'Model saved successfully at {model_save_dir}', 'log_t')
            elif will_proceed=="Cancel":
                _update_log("Training Task Aborted by user", 'log_t')
        except Exception as error:
            _update_log(f'Error initilizing training: {error}', 'log_t')
            sg.popup_cancel(f'Error: {error}', title='Invalid Input')
    
    # Predict Button events
    if event == 'start_to_predict':
        _update_log(f"Prediction Initializing: predict_data_dir->{values['predict_data_dir']}, model_dir->{values['model_path']}, output_dir->{values['output_mask_dir']}", 'log_p')
        try:
            start_predict(predict_data_dir = values['predict_data_dir'], output_mask_dir = values['output_mask_dir'], model_dir = values['model_path'])
            _update_log("Prediction Finished.", 'log_p')
        except Exception as error:
            _update_log(f'Error initilizing prediction: {error}', 'log_p')
            sg.popup_cancel(f'Error: {error}', title='Invalid Input')
    
    # Visualize events
    VISUALIZE_GET_FOLDER_MAP = {
    'visualize_train_orig': 'orig_data_dir',
    'visualize_train_mask': 'mask_data_dir',
    'visualize_pred_orig': 'predict_data_dir'
    }
    if event  in ['visualize_train_orig', 'visualize_train_mask', 'visualize_pred_orig']:
        visualised_dir = values[VISUALIZE_GET_FOLDER_MAP[event]]
        try:
            # the visualised_image is a ByteIO stream
            visualised_image = visualise2d_from_dir(visualised_dir)
            popup_image(visualised_image, '2D Visualisation')
        except ValueError:
            sg.popup_cancel(f'Error: the selected directory does not contain any supported image (.png, .tiff)', title='Invalid Folder')



    # Exit the application, break event listener loop
    if event == sg.WIN_CLOSED or event == 'Exit':
        terminate_app(working_dir,logs)
        break    

window.close()