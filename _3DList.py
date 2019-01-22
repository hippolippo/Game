
class _3DList:
    def __init__(self, xsize, ysize, zsize):
        self.xsize, self.ysize, self.zsize = xsize, ysize, zsize
        self.array = [[[None for z in range(zsize)] for y in range(ysize)] for x in range(xsize)]
    def load(self,file):
        loaded = open(file, "r")
        data = loaded.read()
        loaded.close()
        data = [y.split(",") for y in [x.split(";") for x in data.split('\n')]]
        for x in enumerate(data):
            for y in enumerate(x[0]):
                for z in enumerate(y[0]):
                    self.set_data(x[1],y[1],z[1],z[0])

    def set_data(self,x,y,z,data):
        self.array[x][y][z] = data

    def get_data(self,x,y,z):
        return self.array[x][y][z]

    def select_data(self, xrange = (None,None), yrange = (None,None), zrange = (None,None)):
        if xrange[0] == None:
            xmin = 0
        else:
            xmin = xrange[0]
        if yrange[0] == None:
            ymin = 0
        else:
            ymin = yrange[0]
        if zrange[0] == None:
            zmin = 0
        else:
            zmin = zrange[0]
        if xrange[1] == None:
            xmax = self.xsize - 1
        else:
            xmax = xrange[1]
        if yrange[1] == None:
            ymax = self.ysize - 1
        else:
            ymax = yrange[1]
        if zrange[1] == None:
            zmax = self.zsize - 1
        else:
            zmax = zrange[1]
        selection = [[[z[1] for z in enumerate(self.array[x[0]][y[0]][zmin:zmax])] for y in enumerate(self.array[x[0]][ymin:ymax])] for x in enumerate(self.array[xmin:xmax])]
        dimensions = get_array_dimensions(selection)
        newArray = _3DList(dimensions[0],dimensions[1],dimensions[2])
        newArray.set_array(selection)
        return newArray

    def set_array(self, array):
        self.array = array

    def iterate(self, ignore = ()):
        values = []
        for x in enumerate(self.array):
            for y in enumerate(x[1]):
                for z in enumerate(y[1]):
                    if len(ignore) > 0:
                        if z[1] not in ignore:
                            values.append(((x[0], y[0], z[0]), z[1]))
                    else:
                        values.append(((x[0], y[0], z[0]), z[1]))
        return values

    def dims(self):
        return get_array_dimensions(self.array)


def get_array_dimensions(array):
    return (len(array),len(array[0]),len(array[0][0]))


def get_file_dimensions(file):
    file = open(file, "r")
    data = file.read()
    file.close()
    data = [y.split(",") for y in [x.split(";") for x in data.split('\n')]]
    return (len(data), len(data[0]), len(data[0][0]))
