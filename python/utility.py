import numpy as np

NaN = np.power(10, 9)


# Find and eliminate invalid indices
def del_invalid_indices(mat_votes):

	# Variable to store total number of invalid votes
	invalid_count = 0

	# Iterate through rows of matrix to see if votes are invalid
	for i in range(0, mat_votes.shape[0]):
		# Check for invalidity
		if len(np.unique(np.array(mat_votes[i, :]))) < mat_votes.shape[1]:
			invalid_count += 1

	if invalid_count > 0:
		# Create matrix to store invalid indices
		invalid_indices = np.ndarray(shape=(1, invalid_count), dtype=int, order='C')
		invalid_indices = np.matrix(invalid_indices, dtype=int)

		curr_index = 0

		# Iterate through rows of votes matrix to store invalid indices
		for i in range(0, mat_votes.shape[0]):
			# Check for invalidity
			if len(np.unique(np.array(mat_votes[i, :]))) < mat_votes.shape[1]:
				invalid_indices[0, curr_index] = i
				curr_index += 1

		# Iterate over invalid indices to delete invalid rows
		for i in range(0, invalid_indices.shape[1]):
			# Store invalid index
			index = invalid_indices[0, i]

			# Delete row
			mat_votes = np.delete(mat_votes, index, 0)

			# If the current index is less than the total length, decrement following indices by 1
			if i < (invalid_indices.shape[1] - 1):
				for j in range(i + 1, invalid_indices.shape[1]):
					invalid_indices[0, j] -= 1

	return mat_votes


# Find the indices of the minimum values in a horizontal matrix
def find_min(h_matrix):
	# Find the absolute minimum
	min_value = np.min(h_matrix)

	# Check if other minimum values exist
	log_array = np.matrix(h_matrix == min_value, dtype=int)

	# Calculate the number of equal minimum values
	num_min_values = np.sum(log_array)

	# Create an array to store the multiple minimum values' indices
	min_indices = np.ndarray(shape=(1, num_min_values), dtype=int, order='C')
	min_indices = np.matrix(min_indices, dtype=int)

	j = 0
	for i in range(0, log_array.shape[1]):
		if log_array[0, i]:
			min_indices[0, j] = i
			j += 1

	return min_indices


# Function to resolve ties between 2+ people
def resolve_tie(mat_h_min_indices, int_pref_level, mat_vote_data):
	# Create a matrix to store the distributed preference values
	dist_pref = np.ndarray(shape=(1, mat_vote_data.shape[1]), dtype=int, order='C')
	dist_pref = np.matrix(dist_pref, dtype=int)
	dist_pref[:, :] = NaN

	# Set all the candidates with minimum values dist_pref values to zero
	for i in mat_h_min_indices:
		dist_pref[0, i[0, 0]] = 0

	# Iterate over all the minimum indices to compare to other minimum indices
	for i in mat_h_min_indices[0, :]:
		# Iterate over all indices to check if comparison is possible
		for j in mat_h_min_indices[0, :]:
			# If the current candidate for comparison is itself, skip this iteration
			if i[0, 0] == j[0, 0]:
				continue

			# Else, for every vote in vote data, if the current vote has first preference for the comparison candidate
			# check to see if the current minimum candidate has a matching preference level to check and if true,
			# increment current minimum candidate's preference count
			for k in mat_vote_data:
				if (k[0, j[0, 0]] == 1) and (k[0, i[0, 0]] == int_pref_level):
					dist_pref[0, i[0, 0]] += 1

	# Find the minimum value of dist_pref
	min_value = np.min(dist_pref)

	# Isolate candidates with same minimum value
	log_dist_pref = (dist_pref == min_value)

	# Find the total number of equal minimum value candidates
	num_min_values = np.sum(log_dist_pref)

	# Create a matrix to store the minimum values after the count has been distributed
	new_min_indices = np.ndarray(shape=(1, num_min_values), dtype=int, order='C')
	new_min_indices = np.matrix(new_min_indices, dtype=int)

	# Keep track of current index in new_min_indices
	curr_index = 0

	# Get the current minimum values
	for i in range(0, dist_pref.shape[1]):
		if log_dist_pref[0, i]:
			new_min_indices[0, curr_index] = i
			curr_index += 1

	# Return the candidate to be eliminated
	if new_min_indices.shape[1] > 1:
		return resolve_tie(new_min_indices, int_pref_level + 1, mat_vote_data)
	else:
		return new_min_indices[0, 0]


# Function to eliminate a candidate from the voting data
def eliminate(int_elim_index, mat_vote_data):
	# Iterate through eliminated candidate's votes and set it to NaN
	for i in range(0, mat_vote_data.shape[0]):
		if mat_vote_data[i, int_elim_index] == 1:
			mat_vote_data[i, :] = NaN

	# Set candidate's whole column to NaN
	mat_vote_data[:, int_elim_index] = NaN

	return mat_vote_data


# Function to allocate n-th preference to remaining candidates
def get_next_pref(int_elim_index, mat_vote_data):
	# Create matrix to store next preferences
	next_pref = np.ndarray(shape=(1, mat_vote_data.shape[1]), dtype=int, order='C')
	next_pref = np.matrix(next_pref, dtype=int)
	next_pref[0, :] = 0

	# Cycle through all the rows of vote data to find the rows in which the eliminated candidate has first preference
	for i in range(0, mat_vote_data.shape[0]):
		# Check for first preference
		if mat_vote_data[i, int_elim_index] == 1:
			# Set eliminated candidate's value to NaN so it is not counted in min
			mat_vote_data[i, int_elim_index] = NaN

			# Find the minimum preference index
			min_index = find_min(mat_vote_data[i, :])[0, 0]

			# Increment the particular candidate's index in next_pref by 1
			next_pref[0, min_index] += 1

	# Set the eliminated candidate's index to NaN, so when it is added to FPM, it will stay NaN or greater
	next_pref[0, int_elim_index] = NaN

	return next_pref, mat_vote_data
