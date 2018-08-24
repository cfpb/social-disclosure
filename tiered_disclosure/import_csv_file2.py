import csv


filename = "test.csv"

fields = []
rows = []

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)



    # extracting each data row one by one
    # for row in csvreader:
    #     rows.append(row)

    reader = csv.DictReader(csvfile, fieldnames=fields) #new
    for row in reader:
        print(row['productdims_shown'],row['productdimvals'],row['round_num'])
    # extracting field names through first row
    # get total number of rows
    # print("Total no. of rows: %d"%(csvreader.line_num))

# printing the field names
print('Field names are:' + ', '.join(field for field in fields))

#  printing rows
for row in rows:
    # parsing each column of a row
    for col in row:
        print("%10s"%col),
    print('\n')

# rawvals = [0]*numdims
# for i in range(numdims):
#     val = -1
#     val = rows[i]
#     rawvals[i] = val

# dvalues = copy.copy(rawvals)
# print('dvalues is', dvalues)