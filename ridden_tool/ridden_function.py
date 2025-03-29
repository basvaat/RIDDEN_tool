
from pandas import DataFrame, concat, read_csv
import random
from numpy import array, mean, std
import os

file_path = os.path.dirname(os.path.abspath(__file__))
ridden_model_matrix = f'{file_path}/../ridden_model/ridden_model_matrix.csv'

def get_output_file_name(output_name: str)->str:
    return output_name if output_name.endswith('.csv') else output_name+'.csv'

def permute(genename_list:list, seed:int):
    random.seed(seed)
    random.shuffle(genename_list)
    return genename_list

def permute_genenames(input_data:DataFrame, number_of_permutation:int):
    permuted_genenames_dict = {}
    permuted_genenames_dict[0] = list(input_data.columns)
    for s in range(1, number_of_permutation):

        genenames = list(input_data.columns)
        permuted_genenames_dict[s] = permute(genenames, s)
    return permuted_genenames_dict


def change_gene_name_order_based_on_permutations(chunk_df:DataFrame, permuted_genename_list:list):
    chunk_df_permuted = chunk_df.copy()
    chunk_df_permuted.columns = permuted_genename_list
    return chunk_df_permuted

def estimation_dataframe(lincs_model:DataFrame, chunk_df: DataFrame):
    genes = lincs_model.index.intersection(chunk_df.columns)
    # if the column names are duplicated - error
    return chunk_df.loc[:, genes] @ lincs_model.loc[genes]

def infer_receptor_activity(input_data_filename:str, number_of_permutation: int, chunk_size = 100, output_name = 'output'):
    # read in data
    print('Read in input_data')
    input_data = read_csv(input_data_filename, index_col = 0)
    input_data = input_data.astype(float)
    
    lincs_model = read_csv(ridden_model_matrix, index_col = 0)
    lincs_model = lincs_model.T
    
    input_data = input_data[input_data.columns.intersection(lincs_model.index)]

    print('Start calculation')
    # permute genenames and store as list of indexes
    permuted_genename_lists = permute_genenames(input_data,number_of_permutation)

    num_samples = len(input_data)
    # print('Number of samples:', num_samples)
    chunks = [input_data.index[i:i+chunk_size] for i in range(0, num_samples, chunk_size)]
    print('Number of chunks:', len(chunks))
    permutations = range(0, len(permuted_genename_lists.keys())) # number of permutation
    # print('Number of permutations:', len(permutations))

    # estimation of zscore receptor actvities
    zscore_receptor_activities = {}
    total_chunks = len(chunks)
    chunk_done_increment = max(total_chunks // 10, 1)
    chunk_done_counter = 0

    for i, chunk in enumerate(chunks):
        chunk_df = input_data.loc[chunk].copy() # subset dataframe

        chunk_estimated_values_dict = {}

        for permutation in permutations:
            chunk_df_permuted = change_gene_name_order_based_on_permutations(chunk_df, permuted_genename_lists[permutation])
            # estimated values of a sample and a receptor
            estimated_values_df = estimation_dataframe(lincs_model, chunk_df_permuted)
            chunk_estimated_values_dict[permutation] = estimated_values_df

        array_3d = array([df.values for df in chunk_estimated_values_dict.values()])
        mean_1d = mean(array_3d, axis=0)
        std_1d = std(array_3d, axis=0)
        chunk_receptor_activities_zscore = (chunk_estimated_values_dict[0] - mean_1d) / std_1d

        zscore_receptor_activities[i] = chunk_receptor_activities_zscore

        # Print % of chunks processed
        chunk_done_counter += 1

        if chunk_done_counter == chunk_done_increment:
            # Calculate the percentage done
            percentage_done = min((i + 1) / total_chunks * 100, 100)
            print(f"{int(percentage_done)}% of chunks processed.")
            chunk_done_counter = 0  # Reset the counter

    zscore_receptor_activities_sample_receptor= concat(zscore_receptor_activities, axis=0)
    zscore_receptor_activities_sample_receptor.index = zscore_receptor_activities_sample_receptor.index.get_level_values(1)

    output_file_name = get_output_file_name(output_name)

    zscore_receptor_activities_sample_receptor.to_csv(output_file_name)
    print(f'Result is saved to {output_file_name}')