    for i in np.arange(-20,20,0.5):
        x.append(i)
        results.append(s.stanley_correction(i,s.INITIAL_ΤΗΕΤΑ_ERROR , s.VELOCITY))
        resultm.append(m.mpc_correction(i,m.INITIAL_ΤΗΕΤΑ_ERROR,m.VELOCITY))
