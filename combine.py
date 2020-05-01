import sys
import pandas as pd
import re


from nltk import skipgrams
from nltk import ngrams
from nltk import everygrams

#import pudb; pu.db
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_colwidth', 18)


#################
# pandas example:
# match either 'Tokyo' or 'Paris'
# result = sr.str.match(pat='(Tokyo)|(Paris)')
# df = df[~df['your column'].isin(['list of strings'])]
# new_data = data[~data[1].isin(['yaxi','wo','and'])]
# yaxi_list = data[1].str.match('yaxi')
# data1 = data.drop([0],axis=0)
# data1.reset_index()
# pd.concat([pd.DataFrame([i], columns=['A']) for i in range(5)],
# df.insert(loc=idx, column='A', value=new_col)
#################


#all the functions

def safe_index(lst_or_strng,pattern):
   my_cnt = lst_or_strng.count(pattern)
   if my_cnt != 0:
      return(lst_or_strng.index(pattern))
   else:
      return("UNKNOWN_VALUE")

def intersect_lsts(lst1,list2):
   answer_list=[]

   size_list2 = len(list2)
   size_lst1 = len(lst1)

   i= 0
   while i < size_lst1 :
      j = 0
      ans_lst_j=[]
      while j < size_list2 :
         cur_index = safe_index(list2[j],lst1[i])
         if cur_index != "UNKNOWN_VALUE":
            ans_lst_j.append([i,cur_index,lst1[i],list2[j][cur_index]]) 
         if cur_index == "UNKNOWN_VALUE":
            ans_lst_j.append([i,"-",lst1[i],"-"]) 
         j += 1
      answer_list.append(ans_lst_j)
      i += 1
   return(answer_list)

def composing_sentence(main_lst):
   comp_s = ""
   i=0
   while i < len(main_lst):
      j=0
      while j < len(main_lst[i]):
            wid = main_lst[i][j][0] + 1
            if main_lst[i][j][0] == main_lst[i][j][1]:
               comp_s=comp_s+str(wid)+"%"+str(main_lst[i][j][2]) + " "
            if  main_lst[i][j][1] != "-":
               if main_lst[i][j][0] < main_lst[i][j][1]: comp_s=comp_s+"["+ str(j+1) + "%" + main_lst[i][j][2] +"]" + " "
            if main_lst[i][j][1] == "-":
               comp_s=comp_s+"<<"+str(wid)+"%"+str(main_lst[i][j][2]) +">>"+ " "
            if  main_lst[i][j][1] != "-":
               if main_lst[i][j][0] > main_lst[i][j][1]: comp_s=comp_s+"{"+ str(j+1) + "%" + main_lst[i][j][2] +"}" + " "
            j += 1
      comp_s = comp_s + " rAma "
      i += 1
   return(comp_s)

#rev comparison for getting the new words not present in ref sent
def rev_composing_sentence(main_lst):
   comp_s = ""
   i=0
   while i < len(main_lst):
      j=0
      while j < len(main_lst[i]):
            wid = main_lst[i][j][0] + 1
            if main_lst[i][j][0] == main_lst[i][j][1]:
               comp_s=comp_s+str(wid)+"%"+str(main_lst[i][j][2]) + " "
            if  main_lst[i][j][1] != "-":
               if main_lst[i][j][0] < main_lst[i][j][1]: comp_s=comp_s+"["+ str(j+1) + "%" + main_lst[i][j][2] +"]" + " "
            if main_lst[i][j][1] == "-":
               comp_s=comp_s+'<<'+str(wid)+"%"+str(main_lst[i][j][2])+'>>' + " "
            if  main_lst[i][j][1] != "-":
               if main_lst[i][j][0] > main_lst[i][j][1]: comp_s=comp_s+"{"+ str(j+1) + "%" + main_lst[i][j][2] +"}" + " "
            j += 1
      comp_s = comp_s + " rAma "
      i += 1
   return(comp_s)


file = open(sys.argv[1], 'r', encoding='utf-8', errors='ignore')
#file = open('sens/0009', 'r', encoding='utf-8', errors='ignore')
Lines1 = file.readlines()

