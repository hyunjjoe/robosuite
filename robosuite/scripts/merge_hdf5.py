import h5py
import os
import argparse

def merge_hdf5_files(hdf5_files, combined_file):
    with h5py.File(combined_file, 'w') as combined_hf:
        data_grp = combined_hf.create_group("data")

        # Initialize attributes for the combined file's data group
        common_attrs = {}
        demo_count = 0

        for hdf5_file in hdf5_files:
            try:
                with h5py.File(hdf5_file, 'r') as hf:
                    # Copy attributes from the source data group to the combined data group
                    for attr_name, attr_value in hf["data"].attrs.items():
                        common_attrs[attr_name] = attr_value
                    
                    for demo_name in hf["data"].keys():
                        demo_count += 1
                        new_demo_name = f"demo_{demo_count}"
                        hf.copy(hf[f"data/{demo_name}"], data_grp, name=new_demo_name)

            except Exception as e:
                print(f"Error processing file {hdf5_file}: {e}")

        # Assign collected attributes to the combined data group
        for attr_name, attr_value in common_attrs.items():
            data_grp.attrs[attr_name] = attr_value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple HDF5 files into one.")
    parser.add_argument("--dataset", nargs='+', required=True, help="List of HDF5 files to merge.")
    parser.add_argument("--output", required=True, help="Path to the output combined HDF5 file.")

    args = parser.parse_args()
    
    merge_hdf5_files(args.dataset, args.output)
    print(f"Files merged into {args.output}")
