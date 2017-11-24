import numpy as np

def ccl_summary_stats(params,
                      fname_template='../stats/lhs_mpk_err_lin_%05d_z%d.dat',
                      thresholds=[5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2],
                      scale_ranges = [(1e-4, 1e-2), (1e-2, 1e-1), (1e-1, 1e0)],
                      z_vals = ['1', '2', '3', '4', '5', '6'],
                      cache_name=None):
    """
    Calculate summary stats for the deviation between CCL and reference power 
    spectra as a function of scale and redshift, for a large number of sample 
    points over the cosmological parameter space.
    """
    # Get dimensions of stats array that will be constructed
    N_samp = params['id'].size
    N_thres = len(thresholds)
    N_z = len(z_vals)
    N_kbins = len(scale_ranges)
    
    # Check if data were cached
    if cache_name is not None:
        try:
            stats = np.load("%s.npy" % cache_name)
            print "  Loaded '%s' from cache." % cache_name
            assert stats.shape == (N_samp, N_thres, N_z, N_kbins)
            return stats, params
        except:
            raise
    
    # Create array to hold summary statistics, with shape:
    # (N_samp, N_thres, N_z, N_kbins)
    stats = np.zeros((N_samp, N_thres, N_z, N_kbins))
    
    # Loop over sample points in parameter space and calculate summary stats
    for i in range(N_samp):
        trial = params['id'][i]
        print "  Loading CCL power spectra for parameter set %05d" % i
        
        # Loop over redshift values
        for j in range(N_z):
            
            # Load cached CCL power spectrum data
            fname = fname_template % (i, z_vals[j])
            pk_ccl_dat = np.loadtxt(fname, skiprows=1)
            ccl_k = pk_ccl_dat[:,0]
            ccl_pk = pk_ccl_dat[:,1]
            
            # Calculate summary stats in each k bin
            for m in range(N_kbins):
                kmin, kmax = scale_ranges[m]
                idxs = np.logical_and(ccl_k >= kmin, ccl_k < kmax)
                
                # Calculate deviation statistic, Delta, for a range of 
                # threshold values (only values above the threshold are counted)
                # FIXME: ccl_pk is actually the deviation, which was 
                # precomputed somewhere!
                for n, thres in enumerate(thresholds):
                    # Calculate deviation statistic
                    dev = np.log10(np.abs(ccl_pk[idxs]) / thres)
                    dev[np.where(dev < 0.)] = 0.
                    
                    # Store result in stats array (N_samp, N_thres, N_z, N_kbins)
                    stats[i, n, j, m] = np.sum(dev)
    
    # Save to cache file
    if cache_name is not None:
        np.save(cache_name, stats)
    
    return stats, params


def build_data_dict(stats_arr, prefix):
    """
    Build a data dictionary with columns named according to (k,z) bins, a 
    threshold value, and some prefix.
    
    Assumes that stats_arr has shape: (N_samp, N_thres, N_z, N_kbins)
    """
    # Get no. of points in each dimension.
    N_sam, N_thres, N_z, N_kbins = stats_arr.shape
    
    # Create dictionary with column names that can be used by ColumnDataSource
    data_dict = {}
    for n in range(N_thres):
        for j in range(N_z):
            for m in range(N_kbins):
                key = "tot_%s_h%d_k%d_z%d" % (prefix, n+1, m+1, j+1)
                data_dict[key] = stats_arr[:,n, j, m]
    return data_dict
    