i = 0
for l in Lines1:
    if('NMT:' in l):
        print(i,l)
        i += 1
    else:
        print(l)

Lines = []
for l in Lines1:
    if('NMT:' in l):
        l1 = l.split('NMT: ')[1].strip()
        Lines.append(l1)
    if('ENG: ' in l):
        eng_sen = l



my_list = []
for line in Lines:
   l=line.strip()
   my_list.append(l.split(sep=' ',maxsplit=-1))
   #print(l.split(sep='\t',maxsplit=-1))

no_nmt_op = len(Lines)


i = 0
for l in Lines:
    if(i == 0):
        sen_df = pd.DataFrame([l.split()])
    else:
        tmp_df = pd.DataFrame([l.split()])
        sen_df = sen_df.append(tmp_df)
    i += 1

total_egram = []
for i, sen in sen_df.fillna('NOWORD').iterrows():
    lsen = list(sen)
    l_egram = list(everygrams(lsen))
    for gm in everygrams(lsen):
        total_egram.append(list(gm))
        #print(list(gm))

#print(sen_df)

total_egram_dic = {}
for l in total_egram:
    if(len(l) == 1):
        k = l[0]
    else:
        k = '_'.join(l)
    if k in total_egram_dic:
        total_egram_dic[k] = total_egram_dic[k] + 1
    else:
        total_egram_dic[k] = 1



total_egram_dic_sorted = {k: v for k, v in sorted(total_egram_dic.items(), key=lambda item: item[1])}

i = 0
for k in total_egram_dic_sorted:
    freq = total_egram_dic_sorted[k]
    size = len(k.split('_'))
    data = [k,size,freq]
    if(i == 0):
        tmp_df = pd.DataFrame([data])
        egram_df = pd.DataFrame([0,1,2])
        egram_df = egram_df.append(tmp_df)
    else:
        tmp_df = pd.DataFrame([data])
        egram_df = egram_df.append(tmp_df)
    i += 1


egram_df_soted = egram_df.sort_values(2,1)

total_wds = []
total_grp_wds = []
for i in range(egram_df_soted.shape[0],0,-1):
    row_info = egram_df_soted.iloc[i-1].to_list()
    wds = str(row_info[0]).split('_')
    flag_not_pres = 0
    if('NOWORD' not in wds):
        for wd in wds:
            if (wd not in total_wds):
                total_wds.append(wd)
                flag_not_pres = 1
                wd_flg = wd
        if flag_not_pres:
            total_grp_wds.append(row_info)



for i, sen in sen_df.fillna('NOWORD').iterrows():
    lsen = list(sen)
    break
filled_sen = [0] * len(lsen)

for wds in total_grp_wds:
    if(type(wds[0]) == str):
        wds_split = wds[0].split('_')
        freq = wds[2]
        for wd in lsen:
            if wd in wds_split:
                for w in wds_split:
                    k = 0
                    for i, sen in sen_df.fillna('NOWORD').iterrows():
                        lsen = list(sen)
                        for j in range(0,len(lsen)):
                            if(w == lsen[j]):
                                if(filled_sen[j] == 0):
                                    filled_sen[j] = w+'_'+str(k)
                                else:
                                    tmp_wd = []
                                    full_wd = filled_sen[j].split('/')
                                    for w1 in full_wd:
                                        tmp_wd.append(w1.split('_')[0])
                                    if(w in tmp_wd):
                                        for w1 in full_wd:
                                            if w == w1.split('_')[0]:
                                                nmt_ns = w1.split('_')[1].split('+')
                                                if str(k) not in nmt_ns:
                                                    tmp_new_wd = w1+'+'+str(k)
                                                    tmp_id = full_wd.index(w1)
                                                    full_wd[tmp_id] = tmp_new_wd
                                                    filled_sen[j] = '/'.join(full_wd)
                                    else:
                                        filled_sen[j] = filled_sen[j]+'/'+w+'_'+str(k)
                        k += 1
                break


