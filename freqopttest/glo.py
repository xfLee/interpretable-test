"""A global module containing functions for managing the project."""

__author__ = 'wittawat'

import freqopttest
import os
try:
    import cPickle as pickle 
except:
    import pickle


def get_root():
    """Return the full path to the root of the package"""
    return os.path.abspath(os.path.dirname(freqopttest.__file__))

def result_folder():
    """Return the full path to the result/ folder containing experimental result 
    files"""
    return os.path.join(get_root(), 'result')


def ex_result_folder(ex):
    """Return the full path to the folder containing result files of the specified 
    experiment. 
    ex: a positive integer. """
    rp = result_folder()
    fpath = os.path.join(rp, 'ex%d'%ex )
    if not os.path.exists(fpath):
        os.mkdir(fpath)
    return fpath

def ex_result_file(ex, *relative_path ):
    """Return the full path to the file identified by the relative path as a list 
    of folders/files under the result folder of the experiment ex. """
    rf = ex_result_folder(ex)
    return os.path.join(rf, *relative_path)

def ex_save_result(ex, result, *relative_path):
    """Save a dictionary object result for the experiment ex. Serialization is 
    done with pickle. 
    EX: ex_save_result(1, result, 'data', 'result.p'). Save under result/ex1/data/result.p 
    EX: ex_save_result(1, result, 'result.p'). Save under result/ex1/result.p 
    """
    fpath = ex_result_file(ex, *relative_path)
    with open(fpath, 'w') as f:
        # expect result to be a dictionary
        pickle.dump(result, f)

def ex_load_result(ex, *relative_path):
    """Load a result identified by the  path from the experiment ex"""
    fpath = ex_result_file(ex, *relative_path)
    if not os.path.isfile(fpath):
        raise ValueError('%s does not exist' % fpath)

    with open(fpath, 'r') as f:
        # expect a dictionary
        result = pickle.load(f)
    return result

def ex_file_exists(ex, *relative_path):
    """Return true if the result file in under the specified experiment folder
    exists"""
    fpath = ex_result_file(ex, *relative_path)
    return os.path.isfile(fpath)


"""
For other users, set the config through set_global_config().

 config includes:
 - batch_log_path: full path to the folder used to contain log files for batch 
 processing.

"""

#config = {'batch_log_path': '/nfs/nhome/live/wittawat/'}

def set_global_config(con):
    global config
    config = con
    

