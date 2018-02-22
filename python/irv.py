import pandas as pnd
import utility as ut


def instant_runoff(src_file_path, sheet):
	# Load excel file
	df = pnd.read_excel(src_file_path, sheet_name=sheet)

	# Record the number of candidates
	cand_count = 0
	for column in df:
		cand_count += 1

	# Record the number of candidates left
	cand_left = cand_count

	# Record candidate names
	names = ut.np.ndarray(shape=(1, cand_count), dtype="<U50", order='C')
	names = ut.np.matrix(names, dtype="<U50")

	i = 0
	for column in df:
		names[0, i] = column
		i += 1

	# Load votes as array from DataFrame
	votes = ut.np.asarray(df)
	votes = ut.np.matrix(votes, dtype=int)

	# Record total vote count to display
	total_vote_count = votes.shape[0]

	# Delete invalid rows
	votes = ut.del_invalid_indices(votes)

	# Record current vote count, after invalids deleted
	valid_vote_count = votes.shape[0]

	# Create matrix to store first-preference values on each iteration
	first_pref_matrix = ut.np.ndarray(shape=(cand_count - 1, cand_count), dtype=int, order='C')
	first_pref_matrix = ut.np.matrix(first_pref_matrix, dtype=int)
	first_pref_matrix[:, :] = 0

	# Create logical array to isolate first-round first-preference votes
	log_votes = (votes == 1)

	# Current round of counting
	curr_round = 0

	# Count first preference votes
	for i in range(0, cand_count):
		first_pref_matrix[curr_round, i] = ut.np.sum(log_votes[:, i])

	# Main loop to eliminate candidates till there are 2 left
	while cand_left > 2:
		# Find the candidate to eliminate
		min_indices = ut.find_min(first_pref_matrix[curr_round, :])

		# Test to see if ties exist and resolve them
		if min_indices.shape[1] > 1:
			curr_elim_index = ut.resolve_tie(min_indices, 2, votes)
		else:
			curr_elim_index = min_indices[0, 0]

		curr_round += 1

		# Get next preference values and add it to the previous round FPM
		(next_pref, votes) = ut.get_next_pref(curr_elim_index, votes)
		first_pref_matrix[curr_round, :] = first_pref_matrix[curr_round - 1, :] + next_pref

		# Eliminate minimum value candidate
		votes = ut.eliminate(curr_elim_index, votes)
		cand_left -= 1

	# Get the max result from the FPM matrix
	max_index = 0
	max_value = 0
	for i in range(0, first_pref_matrix.shape[1]):
		if (first_pref_matrix[cand_count - 2, i] < ut.NaN) and (first_pref_matrix[cand_count - 2, i] > max_value):
			max_value = first_pref_matrix[cand_count - 2, i]
			max_index = i

	# Get the min result from the FPM matrix
	min_index = 0
	min_value = ut.NaN
	for i in range(0, first_pref_matrix.shape[1]):
		if (first_pref_matrix[cand_count - 2, i] < ut.NaN) and (first_pref_matrix[cand_count - 2, i] < min_value):
			min_value = first_pref_matrix[cand_count - 2, i]
			min_index = i

	# Check if the candidates left are in a tie
	tie_array = []
	if max_value == min_value:
		log_FPM = (first_pref_matrix[cand_count - 2, :] == max_value)
		for i in range(0, cand_count):
			if log_FPM[0, i]:
				tie_array.append(i)

		max_index = tie_array[0]
		min_index = tie_array[1]

	# Create string to store user-friendly results (captain and vice data, total vote count, valid vote count)
	results_str = names[0, max_index] + "\n" + str(max_value) + "\n" + names[0, min_index] + "\n" + str(min_value) + "\n" + str(total_vote_count) + "\n" + str(valid_vote_count)

	return results_str
