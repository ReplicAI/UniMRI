import SimpleITK as sitk
from .. import __path as path
from .. import __files as files

def process(data):
	for mod in ["path_T1", "path_T2", "path_FLAIR"]:
		filename = data[mod+"_pre"] if path.isfile(data[mod+"_pre"]) else data[mod]
		A = (filename)

		inputImage = sitk.ReadImage(A)
		inputImage = sitk.Cast(inputImage,sitk.sitkFloat32)
		corrector = sitk.N4BiasFieldCorrectionImageFilter()

		output = corrector.Execute(inputImage)
		nome = path.join(path.dirname(data[mod+"_pre"]), "t"+path.lastname(data[mod+"_pre"]))
		#nome = nome.encode("utf-8")
		sitk.WriteImage(output, nome)

		files.replace(nome, data[mod+"_pre"])