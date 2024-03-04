import os
import glob

def init_app(working_dir):
    temp_dir = os.path.join(working_dir, '.temp')
    log_dir = os.path.join(working_dir, 'log')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    print("Application Initized")

def terminate_app(working_dir,log):
    # remove all temp files created in the session
    temp_patterns = os.path.join(os.path.join(working_dir, '.temp'), '*')
    temp_files = glob.glob(os.path.join(working_dir, temp_patterns)) 
    for file in temp_files:
        if os.path.isfile(file):
            os.remove(file)
    # save logs
    log_path =  os.path.join(working_dir, 'log')
    log_name = log.create_at.strftime("%y-%m-%d %H-%M-%S") + " " + str(log.username)
    with open(os.path.join(log_path,log_name), 'w') as f:
        log.update('Application closed.')
        f.write(str(log))
    
    print("Application saftely shutdown")
