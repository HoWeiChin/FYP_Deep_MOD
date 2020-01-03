from math import log
import matplotlib.pyplot as plt
percent_subsets = [0, 2.59, 47, 94]
real_predicted_ratios = [log(3/2.752), log(3/2.943), log(3/2.980), log(3/3.024)] #real/predicted
print(real_predicted_ratios)

fig = plt.figure()
plt.plot(percent_subsets, real_predicted_ratios, color="k", linewidth=4)
plt.axhline(y=0.00, color='r', linestyle='-', label='ground truth equals predicted')
plt.xlabel('Percentage of input data')
plt.ylabel('Log transformed ratio')
plt.legend()
plt.savefig('/gpfs0/home/e0031794/Documents/FYP/FYP_results_11_9_2019/data_slicing/1_trial/acc_vs_subset.png')
