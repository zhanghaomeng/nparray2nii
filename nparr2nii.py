import numpy as np
import nibabel as nib
import os
import argparse


def npy2nii(infolder, outfolder, affine, header):
	for file in os.listdir(infolder):
		if file.endswith(".npy"):
			array = np.load(os.path.join(infolder, file))
			nimg = nib.Nifti1Image(array, affine, header)
			nib.save(nimg, os.path.join(outfolder, '%s.nii.gz' % file[:-4]))


def npz2nii(infolder, outfolder, affine, header):
	for file in os.listdir(infolder):
		if file.endswith(".npz"):
			npz = np.load(os.path.join(infolder, file))
			for label in npz.files:
				array = npz[label]
				nimg = nib.Nifti1Image(array, affine, header)
				if label == 'arr_0':
					nib.save(nimg, os.path.join(outfolder, '%s_AD.nii.gz' % file[:-4]))
				elif label == 'arr_1':
					nib.save(nimg, os.path.join(outfolder, '%s_diff.nii.gz' % file[:-4]))
				elif label == 'arr_2':
					nib.save(nimg, os.path.join(outfolder, '%s_genCN.nii.gz' % file[:-4]))
				elif label == 'arr_3':
					nib.save(nimg, os.path.join(outfolder, '%s_realCN.nii.gz' % file[:-4]))		


def main(args):
	sample = nib.load(args.samplepath)
	if args.npy:
		npy2nii(args.infolder, args.outfolder, sample.affine, sample.header)
	elif args.npz:
		npz2nii(args.infolder, args.outfolder, sample.affine, sample.header)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--npy', action='store_true', help='implement npy2nii')
	parser.add_argument('--npz', action='store_true', help='implement npz2nii')

	parser.add_argument('--samplepath', type=str, dest='samplepath')
	parser.add_argument('--infolder', type=str, dest='infolder')
	parser.add_argument('--outfolder', type=str, dest='outfolder')

	args = parser.parse_args()

	main(args)