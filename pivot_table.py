#!/usr/bin/env python

def zero_fill(result, keys):
    # base case, 1 set of keys
    if (1 == len(keys)):
        for key_value in keys[0]:
            if key_value not in result:
                result[key_value] = 0
        return
    
    for key_value in keys[0]:
        if key_value not in result:
            result[key_value] = {}
        zero_fill(result[key_value], keys[1:])

def pivotSum(oldSum, value):
    return oldSum + value
    
def aggregate_value(result, keys, value, aggregator): 
    result_walker = result
    for key in keys[:-1]:
        if key not in result_walker:
            result_walker[key] = {}
        result_walker = result_walker[key]
        
    if keys[-1] not in result_walker:
        result_walker[keys[-1]] = value
    else:
        result_walker[keys[-1]] = aggregator(result_walker[keys[-1]], value)

    
def create_sort_function(item_sorts, column_items):
    sort_functions = []
    for item in column_items:
        if item in item_sorts:
            sort_functions.append(item_sorts[item])
        else:
            sort_functions.append(lambda x: x)
           
    def functor(value_tuple): 
        result = []
        for idx, value in enumerate(value_tuple):
            result.append(sort_functions[idx](value))
        return tuple(result)
    
    return functor 
    
class PivotTable:     
    def __init__(self, data, data_columns, row_items, 
                 column_items, value_items, item_sorts, aggregator = pivotSum):
        """
        Create a pivot table for the specified 'data', having the specified 'data_columns', where the rows of the 
        pivot table are defined by the items in 'row_items', the columns in the pivot table are defined by 'column_items',
        and the data values in the pivot table are defined by 'value_items', and finally where the values are aggregated with
        the specified 'aggregator' function.
                
        """
        self.result = {}
        self.row_items = row_items
        self.column_items = column_items
        self.value_items = value_items
        self.item_sorts = item_sorts
        
        row_indexes    = []
        column_indexes = []
        value_indexes  = []
    
        # Create sets of the column and value keys used to index 'result'.  Note that
        # the keys must be tuple, so the elements of 'value_items' must be made into
        # tuples.
        column_keys = set()
        value_keys  = set(map(lambda x: tuple([x]), value_items))
    

        # Populate [row|column|value]_indexes with the index into 'data_columns' where the
        # [row|column|value]_items element at the corresponding index can be found.
        for row_item in row_items:
            for (idx, column) in enumerate(data_columns):
                if (row_item == column):
                    row_indexes.append(idx)
    
        for column_item in column_items:
            for (idx, column) in enumerate(data_columns):
                if (column_item == column):
                    column_indexes.append(idx)
            
        for value in value_items:
            for (idx, column) in enumerate(data_columns):
                if (value == column):
                    value_indexes.append(idx)
    
        # Create the pivot table.
        for row in data:       
            row_key = tuple(map(lambda x: row[x], row_indexes))
            column_key = tuple(map(lambda x: row[x], column_indexes))                        
            column_keys.add(column_key)
            for idx, value in enumerate(value_items):
                aggregate_value(self.result, [row_key, column_key, tuple([value])], row[value_indexes[idx]], aggregator)
        
        # Use the higher-order function 'create_sort_function' to generate functions
        # for sorting tuples based on the items_sorts and the items in the tuple.
        column_sorter = create_sort_function(item_sorts, column_items)
        row_sorter = create_sort_function(item_sorts, row_items)
        value_sorter = create_sort_function(item_sorts, value_items)
            
        self.row_keys = sorted(self.result.keys(), key=row_sorter)
        self.column_keys = sorted(list(column_keys), key = column_sorter)
        self.value_keys = sorted(list(value_keys), key = value_sorter)
        
        # Fill in 0 cells for row_key/column_key/value_key combinations not found in the data.
        zero_fill(self.result, [self.row_keys, self.column_keys, self.value_keys])   

    def insert_column_keys(self, keys):
        column_sorter = create_sort_function(self.item_sorts, self.column_items)
        self.column_keys = sorted(set(self.column_keys).union(set(keys)), key = column_sorter)
        zero_fill(self.result, [self.row_keys, self.column_keys, self.value_keys])   
        
    def flatten_table(self):
        """Return a flatten tabular rendering of this pivot table.  The returned 
        object is a tuple whose first item is a list of lists of column headers, and whose second
        item is a list of lists of data rows.  E.g.:
        ([[       "",        "",  "1999",  "1999",  "2000",  "2000"], 
          ["Country", "Product", "Sales", "Costs", "Sales", "Costs"]],
         [[ "Canada",   "Chair",      20,      10,      40,       5],
          [ "Canada",   "Chair",      20,      10,      40,       5],             
          ...
         ])
        """
        assert len(self.column_items) == 1
        assert len(self.value_items) == 1
        
        headers = []
        headers = self.row_items
        for column in self.column_keys:
            headers.append(column[0])
        table = []
        for row in self.row_keys:
            row_value = list(row)
            for column in self.column_keys:
                row_value.append(self.result[row][column][tuple([self.value_items[0]])])
            table.append(row_value)    
        return ([headers], table)
       

def main():
    TEST_DATA_COLS = ["Product", "Country", "Year", "Sales", "Costs"]
    TEST_DATA      = [
        ["Chair", "USA", 1999, 10, 5],
        ["Table", "USA", 1999, 10, 5],
        ["Chair", "USA", 2000, 10, 5],
        ["Table", "USA", 2000, 10, 5],        
        ["Chair", "Canada", 1999, 10, 5],
        ["Chair", "Canada", 1999, 10, 5],        
        ["Table", "Canada", 1999, 10, 5],
        ["Table", "Canada", 2001, 10, 5],        
        ["Chair", "UK", 1999, 20, 5],
        ["Chair", "UK", 1999, 20, 5],        
        ["Piano", "UK", 1999, 20, 5],
        ["Table", "UK", 2001, 20, 5]
        ]
    
    TEST_ROW_ITEMS = ["Country", "Product"]
    TEST_COL_ITEMS = ["Year"]
    TEST_VALUE_ITEMS = ["Sales"]
    
    PRODUCT_SORT_KEY = {"Piano": 1, "Table": 2,  "Chair": 3}
    TEST_ITEM_SORTS = {"Product": lambda x: PRODUCT_SORT_KEY[x]}
    
    pivot = PivotTable(TEST_DATA, TEST_DATA_COLS, TEST_ROW_ITEMS, TEST_COL_ITEMS, TEST_VALUE_ITEMS, TEST_ITEM_SORTS)
    table = pivot.flatten_table()
    print(table[0])
    for row in table[1]:
        print(row)
    
if __name__ == "__main__":
    main()
    