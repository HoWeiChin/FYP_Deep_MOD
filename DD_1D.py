import numpy as np
import os
import pathlib
import random
import argparse

def DD_numr(D, mu, init, source, Lx, Ttotal, dtsave, dx, dt, save_dir):
    
    if dt > dx**2/D:
        print('dt exceeds dtlim = {dx**2/D}')
        return 
    #create path
    pathlib.Path(save_dir).mkdir(parents=True,exist_ok=True)
    """
        nx : total number of spatial intervals
        nt : total number of time intervals
        ns : total number of save intervals

    """
    nx = round(Lx/dx)+1         #get number of spatial intervals        
    nt = round(Ttotal/dt)+1     #get number of time intervals to iterate through   
    ns = round(Ttotal/dtsave)+1 #number of intervals to save data regularly
    dsave = round(dtsave/dt)    #ask about this 
    
    xx = np.arange(0, nx)*dx    #simulation position 
    ss = np.arange(0, ns)*dtsave  #clarify about this
    x,s = np.meshgrid(xx, ss)     #x is the x coord of 2d mat, s is the y coord of 2d mat
    
    u = np.zeros(x.shape) #initialise simulation matrix, where i,j entry is the concentration at position x,
                            #column == j position, row = ith time
    u2 = np.zeros(nx+2) #include boundary condition, left and right, conc of morphogens in 1D
    u2[source+1] = init #set initiation concentration not transpassing into boundaries
    u[0,:] = u2[1:nx+1] #set 1st row, row == 0th time with initial concentration condition 
    
    for ii in range(1,nt):
        u1 = u2
    
        u2[1:nx+1] \
        = (D*dt/(dx**2))*(u1[2:nx+2]+u1[0:nx]-2*u1[1:nx+1]) \
           - mu*dt*u1[1:nx+1] + u1[1:nx+1] #update non-boundary

        u2[0] = u1[1] #update boundary
        u2[-1] = u1[-2] #update boundary 
        u2 = np.clip(u2, a_min = 0, a_max = None) #remove negative values, set all negatives to 0 
    
        if ii%dsave == 0:
            jj = round(ii/dsave)

            u[jj,:] = u2[1:nx+1]
    np.save(os.path.join(save_dir,"x_numer"), x)
    np.save(os.path.join(save_dir,"s_numer"), s)
    np.save(os.path.join(save_dir,"u_numer"),u)
    return x, s, u

def DD_anly(x, t, source, D, m, j, save_dir):
    #create path
    pathlib.Path(save_dir).mkdir(parents=True,exist_ok=True)
    c = j / np.sqrt(4 * np.pi * D * t) * np.exp(- (x-source)**2 / (4 * D * t) - m*t)
    np.save(os.path.join(save_dir,"x_analy"),x)
    np.save(os.path.join(save_dir,"y_analy"),c)
    return c

def randomised_trials(num_trials, save_dir):
    """
        num_trials (int): number of trials to initialise parameters of PDEs
        save_dir (string): parent node of the ith file folder which will store simulated for the ith number of trial.

    """
    mu_lower = 1/(45*600)
    mu_upper = 0.0005
    #dtsave = 0.001 #set this constants
    for i in range(num_trials):
        #let ith dir to store data be save_dir + str(i+1
        ith_save_dir = save_dir + "/" + str(i+1) + "_trial"
        pathlib.Path(ith_save_dir).mkdir(parents=True,exist_ok=True)
        #write parameter/simulation values into ith folder:
        file_name = ith_save_dir + "/" + str(i+1) + "_trial_simulation_values.txt"
        f = open(file_name, "w+")

        #first, let's randomised parameters shared by DD_numr and DD_anly
        Diff_coeff = random.randint(3,10) #[a,b], Diff_coeff = D
        f.write("Diff_coeff(D):" + str(Diff_coeff) + "\n")

        #decay_coeff = random.uniform(mu_lower, mu_upper) #[a,b], decay_coeff = mu
        decay_coeff = 0 
        f.write("decay_coeff(mu):" + str(decay_coeff) + "\n")

        init_conc = random.randint(50,100) #init_conc = init
        f.write("init_conc(init):" + str(init_conc) + "\n")

        Total_sim_time = 10 #Total_sim_time = Ttotal; means total simulation time #time is in seconds
        f.write("Total_sim_time(Ttotal):" + str(Total_sim_time) + "\n")
        
        #randomised dx, Lx, source, dt
        dx = random.uniform(1,2)
        f.write("dx:" + str(dx) + "\n")

        #Lx = random.randint(30,40)
        Lx = 30
        f.write("Lx:" + str(Lx) + "\n")

        dt = random.uniform(0.001, (dx)**2/Diff_coeff)
        f.write("dt:" + str(dt) + "\n")

        source = random.randint(0,round(Lx/dx)-2) #need to be within round(Lx/dx)-2
        f.write("source:" + str(source) + "\n")

        #create xx for DD_anly
        xx = np.arange(0, round(Lx/dx)+1)*dx
        f.write("xx:" + np.array_str(xx) + "\n")
        f.close()

        DD_numr(D=Diff_coeff, mu=decay_coeff, init=init_conc, 
                source=source, Lx=Lx, Ttotal=Total_sim_time, 
                dtsave= dt, dx=dx, dt=dt, 
                save_dir=ith_save_dir
                ) #set dtsave as dt

        DD_anly(x=xx, t=Total_sim_time, source=source, D=Diff_coeff, 
                m=decay_coeff, j=init_conc,
                save_dir=ith_save_dir)


     
if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description="programme to randomised parameter values of PDEs to generate simulated data")
    my_parser.add_argument("-n", type=int, help="Number of times to generate spatial and temporal data based on randomised parameters")
    my_parser.add_argument("-dir", type=str, help="Chosen directory to save generated data")
    args = my_parser.parse_args()
    randomised_trials(args.n, args.dir)
    # mu = 1/(45*60) #done
    # D = 3 #done
    # init = 100 #done
    # dx = 1 #done
    # Lx = 30 #doone
    # Ttotal = 5 #done
    # source = 15 # done
    # xx = np.arange(0, round(Lx/dx)+1)*dx
    # save_dir = "/mnt/mbi/home/e0031794/FYP"
    # DD_numr(D=D, mu=mu, init=init, Lx=Lx, source=source, Ttotal=5, dtsave=0.001, dx=dx, dt=0.001,save_dir=save_dir)
    # #DD_anly(x=xx, t=Ttotal, source=source, D=D, m=mu, j=init,save_dir=save_dir)