print(' '.join(filled_sen))
exit(0)

'''
for i, sen in sen_df.fillna('NOWORD').iterrows():
    lsen = list(sen)
    i = 0
    freq_sen = [0] * len(lsen)
    added_wd = []
    for wd in lsen:
        if(wd not in added_wd):
            for wds in total_grp_wds:
                wds_split =   wds[0].split('_')
                if wd in  wds_split:
                    freq_sen[i] = wds
                    i += 1
                    for x in wds_split:
                        added_wd.append(x)
                    break


'''


'''
#for printing all the sent as it is
for i in my_list:
   print(i)
'''

#nice_print = [print(x) for x in lst]

lst1 = my_list[0]
list2 = my_list[1:]
size_lst1 = len(lst1)
size_list2 = len(list2)

lst3 = intersect_lsts(lst1,list2)

j=0
r_lst=[]
while j < size_list2:
   #print(j)
   i=0
   while i < size_lst1: 
      r_lst.append(lst3[i][j])
      i += 1
   j += 1

main_lst=[]
j=0
while j < size_list2:
   main_lst.append(r_lst[j*size_lst1:(j+1)*size_lst1])
   j += 1

lst = main_lst

#print(composing_sentence(main_lst))
comp_s = (composing_sentence(main_lst))

#program by sriram

# calculate the reverse comparison  ( current sent to ref sent)

rev_main_list = []
k = 0
for i in list2:
   lst4 = intersect_lsts(i, [lst1])
   rev_main_list.append(lst4)
   k += 1

#to properly format the rev_main_list
n_rev_main_list = []
i = 0
j = 0
while i < len(rev_main_list):
    tmp_sent = []
    j = 0
    while j < len(rev_main_list[i]):
      tmp_sent.append(rev_main_list[i][j][0])
      j += 1
    n_rev_main_list.append(tmp_sent)
    i += 1


#print(rev_composing_sentence(n_rev_main_list))


rev_comp_s = (rev_composing_sentence(n_rev_main_list))

#print('---')
'''
for sen,sen_rev in zip(comp_s.split('rAma'), rev_comp_s.split('rAma')):
    print(sen, sen_rev)
'''

sen = comp_s.split('rAma')[0]
sen_rev = rev_comp_s.split('rAma')[0]
length = len(comp_s.split('rAma')[0].split())
length_rev = len(rev_comp_s.split('rAma')[0].split())
l = list(range(length))
l_rev = list(range(length_rev))
all_sen = pd.DataFrame([sen.split()], columns=l)
all_sen_rev = pd.DataFrame([sen_rev.split()], columns=l_rev)


for sen,sen_rev in zip(comp_s.split('rAma'), rev_comp_s.split('rAma')):
    if(len(sen.strip()) != 0):
        tmp_all_sen = pd.DataFrame([sen.split()])
        all_sen = all_sen.append(tmp_all_sen)

        tmp_all_sen_rev = pd.DataFrame([sen_rev.split()])
        all_sen_rev = all_sen_rev.append(tmp_all_sen_rev)


'''
print(all_sen)
print(all_sen_rev)
'''

combined_sen = []
for i in range(0,len(all_sen.columns)):
    words = list(set(all_sen[i].to_list()))
    if(len(words) == 1):
        combined_sen.append(words[0])
    else:
        uw_list = []
        other_uw_list = []
        for w in words:
            if(type(w) == str):
                if re.match('^<<',w) is not None:
                    uw = w.strip('<>[]{}').split('%')[1]
                    if uw not in uw_list:
                            uw_list.append(uw)
                elif re.match('^\[', w) is not None:
                    uw = w.strip('<>[]{}').split('%')[1]
                    if uw not in other_uw_list:
                        other_uw_list.append(uw)
                else:
                    uw = w.strip('<>[]{}').split('%')[1]
                    if uw not in uw_list and uw not in other_uw_list:
                            uw_list.append(uw)

        combined_sen.append([uw_list,other_uw_list])


