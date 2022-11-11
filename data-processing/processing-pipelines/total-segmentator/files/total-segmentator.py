from pathlib import Path
import os
import json
from typing import List

import torch
from totalsegmentator.libs import setup_nnunet, download_pretrained_weights


def total_segmentator(input_path: Path, output_path: Path, fast: bool = False):
    if not torch.cuda.is_available():
        raise ValueError(
            "TotalSegmentator only works with a NVidia CUDA GPU. CUDA not found. " +
            "If you do not have a GPU check out our online tool: www.totalsegmentator.com")

    setup_nnunet()

    from totalsegmentator.nnunet import \
        nnUNet_predict_image  # this has to be after setting new env vars

    quiet = False
    if fast:
        task_id = 256
        resample = 3.0
        trainer = "nnUNetTrainerV2_ep8000_nomirror"
        if not quiet:
            print(
                "Using 'fast' option: resampling to lower resolution (3mm)"
            )
    else:
        task_id = [251, 252, 253, 254, 255]
        resample = 1.5
        trainer = "nnUNetTrainerV2_ep4000_nomirror"
    model = "3d_fullres"

    if type(task_id) is list:
        for tid in task_id:
            download_pretrained_weights(tid)
    else:
        download_pretrained_weights(task_id)

    folds = [0]  # None
    nnUNet_predict_image(
        input_path, output_path, task_id, model=model,
        folds=folds,
        trainer=trainer, tta=False,
        multilabel_image=True,
        resample=resample
    )

    with open(str(output_path / "seg_info.json"), 'w', encoding='utf8') as json_file:
        json.dump({
            "seg_info": [
                {
                    "label_int": "1",
                    "label_name": "adrenal_gland_left"
                },
                {
                    "label_int": "2",
                    "label_name": "adrenal_gland_right"
                },
                {
                    "label_int": "3",
                    "label_name": "aorta"
                },
                {
                    "label_int": "4",
                    "label_name": "autochthon_left"
                },
                {
                    "label_int": "5",
                    "label_name": "autochthon_right"
                },
                {
                    "label_int": "6",
                    "label_name": "brain"
                },
                {
                    "label_int": "7",
                    "label_name": "clavicula_left"
                },
                {
                    "label_int": "8",
                    "label_name": "clavicula_right"
                },
                {
                    "label_int": "9",
                    "label_name": "colon"
                },
                {
                    "label_int": "10",
                    "label_name": "duodenum"
                },
                {
                    "label_int": "11",
                    "label_name": "esophagus"
                },
                {
                    "label_int": "12",
                    "label_name": "face"
                },
                {
                    "label_int": "13",
                    "label_name": "femur_left"
                },
                {
                    "label_int": "14",
                    "label_name": "femur_right"
                },
                {
                    "label_int": "15",
                    "label_name": "gallbladder"
                },
                {
                    "label_int": "16",
                    "label_name": "gluteus_maximus_left"
                },
                {
                    "label_int": "17",
                    "label_name": "gluteus_maximus_right"
                },
                {
                    "label_int": "18",
                    "label_name": "gluteus_medius_left"
                },
                {
                    "label_int": "19",
                    "label_name": "gluteus_medius_right"
                },
                {
                    "label_int": "20",
                    "label_name": "gluteus_minimus_left"
                },
                {
                    "label_int": "21",
                    "label_name": "gluteus_minimus_right"
                },
                {
                    "label_int": "22",
                    "label_name": "heart_atrium_left"
                },
                {
                    "label_int": "23",
                    "label_name": "heart_atrium_right"
                },
                {
                    "label_int": "24",
                    "label_name": "heart_myocardium"
                },
                {
                    "label_int": "25",
                    "label_name": "heart_ventricle_left"
                },
                {
                    "label_int": "26",
                    "label_name": "heart_ventricle_right"
                },
                {
                    "label_int": "27",
                    "label_name": "hip_left"
                },
                {
                    "label_int": "28",
                    "label_name": "hip_right"
                },
                {
                    "label_int": "29",
                    "label_name": "humerus_left"
                },
                {
                    "label_int": "30",
                    "label_name": "humerus_right"
                },
                {
                    "label_int": "31",
                    "label_name": "iliac_artery_left"
                },
                {
                    "label_int": "32",
                    "label_name": "iliac_artery_right"
                },
                {
                    "label_int": "33",
                    "label_name": "iliac_vena_left"
                },
                {
                    "label_int": "34",
                    "label_name": "iliac_vena_right"
                },
                {
                    "label_int": "35",
                    "label_name": "iliopsoas_left"
                },
                {
                    "label_int": "36",
                    "label_name": "iliopsoas_right"
                },
                {
                    "label_int": "37",
                    "label_name": "inferior_vena_cava"
                },
                {
                    "label_int": "38",
                    "label_name": "kidney_left"
                },
                {
                    "label_int": "39",
                    "label_name": "kidney_right"
                },
                {
                    "label_int": "40",
                    "label_name": "liver"
                },
                {
                    "label_int": "41",
                    "label_name": "lung_lower_lobe_left"
                },
                {
                    "label_int": "42",
                    "label_name": "lung_lower_lobe_right"
                },
                {
                    "label_int": "43",
                    "label_name": "lung_middle_lobe_right"
                },
                {
                    "label_int": "44",
                    "label_name": "lung_upper_lobe_left"
                },
                {
                    "label_int": "45",
                    "label_name": "lung_upper_lobe_right"
                },
                {
                    "label_int": "46",
                    "label_name": "pancreas"
                },
                {
                    "label_int": "47",
                    "label_name": "portal_vein_and_splenic_vein"
                },
                {
                    "label_int": "48",
                    "label_name": "pulmonary_artery"
                },
                {
                    "label_int": "49",
                    "label_name": "rib_left_1"
                },
                {
                    "label_int": "50",
                    "label_name": "rib_left_10"
                },
                {
                    "label_int": "51",
                    "label_name": "rib_left_11"
                },
                {
                    "label_int": "52",
                    "label_name": "rib_left_12"
                },
                {
                    "label_int": "53",
                    "label_name": "rib_left_2"
                },
                {
                    "label_int": "54",
                    "label_name": "rib_left_3"
                },
                {
                    "label_int": "55",
                    "label_name": "rib_left_4"
                },
                {
                    "label_int": "56",
                    "label_name": "rib_left_5"
                },
                {
                    "label_int": "57",
                    "label_name": "rib_left_6"
                },
                {
                    "label_int": "58",
                    "label_name": "rib_left_7"
                },
                {
                    "label_int": "59",
                    "label_name": "rib_left_8"
                },
                {
                    "label_int": "60",
                    "label_name": "rib_left_9"
                },
                {
                    "label_int": "61",
                    "label_name": "rib_right_1"
                },
                {
                    "label_int": "62",
                    "label_name": "rib_right_10"
                },
                {
                    "label_int": "63",
                    "label_name": "rib_right_11"
                },
                {
                    "label_int": "64",
                    "label_name": "rib_right_12"
                },
                {
                    "label_int": "65",
                    "label_name": "rib_right_2"
                },
                {
                    "label_int": "66",
                    "label_name": "rib_right_3"
                },
                {
                    "label_int": "67",
                    "label_name": "rib_right_4"
                },
                {
                    "label_int": "68",
                    "label_name": "rib_right_5"
                },
                {
                    "label_int": "69",
                    "label_name": "rib_right_6"
                },
                {
                    "label_int": "70",
                    "label_name": "rib_right_7"
                },
                {
                    "label_int": "71",
                    "label_name": "rib_right_8"
                },
                {
                    "label_int": "72",
                    "label_name": "rib_right_9"
                },
                {
                    "label_int": "73",
                    "label_name": "sacrum"
                },
                {
                    "label_int": "74",
                    "label_name": "scapula_left"
                },
                {
                    "label_int": "75",
                    "label_name": "scapula_right"
                },
                {
                    "label_int": "76",
                    "label_name": "small_bowel"
                },
                {
                    "label_int": "77",
                    "label_name": "spleen"
                },
                {
                    "label_int": "78",
                    "label_name": "stomach"
                },
                {
                    "label_int": "79",
                    "label_name": "trachea"
                },
                {
                    "label_int": "80",
                    "label_name": "urinary_bladder"
                },
                {
                    "label_int": "81",
                    "label_name": "vertebrae_C1"
                },
                {
                    "label_int": "82",
                    "label_name": "vertebrae_C2"
                },
                {
                    "label_int": "83",
                    "label_name": "vertebrae_C3"
                },
                {
                    "label_int": "84",
                    "label_name": "vertebrae_C4"
                },
                {
                    "label_int": "85",
                    "label_name": "vertebrae_C5"
                },
                {
                    "label_int": "86",
                    "label_name": "vertebrae_C6"
                },
                {
                    "label_int": "87",
                    "label_name": "vertebrae_C7"
                },
                {
                    "label_int": "88",
                    "label_name": "vertebrae_L1"
                },
                {
                    "label_int": "89",
                    "label_name": "vertebrae_L2"
                },
                {
                    "label_int": "90",
                    "label_name": "vertebrae_L3"
                },
                {
                    "label_int": "91",
                    "label_name": "vertebrae_L4"
                },
                {
                    "label_int": "92",
                    "label_name": "vertebrae_L5"
                },
                {
                    "label_int": "93",
                    "label_name": "vertebrae_T1"
                },
                {
                    "label_int": "94",
                    "label_name": "vertebrae_T10"
                },
                {
                    "label_int": "95",
                    "label_name": "vertebrae_T11"
                },
                {
                    "label_int": "96",
                    "label_name": "vertebrae_T12"
                },
                {
                    "label_int": "97",
                    "label_name": "vertebrae_T2"
                },
                {
                    "label_int": "98",
                    "label_name": "vertebrae_T3"
                },
                {
                    "label_int": "99",
                    "label_name": "vertebrae_T4"
                },
                {
                    "label_int": "100",
                    "label_name": "vertebrae_T5"
                },
                {
                    "label_int": "101",
                    "label_name": "vertebrae_T6"
                },
                {
                    "label_int": "102",
                    "label_name": "vertebrae_T7"
                },
                {
                    "label_int": "103",
                    "label_name": "vertebrae_T8"
                },
                {
                    "label_int": "104",
                    "label_name": "vertebrae_T9"
                }
            ]
        }, json_file, ensure_ascii=False)


