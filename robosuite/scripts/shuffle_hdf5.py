import h5py
import numpy as np
import argparse

def shuffle_and_rename_hdf5_file(input_file, output_file):
    with h5py.File(input_file, 'r') as hf:
        data_grp = hf["data"]
        demos = list(data_grp.keys())
        np.random.shuffle(demos)
        
        with h5py.File(output_file, 'w') as shuffled_hf:
            shuffled_data_grp = shuffled_hf.create_group("data")
            
            # Copy attributes from the source data group to the shuffled data group
            for attr_name, attr_value in data_grp.attrs.items():
                shuffled_data_grp.attrs[attr_name] = attr_value
            
            # Copy and rename shuffled demos to the new file
            for i, demo_name in enumerate(demos):
                new_demo_name = f"demo_{i+1}"
                hf.copy(f"data/{demo_name}", shuffled_data_grp, name=new_demo_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shuffle and rename an HDF5 file and output to a new file.")
    parser.add_argument("--input", required=True, help="Path to the input HDF5 file.")
    parser.add_argument("--output", required=True, help="Path to the output shuffled and renamed HDF5 file.")

    args = parser.parse_args()
    
    shuffle_and_rename_hdf5_file(args.input, args.output)
    print(f"File shuffled, demos renamed, and saved to {args.output}")
