
# for help with 1d), visualizing patterns in the binary representations
# of the first n multiples of 7 in terminal. w and h refer to the terminal
# window dimensions

def one_d(n, width, height):
	
	row_h = height/n
	row_w = (width/n)*n
	
	# the ith row is divided into 2^i rectangles representing each binary string
	# of length i. The row's jth rectangle is dark (###) or light (alternately ... and ,,,) 
	# if j is a multiple of 7
	for i in range(1,n+1):
		row = ''
		n_rects = pow(2,i)
		rect_w = row_w/n_rects
		for j in range(n_rects):
			char = '#' if (j%7 == 0) else ('.' if (j%2 == 0) else ',')
			chars = char * rect_w
			row += chars
		for r in range(row_h):
			print row

one_d(10,1094,228)