# if args.statistics:
#     if not quiet: print("Calculating statistics...")
#     st = time.time()
#     get_basic_statistics_for_entire_dir(seg, args.input, args.output / "statistics.json", quiet)
#     # get_radiomics_features_for_entire_dir(args.input, args.output, args.output / "statistics_radiomics.json")
#     if not quiet: print(f"  calculated in {time.time()-st:.2f}s")
#
# if args.radiomics:
#     if not quiet: print("Calculating radiomics...")
#     st = time.time()
#     get_radiomics_features_for_entire_dir(args.input, args.output, args.output / "statistics_radiomics.json")
#     if not quiet: print(f"  calculated in {time.time()-st:.2f}s")


batch_folders: List[Path] = sorted([*Path('/', os.environ['WORKFLOW_DIR'], os.environ['BATCH_NAME']).glob('*')])

for batch_element_dir in batch_folders:

    element_input_dir = batch_element_dir / os.environ['OPERATOR_IN_DIR']
    element_output_dir = batch_element_dir / os.environ['OPERATOR_OUT_DIR']

    element_output_dir.mkdir(exist_ok=True)

    # The processing algorithm
    print(
        f'Checking {str(element_input_dir)} for nifti files and writing results to {str(element_output_dir)}'
    )
    nifti_files: List[Path] = sorted([*element_input_dir.rglob("*.nii.gz")])

    if len(nifti_files) == 0:
        print("No nifti file found!")
        exit(0)
    else:
        for nifti_file in nifti_files:
            print(f"# running total segmentator")
            try:
                total_segmentator(
                    nifti_file.absolute(),
                    element_output_dir.absolute()
                )
                print("# Successfully processed")
            except Exception as e:
                print("Processing failed with exception: ", e)
