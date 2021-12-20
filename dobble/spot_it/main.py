import numpy as np
import pandas as pd

order = 11
n = order
num_of_cards = n*n + n + 1
num_of_symbols = n*n + n + 1

Matrix = np.zeros((num_of_cards,num_of_symbols),dtype=int)

cards = [ ]
card = [ ]

# first card
for i in range(1,n+2) :
    card.append(i)
    Matrix[0][i-1] = 1
cards.append(card)

# next n cards
for i in range(1,n+1) :
    card = [ ]
    card.append(1)
    Matrix[i][0] = 1

    for k in range(1,n+1):
        card.append(n*i + k+1)
        Matrix[i][n*i + k] = 1

# next n*n cards
for i in range(1,n+1) :
      for j in range (1,n+1) :
            card = []
            card.append(i+1)
            Matrix[n*i + j ][i] = 1
            for k in range(1,n+1) :
                card.append(n+2+n*(k-1)+(((i-1)*(k-1)+j-1) % n))
                Matrix[n*i + j][n+1+n*(k-1)+(((i-1)*(k-1)+j-1) % n)] = 1
            cards.append(card)

for i,card in enumerate(cards):
    print("card",i,card)
cols=[]
rows=[]
for i in range(1,num_of_cards+1):
    cols.append("P_{}".format(i))
    rows.append("L_{}".format(i))

df = pd.DataFrame(Matrix,columns=cols,index=rows)
print(df)



      

