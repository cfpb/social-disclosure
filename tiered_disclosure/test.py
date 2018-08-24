import pandas as pd
filename = "justvals.csv"
data = pd.read_csv(filename, quotechar='"', skipinitialspace=True).to_dict()
print(data['productdimvals'])
print(data['productdimvals'][0])

filename = "justvals.csv"
data = pd.read_csv(filename, quotechar='"', skipinitialspace=True).to_dict()
products = data['productdimvals']
num_rounds = 16
current_round = 1
round_index = current_round - 1
current_product = 1
product_index = current_product - 1
product_dims = [data['productdimvals'][i].replace('[','').replace(']','').split(';') for i in range(num_rounds - 1)]
products_list = product_dims[round_index]
product = product_dims[round_index][product_index].split(',')

print(product_dims)
print(product_dims[round_index])
print(products_list)

    # import pandas as pd
    # filename = "justvals.csv"
    # data = pd.read_csv(filename, quotechar='"', skipinitialspace=True).to_dict()
    # print(data['productdimvals'])
    # print(data['productdimvals'][0])

    # filename = "justvals.csv"
    # data = pd.read_csv(filename, quotechar='"', skipinitialspace=True).to_dict()
    # products = data['productdimvals']
    # for i in range(10):
    # 	["productdims_round" + str(i)] = data['productdimvals'][i].replace('[','').replace(']','').split(';')
    # product_dims = products
    
    # print(product_dims)
