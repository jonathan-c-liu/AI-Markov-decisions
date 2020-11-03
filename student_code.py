import common

def drone_flight_planner (map,policies, values, delivery_fee, battery_drop_cost, dronerepair_cost, discount):
	# PUT YOUR CODE HERE
	# access the map using "map[y][x]"
	# access the policies using "policies[y][x]"
	# access the values using "values[y][x]"
	# y between 0 and 5
	# x between 0 and 5
	# function must return the value of the cell corresponding to the starting position of the drone
	#
	newvalues = [[0 for x in range(6)] for x in range(6)]
	for y in range(6):
		for x in range(6):
			if map[y][x] == common.constants.PIZZA:
				startpos = (y, x)
	while True:
		for y in range(6):
			for x in range(6):
				if map[y][x] == common.constants.CUSTOMER:
					policies[y][x] = common.constants.EXIT
					newvalues[y][x] = delivery_fee
				elif map[y][x] == common.constants.RIVAL:
					policies[y][x] = common.constants.EXIT
					newvalues[y][x] = -dronerepair_cost
				else:
					actionvals = calculatevals(values, battery_drop_cost, discount, y, x)
					maxval = max(actionvals)
					newvalues[y][x] = maxval
					policies[y][x] = actionvals.index(maxval)

		done = True
		for y in range(6):
			for x in range(6):
				if values[y][x] == 0 or (newvalues[y][x] - values[y][x]) / values[y][x] > .00001:
					done = False
		if done:
			break
		else:
			for y in range(6):
				for x in range(6):
					values[y][x] = newvalues[y][x]

	return values[startpos[0]][startpos[1]]


def calculatevals(values, battery_drop_cost, discount, y, x):
	actionvals = [float("-inf")] * 9

	if x == 0:
		xw = x
	else:
		xw = x - 1
	if x == 5:
		xe = x
	else:
		xe = x + 1
	if y == 0:
		yn = y
	else:
		yn = y - 1
	if y == 5:
		ys = y
	else:
		ys = y + 1

	actionvals[common.constants.SOFF] = .7 * (-battery_drop_cost + discount * values[ys][x]) + .15 * (-battery_drop_cost + discount * values[y][xw]) + .15 * (-battery_drop_cost + discount * values[y][xe])
	actionvals[common.constants.SON] = .8 * (-2 * battery_drop_cost + discount * values[ys][x]) + .1 * (-2 * battery_drop_cost + discount * values[y][xw]) + .1 * (-2 * battery_drop_cost + discount * values[y][xe])
	actionvals[common.constants.WOFF] = .7 * (-battery_drop_cost + discount * values[y][xw]) + .15 * (-battery_drop_cost + discount * values[yn][x]) + .15 * (-battery_drop_cost + discount * values[ys][x])
	actionvals[common.constants.WON] = .8 * (-2 * battery_drop_cost + discount * values[y][xw]) + .1 * (-2 * battery_drop_cost + discount * values[yn][x]) + .1 * (-2 * battery_drop_cost + discount * values[ys][x])
	actionvals[common.constants.NOFF] = .7 * (-battery_drop_cost + discount * values[yn][x]) + .15 * (-battery_drop_cost + discount * values[y][xw]) + .15 * (-battery_drop_cost + discount * values[y][xe])
	actionvals[common.constants.NON] = .8 * (-2 * battery_drop_cost + discount * values[yn][x]) + .1 * (-2 * battery_drop_cost + discount * values[y][xw]) + .1 * (-2 * battery_drop_cost + discount * values[y][xe])
	actionvals[common.constants.EOFF] = .7 * (-battery_drop_cost + discount * values[y][xe]) + .15 * (-battery_drop_cost + discount * values[yn][x]) + .15 * (-battery_drop_cost + discount * values[ys][x])
	actionvals[common.constants.EON] = .8 * (-2 * battery_drop_cost + discount * values[y][xe]) + .1 * (-2 * battery_drop_cost + discount * values[yn][x]) + .1 * (-2 * battery_drop_cost + discount * values[ys][x])

	return actionvals