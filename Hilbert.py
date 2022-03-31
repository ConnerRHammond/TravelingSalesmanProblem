class Hilbert:

	# //convert (x,y) to d
	# int xy2d (int n, int x, int y) {
	#     int rx, ry, s, d=0;
	#     for (s=n/2; s>0; s/=2) {
	#         rx = (x & s) > 0;
	#         ry = (y & s) > 0;
	#         d += s * s * ((3 * rx) ^ ry);
	#         rot(n, &x, &y, rx, ry);
	#     }
	#     return d;
	# }
	def xy2d (self,n,x,y):
		d = 0
		s = n/2
		while s > 0:
			rx = x & s > 0
			ry = x & s > 0
			d += s * s * ((3 * rx) ^ ry)
			self.rot(n,x,y,rx,ry)
			s = n/2
		return d

	# //convert d to (x,y)
	# void d2xy(int n, int d, int *x, int *y) {
	#     int rx, ry, s, t=d;
	#     *x = *y = 0;
	#     for (s=1; s<n; s*=2) {
	#         rx = 1 & (t/2);
	#         ry = 1 & (t ^ rx);
	#         rot(s, x, y, rx, ry);
	#         *x += s * rx;
	#         *y += s * ry;
	#         t /= 4;
	#     }
	# }
	#
	def d2xy(self,n,d,x,y):
		t = d
		x = 0
		y = 0
		s = 1
		while s < n:
			rx = 1 & (t/2)
			ry = 1 & (t ^ rx)
			self.rot(s,x,rx,ry)
			x += s * rx
			y += s * ry
			t = t/4
			s = s * 2

	# //rotate/flip a quadrant appropriately
	# void rot(int n, int *x, int *y, int rx, int ry) {
	#     if (ry == 0) {
	#         if (rx == 1) {
	#             *x = n-1 - *x;
	#             *y = n-1 - *y;
	#         }
	#
	#         //Swap x and y
	#         int t  = *x;
	#         *x = *y;
	#         *y = t;
	#     }
	# }
	def rot(self, n, x, y, rx, ry):
		if ry == 0:
			x = n-1 - x
			y = n-1 - y
		t = x
		x = y
		y = t