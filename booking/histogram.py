# post processing script
# file format convert from csv to excel through pandas 
# create histogram through pandas 
# -- Bo Yang

import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
	# load data 
	df = pd.read_csv('../data.csv', header=0, 
			names=['Review Score','Review Count','Name'])
	# convert to excel
	df.to_excel('../data.xlsx', sheet_name='Paris')
	# create figure
	fig = plt.figure()
	ax = fig.add_subplot()
	# create histogram
	df['Review Score'].hist(alpha=0.7, ax=ax,
			bins=20, normed=False, rwidth=0.8, align='mid')
	fig.suptitle("Paris Hotels Review Score Distributions")
	# save the figure
	fig.savefig("../histogram.png")
	