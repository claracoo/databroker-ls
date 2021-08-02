import pytest
from mongo_query import output_bluesky_docs
import yaml

# --------------------------------------------------
def test_output():
    uid = "6834f071-7fef-4b01-9bc5-eb60790ae641"
    output_bluesky_docs(uid)
    filename = "bluesky_doc_" + uid + ".yml"
    with open(filename, "r") as f:  # open the yaml file we now know exists
            documents = yaml.load(f)  # load the contents
            start_dict = {'detectors': ['det'], 'hints': {'dimensions': [[['time'], 'primary']]}, 'num_intervals': 0, 'num_points': 1, 'plan_args': {'detectors': ["SynGauss(prefix='', name='det', read_attrs=['val'], configuration_attrs=['Imax', 'center', 'sigma', 'noise', 'noise_multiplier'])"], 'num': 1}, 'plan_name': 'count', 'plan_type': 'generator', 'scan_id': 1, 'time': 1627318916.3433862, 'uid': '6834f071-7fef-4b01-9bc5-eb60790ae641', 'versions': {'bluesky': '1.7.0', 'ophyd': '1.6.1'}}
            descriptor_dict = {'configuration': {'det': {'data': {'det_Imax': 1, 'det_center': 0, 'det_noise': 'none', 'det_noise_multiplier': 1, 'det_sigma': 1}, 'data_keys': {'det_Imax': {'dtype': 'integer', 'shape': [], 'source': 'SIM:det_Imax'}, 'det_center': {'dtype': 'integer', 'shape': [], 'source': 'SIM:det_center'}, 'det_noise': {'dtype': 'integer', 'enum_strs': ['none', 'poisson', 'uniform'], 'shape': [], 'source': 'SIM:det_noise'}, 'det_noise_multiplier': {'dtype': 'integer', 'shape': [], 'source': 'SIM:det_noise_multiplier'}, 'det_sigma': {'dtype': 'integer', 'shape': [], 'source': 'SIM:det_sigma'}}, 'timestamps': {'det_Imax': 1627318916.322241, 'det_center': 1627318916.322228, 'det_noise': 1627318916.322082, 'det_noise_multiplier': 1627318916.322211, 'det_sigma': 1627318916.3222551}}}, 'data_keys': {'det': {'dtype': 'number', 'object_name': 'det', 'precision': 3, 'shape': [], 'source': 'SIM:det'}}, 'hints': {'det': {'fields': ['det']}}, 'name': 'primary', 'object_keys': {'det': ['det']}, 'run_start': '6834f071-7fef-4b01-9bc5-eb60790ae641', 'time': 1627318916.3824692, 'uid': '2a15a0b9-ddb7-40ca-be45-d344dd4df4d4'}
            event_dict = {'data': {'det': 1.0}, 'descriptor': '2a15a0b9-ddb7-40ca-be45-d344dd4df4d4', 'filled': {}, 'seq_num': 1, 'time': 1627318916.386265, 'timestamps': {'det': 1627318916.380264}, 'uid': '34d4b47d-920a-4435-b56a-410f6026b5ef'}
            stop_dict = {'exit_status': 'success', 'num_events': {'primary': 1}, 'reason': '', 'run_start': '6834f071-7fef-4b01-9bc5-eb60790ae641', 'time': 1627318916.3885171, 'uid': '7551f1c2-eb3e-41d3-960a-510a58ef21ab'}
            assert start_dict == documents["start"]
            assert descriptor_dict == documents["descriptor"]
            assert event_dict == documents["event"]
            assert stop_dict == documents["stop"]
