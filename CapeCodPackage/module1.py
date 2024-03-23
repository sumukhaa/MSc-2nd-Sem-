import pandas as pd
import numpy as np

#Displays accident years
def accident_year(df):
    new_df=pd.DataFrame(df.index, columns=['Accident Year'])
    return new_df

#Reported Claims (diagonal elements of a ldt)
def latest_diagonal(df,x='Reported'):
    reported_claims=[]
    row, col = df.index, df.columns
    # To find the reported claims, we fetch Diagonal elements of ldt
    for i in range(len(row)):
        reported_claims.append(int(df.iloc[i,len(row)-i-1]))
    

    new_df=pd.DataFrame(reported_claims, columns=['{} Claims at {}'.format(x,max(df.index))])
    new_df.index=df.index
    return new_df

#n is the no. of recent years to which you want to calculate cdfs by taking mean
def cumulative_cdf(df,n=3):
    #Creating a 2d array for finding the age-to-age factor and store them in it
    factors=[]
    order=df.shape[0]
    limit=order

    #Range is kept in such a way that only the upper triangle is touched
    for y in range(order-1):
        arr=[]
        for x in range(limit-1):
            z=df.iloc[x,y+1]/df.iloc[x,y]
            arr.append(np.round(z,3))
        limit-=1
        factors.append(arr)
    # factors IS A 2D LIST WHICH HAS ALL AGE-TO-AGE FACTORS LIKE A LDT

    '-----------------------------------------------------'

    #Taking average of age-to-age factors of last n=3 years for each time period
    avg_factors=[]

    for x in factors: 
        avg=sum(x[-n:])/min(n,len(x[-n:])) #divide by 3 when len(arr)=3, by other no. when len<3
        avg_factors.append(round(avg,4))

    avg_factors
    # avg_factors IS A 1D LIST WHICH HAS AVG OF LAST N AGE-TO-AGE FACTORS FOR EACH PERIOD

    '-----------------------------------------------------'

    #Calculating Cumulative Claim Development Factors
    cdf=[avg_factors[-1]]
    prod=1
    for x in avg_factors[::-1]:
        prod=prod*x
        cdf.append(round(prod,4))

    # cdf HAS CUMULATIVE CLAIM DEVELOPMENT FACTORS
    '-----------------------------------------------------'
    
    new_df=pd.DataFrame(cdf, columns=['Reported CDF to Ult'])
    new_df.index=df.index
    return new_df

#Percentage of Ultimate Reported = 1/CDF
def percent_reported(df,n=3):
    arr=cumulative_cdf(df,n).values

    pcent_reported= ["{:.1%}".format(1/x) for x in arr.flatten()]

    new_df=pd.DataFrame(pcent_reported, columns=[f'% of Ultimate Reported'])
    new_df.index=df.index
    return new_df

#Used Up Premium = Earned Premium * %age of Ult Reported
def used_up_premium(df,earned_premium,n=3):
    used_up_premium=[]
    arr=[float(x.rstrip('%'))/100 for x in percent_reported(df,n).values.flatten()]

    #Multiplying corresponding elements of 2 arrays
    for x,y in zip(arr, earned_premium):
        used_up_premium.append(int(x*y))

    new_df=pd.DataFrame(earned_premium, columns=['Earned Premium'])
    new_df[f'% of Ult Reported']=percent_reported(df,n).values.flatten()
    new_df['Used Up Premium']=used_up_premium
    new_df.index=df.index
    return new_df
    
#Estimated Claim Ratios = Reported Claims / Used up Premium
def est_claim_ratios(df,earned_premium,n=3):
    arr1=latest_diagonal(df).values.flatten()
    arr2=[x[-1] for x in used_up_premium(df,earned_premium,n).values]
    est_claim_ratios_arr= ["{:.1%}".format(x/y) for x, y in zip(arr1, arr2)]

    new_df=pd.DataFrame(arr1, columns=['Reported Claims'])
    new_df['Used Up Premium']=arr2
    new_df['Estimated Claim Ratios']=est_claim_ratios_arr
    new_df.index=df.index
    return new_df

#EXPECTED Estimated Claim Ratio
def exp_est_claim_ratio(df,earned_premium,n):
    arr=[float(x[-1].rstrip('%'))/100 for x in est_claim_ratios(df,earned_premium,n).values]
    exp_est_claim_ratio=round(sum(arr)/len(arr),1)
    return exp_est_claim_ratio

