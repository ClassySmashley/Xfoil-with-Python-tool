# airfoil file sourced from http://airfoiltools.com/airfoil/details?airfoil=naca633618-il

import subprocess
import os
import numpy
import matplotlib.pyplot

# Questions
# which version of python?

# Functions
def polar(Re):
	# Function runs polar in xfoil for the given reynolds number and saves the results

	xfoil = subprocess.Popen([xfoilpath], stdin = subprocess.PIPE) # Text is 3.7 and up universal_newlines for older
	print('Starting xfoil\n')
	# select the airfoil naca63(3)-618 Re: 3e6, 10e6, 15e6
	xfoil.stdin.write(nacafile)

	# convert input strings to bits for subprocess.write compatibility
	polarfile = 'NACA Polar' + Re + '.dat\n'
	# naca polar array
	polarfilearray = [polarfile[:-1]]
	polarfile = polarfile.encode('utf-8')
	# dumpfile = 'dump' + Re + '.dat\n'
	# dumpfile = dumpfile.encode('utf-8')
	blfilename = 'bl' + Re + ' '
	blfilearray = ['bl files']

	Re = 'v' + Re + '\n'
	Re = Re.encode('utf-8')
	
	# enter menu
	xfoil.stdin.write(b'oper\n')

	# select viscous flow and reynolds number
	xfoil.stdin.write(Re)	

	# increase iteration number
	xfoil.stdin.write(b'iter 200\n')

	# save polar output
	xfoil.stdin.write(b'pacc\n')
	xfoil.stdin.write(polarfile)
	xfoil.stdin.write(b'\n')

	# get the cl, cd, cm, cl/cd for the aoa's -10 to 20 deg
	currentalfa = -10
	for x in range(31):
		alfa = 'alfa' + str(currentalfa) + '\n'
		alfa = alfa.encode('utf-8')
		xfoil.stdin.write(alfa)
		blfilenamebytes = blfilename + str(currentalfa) + 'deg.dat\n'
		# array for plotting and clean up
		blfilearray = blfilearray + [blfilenamebytes[2:-1]]
		blfilenamebytes = blfilenamebytes.encode('utf-8')
		xfoil.stdin.write(b'dump')
		xfoil.stdin.write(blfilenamebytes)
		currentalfa = currentalfa + 1
		
		pass

	# exit polar mode
	xfoil.stdin.write(b'p\n')
	# return to top menu
	xfoil.stdin.write(b'\n')

	# close xfoil
	xfoil.communicate(b'quit')

	# create plots for the cl, cd, cm, cl/cd for the aoa's -10 to 20 deg
	return blfilearray, polarfilearray

def pressDist(Re):
	# get the pressure coefficient distributions at 0, 4, 8, 12 deg
	# convert input strings to bits for subprocess.write compatibility
	# open xfoil
	xfoil = subprocess.Popen([xfoilpath], stdin = subprocess.PIPE) # Text is 3.7 and up universal_newlines for older
	print('Starting xfoil\n')

	# select the airfoil naca63(3)-618 Re: 3e6, 10e6, 15e6
	xfoil.stdin.write(nacafile)

	data = 'pressure distribution' + Re
	distributionfilearray = ['Pressure Distribution files']
	
	Re = 'v ' + Re + '\n'
	Re = Re.encode('utf-8')
	# enter menu and select viscosity
	xfoil.stdin.write(b'oper\n')
	xfoil.stdin.write(Re)

	# increase iteration number
	xfoil.stdin.write(b'iter 200\n')

	currentalfa = 0
	for x in range(5):
		alfa = 'alfa ' + str(currentalfa) + '\n'
		alfa = alfa.encode('utf-8')
		if x != 0:
			xfoil.stdin.write(b'cpwr')
			file = data + ' ' + str(currentalfa-4) + 'deg.dat\n'
			distributionfilearray = distributionfilearray + [file[9:-1]]
			file = file.encode('utf-8')	
			xfoil.stdin.write(file)
		xfoil.stdin.write(alfa)
		currentalfa = currentalfa + 4

	xfoil.stdin.write(b'\n')

	# close xfoil
	xfoil.communicate(b'quit')

	return distributionfilearray

