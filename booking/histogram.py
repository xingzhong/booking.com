import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
	df = pd.read_csv('../data.csv', header=0, 
			names=['Review Score','Review Count','Name'])
	df.to_excel('../data.xlsx', sheet_name='Paris')
	fig = plt.figure()
	ax = fig.add_subplot()
	df['Review Score'].hist(alpha=0.7, ax=ax,
			bins=20, normed=False, rwidth=0.8, align='mid')
	fig.suptitle("Paris Hotels Review Score Distributions")
	fig.savefig("../histogram.png")
	