class Heuristics:
	# When a choice between multiple operations is available, always pick the first one
	@staticmethod
	def select_first_operation(jobs_to_be_done, max_operations, _):
		best_candidates = {}

		for job in jobs_to_be_done:
			current_activity = job.current_activity
			best_operation = current_activity.next_operations[0]

			if best_candidates.get(best_operation.id_machine) is None:
				best_candidates.update({best_operation.id_machine: [(current_activity, best_operation)]})
			elif len(best_candidates.get(best_operation.id_machine)) < max_operations:
				list_operations = best_candidates.get(best_operation.id_machine)
				list_operations.append((current_activity, best_operation))
				best_candidates.update({best_operation.id_machine: list_operations})
			else:
				list_operations = best_candidates.get(best_operation.id_machine)

				for key, (_, operation) in enumerate(list_operations):
					if operation.duration < best_operation.duration:
						list_operations.pop(key)
						break

				if len(list_operations) < max_operations:
					list_operations.append((current_activity, best_operation))
					best_candidates.update({best_operation.id_machine: list_operations})

		return best_candidates

	# LEPT rule
	@staticmethod
	def longest_expected_processing_time_first(jobs_to_be_done, max_operations, current_time):
		pass

	# Shortest slack per remaining operations
	# S/RO = [(Due date - Today’s date) - Total shop time remaining] / Number of operations remaining
	@staticmethod
	def shortest_slack_per_remaining_operations(jobs_to_be_done, max_operations, current_time):
		pass

	# Highest critical ratios
	# CR = Processing Time / (Due Date – Current Time)
	@staticmethod
	def highest_critical_ratios(jobs_to_be_done, max_operations, current_time):
		best_candidates = {}
		critical_ratios = {}
		assignment = {}

		for job in jobs_to_be_done:
			current_activity = job.current_activity

			# Compute critical ratio for each operation for an activity
			for operation in current_activity.next_operations:
				critical_ratio = operation.duration / (job.total_shop_time - current_time)
				critical_ratios.update({job.id_job: (current_activity, operation, critical_ratio)})

			for id_job, current_activity, operation, critical_ratio in critical_ratios.items():
				if assignment.get(operation.id_machine) is None:
					assignment.update({operation.id_machine: (current_activity, operation, critical_ratio)})

				elif len(assignment.get(operation.id_machine)) < max_operations:
					list_operations = assignment.get(operation.id_machine)
					list_operations.append((current_activity, operation, critical_ratio))
					best_candidates.update({operation.id_machine: list_operations})

		# TODO: end that
