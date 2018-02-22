import seaborn as sns
import pandas as pd
import os
import matplotlib.pyplot as plt
import sys

def boxplotter(df, ind, dep, separator = None, save = True):
  '''Plots boxplots for the data frame and desired features to visualize.

  Args:
    - df        (DataFrame): The dataframe all data (malignant and benign)
    - ind       (String)   : The name of the column to be placed on the x axis
    - dep       (String)   : The name of the column to be placed on the y axis
    - separator (String)   : The name of a column that will be used to further slice the x values
    - save      (Boolean)  : Saves the file by default, if set to False, displays the plot instead
  Raises:
    KeyError: If either feature1 or feature2 is not a valid column, raise an error.
  '''
  output_dir = 'output/boxplots/'

  sns.set_style('whitegrid')
  fig = plt.figure(figsize = (15, 9))
  try:
    ax = sns.boxplot(x = ind, y = dep, data = df, hue = separator, order = sorted(set(df[ind])), palette = 'Set2', showfliers=False)
  except KeyError as e:
    raise('Please pass in a column that is valid for the data frame.')

  fname = ' '.join([dep, 'by', ind])
  if separator is not None:
    fname = ' '.join([fname, 'and', separator])
  plt.title(fname)

  if save:
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    plt.savefig(output_dir + fname)
  else:
    plt.show()
  plt.close()

def histogram(df, x, separator, save = True):
  '''Plots histograms for the data frame and desired features to visualize.

  Args:
    - df        (DataFrame): The dataframe all data (malignant and benign)
    - ind       (String)   : The name of the column to be placed on the x axis
    - dep       (String)   : The name of the column to be placed on the y axis
    - separator (String)   : The name of a column that will be used to further slice the x values
    - save      (Boolean)  : Saves the file by default, if set to False, displays the plot instead
    - order     (List)     : A list defining the order of x axis labels
  Raises:
    KeyError: If either feature1 or feature2 is not a valid column, raise an error.
  '''
  output_dir = 'output/histograms/'
  sns.set_style('whitegrid')

  plt.figure(figsize=(15,9))
  prop_df = (df[x]
             .groupby(df[separator])
             .value_counts(normalize=True)
             .rename('Percentage')
             .reset_index())

  try:
    sns.barplot(x = x, y = 'Percentage', hue = separator, data = prop_df, palette = 'Set2')
  except KeyError as e:
    raise('Please pass in a column that is valid for the data frame.')
  plt.yticks(rotation = 90)
  fname = ' '.join([separator, 'by', x])
  plt.title(fname)

  if save:
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    plt.savefig(output_dir + fname)
  else:
    plt.show()
  plt.close()

if __name__ == '__main__':
  df = pd.read_csv('files/September2017.csv')
  print(df.head())

  df.drop(['Age'], axis = 1, inplace = True)
  education_order = ['DF/REF', 'Other', 'High School', 'Some college', 'College degree', 'Graduate degree']
  df.rename(columns = {
    'Do you approve or disapprove of how Donald Trump is handling his job as president?':'Approve/Disapprove Trump',
    'What is your highest level of education? ':'Highest level of education',
    'What is your race?':'Race',
    'Do you agree or disagree with the following statement: vaccines are safe and protect children from disease.':'vaccines are safe and protect children from disease',
    'How many books, if any, have you read in the past year?':'Books read in last year',
    'What percentage of the federal budget would you estimate is spent on scientific research?':'Percent of federal budget spent on scientific research',
    'Do you think it is acceptable or unacceptable to urinate in the shower?':'Acceptable/unacceptable to urinate in shower'
    }, inplace = True)

  #EDA with some demographic data and income equality
  boxplotter(df, 'Age Range', 'Income')
  boxplotter(df, 'Age Range', 'Income', 'Political Affiliation')
  boxplotter(df, 'Political Affiliation', 'Income')
  boxplotter(df, 'Gender', 'Income')
  boxplotter(df, 'Highest level of education', 'Income')
  boxplotter(df, 'Highest level of education', 'Income', 'Gender')

  #Histogram data of nonsensical questions because it's fun
  histogram(df, 'Highest level of education', 'Do you believe in ghosts?')
  histogram(df, 'Do you believe in ghosts?','Highest level of education')
  histogram(df, 'Political Affiliation', 'Do you believe in ghosts?')
  histogram(df, 'Age Range', 'Do you believe in ghosts?')
  histogram(df, 'Highest level of education', 'Do you believe in ghosts?')

