import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# poisson function, parameter mu and sigma is the fit parameter
def normal(k, mu, sigma):
    return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (k - mu)**2 / (2 * sigma**2) )

#========== User probability distribution	
mu, sigma = 50, 20 # mean and standard deviation
s = np.random.normal(mu, sigma, 1000) # 1000 random number following normal distribution

plt.xlabel('User')
plt.ylabel('Probability')
plt.title('Probability Distribution of User (mu=%d,sigma=%d)'%(mu, sigma))

plt.grid(True)
count, bins, ignored = plt.hist(s, 100, range=[0,100], normed=True)
plt.plot(bins, normal(bins, mu, sigma), linewidth=2, color='r')

pp = PdfPages('output/user.pdf')
plt.savefig(pp, format='pdf')
pp.savefig()
pp.close()


#============ Role probability distribution	
mu, sigma = 3, 5 # mean and standard deviation
s = np.random.normal(mu, sigma, 1000) # 1000 random number following normal distribution

plt.clf()
plt.xlabel('Role')
plt.ylabel('Probability')
plt.title('Probability Distribution of Role (mu=%d,sigma=%d)'%(mu, sigma))

plt.grid(True)
count, bins, ignored = plt.hist(s, 6, range=[0,6], normed=True)
plt.plot(bins, normal(bins, mu, sigma), linewidth=2, color='r')

pp = PdfPages('output/role.pdf')
plt.savefig(pp, format='pdf')
pp.savefig()
pp.close()

#============ Patient probability distribution	
mu, sigma = 150, 50 # mean and standard deviation
s = np.random.normal(mu, sigma, 1000) # 1000 random number following normal distribution

plt.clf()
plt.xlabel('Patient')
plt.ylabel('Probability')
plt.title('Probability Distribution of Patient (mu=%d,sigma=%d)'%(mu, sigma))

plt.grid(True)
count, bins, ignored = plt.hist(s, 300, range=[0,300], normed=True)
plt.plot(bins, normal(bins, mu, sigma), linewidth=2, color='r')

pp = PdfPages('output/patient.pdf')
plt.savefig(pp, format='pdf')
pp.savefig()
pp.close()


#============ Date probability distribution	
mu, sigma = 15, 50 # mean and standard deviation
s = np.random.normal(mu, sigma, 1000) # 1000 random number following normal distribution

plt.clf()
plt.xlabel('Date')
plt.ylabel('Probability')
plt.title('Probability Distribution of Date (mu=%d,sigma=%d)'%(mu, sigma))

plt.grid(True)
count, bins, ignored = plt.hist(s, 31, range=[0,31], normed=True)
plt.plot(bins, normal(bins, mu, sigma), linewidth=2, color='r')

pp = PdfPages('output/date.pdf')
plt.savefig(pp, format='pdf')
pp.savefig()
pp.close()