def importfile(filename, header, ycol, bl = False, xcol = 0):
	array = numpy.loadtxt(filename, skiprows = header)
	# pulling in the bl parameter's causes an exception due to the file formatting from xfoil
	# in this case ycol is passed in as an array
	if bl:
		dstar = array[ycol[0]]
		theta = array[ycol[1]]
		H = array[ycol[2]]
		return dstar, theta, H
	else:
		xarray = array[ : , xcol]
		yarray = array[ : , ycol]

	return xarray, yarray

# Main program #

xfoilpath = input('Please enter the location of xfoil (including the xoil file name and extension)\n')
nacafile = input('Please enter the location of the NACA file (including the file name and extension\n')

nacafile = 'load ' + nacafile + '\n'

# Change inputs to bytes
xfoilpath = xfoilpath.encode('utf-8')
nacafile = nacafile.encode('utf-8')
# nacafile = b'load naca633618.dat\n' # must change



# have user select which function to run
# run tags
run = True
choice1execute = False
choice2execute = False

# The loop will launch the function and analyis in xfoil and keep the program open until the user decides to exit
while (run == True):
	choice = input('Choose function to run (enter 1, 2, 3, or 4):\noption 1: find polar coefficients and trailing edge boundary parameters\noption 2: find pressure distributions\noption 3: plot menu\noption 4: end program\n')
	if choice == '1':

		# Tag choice 1 as having run
		choice1execute = True

		blfilearray1, polarfilearray1 = polar('3e6')
		blfilearray2, polarfilearray2 = polar('10e6')
		blfilearray3, polarfilearray3 = polar('15e6')
		# polar file arrays for plotting and clean up
		blfilearray = blfilearray1 + blfilearray2 + blfilearray3
		polarfilearray = polarfilearray1 + polarfilearray2 + polarfilearray3

	elif choice == '2':

		choice2execute = True
		distributionfilearray1 = pressDist('3e6')
		distributionfilearray2 = pressDist('10e6')
		distributionfilearray3 = pressDist('15e6')
		distributionfilearray = distributionfilearray1 + distributionfilearray2 + distributionfilearray3

	elif choice == '3':
		choice = input('Choose plot type (enter 1, 2, 3, or 4):\noption 1: polar plots for angle of attacks from -10 deg to 20 deg\noption 2: pressure coefficient distributions at 0 deg, 4 deg, 8 deg, and 12 deg\noption 3: plot trailing edge boundary layer properties for angle of attack from -10 to 20 deg\noption 4: return to previous menu\n')
		if choice == '1':
			# check if data exists by checking if the function to get that data has run
			if choice1execute:
				# plot polar coefficients
				print('polar plots')
				# initialize arrays for plotting
				xarray = ['line 1', 'line 2', 'line 3']
				clyarray = ['line 1', 'line 2', 'line 3']
				cdyarray = ['line 1', 'line 2', 'line 3']
				cmyarray = ['line 1', 'line 2', 'line 3']
				# index counter
				i = 0
				for x in polarfilearray:
					cl = 1
					cd = 2
					cm = 4
					alpha = 0
					xarray[i], clyarray[i] = importfile(x, 12, cl, xcol = alpha)
					xarray[i], cdyarray[i] = importfile(x, 12, cd, xcol = alpha)
					xarray[i], cmyarray[i] = importfile(x, 12, cm, xcol = alpha)
					i = i + 1

				# split arrays for plotting
				xarray3 = xarray[0]
				xarray10 = xarray[1]
				xarray15 = xarray[2]
				clyarray3 = clyarray[0]
				clyarray10 = clyarray[1]
				clyarray15 = clyarray[2]
				cdyarray3 = cdyarray[0]
				cdyarray10 = cdyarray[1]
				cdyarray15 = cdyarray[2]
				cmyarray3 = cmyarray[0]
				cmyarray10 = cmyarray[1]
				cmyarray15 = cmyarray[2]

				# create clcd arrays
				clcdyarray3 = clyarray3/cdyarray3
				clcdyarray10 = clyarray10/cdyarray10
				clcdyarray15 = clyarray15/cdyarray15

				# plot the cl polars
				plt = matplotlib.pyplot
				plt.plot(xarray3, clyarray3, 'r', xarray10, clyarray10, 'b', xarray15, clyarray15, 'g')
				plt.xlabel('Angle of Attack (degrees)')
				plt.ylabel('Coefficient of Lift')
				plt.title('Cl vs AoA')
				plt.legend(['Re: 3e6', 'Re: 10e6', 'Re: 15e6'])
				plt.show()

				# plot the cd polars
				plt.plot(xarray3, cdyarray3, 'r', xarray10, cdyarray10, 'b', xarray15, cdyarray15, 'g')
				plt.xlabel('Angle of Attack (degrees)')
				plt.ylabel('Coefficient of Drag')
				plt.title('Cd vs AoA')
				plt.legend(['Re: 3e6', 'Re: 10e6', 'Re: 15e6'])
				plt.show()

				# plot the cm polars
				plt.plot(xarray3, cmyarray3, 'r', xarray10, cmyarray10, 'b', xarray15, cmyarray15, 'g')
				plt.xlabel('Angle of Attack (degrees)')
				plt.ylabel('Coefficient of Moment')
				plt.title('Cm vs AoA')
				plt.legend(['Re: 3e6', 'Re: 10e6', 'Re: 15e6'])
				plt.show()

				# plot the clcd polars
				plt.plot(xarray3, clcdyarray3, 'r', xarray10, clcdyarray10, 'b', xarray15, clcdyarray15, 'g')
				plt.xlabel('Angle of Attack (degrees)')
				plt.ylabel('Lift/Drag Ratio')
				plt.title('Cl/Cd vs AoA')
				plt.legend(['Re: 3e6', 'Re: 10e6', 'Re: 15e6'])
				plt.show()
			else:
				print('The data for these plots has not been generated. Please select option 1 from the main menu.\n')
		elif choice == '2':
			# check if data exists by checking if the function to get that data has run
			if choice2execute:
				print('pressure plots')

				# initialize arrays for plotting
				xarray = ['line 1', 'line 2', 'line 3', 'line 4', 'line 1', 'line 2', 'line 3', 'line 4', 'line 1', 'line 2', 'line 3', 'line 4']
				cpyarray = ['line 1', 'line 2', 'line 3', 'line 4', 'line 1', 'line 2', 'line 3', 'line 4', 'line 1', 'line 2', 'line 3', 'line 4']

				# index counter
				i = 0
				for x in distributionfilearray:
					if x != 'Pressure Distribution files':
						xarray[i], cpyarray[i] = importfile(x, 3, 2, xcol = 0) 
						i = i + 1

				# split arrays for plotting
				xarray3_0deg = xarray[0]
				xarray3_4deg = xarray[1]
				xarray3_8deg = xarray[2]
				xarray3_12deg = xarray[3]
				xarray10_0deg = xarray[4]
				xarray10_4deg = xarray[5]
				xarray10_8deg = xarray[6]
				xarray10_12deg = xarray[7]
				xarray15_0deg = xarray[8]
				xarray15_4deg = xarray[9]
				xarray15_8deg = xarray[10]
				xarray15_12deg = xarray[11]
				cpyarray3_0deg = cpyarray[0]
				cpyarray3_4deg = cpyarray[1]
				cpyarray3_8deg = cpyarray[2]
				cpyarray3_12deg = cpyarray[3]
				cpyarray10_0deg = cpyarray[4]
				cpyarray10_4deg = cpyarray[5]
				cpyarray10_8deg = cpyarray[6]
				cpyarray10_12deg = cpyarray[7]
				cpyarray15_0deg = cpyarray[8]
				cpyarray15_4deg = cpyarray[9]
				cpyarray15_8deg = cpyarray[10]
				cpyarray15_12deg = cpyarray[11]

				# plot coefficients of pressure at each angle for a given reynolds number
				# plot for a reynolds number of 3e6
				plt = matplotlib.pyplot
				plt.plot(xarray3_0deg, cpyarray3_0deg, 'r', xarray3_4deg, cpyarray3_4deg, 'b', xarray3_8deg, cpyarray3_8deg, 'g', xarray3_12deg, cpyarray3_12deg, 'k')
				plt.xlabel('x position on airfoil')
				plt.ylabel('Coefficient of Pressure')
				plt.title('Cp vs x with Re = 3e6')
				plt.legend(['AoA: 0 deg', 'AoA: 4 deg', 'AoA: 8 deg', 'AoA: 12 deg'])
				plt.show()

				# plot for a reynolds number of 10e6
				plt = matplotlib.pyplot
				plt.plot(xarray10_0deg, cpyarray10_0deg, 'r', xarray10_4deg, cpyarray10_4deg, 'b', xarray10_8deg, cpyarray10_8deg, 'g', xarray10_12deg, cpyarray10_12deg, 'k')
				plt.xlabel('x position on airfoil')
				plt.ylabel('Coefficient of Pressure')
				plt.title('Cp vs x with Re = 10e6')
				plt.legend(['AoA: 0 deg', 'AoA: 4 deg', 'AoA: 8 deg', 'AoA: 12 deg'])
				plt.show()

				# plot for a reynolds number of 15e6
				plt = matplotlib.pyplot
				plt.plot(xarray15_0deg, cpyarray15_0deg, 'r', xarray15_4deg, cpyarray15_4deg, 'b', xarray15_8deg, cpyarray15_8deg, 'g', xarray15_12deg, cpyarray15_12deg, 'k')
				plt.xlabel('x position on airfoil')
				plt.ylabel('Coefficient of Pressure')
				plt.title('Cp vs x with Re = 15e6')
				plt.legend(['AoA: 0 deg', 'AoA: 4 deg', 'AoA: 8 deg', 'AoA: 12 deg'])
				plt.show()

			else:
				print('The data for these plots has not been generated. Please select option 2 from the main menu.\n')
		elif choice == '3':
			# check if data exists by checking if the function to get that data has run
			if choice1execute:
				# plot bl properties
				print(' boundary layer plots')

				# initialize arrays for plotting
				# xarray = ['line 1', 'line 2', 'line 3', 'line 4', 'line 1', 'line 2', 'line 3', 'line 4', 'line 1', 'line 2', 'line 3', 'line 4']
				# yarray = ['line 1', 'line 2', 'line 3', 'line 4', 'line 1', 'line 2', 'line 3', 'line 4', 'line 1', 'line 2', 'line 3', 'line 4']

				# index counter
				i = 0
				dstar = 4
				theta = 5
				H = 7
				parameters = [dstar, theta, H]
				dstar = numpy.zeros((93))
				theta = numpy.zeros((93))
				H = numpy.zeros((93))

				for x in blfilearray:
					if x != 'bl files':
						dstar[i], theta[i], H[i]= importfile(x, 59, ycol = parameters, bl = True)
						i = i + 1

				# split arrays for plotting
				xarray = numpy.linspace(-10, 20, num = 31)
				dstar3e6 = dstar[0:31]
				dstar10e6 = dstar[31:62]
				dstar15e6 = dstar[62:93]
				theta3e6 = theta[0:31]
				theta10e6 = theta[31:62]
				theta15e6 = theta[62:93]
				H3e6 = H[0:31]
				H10e6 = H[31:62]
				H15e6 = H[62:93]

				# plot the trailing edge bl parameter displacement thickness
				plt = matplotlib.pyplot
				plt.plot(xarray, dstar3e6, 'r', xarray, dstar10e6, 'b', xarray, dstar15e6, 'g')
				plt.xlabel('Angle of Attack (degrees)')
				plt.ylabel('Displacement Thickness')
				plt.title('Displacement Thickness at Trailing edge vs AoA with Re = 3e6')
				plt.legend(['Re: 3e6', 'Re: 10e6', 'Re: 15e6'])
				plt.show()

				# plot the trailing edge bl parameter momentum thickness
				plt = matplotlib.pyplot
				plt.plot(xarray, theta3e6, 'r', xarray, theta10e6, 'b', xarray, theta15e6, 'g')
				plt.xlabel('Angle of Attack (degrees)')
				plt.ylabel('Momentum Thickness')
				plt.title('Momentum Thickness at Trailing edge vs AoA')
				plt.legend(['Re: 3e6', 'Re: 10e6', 'Re: 15e6'])
				plt.show()

				# plot the trailing edge bl parameter shape factor
				plt = matplotlib.pyplot
				plt.plot(xarray, H3e6, 'r', xarray, H10e6, 'b', xarray, H15e6, 'g')
				plt.xlabel('Angle of Attack (degrees)')
				plt.ylabel('Shape Factor')
				plt.title('Shape Factor at Trailing edge vs AoA')
				plt.legend(['Re: 3e6', 'Re: 10e6', 'Re: 15e6'])
				plt.show()
						
			else:
				print('The data for these plots has not been generated. Please select option 1 from the main menu.\n')
	else:
		# Clean up and close program

		if choice1execute:
			# Remove files created for plotting
			for x in blfilearray:
				if x != 'bl files':
					os.remove(x)
			for x in polarfilearray:
				os.remove(x)
		if choice2execute:
			for x in distributionfilearray:
				if x != 'Pressure Distribution files':
					os.remove(x)
		run = False

print('All Done!')

