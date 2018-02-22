import irv as IRV

# Create interface to retrieve filepath of votes
vote_file_data = open("vote_data_filepath.txt", 'r')
vote_file_path = vote_file_data.readline()
vote_file_path = vote_file_path.replace(" \n", "")
vote_sheet = vote_file_data.readline()
vote_file_data.close()

# Get results string for writing
results = IRV.instant_runoff(vote_file_path, vote_sheet)

# Write results to results.txt
results_file = open("results.txt", 'w')
results_file.write(results)
results_file.close()
