#Created by:
#Devi Fatmawati, Iyas Yustira

import pandas as pd
import numpy as np


def check(data):
    sum_a = data['Supply'].sum()
    sum_b = data.loc['Demand'].sum()
    if sum_a == sum_b: 
        print('Balanced data = {:d}'.format(sum_a))
        pass
    elif sum_a < sum_b:
        print('Unbalanced data: total supply < total demand ({:d} < {:d})'.format(sum_a, sum_b))
        data_T = data.transpose()
        dm = data_T.pop('Demand')
        data_T['Dum'] = np.zeros(len(dm))
        data_T['Demand'] = dm
        data = data_T.transpose()
        data.loc['Dum', 'Supply'] = sum_b - sum_a
    elif sum_a > sum_b:
        print('Unbalanced data: total supply > total demand ({:d} > {:d})'.format(sum_a, sum_b))
        Supply = data.pop('Supply').reset_index()
        data['Dum'] = np.zeros(len(data.index))
        data['Supply'] = Supply.Supply.to_numpy()
        data.loc['Demand', 'Dum'] = sum_a - sum_b
    else:
        print('Error in checking total demand and supply')
    return data

def transform(data):
    data['Penalty'] = np.zeros(data.shape[0])
    data.loc['Penalty'] = np.zeros(data.shape[1])
    m = data.index[:-2]
    n = data.columns[:-2]
    for i in m:
        xi_min = TP.loc[i][:-1].min()
        for j in n:
            xj_min = TP[j][:-1].min()
            T = TP.loc[i, j] - xi_min
            B = TP.loc[i, j] - xj_min
            mean_xij = np.array([T, B]).mean()
            data.loc[i, j] = mean_xij
    return data

def penalty(data, m, n):
    for i in m:
        xj = data.loc[i][:-2].sort_values().unique()
        if len(xj) == 1:
            ai = xj[0]
        else:
            ai = xj[1] - xj[0]
        data.loc[i, 'Penalty'] = ai
        
    for j in n:
        xi = data[j][:-2].sort_values().unique()
        if len(xi) == 1:
            bi = xi[0]
        else:
            bi = xi[1] - xi[0]
        data.loc['Penalty', j] = bi
    
    if len(m) <= 2 or len(n) <= 2:
        max_a = data['Penalty'][:-2].max()
        max_b = data.loc['Penalty'][:-2].max()

        m = data['Penalty'][:-2][data['Penalty'][:-2] == max_a].index
        n = data.loc['Penalty'][:-2][data.loc['Penalty'][:-2] == max_b].index
        
        if max_a == max_b:
            for i in m:
                xj = data.loc[i][:-2].sort_values().unique()
                data.loc[i, 'Penalty'] =  xj.max()
            for j in n:
                xi = data[j][:-2].sort_values().unique()
                data.loc['Penalty', j] = xi.max()        
        elif max_a > max_b:
            if len(m) > 1:
                for i in m:
                    xj = data.loc[i][:-2].sort_values().unique()
                    data.loc[i, 'Penalty'] =  xj.max()
            else:
                pass
        else:
            if len(n) > 1:
                for j in n:
                    xi = data[j][:-2].sort_values().unique()
                    data.loc['Penalty', j] = xi.max()
            else:
                pass
    else:
        max_a = data['Penalty'][:-2].max()
        max_b = data.loc['Penalty'][:-2].max()

        m = data['Penalty'][:-2][data['Penalty'][:-2] == max_a].index
        n = data.loc['Penalty'][:-2][data.loc['Penalty'][:-2] == max_b].index
        
        if max_a == max_b:
            for i in m:
                xj = data.loc[i][:-2].sort_values().unique()
                data.loc[i, 'Penalty'] =  xj[2]-xj[1]
            for j in n:
                xi = data[j][:-2].sort_values().unique()
                data.loc['Penalty', j] = xi[2]-xi[1]        
        elif max_a > max_b:
            if len(m) > 1:
                for i in m:
                    xj = data.loc[i][:-2].sort_values().unique()
                    data.loc[i, 'Penalty'] =  xj[2]-xj[1]
            else:
                pass
        else:
            if len(n) > 1:
                for j in n:
                    xi = data[j][:-2].sort_values().unique()
                    data.loc['Penalty', j] = xi[2]-xi[1]
            else:
                pass
    
    return data

def idx_aloc(data):
    max_a = data['Penalty'][:-2].max()
    max_b = data.loc['Penalty'][:-2].max()

    if max_a > max_b:
        Xi = data['Penalty'][:-2][data['Penalty'][:-2] == max_a].index[0]
        Xj = data.loc[Xi][:-2][data.loc[Xi][:-2] == data.loc[Xi][:-2].min()].index[0]
    else:
        Xj = data.loc['Penalty'][:-2][data.loc['Penalty'][:-2] == max_b].index[0]
        Xi = data[Xj][:-2][data[Xj][:-2] == data[Xj][:-2].min()].index[0]
    print('Alocation to {:s} and {:s}'.format(Xi, Xj))
    return Xi, Xj

def cost_aloc(data, Xi, Xj):
    ai = data.loc[Xi, 'Supply'] 
    bi = data.loc['Demand', Xj]
    if ai > bi:
        val = TP.loc[Xi, Xj]*bi
        data.loc[Xi, 'Supply'] = data.loc[Xi, 'Supply'] - bi
        data.drop(Xj, axis=1, inplace=True)
    else:
        val = TP.loc[Xi, Xj]*ai
        data.loc['Demand', Xj] = data.loc['Demand', Xj] - ai
        data.drop(Xi, axis=0, inplace=True)
    cost.append(val)
    print('Cost:', val)
    return data

fn = input('Enter file name:')
TP = pd.read_excel('Data/' + fn + '.xlsx')
TP.set_index('Index', inplace=True)
print('\n', TP, '\n')

cost = []
data = TP.copy()
data = check(data)
TP = data.copy()
data = transform(data)
i = 0
while True:
    i+=1
    print('\nIteration', i)
    m = data.index[:-2]
    n = data.columns[:-2]
    data = penalty(data, m, n)
    if len(m) == 1 and len(n) == 1:
        Xi, Xj = data.index[0], data.columns[0]
        val = TP.loc[Xi, Xj]*data.loc['Demand', Xj]
        cost.append(val)
        print('Alocation to {:s} and {:s}'.format(Xi, Xj))
        print('Cost:', val)
        break
    else:
        Xi, Xj = idx_aloc(data)
        data = cost_aloc(data, Xi, Xj)

total_cost = np.array(cost).sum()
print('\nTotal cost:', total_cost)