#Estimated Expected Claims = Earned Premium * Expected est claim ratio
def est_exp_claims(df,earned_premium,n,est_claim_ratio=0):
    exp_est_claim_ratio_arr= ["{:.1%}".format(exp_est_claim_ratio(df,earned_premium,n))] * 10

    if est_claim_ratio!=None:
        ratio=est_claim_ratio
    else:
        ratio=exp_est_claim_ratio(df,earned_premium,n)

    est_exp_claims_arr=[int(x*ratio) for x in earned_premium]

    new_df=pd.DataFrame(earned_premium, columns=['Earned Premium'])
    new_df['Exp Est Claim Ratio']=exp_est_claim_ratio_arr
    new_df['Estimated Expected Claims']=est_exp_claims_arr
    new_df.index=df.index

    return new_df

#Percentage of Unreported = 1-(1/CDF)
def percent_unreported(df,n=3):
    arr=cumulative_cdf(df,n).values

    pcent_unreported= ["{:.1%}".format(1-(1/x)) for x in arr.flatten()]

    new_df=pd.DataFrame(pcent_unreported, columns=[f'% Unreported'])
    new_df.index=df.index
    return new_df

#Expected Unreported Claims = Est Expected Claims * %age Unreported
def exp_unreported_claims(df,earned_premium,n, est_claim_ratio):
    exp_unreported_claims=[]
    arr1=[float(x[-1].rstrip('%'))/100 for x in percent_unreported(df,n).values]
    arr2=[x[-1] for x in est_exp_claims(df, earned_premium, n, est_claim_ratio).values]

    #Multiplying corresponding elements of 2 arrays
    for x,y in zip(arr1, arr2):
        exp_unreported_claims.append(int(x*y))
    
    new_df=pd.DataFrame(arr2, columns=['Est Expected Claims'])
    new_df['% Unreported']=percent_unreported(df,n).iloc[:,-1:]
    new_df['Expected Unreported Claims (IBNR)']=exp_unreported_claims
    new_df.index=df.index

    return new_df

#Projected Ultimate Claims = Expected Unreported Claims + Reported Claims
def proj_ult_claims(df,earned_premium,n,est_claim_ratio):
    proj_ult_claims=[]
    arr1=latest_diagonal(df).values
    arr2=exp_unreported_claims(df,earned_premium,n,est_claim_ratio).iloc[:,-1:].values

    for x,y in zip(arr1,arr2):
        proj_ult_claims.append(int(x+y))
    
    new_df=pd.DataFrame(arr1, columns=['Reported Claims'])
    new_df['Expected Unreported Claims (IBNR)']=arr2
    new_df['Projected Ultimate Claims']=proj_ult_claims
    new_df.index=df.index

    return new_df

#Case Outstanding = Reported Claims - Paid Claims
def case_outstanding(df,paid_claims_df):
    case_outstanding=[]

    arr1=latest_diagonal(df).values             #Reported Claims
    arr2=latest_diagonal(paid_claims_df).values #Paid Claims

    for x,y in zip(arr1,arr2):
        case_outstanding.append(int(x-y))
    
    new_df=pd.DataFrame(arr1, columns=['Reported Claims'])
    new_df['Paid Claims']=arr2
    new_df['Case Outstanding']=case_outstanding
    new_df.index=df.index

    return new_df

#Total Unpaid Claim Estimate = Case Outstanding + IBNR 
def total_unpaid_claim_est(df,paid_claims_df,earned_premium,n,est_claim_ratio):
    total_unpaid_claim_est=[]
    arr1=case_outstanding(df,paid_claims_df).iloc[:,-1:].values
    arr2=exp_unreported_claims(df,earned_premium,n,est_claim_ratio).iloc[:,-1:].values

    for x,y in zip(arr1,arr2):
        total_unpaid_claim_est.append(int(x+y))
    
    new_df=pd.DataFrame(arr1, columns=['Case Outstanding'])
    new_df['Expected Unreported Claims (IBNR)']=arr2
    new_df['TOTAL Unpaid Claim Estimate']=total_unpaid_claim_est
    new_df.index=df.index

    return new_df

#Returns a df of dev triangle from csv file of 1000s of records
def dev_triangle(df,feature):

    if feature not in df.columns:
        feature=feature.capitalize()

    #Creating a dataframe that displays an empty development triangle
    start=min(df['AccidentYear'])
    end=max(df['AccidentYear'])
    rows,cols=[],[]

    count=1
    for x in range(start,end+1):
        # All the development years available in csv file will be saved in array rows
        # Multiples of 12 saved in array cols
        rows.append(x)
        cols.append(12*count)
        count+=1
    
    # Create an empty dataframe with the specified column and row names
    new_df = pd.DataFrame(columns=cols, index=rows)
    
    # Filling null values
    mask = new_df.isna()
    new_df[mask]=0
    
    no_of_rows=df.shape[0]
    for x in range(no_of_rows):
    #iterating through each row of the original dataframe
        dev_year  = df.loc[x,'DevelopmentYear']
        acc_year  = df.loc[x,'AccidentYear']
        inc_amount= df.loc[x, feature]

        year_diff = dev_year - acc_year

        new_df.loc[acc_year, 12*(year_diff+1)]+=inc_amount

    return new_df

