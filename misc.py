class Transform(object):
    def __init__(self):
        self.xp = 0.0
        self.yp = 0.0
        self.zp = 0.0
        self.xr = 0.0
        self.yr = 0.0
        self.zr = 0.0
        self.xs = 0.0
        self.ys = 0.0
        self.zs = 0.0

    def __init__(self,xp = .0,yp = .0,zp = .0,xr = .0 ,yr = .0,zr = .0,xs = .0,ys = .0,zs = .0):
        self.xp = xp
        self.yp = yp
        self.zp = zp
        self.xr = xr
        self.yr = yr
        self.zr = zr
        self.xs = xs
        self.ys = ys
        self.zs = zs
