from TSPClasses import *
import time


class Hilbert:

	def __init__(self, cities):
		self.cities = cities
		self.n = 1000

	def solve(self, time_allowance):
		startTime = time.time()
		n = self.n ** 2
		self.maxX, self.maxY, self.minX, self.minY = self.findingMaxs(self.cities)
		self.middleX = (self.maxX - self.minX) / 2 + self.minX
		self.middleY = (self.maxY - self.minY) / 2 + self.minY

		self.xConversion = 0 - self.minX
		self.yConversion = 0 - self.minY

		hilbertQuad1 = dict({})
		hilbertQuad2 = dict({})
		hilbertQuad3 = dict({})
		hilbertQuad4 = dict({})

		# Map all the cities to the 4 hilbert curves -> Complexity O(nlogn)
		for city in self.cities:
			currX = city._x
			currY = city._y
			quadrant = -1

			if currX >= self.middleX and currY >= self.middleY:
				quadrant = 1
			elif currX > self.middleX and currY < self.middleY:
				quadrant = 4
			elif currX < self.middleX and currY > self.middleY:
				quadrant = 2
			elif currX <= self.middleX and currY <= self.middleY:
				quadrant = 3
			
			transX, transY = self.translateCoordinates(currX, currY, quadrant)
			index = self.xy2d(n, int(transX * 1000000), int(transY * 1000000))

			if quadrant == 1:
				self.updateDictionary(hilbertQuad1, index, city)
			elif quadrant == 2:
				self.updateDictionary(hilbertQuad2, index, city)
			elif quadrant == 3:
				self.updateDictionary(hilbertQuad3, index, city)
			elif quadrant == 4:
				self.updateDictionary(hilbertQuad4, index, city)

		# Iterate through the cities in the order of the curves
		# 2 -> 1 -> 4 backwards -> 3 backwards
		route, unreached = self.buildFullRoute(hilbertQuad2, hilbertQuad1, hilbertQuad4, hilbertQuad3, False, False, True, True)

		if len(unreached) > 0:
			route, unreached = self.buildFullRoute(hilbertQuad1, hilbertQuad4, hilbertQuad3, hilbertQuad2, False, True, True, False)

		if len(unreached) > 0:
			route, unreached = self.buildFullRoute(hilbertQuad4, hilbertQuad3, hilbertQuad2, hilbertQuad1, True, True, False, False)

		if len(unreached) > 0:
			route, unreached = self.buildFullRoute(hilbertQuad3, hilbertQuad2, hilbertQuad1, hilbertQuad4, True, False, False, True)

		results = {}
		results['soln'] = TSPSolution(route)
		results['cost'] = results['soln'].cost
		results['time'] = time.time() - startTime
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		results['count'] = None

		return results

	def buildFullRoute(self, quad1, quad2, quad3, quad4, reverse1, reverse2, reverse3, reverse4): # must pass the quadrants in clockwise order
		route = []
		unReachedCities = []
		self.buildRouteFromDict(route, quad1, unReachedCities, reverse1)
		self.buildRouteFromDict(route, quad2, unReachedCities, reverse2)
		self.buildRouteFromDict(route, quad3, unReachedCities, reverse3)
		self.buildRouteFromDict(route, quad4, unReachedCities, reverse4)

		return route, unReachedCities

	def buildRouteFromDict(self, route, dictionary, unReachedCities, reverse=False):
		keys = list(dictionary.keys())
		if reverse:
			keys.reverse()
		
		for bucket in keys:
			currCities = dictionary[bucket]
			for city in currCities:
				if len(route) < 1:
					route.append(city)
					continue

				# Iterate through all the cities on the queue to and check to see if they can be visited
				i = 0
				while len(unReachedCities) > 0 and i < len(unReachedCities):
					cost = route[-1].costTo(unReachedCities[i])
					if cost != float("inf"):
						route.append(unReachedCities.pop(i))
						i = 0
					else:
						i += 1
				
				cost = route[-1].costTo(city)
				if cost != float("inf"):
					route.append(city)
				else:
					unReachedCities.append(city)



	def updateDictionary(self, dictionary, key, value):
		if key in dictionary:
			dictionary[key].append(value)
		else:
			dictionary[key] = [value]


	def translateCoordinates(self, x, y, quadrant): # TODO IF STUFF BREAKS CHECK THIS FIRST
		if quadrant == 1:
			return x - self.middleX, y - self.middleY
		elif quadrant == 2:
			return x + self.xConversion, y - self.middleY
		elif quadrant == 3:
			return x + self.xConversion, -(y - self.middleY)
		elif quadrant == 4:
			return x + self.middleX, -(y - self.middleY)


	def findingMaxs(self, cities):
		maxX = float('-inf')
		maxY = float('-inf')
		minX = float('inf')
		minY = float('inf')
		for city in cities:
			maxX = city._x if city._x > maxX else maxX
			maxY = city._y if city._y > maxY else maxY
			minX = city._x if city._x < minX else minX
			minY = city._y if city._y < minY else minY
		return  maxX, maxY, minX, minY

	# convert (x,y) to d
	def xy2d (self,n,x,y):
		d = 0
		s = int(n//2)
		while s > 0:
			rx = (x & s) > 0
			ry = (x & s) > 0
			d += s * s * ((3 * rx) ^ ry)
			self.rot(n,x,y,rx,ry)
			s //= 2
		return d

	# convert d to (x,y)
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

	# rotate/flip a quadrant appropriately
	def rot(self, n, x, y, rx, ry):
		if ry == 0:
			x = n-1 - x
			y = n-1 - y
		t = x
		x = y
		y = t