combined_sen_rev = []
for i in range(0,len(all_sen_rev.columns)):
    words = list(set(all_sen_rev[i].to_list()))
    if(len(words) == 1):
        combined_sen_rev.append(words[0])
    else:
        uw_list = []
        other_uw_list = []
        for w in words:
            if(type(w) == str):
                if re.match('^<<',w) is not None:
                    uw = w.strip('<>[]{}').split('%')[1]
                    if uw not in uw_list:
                            uw_list.append(uw)
                elif re.match('^\[', w) is not None:
                    uw = w.strip('<>[]{}').split('%')[1]
                    if uw not in other_uw_list:
                        other_uw_list.append(uw)
                else:
                    uw = w.strip('<>[]{}').split('%')[1]
                    if uw not in uw_list and uw not in other_uw_list:
                            uw_list.append(uw)

        combined_sen_rev.append([uw_list,other_uw_list])


'''
print(combined_sen)
print(combined_sen_rev)
'''
final_sen = []
for wd, wd_rev in zip(combined_sen, combined_sen_rev):
    alt_wd = []
    no_alt_wd = []
    if(type(wd[0]) == list):
        for w in wd[0]:
            if w not in alt_wd:
                alt_wd.append(w)
        if(type(wd_rev[0] == list)):
            for w in wd_rev[0]:
                if w not in alt_wd:
                    alt_wd.append(w)
        else:
            w = wd_rev.split('%')[1]
            alt_wd.append(w)

        for w in wd[1]:
            if w not in alt_wd and w not in no_alt_wd:
                no_alt_wd.append(w)
        if (type(wd_rev[1] == list)):
            for w in wd_rev[1]:
                if w not in alt_wd and w not in no_alt_wd:
                        no_alt_wd.append(w)
        else:
            w = wd_rev.split('%')[1]
            no_alt_wd.append(w)

        #print(alt_wd, '|', no_alt_wd)
        final_sen.append([alt_wd,no_alt_wd])
    else:
        #print(wd,'|',wd_rev)
        final_sen.append(wd)
'''
print(sen_df)
print(final_sen)
'''
i = 0
for wd in final_sen:
    if(type(wd) == str):
        wd1 = wd.split('%')[1]
        #add to the data frame
        if(i ==0):
            final_sen_df = pd.DataFrame([wd1], columns=[i])
            i += 1
        else:
            final_sen_df.insert(loc=i, column=i, value=wd1)
            i += 1
    else:
        for w in wd:
            for w1 in w:
                if (i == 0):
                    final_sen_df = pd.DataFrame([w1], columns=[i])
                    i += 1
                else:
                    final_sen_df.insert(loc=i, column=i, value=w1)
                    i += 1


#print(final_sen_df)
for i in range(1,no_nmt_op+1):
    final_sen_df.loc[i] = '0'


row1 = 0
for i,wd in final_sen_df.iterrows():
    sen_row = 1
    wd_no = 0
    col1 = 0
    for wd1 in wd:
        row2 = 0
        for j, wd2 in sen_df.iterrows():
            for w in wd2:
                if(wd1 == w):
                    #print(i,j,row1,row2)
                    final_sen_df.loc[final_sen_df.index[row2+1],col1] = 1
            row2 +=1
        col1 += 1
    row1 += 1


final_sen_df.to_csv(sys.argv[2], sep='\t', header=False, index=False)

#################
# pandas example:
# match either 'Tokyo' or 'Paris'
# result = sr.str.match(pat='(Tokyo)|(Paris)')
# df = df[~df['your column'].isin(['list of strings'])]
# new_data = data[~data[1].isin(['yaxi','wo','and'])]
# yaxi_list = data[1].str.match('yaxi')
# data1 = data.drop([0],axis=0)
# data1.reset_index()
# pd.concat([pd.DataFrame([i], columns=['A']) for i in range(5)],
# df.insert(loc=idx, column='A', value=new_col)
#################






