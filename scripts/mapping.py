import scipy.sparse as sc

with open("Oregon.txt", 'r') as f:
    encoded_data = f.read()
new_data = [i.strip().split(" ") for i in encoded_data.split('\n') if i != ""]

rows = [int(i[1]) for i in new_data[1:] if len(i) == 4]
cols = [int(i[2]) for i in new_data[1:] if len(i) == 4]
data = [int(i[3]) for i in new_data[1:] if len(i) == 4]
length = max(max(rows), max(cols))
#col  = [1,1,2,3,4,42,1]
#row = [ 2,2,423,12,34,123,5]
#data = [10,30,20,12,31,50,1]

matrix = sc.csr_matrix((data, (rows,cols)),shape = (length+1, length+1))
print(matrix[1,3])

indexorder = sc.csgraph.reverse_cuthill_mckee(matrix)
print(len(indexorder))