#df=reported_claims_df
def cape_cod_summary(df,paid_claims_df,earned_premium,n=3, est_claim_ratio=0):
    #0 Creating an empty Dataframe
    dfop=pd.DataFrame()

    #1 Row index set as accident years from parent df
    dfop.index=df.index

    #2 Earned Premium
    dfop['Earned Premium']=earned_premium

    #3 Reported Claims
    dfop=dfop.merge(latest_diagonal(df),left_index=True, right_index=True, how='inner') #merge based on index vals

    #4 Reported CDF to Ultimate
    dfop=dfop.merge(cumulative_cdf(df,n),left_index=True, right_index=True, how='inner')

    #5 Percentage of Ult Reported
    dfop=dfop.merge(percent_reported(df,n),left_index=True, right_index=True, how='inner')

    #6 Used Up premium
    used_up_premium_df=used_up_premium(df,earned_premium,n).iloc[:,-1:] #fetch last col of the df
    dfop=dfop.merge(used_up_premium_df,left_index=True, right_index=True, how='inner')

    #7 Estimated Claim Ratios
    est_claim_ratios_df=est_claim_ratios(df,earned_premium,n).iloc[:,-1:] #fetch last col of the df
    dfop=dfop.merge(est_claim_ratios_df,left_index=True, right_index=True, how='inner')
    
    ####    Calculating Expected Estimated Claim Ratio    ####
    #8 Appending Expected Estimated Claim Ratio into df
    if est_claim_ratio!=None:
        x=est_claim_ratio
    else:
        x=exp_est_claim_ratio(df,earned_premium,n,est_claim_ratio)

    exp_est_claim_ratio_arr= ["{:.1%}".format(x)] * 10
    dfop['Expected Claim Ratio']=exp_est_claim_ratio_arr

    #9 Estimated Expected Claims
    est_exp_claims_df=est_exp_claims(df,earned_premium,n,est_claim_ratio).iloc[:,-1:] #fetch last col of the df
    dfop=dfop.merge(est_exp_claims_df,left_index=True, right_index=True, how='inner')

    #10 Percentage of Unreported
    # dfop=dfop.merge(percent_unreported(df,n),left_index=True, right_index=True, how='inner')

    #11 Expected Unreported Claims (IBNR)
    exp_unrep_claims_df=exp_unreported_claims(df,earned_premium,n,est_claim_ratio).iloc[:,-1:] #fetch last col of the df
    dfop=dfop.merge(exp_unrep_claims_df,left_index=True, right_index=True, how='inner')

    #12 Projected Ultimate Claims
    proj_ult_claims_df=proj_ult_claims(df,earned_premium,n,est_claim_ratio).iloc[:,-1:] #fetch last col of the df
    dfop=dfop.merge(proj_ult_claims_df,left_index=True, right_index=True, how='inner')

    #13 Paid Claims
    dfop=dfop.merge(latest_diagonal(paid_claims_df,x='Paid'),left_index=True, right_index=True, how='inner')

    #14 Case Outstanding
    case_outstanding_df=case_outstanding(df,paid_claims_df).iloc[:,-1:] #fetch last col of the df
    dfop=dfop.merge(case_outstanding_df,left_index=True, right_index=True, how='inner')

    #15 Total Unpaid Claim Estimate
    total_unpaid_df=total_unpaid_claim_est(df,paid_claims_df,earned_premium,n,est_claim_ratio).iloc[:,-1:] #fetch last col of the df
    dfop=dfop.merge(total_unpaid_df,left_index=True, right_index=True, how='inner')

    #16 Appending the Total Row
    selected_columns = ['Earned Premium', 'Reported Claims at {}'.format(max(df.index)), 'Used Up Premium',
     'Estimated Expected Claims', 'Expected Unreported Claims (IBNR)', 'Projected Ultimate Claims',
     'Paid Claims at {}'.format(max(df.index)), 'Case Outstanding', 'TOTAL Unpaid Claim Estimate']
    total_values = dfop[selected_columns].sum()
    total_row = pd.DataFrame([total_values.values], columns=total_values.index, index=['Total'])
    dfop = pd.concat([dfop, total_row])
    dfop=dfop.replace(np.nan,'-')

    return dfop
