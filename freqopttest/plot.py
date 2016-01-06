"""
A module for plotting experimental results
"""

__author__ = 'wittawat'
import freqopttest.ex.exglobal as exglo
import freqopttest.glo as glo
import matplotlib.pyplot as plt
import numpy as np


def plot_prob_stat_above_thresh(ex, fname, h1_true, func_xvalues, xlabel,
        func_title=None):
    """
    plot the empirical probability that the statistic is above the theshold.
    This can be interpreted as type-1 error (when H0 is true) or test power 
    (when H1 is true). The plot is against the specified x-axis.

    - ex: experiment number 
    - fname: file name of the aggregated result
    - h1_true: True if H1 is true 
    - func_xvalues: function taking results dictionary and return the values 
        to be used for the x-axis values.            
    - xlabel: label of the x-axis. 
    - func_title: a function: results dictionary -> title of the plot

    Return loaded results
    """

    results = glo.ex_load_result(ex, fname)
    f_pval = lambda cell: cell['h0_rejected']
    vf_pval = np.vectorize(f_pval)
    pvals = vf_pval(results['test_results'])
    repeats, _, n_methods = results['test_results'].shape
    mean_pvals = np.mean(pvals, axis=0)
    #std_pvals = np.std(pvals, axis=0)
    #std_pvals = np.sqrt(mean_pvals*(1.0-mean_pvals))

    xvalues = func_xvalues(results)

    #ns = np.array(results[xkey])
    #te_proportion = 1.0 - results['tr_proportion']
    #test_sizes = ns*te_proportion
    line_styles = exglo.func_plot_fmt_map()
    method_labels = exglo.get_func2label_map()
    
    func_names = [f.__name__ for f in results['method_job_funcs'] ]
    for i in range(n_methods):    
        te_proportion = 1.0 - results['tr_proportion']
        fmt = line_styles[func_names[i]]
        #plt.errorbar(ns*te_proportion, mean_pvals[:, i], std_pvals[:, i])
        method_label = method_labels[func_names[i]]
        plt.plot(xvalues, mean_pvals[:, i], fmt, label=method_label)
    '''
    else:
        # h0 is true 
        z = stats.norm.isf( (1-confidence)/2.0)
        for i in range(n_methods):
            phat = mean_pvals[:, i]
            conf_iv = z*(phat*(1-phat)/repeats)**0.5
            #plt.errorbar(test_sizes, phat, conf_iv, fmt=line_styles[i], label=method_labels[i])
            plt.plot(test_sizes, mean_pvals[:, i], line_styles[i], label=method_labels[i])
    '''
            
    ylabel = 'test power' if h1_true else 'type-1 error'
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks( np.hstack((xvalues) ))
    
    alpha = results['alpha']
    """
    if not h1_true:
        # plot Wald interval if H0 is true
        # https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
        z = stats.norm.isf( (1-confidence)/2.0)
        gap = z*(alpha*(1-alpha)/repeats)**0.5
        lb = alpha-gap
        ub = alpha+gap
        plt.plot(test_sizes, np.repeat(lb, len(test_sizes)), '--', linewidth=2, 
                 label='99%-Conf', color='k')
        plt.plot(test_sizes, np.repeat(ub, len(test_sizes)), '--', linewidth=2, color='k')
        plt.ylim([lb-0.005, ub+0.005])
    """
    
    plt.legend(loc='best')
    title = '%s. %d trials. $\\alpha$ = %.2g.'%( results['prob_label'],
            repeats, alpha) if func_title is None else func_title(results)
    plt.title(title)
    #plt.grid()
    return results
        