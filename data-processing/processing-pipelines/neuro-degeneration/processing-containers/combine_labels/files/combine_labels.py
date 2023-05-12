 #!/usr/bin/env python
#pip install SimpleITK==1.2.4

import SimpleITK as sitk
import sys, os, glob, csv
from datetime import datetime

# For local testng
#os.environ["WORKFLOW_DIR"] = "D:/ashish/work/projects/Kaapana/sampledata/dcm2nifti-210519201059552217" #"<your data directory>"
#os.environ["BATCH_NAME"] = "batch"
#os.environ["OPERATOR_IN_DIR"] = "dcm-converter"
#os.environ["OPERATOR_OUT_DIR"] = "output"
#os.environ["OPERATOR_IN_MASK_DIR"] = "None"

def write_image(img, output_file_path):
    writer = sitk.ImageFileWriter()
    writer.SetFileName ( output_file_path )
    writer.Execute ( img )

def readimage(input_file_path):
    reader = sitk.ImageFileReader()
    reader.SetFileName ( input_file_path )
    image = reader.Execute()
    return image

def removeFilesFromFolder(folder):
    folder += '/*.*'
    files = glob.glob(folder, recursive=True)
    print(files)
    for f in files:
        os.remove(f)
        print('removing temp file: ', f)

def read_csv(csv_path):
    with open(csv_path) as roiMap:
        reader = csv.reader(roiMap, delimiter=',')

        # Read mapping csv to dictionary
        mapDict = {}
        for row in reader:
            # Append the ROI number to the list
            #first item is muse ROI number, 2nd item is key (new value we want to assign to a collection of labels)
            newval = int(row[1])
            print('newval: ', newval)
            #labels to be combined are from 3 onwards
            for x in row[3:]:
                key = int(x)
                print('key: ', key)
                mapDict[key] = newval
    return mapDict

def remove_unwanted_labels(muse_mask, mapDict):
    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(muse_mask)
    print("labels in muse: ", stats.GetNumberOfLabels())
    print("labels in mapped dict: ", len(mapDict.keys()))

    #create relabel map for use with changelabel class
    #[keep only those labels that are defined in mapping csv, assign all others to background i.e. zero]
    newDict =  { i : 0 for i in stats.GetLabels() if (int(i) not in mapDict.keys()) }
    #merge newDict with mapping dict
    newDict.update(mapDict)
    return newDict

batch_folders = [f for f in glob.glob(os.path.join('/', os.environ['WORKFLOW_DIR'], os.environ['BATCH_NAME'], '*'))]
#print('batch_folders: ',batch_folders)

for batch_element_dir in batch_folders:

    image_input_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_IN_DIR'])

    nrrd_files = sorted(glob.glob(os.path.join(image_input_dir, "*.nrrd*"), recursive=True))

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'MUSE_Kapaana_DerivedRegions_v3.csv')

    if len(nrrd_files) == 0 and len(file_path) == 0:
        print("Nrrd or csv file not found!")
        exit(1)
    else:
        print("combine labels started for files %s" % nrrd_files)

        image = readimage(nrrd_files[0])
        print("input label map read")

        mapDict = read_csv(file_path)
        print('items in mapping csv: ', len(mapDict))

        relabelMap = remove_unwanted_labels(image,mapDict)

        print('relabelMap: ', relabelMap)
        output = sitk.ChangeLabel(image, changeMap=relabelMap)

        element_output_dir = os.path.join(batch_element_dir, os.environ['OPERATOR_OUT_DIR'])
        if not os.path.exists(element_output_dir):
            os.makedirs(element_output_dir)

        output_file_path = os.path.join(element_output_dir, "{}.nrrd".format(os.path.basename(batch_element_dir)))

        write_image(output,output_file_path)
        print("combined label map written as nrrd to path: ",output_file_path)
