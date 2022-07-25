#Created by:
#Iyas Yustira, Devi Fatmawati

import numpy as np
import pandas as pd

def is_balanced(data):
    sum_a = data['Supply'].sum()
    sum_b = data.loc['Demand'].sum()
    if sum_a == sum_b: 
        print('Balanced data: {:d}'.format(sum_a))
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
    dat_trans = data.copy()
    dat_trans['Penalty'] = np.zeros(dat_trans.shape[0])
    dat_trans.loc['Penalty'] = np.zeros(dat_trans.shape[1])
    m = dat_trans.index[:-2]
    n = dat_trans.columns[:-2]
    for i in m:
        min_xj = data.loc[i][:-1].min()
        for j in n:
            min_xi = data[j][:-1].min()
            top_val = data.loc[i, j] - min_xj
            bot_val = data.loc[i, j] - min_xi
            dat_trans.loc[i, j] = abs(top_val - bot_val)
    return dat_trans

def penalty(dat_trans):
    m = dat_trans.index[:-2]
    n = dat_trans.columns[:-2]
    # row penalty
    for i in m:
        dat_trans.loc[i, 'Penalty'] = np.round(dat_trans.loc[i][:-2].mean(), 2)
    # column penalty
    for j in n:
        dat_trans.loc['Penalty', j] = np.round(dat_trans[j][:-2].mean(), 2)
    return dat_trans

def init_cell(dat_trans):
    pr_max = dat_trans['Penalty'][:-2].max()
    pc_max = dat_trans.loc['Penalty'][:-2].max()
    m = dat_trans['Penalty'][:-2][dat_trans['Penalty'][:-2] == pr_max].index
    n = dat_trans.loc['Penalty'][:-2][dat_trans.loc['Penalty'][:-2] == pc_max].index
    glc = {}
    if pr_max == pc_max:
        for i in m:
            glc[dat_trans.loc[i, 'Supply']] = i
        for j in n:
            glc[data.loc['Demand', j]] = j
        rc = glc[max(glc)]
    elif pr_max > pc_max:
        if len(m) > 1:
            for i in m:
                glc[dat_trans.loc[i, 'Supply']] = i
            rc = glc[max(glc)]
        else:
            rc = dat_trans['Penalty'][:-2][dat_trans['Penalty'][:-2] == pr_max].index[0]
    else:
        if len(n) > 1:
            for j in n:
                glc[data.loc['Demand', j]] = j
            rc = glc[max(glc)]    
        else:
            rc = dat_trans.loc['Penalty'][:-2][dat_trans.loc['Penalty'][:-2] == pc_max].index[0]
    return rc

def cell_allocation(data, rc, m, n):
    glc = {}
    if rc in m:
        df_c = pd.DataFrame(data.loc[[rc, 'Demand']])
        xj_min = df_c.loc[rc][:-1].min()
        n = df_c.loc[rc][:-1][df_c.loc[rc][:-1] == xj_min].index
        if len(n) > 1:
            for j in n:
                glc[df_c.loc['Demand', j]] = j
            ri = rc
            cj = glc[max(glc)]
        else:
            cj = n[0]
            ri = rc
        
    else:
        df_r = pd.DataFrame(data[[rc, 'Supply']])
        xi_min = df_r[rc][:-1].min()
        m = df_r[rc][:-1][df_r[rc][:-1] == xi_min].index
        if len(m) > 1:
            for i in m:
                glc[df_r.loc[i, 'Supply']] = i
            cj = rc
            ri = glc[max(glc)]
        else:
            ri = m[0]
            cj = rc
       
    print('Allocation to {:s} and {:s}'.format(ri, cj))
    return ri, cj

