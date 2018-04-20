import requests
import pandas as pd

def main(companyName):
    url = 'https://salarydog.com/api/salary'
    companyJson = {"name":companyName}
    response = requests.post(url,json=companyJson)
    data = response.json()
    df = pd.DataFrame(data)
    df[['Month','Day','Year']] = df['EMPLOYMENT_START_DATE'].str.split('/',expand=True)    
    df[['Month','Day','Year']] = df[['Month','Day','Year']].astype(str)
    def addLeadingZeros(row):
        if len(row) < 2:
            return "0"+row
        else:
            return row
    df['Month'] = df['Month'].apply(addLeadingZeros)
    df['Day'] = df['Day'].apply(addLeadingZeros)
    df['EMPLOYMENT_START_DATE'] = df['Year'] + '-' + df['Month'] + '-' + df['Day']
    df['EMPLOYMENT_START_DATE'] = df['EMPLOYMENT_START_DATE'].astype('datetime64[ns]')
    df['WAGE_RATE_OF_PAY_FROM'] = df['WAGE_RATE_OF_PAY_FROM'].astype('float')
    
    plots = {'wageDistPlot':sns.distplot(df['WAGE_RATE_OF_PAY_FROM']),
             'wageLinePlot':df.set_index(['EMPLOYMENT_START_DATE'])['WAGE_RATE_OF_PAY_FROM'].plot(kind='line'),
             'medianWageByYear': df[df['EMPLOYMENT_START_DATE']>='2011-01-01'].set_index(['EMPLOYMENT_START_DATE'])['WAGE_RATE_OF_PAY_FROM'].resample('YS').median().plot(kind='line')
    }
    from os.path import expanduser
    download_path = expanduser("~/Downloads")
    for plot_name in plots:
        fig = plots[plot_name].get_figure()
        fig.savefig(os.path.join(download_path,plot_name), dpi=1000)