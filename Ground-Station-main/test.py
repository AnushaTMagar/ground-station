s = '2654.59032'
y = '08604.81603'

lat = float(s[0][:-8]) + float("{:.8f}".format((float(s[0][-8:])/60)))
lon = float(y[1][:-8]) + float("{:.8f}".format((float(y[1][-8:])/60)))


