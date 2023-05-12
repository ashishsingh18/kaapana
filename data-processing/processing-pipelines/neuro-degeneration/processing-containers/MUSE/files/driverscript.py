 #!/usr/bin/env python

from DeepMRSeg import deepmrseg_test, utils
import SimpleITK as sitk
import nibabel
import sys, os
import glob
from datetime import datetime

### For local testng
#os.environ["WORKFLOW_DIR"] = "D:/ashish/work/projects/Kaapana/sampledata/dcm2nifti-210519201059552217" #"<your data directory>"
#os.environ["BATCH_NAME"] = "batch"
#os.environ["OPERATOR_IN_DIR"] = "dcm-converter"
#os.environ["OPERATOR_OUT_DIR"] = "output"

lps_model_path = ["/models/MUSE/LPS"]
psl_model_path = ["/models/MUSE/PSL"]
slp_model_path = ["/models/MUSE/SLP"]

def write_image(output, output_file_path):
    writer = sitk.ImageFileWriter()
    writer.SetFileName ( output_file_path )
    writer.Execute ( output )

def read_image(input_file_path):
    reader = sitk.ImageFileReader()
    reader.SetFileName ( input_file_path )
    image = reader.Execute()
    return image

def remove_files_from_folder(folder):
    folder += '/*.*'
    files = glob.glob(folder, recursive=True)
    print(files)
    for f in files:
        os.remove(f)
        print('removing temp file: ', f)

batch_folders = [f for f in glob.glob(os.path.join('/', os.environ['WORKFLOW_DIR'], os.environ['BATCH_NAME'], '*'))]
print('batch_folders: ',batch_folders)

for batch_element_dir in batch_folders:

    mask_input_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_IN_MASK_DIR'])
    image_input_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_IN_DIR'])
    nifti_files = sorted(glob.glob(os.path.join(image_input_dir, "*.nii.gz*"), recursive=True))
    mask_files = sorted(glob.glob(os.path.join(mask_input_dir, "*.nrrd*"), recursive=True))
    batch_size = os.environ['BATCH_SIZE']

    if len(nifti_files) == 0 and len(mask_files) == 0:
        print("Nifti or Nrrd file not found!")
        exit(1)
    else:
        print("Applying mask to image: %s" % nifti_files)

        image = read_image(nifti_files[0])
        print("input image read")

        mask = read_image(mask_files[0])
        print("mask read")

        maskfilter = sitk.MaskImageFilter()
        maskedoutput = maskfilter.Execute(image,mask)
        print("mask applied on input image")

        temp_muse_input_image = os.path.join("/tempmuse/",os.path.basename(batch_element_dir) + ".nii.gz")

        write_image(maskedoutput,temp_muse_input_image)
        print("masked image written internally as nii")

        print("Starting Muse computation on image: %s" % temp_muse_input_image)

        #generate temp nii.gz file path for muse output
        temp_muse_output_nii = os.path.join("/tempmuse/",os.path.basename(batch_element_dir) + "_muse.nii.gz")

#        cmd = "deepmrseg_test" + " --mdlDir " + lps_model_path[0] + \
#            " --mdlDir " + psl_model_path[0] + \
#            " --mdlDir " + slp_model_path[0] + \
#            " --inImg " + temp_muse_input_image + \
#            " --outImg " + temp_muse_output_nii

        cmd = ["deepmrseg_test",
            "--mdlDir",lps_model_path[0],
            "--mdlDir", psl_model_path[0],
            "--mdlDir", slp_model_path[0],
            "--inImg", temp_muse_input_image,
            "--outImg", temp_muse_output_nii,
            "--batch", batch_size]

        #deepmrseg_test.Run(lps_model_path[0], psl_model_path[0],mdlDir slp_model_path[0],nifti_files[0],tempoutputpath)

        deepmrseg_test._main_warg(cmd)

        print("Muse Finished")
        #Muse specific stuff ends here

        element_output_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_OUT_DIR'])
        if not os.path.exists(element_output_dir):
            os.makedirs(element_output_dir)

        #generate output nrrd file path
        output_file_path = os.path.join(element_output_dir, "{}.nrrd".format(os.path.basename(batch_element_dir)))

        #read nifti & write output as nrrd
        muse_nii_result = read_image(temp_muse_output_nii)
        write_image(muse_nii_result,output_file_path)

        #delete all temp files
        remove_files_from_folder('/tempmuse')