def cost_allocation(data, ri, cj, k):
    ai = data.loc[ri, 'Supply']
    bi = data.loc['Demand', cj]
    if ai == bi:
        cost_val = ai * data.loc[ri, cj]
        cost.append(cost_val)
        print('Cost: {:0.1f}'.format(cost_val), '\n')
        k = 2 + k
        print('-'*16)
        print(' Iteration: ', k)
        print('-'*16, '\n')
        print(data, '\n')
        df_r = data.loc[[ri, 'Demand']].copy()
        df_c = data[[cj, 'Supply']].copy()
        data.drop(ri, axis=0, inplace=True)
        data.drop(cj, axis=1, inplace=True)
        df_r.drop(cj, axis=1, inplace=True)
        df_c.drop(ri, axis=0, inplace=True)
        df_r_min = df_r.loc[ri][:-1].min()
        df_c_min = df_c[cj][:-1].min()
        n = df_r.loc[ri][:-1][df_r.loc[ri][:-1] == df_r_min].index
        m = df_c[cj][:-1][df_c[cj][:-1] == df_c_min].index
        glc_r = {}
        glc_c = {}
        df_r_min = df_r.loc[ri][:-1].min()
        df_c_min = df_c[cj][:-1].min()        
        if df_r_min > df_c_min:
            if len(n) > 1:
                for j in n:
                    glc_c[df_r.loc['Demand', j]] = j
            else:
                for j in n:
                    glc_c[df_r[j][:-1].values[0]] = j
                    
            if len(m) > 1:
                for i in m:
                    glc_r[df_c.loc[i, 'Supply']] = i
            else:
                for i in m:
                    glc_r[df_c.loc[i][:-1].values[0]] = i
        else:
            if len(m) > 1:
                for i in m:
                    glc_r[df_c.loc[i, 'Supply']] = i
            else:
                for i in m:
                    glc_r[df_c.loc[i].values[0]] = i
                    
            if len(n) > 1:
                for j in n:
                    glc_c[df_r.loc['Demand', j]] = j
            else:
                for j in n:
                    glc_c[df_r[j].values[0]] = j
            
        if max(glc_r) > max(glc_c):
            cj = glc_c[max(glc_c)]
            rc.append(cj)
            rc.append(cj)
            print('Allocation to {:s} and {:s}'.format(ri, cj))
            cost_val = df_r.loc[ri, cj] * 0
            cost.append(cost_val)
            print('Cost: {:0.1f}'.format(cost_val))
        else:
            ri = glc_r[max(glc_r)]
            rc.append(ri)
            rc.append(ri)
            print('Allocation to {:s} and {:s}'.format(ri, cj))
            cost_val = df_c.loc[ri, cj] * 0
            cost.append(cost_val)
            print('Cost: {:0.1f}'.format(cost_val))
        k = k - 1
    elif ai > bi:
        cost_val = bi * data.loc[ri, cj]
        cost.append(cost_val)
        data.loc[ri, 'Supply'] = ai - bi
        data.drop(cj, axis=1, inplace=True)
        rc.append(ri)
        print('Cost: {:0.1f}'.format(cost_val))
    else:
        cost_val = ai * data.loc[ri, cj]
        cost.append(cost_val)
        data.loc['Demand', cj] = bi - ai
        data.drop(ri, axis=0, inplace=True)
        rc.append(cj)
        print('Cost: {:0.1f}'.format(cost_val))
    return data, k

print()
fn = input('Enter file name:')
data = pd.read_excel('Data/' + fn + '.xlsx')
data.set_index('Index', inplace=True)
print()
print(data, '\n')
data = is_balanced(data)
print()
dat_trans = transform(data)
dat_trans = penalty(dat_trans)
print(dat_trans, '\n')
rc = []
rc.append(init_cell(dat_trans))
k = 0
cost = []
while True:
#for z in range(10):
    print('-'*16)
    print(' Iteration: ', k+1)
    print('-'*16, '\n')
    print(data, '\n')
    m = data.index[:-1]
    n = data.columns[:-1]
    if len(m) == 1 and len(n) == 1:
        ri, cj = cell_allocation(data, rc[k], m, n)
        ai = data.loc[ri, 'Supply']
        cost_val = ai * data.loc[ri, cj]
        cost.append(cost_val)
        print('Cost: {:0.1f}'.format(cost_val), '\n')
        break
    else:
        ri, cj = cell_allocation(data, rc[k], m, n)
        data, k = cost_allocation(data, ri, cj, k)
        k += 1
    print()
print('-'*21)
print('  Total Cost: {:0.0f}'.format(sum(cost)))
print('-'*21, '\n')