'''
for sen,sen_rev in zip(comp_s.split('rAma'), rev_comp_s.split('rAma')):
    for wd, wd_rev in zip(sen.split(), sen_rev.split()):
        id = wd.split('%')[0]
        word = wd.split('%')[1]

        id_rev = wd_rev.split('%')[0]
        word_rev = wd_rev.split('%')[1]

        if(id == id_rev) and (word == word_rev):
            print(id+'%'+word)
        else:
            print(word+'/'+word_rev)
    print('-------')



'''







#################
# Mix the ref-test and test-ref o/p together

#Are we looking at the thought process or reasoning ability of the system?
#First:
#kyA hama [praNAli/waMwra/sistam/] [kI](x) [vEcArika/soca/vicAra] [kI](1-x)
# prakriyA yA warka/safkewa/reasoning kRamawA/yogyawA kI_ora/ko xeKa rahe hEM?

#Second:
#eka xqRtikona/mawa/vicAra/xqSya [yaha] hE ki kqwrima buxXi/buxXimawwA
# [Ese/una] dijAiniMga/praNAliyoM kI rupareKA/dijAina [karane] ke bAre meM
# hE [jo] mAnava/mnuRyoM/manuRya ki_waraha/ke_rUpa_meM [hI] buxXimAna hEM


#['kyA', 'hama', 'waMwra', 'kI', 'vicAra', 'prakriyA', 'yA', 'warka', 'kRamawA', 'ko', 'xeKa', 'rahe', 'hEM', '?']
#['kyA', 'hama', 'sistama', 'kI', 'vicAra', 'prakriyA', 'yA', 'warka', 'kRamawA', 'ko', 'xeKa', 'rahe', 'hEM', '?']
#['kyA', 'hama', 'vicAra', 'prakriyA', 'yA', 'waMwra', 'kI', 'warka', 'kRamawA', 'ko', 'xeKa', 'rahe', 'hEM', '?']
#['kyA', 'hama', 'vicAra', 'prakriyA', 'yA', 'praNAlI', 'kI', 'warka', 'kRamawA', 'ko', 'xeKawe', 'hEM', '?']
#['kyA', 'hama', 'praNAlI', 'kI', 'vicAra', 'prakriyA', 'yA', 'warka', 'kRamawA', 'ko', 'xeKa', 'rahe', 'hEM', '?']
#1%kyA 2%hama <<3%waMwra>> 4%kI 5%vicAra 6%prakriyA 7%yA 8%warka 9%kRamawA 10%ko 11%xeKa 12%rahe 13%hEM 14%?  rAma 1%kyA 2%hama [3% waMwra] [4% kI] {5% vicAra} {6% prakriyA} {7% yA} 8%warka 9%kRamawA 10%ko 11%xeKa 12%rahe 13%hEM 14%?  rAma 1%kyA 2%hama <<3%waMwra>> [4% kI] {5% vicAra} {6% prakriyA} {7% yA} 8%warka 9%kRamawA 10%ko <<11%xeKa>> <<12%rahe>> {13% hEM} {14% ?}  rAma 1%kyA 2%hama <<3%waMwra>> 4%kI 5%vicAra 6%prakriyA 7%yA 8%warka 9%kRamawA 10%ko 11%xeKa 12%rahe 13%hEM 14%?  rAma 

#1%kyA 2%hama <<3%sistama>> 4%kI 5%vicAra 6%prakriyA 7%yA 8%warka 9%kRamawA 10%ko 11%xeKa 12%rahe 13%hEM 14%?  rAma 1%kyA 2%hama [3% vicAra] [4% prakriyA] [5% yA] {6% waMwra} {7% kI} 8%warka 9%kRamawA 10%ko 11%xeKa 12%rahe 13%hEM 14%?  rAma 1%kyA 2%hama [3% vicAra] [4% prakriyA] [5% yA] <<6%praNAlI>> {7% kI} 8%warka 9%kRamawA 10%ko <<11%xeKawe>> [12% hEM] [13% ?]  rAma 1%kyA 2%hama <<3%praNAlI>> 4%kI 5%vicAra 6%prakriyA 7%yA 8%warka 9%kRamawA 10%ko 11%xeKa 12%rahe 13%hEM 14%?  rAma

##################

#compare with all the sens incrementally





